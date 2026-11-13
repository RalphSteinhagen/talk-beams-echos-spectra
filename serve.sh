#!/usr/bin/env bash
# Serves this deck and opens it in a gr4-present viewer.
#
#   ./serve.sh            serve on port 8000, open the viewer
#   ./serve.sh -p 8010    another port
#   ./serve.sh --no-open  serve only
#
# The deck needs a viewer with the `masters:` key (gr4-present branch `deck-masters`). With GR4_PRESENT set to
# such a checkout whose WASM-Minimal build exists, that viewer is served on port 8080 and opened; otherwise the
# public page https://ralphsteinhagen.github.io/gr4-present/ is opened (GR4_PRESENT_VIEWER overrides), which
# shows the slides without their masters until it carries the branch. The public page reads the deck through
# devtools/serve.mjs --cors; Chrome asks once for "local network access" the first time it reads localhost.
# Tick "follow edits" in the viewer's side menu (Ctrl+O) to reload the deck when a file changes.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
viewer="${GR4_PRESENT_VIEWER:-https://ralphsteinhagen.github.io/gr4-present/}"
port=8000
open=1
while [ $# -gt 0 ]; do
  case "$1" in
    -p|--port) port="$2"; shift 2 ;;
    --no-open) open=0; shift ;;
    -h|--help) sed -n '2,12p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done
local_viewer="${GR4_PRESENT:-$HOME/git/gr4-present}/cmake-build-WASM-Minimal/viewer-web"
if [ -z "${GR4_PRESENT_VIEWER:-}" ] && [ -f "$local_viewer/index.html" ]; then
  if ! curl -s "http://localhost:8080/index.html" >/dev/null; then
    node "${here}/devtools/serve.mjs" --no-browser --directory "$local_viewer" --port 8080 >/dev/null 2>&1 &
    trap 'kill $! 2>/dev/null' EXIT
  fi
  viewer="http://localhost:8080/"
fi
address="${viewer}?presentation=http://localhost:${port}"
echo "deck:   ${here}"
echo "viewer: ${address}"
if [ "$open" = 1 ]; then
  (sleep 1; xdg-open "$address" >/dev/null 2>&1 || true) &
fi
exec node "${here}/devtools/serve.mjs" --cors --no-browser --directory "${here}" --port "${port}"
