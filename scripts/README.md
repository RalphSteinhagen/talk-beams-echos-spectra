# Archiving on Zenodo

The talk gets its own Zenodo DOI (type *presentation*), as the talks of [fair-acc/gremlin](https://github.com/fair-acc/gremlin/tree/main/talks)
do. Tools: [`zenodo_talks.py`](zenodo_talks.py), [`talk_pdfs.sh`](talk_pdfs.sh),
[`update_viewer.sh`](update_viewer.sh), workflow [`zenodo-talks.yml`](../.github/workflows/zenodo-talks.yml).

1. **Describe:** `zenodo.yml` holds title, description, date and conference; creators and keywords come from
   `.zenodo.json`. Check: `scripts/zenodo_talks.py plan`.
2. **Reserve the DOI** (token below), commit `zenodo.yml`:
   ```bash
   scripts/zenodo_talks.py reserve
   ```
   Put the DOI on the title slide, in the [README](../README.md) (its DOI badge) and in `CITATION.cff` (`preferred-citation`).
3. **PDFs** (stored on Zenodo only, never in git), when the talk is final and committed:
   ```bash
   scripts/talk_pdfs.sh                 # to ~/.cache/beams-echoes-talks/<name>/, check them
   scripts/zenodo_talks.py upload       # into the reserved draft; commit zenodo.yml (pdfs_from)
   ```
   Needs a native gr4-present build with OpenDigitizer of the pinned viewer's commit (`GR4_PRESENT_BIN`). A later
   deck change makes them stale: export and upload again.
4. **Push** to `main`: the Pages workflow deploys the live slides (Settings → Pages → Source: *GitHub Actions*). The
   Zenodo record links them as `…/viewer/<viewer>/?presentation=../../default`.
5. **Publish** before the talk (a reserved DOI does not resolve yet): the next GitHub release, or Actions → *Archive
   the talk on Zenodo* → mode `publish`, *sandbox* unticked. The record links this repository, so make it public
   first.
6. **Verify** `https://doi.org/<doi>`: two PDFs, the deck zip, the live-slides link.

Optional dry run on sandbox.zenodo.org: add `--sandbox` to `reserve`/`upload`/`publish`. Never cite a sandbox DOI. A
publish is permanent; a published talk is skipped on later runs.

**The viewer.** The live slides open in a pinned gr4-present web viewer, so a later gr4-present cannot change how
the published talk looks. gremlin keeps its (minimal) viewer in git; this deck needs the full one (live GNU Radio 4
and OpenDigitizer), whose `index.wasm` (~190 MB) exceeds GitHub's 100 MB file limit. So git keeps the pin only,
`viewer/<commit>/VERSION` (release, commit, the archive's SHA-256), and the Pages workflow fetches that release at
deploy time and refuses any other build:

```bash
scripts/update_viewer.sh               # gr4-present's latest full viewer, pinned in viewer/<commit>/VERSION
scripts/update_viewer.sh v0.2.0 full   # a tagged release
```

Name the folder as `viewer: "<commit>"` in `zenodo.yml` once the deck looks right in it; remove a pin once nothing
names it. `latest` is rebuilt in place, so its pin holds only until gr4-present's next build: pin a tagged release
for the published talk.

**Tokens.** Zenodo → Applications → **Personal access token** (not *Developer application*), scopes
`deposit:write` and `deposit:actions`; one on [zenodo.org](https://zenodo.org/account/settings/applications/tokens/new/),
one on [sandbox.zenodo.org](https://sandbox.zenodo.org/account/settings/applications/tokens/new/).

- CI: `gh secret set ZENODO_TOKEN -R RalphSteinhagen/talk-beams-echos-spectra` (and `ZENODO_SANDBOX_TOKEN`).
- Locally, paste at the silent prompt, then Enter:
  ```bash
  read -rsp 'Zenodo token: ' ZENODO_TOKEN && export ZENODO_TOKEN
  scripts/zenodo_talks.py check
  ```
- Never put a token on a command line, in a file, an issue or a chat.
