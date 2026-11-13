#!/usr/bin/env bash
# Presents the talk from this computer without a network: the pinned gr4-present viewer (`viewer:` in zenodo.yml,
# viewer/<commit>/VERSION) kept in ~/.cache/beams-echoes-viewer/<commit>, fetched and checked against VERSION's SHA-256
# when missing, this deck linked beside its index.html as `beams`, both served from that one folder by devtools/serve.mjs
# (the COOP/COEP headers the viewer's threads need), and Chrome opened on it. Ctrl+C stops the server.
#
#   devtools/present-offline.sh [--port N] [--view <slide id>] [--no-open]      (default port 8090)
#
#   http://localhost:<port>/?presentation=beams&theme=dark[#view=<slide id>]
#
# Run it once while online, so the viewer is in the cache; then it needs no network. The deck is linked, not copied: an
# edit shows on the next reload. Port 8090 is the one Chrome has granted the microphones, the camera and the dongle on (a
# grant holds per address), and a server already answering there is used only if it serves this pinned viewer and
# this deck; any other stops the script rather than open a stale build. BEAMS_VIEWER_CACHE moves the cache.
set -euo pipefail

here=$(cd "$(dirname "$0")/.." && pwd)
port=8090
view=""
open=1
while (($#)); do
  case $1 in
  --port) port=${2:?--port needs a number}; shift 2 ;;
  --view) view=${2:?--view needs a slide id}; shift 2 ;;
  --no-open) open=0; shift ;;
  -h | --help) sed -n '2,15p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
  *) echo "unknown option $1 (see --help)" >&2; exit 1 ;;
  esac
done

short=$(sed -nE 's/^viewer: *"?([0-9a-f]{7})"?.*/\1/p' "$here/zenodo.yml")
version_file="$here/viewer/$short/VERSION"
[[ -n "$short" && -f "$version_file" ]] || { echo "zenodo.yml names no viewer pinned in viewer/<commit>/VERSION" >&2; exit 1; }
release=$(awk '/^release:/ {print $2}' "$version_file")
release_page=$(awk '/^release:/ {print $3}' "$version_file")
archive=$(awk '/^archive:/ {print $2}' "$version_file")
sha=$(awk '/^archive:/ {print $4}' "$version_file")

cache=${BEAMS_VIEWER_CACHE:-$HOME/.cache/beams-echoes-viewer}
viewer="$cache/$short"
if [[ ! -f "$viewer/index.wasm" ]]; then
  mkdir -p "$cache"
  if ! echo "$sha  $cache/$archive" | sha256sum --check --status 2>/dev/null; then
    echo "fetching the pinned viewer $release ($short), about 60 MB"
    curl -fL --retry 5 -C - -o "$cache/$archive" "${release_page/\/tag\//\/download\/}/$archive"
  fi
  echo "$sha  $cache/$archive" | sha256sum --check --quiet || {
    echo "$cache/$archive is not the archive viewer/$short/VERSION pins: delete it and run again" >&2
    exit 1
  }
  unpacked=$(mktemp -d "$cache/.unpack.XXXXXX")
  tar -xzf "$cache/$archive" -C "$unpacked"
  mv "$unpacked/${archive%.tar.gz}" "$viewer"
  rmdir "$unpacked"
fi

# the deck beside index.html, where `?presentation=beams` finds it
if [[ -e "$viewer/beams" && ! -L "$viewer/beams" ]]; then
  echo "$viewer/beams exists and is not a link to this deck: move it away" >&2
  exit 1
fi
ln -sfn "$here" "$viewer/beams"

address="http://localhost:$port/?presentation=beams&theme=dark${view:+#view=$view}"
open_browser() {
  ((open)) || return 0
  local browser=${GR4_PRESENT_BROWSER:-}
  for candidate in google-chrome google-chrome-stable chromium chromium-browser xdg-open; do
    [[ -n "$browser" ]] && break
    command -v "$candidate" >/dev/null 2>&1 && browser=$candidate
  done
  "$browser" "$address" >/dev/null 2>&1 &
}

if curl -s -o /dev/null "http://localhost:$port/"; then
  # someone serves this port already: this viewer's build (its service worker carries the build id) and this deck?
  if curl -s "http://localhost:$port/gr4-serviceworker.js" | cmp -s - "$viewer/gr4-serviceworker.js" &&
    curl -s "http://localhost:$port/beams/index.yml" | cmp -s - "$here/index.yml"; then
    echo "already served on port $port: $address"
    open_browser
    exit 0
  fi
  echo "port $port serves something else (another viewer build or deck): stop it, or pick --port <n>" >&2
  exit 1
fi

node "$here/devtools/serve.mjs" --no-browser --directory "$viewer" --port "$port" >/dev/null &
server=$!
trap 'kill "$server" 2>/dev/null || true' EXIT INT TERM
for _ in $(seq 100); do
  curl -s -o /dev/null "http://localhost:$port/index.html" && break
  kill -0 "$server" 2>/dev/null || { echo "the server did not start (port $port taken?)" >&2; exit 1; }
  sleep 0.1
done
echo "presenting the pinned viewer $release ($short) with this deck: $address"
echo "Ctrl+C stops the server"
open_browser
wait "$server"
