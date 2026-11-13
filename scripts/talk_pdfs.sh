#!/usr/bin/env bash
# Exports this deck to the two PDFs its Zenodo record carries, outside the repository:
#
#   $TALK_PDFS/<name>/<name>_slides.pdf   one page per slide, at its last step (the handout)
#   $TALK_PDFS/<name>/<name>_steps.pdf    one page per step (as presented)
#   (default TALK_PDFS: ~/.cache/beams-echoes-talks; <name>: `name:` in zenodo.yml)
#
#   scripts/talk_pdfs.sh
#
# Run it when the talk is final and committed, check the PDFs, then `scripts/zenodo_talks.py upload` puts them into
# the reserved Zenodo draft. The PDFs never enter git; export.stamp records the commit they show.
#
# The viewer is $GR4_PRESENT_BIN, else the newest cmake-build-*Release*/src/app/gr4-present in $GR4_PRESENT
# (default ~/git/gr4-present). Build it from the commit the live slides pin (`viewer:` in zenodo.yml), with
# OpenDigitizer, so the live regions export as they look: an older viewer silently drops what it does not know yet
# (masters, pictures, attributes) and ignores the deck's `export: { dpi: 150 }` picture resolution in index.yml.
set -euo pipefail
[ $# -eq 0 ] || { sed -n '2,16p' "$0"; exit 2; }
root="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
name="$(sed -n 's/^name:[[:space:]]*"\{0,1\}\([^"#[:space:]]*\)"\{0,1\}.*$/\1/p' "$root/zenodo.yml")"
[ -n "$name" ] || { echo "zenodo.yml has no name:" >&2; exit 1; }
out="${TALK_PDFS:-${XDG_CACHE_HOME:-$HOME/.cache}/beams-echoes-talks}/$name"
viewer="${GR4_PRESENT_BIN:-}"
if [ -z "$viewer" ]; then
  # shellcheck disable=SC2012 # build-directory names are plain
  viewer="$(ls -t "${GR4_PRESENT:-$HOME/git/gr4-present}"/cmake-build-*Release*/src/app/gr4-present 2>/dev/null | head -1)"
fi
[ -x "$viewer" ] || { echo "no gr4-present viewer; set GR4_PRESENT_BIN or GR4_PRESENT" >&2; exit 1; }
# the PDFs show the committed deck only when its tracked files match HEAD; README, licences, metadata and the
# infrastructure do not count (the lists in scripts/zenodo_talks.py: NOT_DECK, INFRASTRUCTURE)
state=clean
git -C "$root" diff --quiet HEAD -- . \
  ':(exclude)README.md' ':(exclude)CITATION.cff' ':(exclude).zenodo.json' ':(exclude)LICENSE' ':(exclude)LICENSES' \
  ':(exclude).github' ':(exclude).claude' ':(exclude)scripts' ':(exclude)viewer' ':(exclude).gitignore' \
  ':(exclude)zenodo.yml' ':(exclude)CLAUDE.md' ':(exclude)AGENTS.md' ':(exclude)CORE_*.md' || state=dirty
[ "$state" = clean ] || echo "warning: the deck has uncommitted changes; these PDFs cannot be uploaded" >&2
echo "viewer: $viewer ($(date -r "$viewer" +%F))"
mkdir -p "$out"
rm -f "$out/export.stamp"
for mode in slides steps; do
  pdf="$out/${name}_${mode}.pdf"
  log="$(mktemp)"
  "$viewer" --presentation "$root" --export "$mode" --export-to "$pdf" >"$log" 2>&1 || { cat "$log" >&2; exit 1; }
  # "stays a picture": a drawing embedded as pixels, not vectors; expected, so only counted
  echo "$pdf: $(pdfinfo "$pdf" 2>/dev/null | awk '/^Pages/ {print $2}') pages, $(du -h "$pdf" | cut -f1)," \
    "$(grep -c 'stays a picture' "$log" || true) drawings as pictures"
  grep WARNING "$log" | grep -v 'stays a picture' | sed 's/^/  /' || true
  rm -f "$log"
done
echo "$(git -C "$root" rev-parse HEAD) $state" >"$out/export.stamp"
echo "check both PDFs, then: scripts/zenodo_talks.py upload   (--sandbox for a trial)"
