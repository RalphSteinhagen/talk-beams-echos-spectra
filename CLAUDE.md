# CLAUDE.md (AGENTS.md) — talk-beam_echoes

> For LLM coding agents. This repository is a [gr4-present](https://github.com/RalphSteinhagen/gr4-present) slide deck,
> "Beams, Echoes and Spectra", whose live demonstrations run GNU Radio 4 and OpenDigitizer flow-graphs. GR4's rules
> apply unchanged; this file adds only what differs here.

## 1 · Rules

GR4's [`CLAUDE.md`](https://github.com/fair-acc/gnuradio4/blob/main/CLAUDE.md) is authoritative: the working agreement,
design, naming, layout, documentation, testing, commits (`git commit -s`, no other trailer; commit, amend and push only
when asked, each time) and the pre-submit checklist. Read it first.

The local copies below are taken verbatim from OpenDigitizer `d00d0f0` (2026-11-13), whose copies are GR4 `bd3d68bb`
(2026-10-29):

| File                            | Purpose                                                 |
| ------------------------------- | ------------------------------------------------------- |
| `CORE_DEVELOPMENT_GUIDELINE.md` | rationale                                               |
| `CORE_NAMING_GUIDELINE.md`      | naming                                                  |
| `CORE_AGENT_WORKFLOW.md`        | orchestration                                           |
| `CORE_REVIEW_GUIDELINE.md`      | review                                                  |
| `.claude/commands/`             | review commands and the refactor and fix-style commands |

Where these files speak of C++ modules, builds and tests, the counterparts here are the Python generators in
`devtools/`, the flow-graphs in `workflows/` and `demo/`, and the rendered deck. This file and the copies MUST NOT be
changed without the author's express approval.

## 2 · Repository

- **The deck.** `talk.md` (gr4-present Markdown: slides, speaker notes, citations) and `index.yml` (masters, fonts,
  sizes); assets in `figures/`, `media/`, `effects/`, `fonts/`. How to show it: `README.md`.
- **Generated, not hand-edited.** `figures/` (`make-figures.py`, `make-masters.py`, `make-montage.py`),
  `workflows/*.grc` (`make-workflows.py`), `data/*.csv` and the two experiment-4 WAV files (`make-demo-data.py`): change
  the script, re-run it, and check that the outputs you did not mean to change stay byte-identical. The portraits, the
  other 4:5 crops and the title banner are final files; their originals are not kept.
- **Untracked by design**, never committed and never listed in `.gitignore`: `claude_wip.md`,
  `claude_gr4_demo_report.md`, `talk_walkthrough.md`, `draft_*.md`, `.idea/`.
- **Pins.** The live regions run in the public viewer, whose GR4 and OpenDigitizer revisions are set in gr4-present's
  `cmake/DependenciesSHAs.cmake`; read the blocks at those revisions, not at a local checkout's. `.grc` settings keys
  are wire keys: GR4 ignores an unknown one silently — run `devtools/check-workflows.py` against the pinned trees.

## 3 · Checks

- **Render, then claim.** A slide is checked in the public viewer at 1600 × 900 (`devtools/shoot.mjs`, deck served by
  `./serve.sh --no-open`); the local WASM-Minimal viewer lacks OpenDigitizer and shows no live region.
- **Sources.** Every picture has its row in `media/CREDITS.md` or `media/portraits/PORTRAITS.md`; items marked "talk
  only" are cleared before the deck is published. A historical claim is either cited or marked `[verify]`, and a
  crossing between domains is named as a transfer, co-evolution or parallel invention — never more than the source says.
