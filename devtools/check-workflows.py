#!/usr/bin/env python3
"""Checks every parameter a workflow sets against the settings its block reflects, since GNU Radio 4 drops an unknown
parameter without a word: python3 devtools/check-workflows.py <source-tree> ... [workflow.grc ...]
(default workflows: workflows/*.grc). Name the GR4 and OpenDigitizer trees at the revisions the viewer pins
(gr4-present's cmake/DependenciesSHAs.cmake; a viewer build's _deps/*-src), and gr4-present's src/app/blocks for its own.
A block id that names no reflected struct in any tree is reported as unknown."""
import re
import sys

import yaml
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
# registered names that differ from the struct that implements them
ALIASES = {"SchmittTriggerNoInterpolation": "SchmittTrigger", "SchmittTriggerBasic": "SchmittTrigger",
           "SchmittTriggerPolynomial": "SchmittTrigger", "StreamToDataSet": "StreamFilterImpl",
           "Add": "ReduceOp", "Subtract": "ReduceOp", "Multiply": "ReduceOp", "Divide": "ReduceOp", "Max": "ReduceOp",
           "AddConst": "ConstOp", "SubtractConst": "ConstOp", "MultiplyConst": "ConstOp", "DivideConst": "ConstOp",
           "LevelTrigger": "ValueTrigger", "AudioSourceMultiplexed": "AudioSource",
           "BasicFilter": "BasicFilterProto", "AddPair": "MathOpPairImpl", "SubtractPair": "MathOpPairImpl"}


def reflected(trees):
    fields = {}
    pattern = re.compile(r"GR_MAKE_REFLECTABLE\(\s*(\w+)\s*,([^;]*?)\);", re.S)
    for tree in trees:
        for header in Path(tree).rglob("*.hpp"):
            relative = str(header.relative_to(tree))
            if "test" in relative.split("/")[:-1] or "_deps" in relative.split("/"):
                continue
            for name, members in pattern.findall(header.read_text(errors="ignore")):
                fields.setdefault(name, set()).update(m.strip() for m in members.replace("//", ",").split(",") if m.strip())
    return fields


class Loader(yaml.SafeLoader):
    """Reads GR4's typed scalars and lists (!!float32, !!uint32, ...) as plain values."""


def typed(loader, node, *_):
    if isinstance(node, yaml.SequenceNode):
        return loader.construct_sequence(node)
    if isinstance(node, yaml.MappingNode):
        return loader.construct_mapping(node)
    return loader.construct_scalar(node)


Loader.add_multi_constructor("tag:yaml.org,2002:", lambda loader, suffix, node: typed(loader, node))
Loader.add_constructor("tag:yaml.org,2002:str", typed)   # GR4 writes a list of strings as !!str [ ... ]


def blocks_of(text):
    """(id, {parameter: value}) per block of a .grc, then per chart of its dashboard (a control may target a chart)."""
    document = yaml.load(text, Loader=Loader) or {}
    plots = (document.get("dashboard") or {}).get("plots") or []
    return ([(str(b.get("id", "")), b.get("parameters") or {}) for b in document.get("blocks", [])],
            [(str(p.get("type", "")), p.get("parameters") or {}) for p in plots])


def main():
    trees = [a for a in sys.argv[1:] if not a.endswith(".grc")]
    if not trees:
        sys.exit(__doc__)
    fields = reflected(trees)
    files = [Path(f) for f in sys.argv[1:] if f.endswith(".grc")] or sorted((HERE / "workflows").glob("*.grc"))
    problems = 0
    for file in files:
        try:
            parsed, charts = blocks_of(file.read_text())
        except yaml.YAMLError as error:
            print(f"{file.name}: not YAML: {str(error).splitlines()[0]} {getattr(error, 'problem_mark', '')}")
            problems += 1
            continue
        structs = {}   # block name -> its struct, for the controls' target maps
        for block_id, parameters in parsed + charts:
            short = block_id.split("<")[0].split("::")[-1]
            structs[str(parameters.get("name", ""))] = ALIASES.get(short, short)
        for block_id, parameters in parsed:
            if block_id.endswith("ImControlNumber"):
                for target in str(parameters.get("target_map", "")).split(";"):
                    names, _, setting = target.rpartition(":")
                    for name in filter(None, names.split(",")):
                        struct = structs.get(name.strip())
                        if struct is None:
                            print(f"{file.name}: control {parameters.get('name')}: no block '{name}'")
                            problems += 1
                        elif struct in fields and setting not in fields[struct] | fields.get("Block", set()):
                            print(f"{file.name}: control {parameters.get('name')}: {name} has no setting '{setting}'")
                            problems += 1
            short = block_id.split("<")[0].split("::")[-1]
            struct = ALIASES.get(short, short)
            if struct not in fields:
                print(f"{file.name}: {block_id}: no such block")
                problems += 1
                continue
            allowed = fields[struct] | fields.get("Block", set())   # every block also takes the Block base's settings,
            if struct.startswith("ImControl"):                     # a dashboard control its ImControl base's
                allowed |= fields.get("ImControl", set())
            for key in parameters:
                if key not in allowed:
                    print(f"{file.name}: {block_id}: no setting '{key}'")
                    problems += 1
    print(f"{len(files)} workflows, {problems} problems")
    sys.exit(1 if problems else 0)


main()
