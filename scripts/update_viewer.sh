#!/usr/bin/env bash
# Pins a gr4-present web viewer for the live slides: viewer/<commit>/VERSION, which the Pages workflow reads to fetch
# that viewer at deploy time and serve it beside the deck:
#
#   scripts/update_viewer.sh [latest|vX.Y.Z] [full|minimal]          (default: latest full)
#
#   https://ralphsteinhagen.github.io/talk-beams-echos-spectra/viewer/<commit>/?presentation=../../default
#
# As fair-acc/gremlin's script of the same name, but the viewer stays out of git: this deck's live regions need the
# full viewer (live GNU Radio 4 and OpenDigitizer), whose index.wasm (~190 MB) exceeds GitHub's 100 MB file limit.
# The script downloads gr4-present-web-<flavour>-<version>.tar.gz from the gr4-present releases, checks it against the
# release's SHA256SUMS, and records release, commit and the archive's SHA-256 in VERSION; the Pages workflow refuses
# an archive whose SHA-256 differs. `latest` is rebuilt in place, so its pin holds until gr4-present's next build:
# pin a tagged release (vX.Y.Z) for a talk that is published.
#
# Name the folder as `viewer:` in zenodo.yml once the deck looks right in it (export the PDFs with a native build of
# the same commit); remove a folder once nothing names it.
set -euo pipefail
version=${1:-latest}
flavour=${2:-full}
repository=RalphSteinhagen/gr4-present
[[ "$version" =~ ^(latest|v[0-9]+\.[0-9]+\.[0-9]+)$ && "$flavour" =~ ^(minimal|full)$ ]] || {
  sed -n '2,19p' "$0"
  exit 2
}
root="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
name="gr4-present-web-${flavour}-${version}"

# the commit the release tag points to (`latest` moves with main): an annotated tag (vX.Y.Z) lists its own object first
# and the commit as `^{}`, a lightweight one (`latest`) only the commit
commit=$(git ls-remote "https://github.com/${repository}" "refs/tags/${version}^{}" "refs/tags/${version}" | awk '/\^\{\}$/ {peeled = $1} !/\^\{\}$/ {plain = $1} END {print peeled ? peeled : plain}')
[[ "$commit" =~ ^[0-9a-f]{40}$ ]] || {
  echo "no release tag ${version} in ${repository}" >&2
  exit 1
}
short=${commit:0:7}
target="$root/viewer/$short"
[[ ! -e "$target/VERSION" ]] || {
  echo "viewer/$short exists: that build is pinned already" >&2
  exit 1
}

work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
base="https://github.com/${repository}/releases/download/${version}"
curl -fsSL --retry 3 -o "$work/$name.tar.gz" "$base/$name.tar.gz"
curl -fsSL --retry 3 -o "$work/SHA256SUMS" "$base/SHA256SUMS"
(cd "$work" && grep -E "  ${name}\.tar\.gz\$" SHA256SUMS | sha256sum -c -)
sha=$(sha256sum "$work/$name.tar.gz" | cut -d' ' -f1)
# `latest` is rebuilt in place: the tag may have moved between the lookup above and the download
[[ "$version" != latest ]] || [[ "$(git ls-remote "https://github.com/${repository}" refs/tags/latest | cut -f1)" == "$commit" ]] || {
  echo "the latest release moved during the download; run again" >&2
  exit 1
}
tar -xzf "$work/$name.tar.gz" -C "$work"
for file in index.html index.js index.wasm gr4-serviceworker.js manifest.webmanifest icon.png; do
  [[ -f "$work/$name/$file" ]] || { echo "the archive lacks $file" >&2; exit 1; }
done
grep -q '<meta name="gr4-site" content="' "$work/$name/index.html" || {
  echo "index.html has no gr4-site address for the Pages workflow to replace; check the archive's page" >&2
  exit 1
}
mkdir -p "$target"
cat >"$target/VERSION" <<EOF
gr4-present web viewer (${flavour}), pinned by scripts/update_viewer.sh on $(date -u +%F); fetched at deploy time
release: ${version}  https://github.com/${repository}/releases/tag/${version}
commit:  ${commit}  https://github.com/${repository}/commit/${commit}
archive: ${name}.tar.gz  sha256 ${sha}
licence: GPL-3.0-or-later (LICENSES/GPL-3.0-or-later.txt), (C) R. J. Steinhagen, GSI/FAIR
EOF
echo "viewer/$short: the $flavour viewer $version ($commit), archive $(du -h "$work/$name.tar.gz" | cut -f1)"
echo "name it in zenodo.yml (viewer: \"$short\") once the deck looks right in it"
