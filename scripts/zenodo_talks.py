#!/usr/bin/env python3
"""Archives this talk on Zenodo as one 'presentation' record (and DOI), as fair-acc/gremlin does for its talks/.

The deck is this repository: its sidecar `zenodo.yml` (at the root) carries the talk's own metadata (title,
description, conference, ...) and the state of its record. Creators and keywords are inherited from the repository's
`.zenodo.json`; any key in the sidecar overrides the inherited one. The archived deck is every tracked file except the
infrastructure (CI, scripts, the viewer pin, the agent guidance, the sidecar).

A publish on Zenodo is permanent, so the DOI goes into the repository before anything is published. The PDFs live on
Zenodo only, never in git: they go into the reserved draft (whose files can change until it is published), and the
sidecar records which state of the deck they show.

  plan          (default) shows the talk and what `publish` would do; no network access
  check         tests the token: lists your depositions on Zenodo, read-only
  reserve       creates a draft, pre-reserves its DOI, and writes `record_id` + `doi` into zenodo.yml (commit that
                change: the DOI can go on the title slide before the talk)
  upload        uploads the `files:` exported by scripts/talk_pdfs.sh (from $TALK_PDFS/<name>/, default
                ~/.cache/beams-echoes-talks/<name>/) into the reserved draft, replacing earlier uploads, and writes
                `pdfs_from`, the deck's fingerprint, into zenodo.yml (commit it). Refuses PDFs exported from
                uncommitted changes or from another state of the deck
  publish       with a reserved draft: refreshes the metadata, replaces the zip of the deck, and publishes. A published
                talk is skipped; a talk without a reservation, without its uploaded `files:`, or whose deck changed
                after the upload is reported as an error and never published
  --draft-only  with `publish`: upload everything but leave the draft for a manual click on Zenodo
  --sandbox     use https://sandbox.zenodo.org (token ZENODO_SANDBOX_TOKEN, state keys `sandbox_record_id`,
                `sandbox_doi`, `sandbox_pdfs_from`) instead of https://zenodo.org (token ZENODO_TOKEN, keys
                `record_id`, `doi`, `pdfs_from`)
  --ref <ref>   the commit to archive and to link to (default: $GITHUB_REF_NAME, else HEAD)

The token needs the scopes deposit:write and deposit:actions. Needs PyYAML to read the sidecar.

  ZENODO_SANDBOX_TOKEN=... scripts/zenodo_talks.py reserve --sandbox
  ZENODO_TOKEN=...         scripts/zenodo_talks.py reserve
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
REPO_URL = "https://github.com/RalphSteinhagen/talk-beams-echos-spectra"
PAGES_URL = "https://ralphsteinhagen.github.io/talk-beams-echos-spectra"
VIEWER_URL = "https://ralphsteinhagen.github.io/gr4-present/"  # when zenodo.yml names no pinned `viewer:`
# each publish asks these to include the record; their curators accept it (https://zenodo.org/communities/<id>/)
COMMUNITIES = ("gsi-fair",)  # GSI/FAIR
USER_AGENT = f"beams-echoes-zenodo-talks/1.0 (+{REPO_URL})"
INHERITED = (
    "creators",
    "keywords",
)  # taken from .zenodo.json unless the sidecar names them
SIDECAR_ONLY = (
    "name",
    "files",
    "exclude",
    "record_id",
    "doi",
    "sandbox_record_id",
    "sandbox_doi",
    "pdfs_from",
    "sandbox_pdfs_from",
    "viewer",
)  # not Zenodo metadata
# tracked files that are not the deck: neither archived nor part of its fingerprint
INFRASTRUCTURE = (
    ".github/",
    ".claude/",
    "scripts/",
    "viewer/",
    ".gitignore",
    "zenodo.yml",
    "CLAUDE.md",
    "AGENTS.md",
    "CORE_AGENT_WORKFLOW.md",
    "CORE_DEVELOPMENT_GUIDELINE.md",
    "CORE_NAMING_GUIDELINE.md",
    "CORE_REVIEW_GUIDELINE.md",
)
# archived with the deck, but edited after the export without changing the slides: not part of the fingerprint
NOT_DECK = (
    "README.md",
    "CITATION.cff",
    ".zenodo.json",
    "LICENSE",
    "LICENSES/",
)
FINGERPRINT_NOTE = re.compile(r"deck fingerprint ([0-9a-f]{40})")


def fail(message):
    print(
        (
            f"::error::{message}"
            if os.environ.get("GITHUB_ACTIONS")
            else f"error: {message}"
        ),
        file=sys.stderr,
    )


def git(*args, binary=False):
    out = subprocess.run(
        ["git", "-C", str(REPO_ROOT), *args], check=True, capture_output=True
    ).stdout
    return out if binary else out.decode().strip()


def matches(path, entries):
    return any(path == e or (e.endswith("/") and path.startswith(e)) for e in entries)


class Zenodo:
    def __init__(self, sandbox):
        self.base = (
            "https://sandbox.zenodo.org/api" if sandbox else "https://zenodo.org/api"
        )
        variable = "ZENODO_SANDBOX_TOKEN" if sandbox else "ZENODO_TOKEN"
        self.token = os.environ.get(variable)
        if not self.token:
            raise SystemExit(f"error: {variable} is not set")

    def call(self, method, url, body=None, data=None):
        headers = {"Authorization": f"Bearer {self.token}", "User-Agent": USER_AGENT}
        if body is not None:
            data, headers["Content-Type"] = (
                json.dumps(body).encode(),
                "application/json",
            )
        elif data is not None:
            headers["Content-Type"] = "application/octet-stream"
        url = url if url.startswith("https://") else self.base + url
        request = urllib.request.Request(url, data=data, method=method, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=300) as response:
                payload = response.read()
        except urllib.error.HTTPError as error:
            raise SystemExit(
                f"error: {method} {url}: HTTP {error.code}: {error.read().decode(errors='replace')}"
            )
        return json.loads(payload) if payload else None


class Talk:
    def __init__(self, sandbox):
        self.dir = REPO_ROOT
        self.sidecar = self.dir / "zenodo.yml"
        self.meta = yaml.safe_load(self.sidecar.read_text()) or {}
        self.name = str(self.meta.get("name") or REPO_ROOT.name)
        self.sandbox = sandbox
        prefix = "sandbox_" if sandbox else ""
        self.key_id, self.key_doi, self.key_pdfs = (
            f"{prefix}{key}" for key in ("record_id", "doi", "pdfs_from")
        )

    @property
    def record_id(self):
        return self.meta.get(self.key_id)

    def store(self, **state):
        """Writes state keys in place, so the comments and layout of the sidecar survive."""
        text = self.sidecar.read_text()
        for key, value in state.items():
            line = f'{key}: "{value}"' if isinstance(value, str) else f"{key}: {value}"
            text, n = re.subn(rf"^{key}:.*$", line, text, count=1, flags=re.M)
            if not n:
                text = text.rstrip("\n") + f"\n{line}\n"
            self.meta[key] = value
        self.sidecar.write_text(text)

    def viewer(self):
        """The live slides on the project page."""
        if build := self.meta.get("viewer"):
            # pinned by scripts/update_viewer.sh in viewer/<commit>/VERSION, fetched and served by the Pages workflow
            if not (REPO_ROOT / "viewer" / str(build) / "VERSION").exists():
                raise SystemExit(
                    f"error: zenodo.yml names viewer {build}, but viewer/{build}/VERSION is missing"
                )
            return f"{PAGES_URL}/viewer/{build}/?presentation=../../default"
        return f"{VIEWER_URL}?presentation={PAGES_URL}/default/"

    def deck(self, ref):
        """The deck's tracked files at `ref`: `git ls-tree` lines, without the infrastructure."""
        return [
            line
            for line in git("ls-tree", "-r", ref).splitlines()
            if not matches(line.split("\t", 1)[1], INFRASTRUCTURE)
        ]

    def fingerprint(self, ref):
        """The deck's tracked files at `ref` (names and contents), without the README, the licences and metadata."""
        deck = "\n".join(
            line for line in self.deck(ref) if not matches(line.split("\t", 1)[1], NOT_DECK)
        )
        return hashlib.sha1(deck.encode()).hexdigest()

    def staging(self):
        """Where scripts/talk_pdfs.sh exports the PDFs, outside the repository."""
        cache = Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache")
        return Path(os.environ.get("TALK_PDFS") or cache / "beams-echoes-talks") / self.name

    def pdf_state(self, ref):
        """None when the uploaded PDFs show the deck at `ref`, else why not."""
        uploaded = self.meta.get(self.key_pdfs)
        if not self.meta.get("files"):
            return None
        if not uploaded:
            return "PDFs not uploaded; scripts/talk_pdfs.sh, then upload"
        if uploaded != self.fingerprint(ref):
            return "deck changed after the PDF upload; re-export and upload again"
        return None

    def metadata(self, ref):
        base = json.loads((REPO_ROOT / ".zenodo.json").read_text())
        meta = {key: base[key] for key in INHERITED if key in base}
        meta.update(
            upload_type="presentation",
            access_right="open",
            license="cc-by-4.0",
            language="eng",
        )
        if not self.sandbox:  # the communities exist on zenodo.org only
            meta["communities"] = [{"identifier": c} for c in COMMUNITIES]
        meta.update({k: v for k, v in self.meta.items() if k not in SIDECAR_ONLY})
        # YAML reads a bare date as datetime.date
        meta["publication_date"] = str(meta.get("publication_date", ""))
        commit = git("rev-parse", "--verify", f"{ref}^{{commit}}")
        related = [
            {"identifier": f"{REPO_URL}/tree/{commit}", "relation": "isDerivedFrom"},
        ]
        viewer = self.viewer()
        related.append({"identifier": viewer, "relation": "isVariantFormOf"})
        live = f'<p>Live slides in the browser: <a href="{viewer}">{viewer}</a></p>'
        meta["description"] = meta.get("description", "") + live
        meta["related_identifiers"] = related + meta.get("related_identifiers", [])
        note = f"Archived from {REPO_URL} at commit {commit}, deck fingerprint {self.fingerprint(ref)}."
        meta["notes"] = f"{meta['notes']} {note}" if meta.get("notes") else note
        meta["prereserve_doi"] = True  # keeps the reserved DOI on every metadata update
        return meta

    def archive(self, ref):
        """Zip of the deck's tracked files at `ref`, without the infrastructure, the `files:` and `exclude:`;
        untracked files never enter it."""
        left_out = [*INFRASTRUCTURE, *self.meta.get("files", []), *self.meta.get("exclude", [])]
        pathspec = [f":(exclude){p.rstrip('/')}" for p in left_out]
        args = ["archive", "--format=zip", f"--prefix={self.name}/", ref, "--", "."]
        return git(*args, *pathspec, binary=True)


def plan(talk, ref):
    size = len(talk.archive(ref)) / 1e6
    files = ", ".join(talk.meta.get("files", [])) or "none"
    if talk.record_id:
        state = f"reserved {talk.record_id}, DOI {talk.meta.get(talk.key_doi)}"
    else:
        state = "NOT reserved"
    print(f"{talk.name}: {state}\n  zip {size:.1f} MB at {ref} ({len(talk.deck(ref))} files), files: {files}")
    print(f"  live slides: {talk.viewer()}")
    if files != "none":
        pdfs = talk.pdf_state(ref) or f"uploaded, match the deck at {ref}"
        print(f"  PDFs: {pdfs}")


def check(zenodo):
    """An authenticated read: a token without the deposit scopes, or not a personal token, fails with HTTP 403."""
    depositions = zenodo.call("GET", "/deposit/depositions?size=100&all_versions=true")
    print(f"{zenodo.base}: token accepted, {len(depositions)} deposition(s) visible")
    for d in depositions:
        state = "published" if d.get("submitted") else "draft"
        print(
            f"  {d['id']} {state:9} {d.get('doi') or ''} {d['metadata'].get('title', '')}"
        )


def reserve(zenodo, talk, ref):
    if talk.record_id:
        print(
            f"{talk.name}: already reserved as {talk.record_id} ({talk.meta.get(talk.key_doi)}), nothing to do"
        )
        return
    deposition = zenodo.call(
        "POST", "/deposit/depositions", {"metadata": talk.metadata(ref)}
    )
    doi = deposition["metadata"]["prereserve_doi"]["doi"]
    talk.store(**{talk.key_id: deposition["id"], talk.key_doi: doi})
    print(f"{talk.name}: reserved draft {deposition['id']}, DOI {doi} (https://doi.org/{doi}); commit zenodo.yml")
    if summary := os.environ.get(
        "GITHUB_STEP_SUMMARY"
    ):  # CI cannot commit the sidecar: hand over the lines
        with open(summary, "a") as out:
            out.write(
                f"- `zenodo.yml`: `{talk.key_id}: {deposition['id']}`, `{talk.key_doi}: \"{doi}\"`\n"
            )


def upload(zenodo, talk):
    """The exported PDFs into the reserved draft; they show the committed deck at HEAD, or nothing is sent."""
    stamp = talk.staging() / "export.stamp"  # written by scripts/talk_pdfs.sh: "<commit> clean|dirty"
    names = talk.meta.get("files", [])
    problem = None
    if not talk.record_id:
        problem = "no reserved record; reserve first"
    elif not names:
        problem = "no `files:` in zenodo.yml"
    elif not stamp.exists():
        problem = f"no export in {talk.staging()}; run scripts/talk_pdfs.sh"
    else:
        commit, state = stamp.read_text().split()
        if state != "clean":
            problem = "exported from uncommitted deck changes; commit, then re-export"
        elif talk.fingerprint(commit) != talk.fingerprint("HEAD"):
            problem = "the deck changed after the export; re-export"
        elif missing := [n for n in names if not (talk.staging() / n).is_file()]:
            problem = f"missing in {talk.staging()}: {', '.join(missing)}"
    if problem:
        fail(f"{talk.name}: {problem}; nothing uploaded")
        return 1
    deposition = zenodo.call("GET", f"/deposit/depositions/{talk.record_id}")
    if deposition.get("submitted"):
        fail(f"{talk.name}: already published as {deposition['doi']}; files are final")
        return 1
    for old in zenodo.call("GET", f"/deposit/depositions/{talk.record_id}/files"):
        if old["filename"] in names:
            zenodo.call(
                "DELETE", f"/deposit/depositions/{talk.record_id}/files/{old['id']}"
            )
    bucket = deposition["links"]["bucket"]
    for name in names:
        data = (talk.staging() / name).read_bytes()
        zenodo.call("PUT", f"{bucket}/{name}", data=data)
        print(f"{talk.name}: uploaded {name} ({len(data) / 1e6:.1f} MB)")
    talk.store(**{talk.key_pdfs: talk.fingerprint("HEAD")})
    record = zenodo.base.removesuffix("/api") + f"/records/{talk.record_id}/files"
    print(f"{talk.name}: commit zenodo.yml ({talk.key_pdfs}); once published:")
    for name in names:
        print(f"  {record}/{name}")
    return 0


def publish(zenodo, talk, ref, draft_only):
    if not talk.record_id:
        fail(f"{talk.name}: no reserved record; run `scripts/zenodo_talks.py reserve` and commit the sidecar")
        return 1
    deposition = zenodo.call("GET", f"/deposit/depositions/{talk.record_id}")
    if deposition.get("submitted"):
        published = FINGERPRINT_NOTE.search(deposition["metadata"].get("notes", ""))
        if published and published.group(1) != talk.fingerprint(ref):
            print(
                f"::warning::{talk.name}: changed since its publication as {deposition['doi']}; a new Zenodo version is not automated"
            )
        else:
            print(f"{talk.name}: already published as {deposition['doi']}, skipped")
        return 0
    if problem := talk.pdf_state(ref):
        fail(f"{talk.name}: {problem}; not published")
        return 1
    deposition = zenodo.call(
        "PUT",
        f"/deposit/depositions/{talk.record_id}",
        {"metadata": talk.metadata(ref)},
    )
    doi = deposition["metadata"].get("prereserve_doi", {}).get("doi")
    if doi != talk.meta.get(talk.key_doi):
        fail(f"{talk.name}: Zenodo holds DOI {doi}, the sidecar {talk.meta.get(talk.key_doi)}; not published")
        return 1
    names = talk.meta.get("files", [])
    files = f"/deposit/depositions/{talk.record_id}/files"
    for old in zenodo.call("GET", files):  # a re-run replaces the zip; the PDFs stay
        if old["filename"] not in names:
            zenodo.call("DELETE", f"{files}/{old['id']}")
    bucket = deposition["links"]["bucket"]
    zenodo.call("PUT", f"{bucket}/{talk.name}.zip", data=talk.archive(ref))
    held = {f["filename"]: f.get("filesize", 0) for f in zenodo.call("GET", files)}
    if missing := [n for n in names if not held.get(n)]:
        fail(f"{talk.name}: the draft lacks {', '.join(missing)}; upload first; not published")
        return 1
    if draft_only:
        print(f"{talk.name}: draft {talk.record_id} ready for review: {deposition['links']['html']}")
        return 0
    published = zenodo.call(
        "POST", f"/deposit/depositions/{talk.record_id}/actions/publish"
    )
    print(f"{talk.name}: published as https://doi.org/{published['doi']}")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "mode",
        nargs="?",
        choices=("plan", "check", "reserve", "upload", "publish"),
        default="plan",
    )
    parser.add_argument("--sandbox", action="store_true")
    parser.add_argument("--draft-only", action="store_true")
    parser.add_argument("--ref", default=os.environ.get("GITHUB_REF_NAME") or "HEAD")
    args = parser.parse_args()
    talk = Talk(args.sandbox)
    if args.mode == "plan":
        return plan(talk, args.ref)
    zenodo = Zenodo(args.sandbox)
    if args.mode == "check":
        return check(zenodo)
    if args.mode == "reserve":
        return reserve(zenodo, talk, args.ref)
    if args.mode == "upload":
        return upload(zenodo, talk)
    return publish(zenodo, talk, args.ref, args.draft_only)


if __name__ == "__main__":
    sys.exit(main())
