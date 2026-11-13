#!/usr/bin/env bash
# The live experiment slides read four microphones in the browser, but Chrome captures at most two channels per audio
# source: this exposes the 4-channel USB interface as two stereo PipeWire sources, BEAMS_PAIR_A (channels 1, 2) and
# BEAMS_PAIR_B (channels 3, 4), which the workflows' opendigitizer::video::BrowserMicrophonePairs opens and re-aligns.
# Copied from OpenDigitizer's src/blocks/video/tools/uma16-browser-pairs.sh (the UMA16 corner pairs), for any 4-channel
# interface. Runtime only (gone after re-login); native applications keep the 4-channel source. Run it before opening the
# deck, `revert` afterwards to return to the default set-up.
# Usage: four-mics-browser-pairs.sh setup|revert|status   (FOUR_MIC_SOURCE=<substring> picks the interface by name)
set -euo pipefail

pairs=("beams_pair_a BEAMS_PAIR_A 0,1" "beams_pair_b BEAMS_PAIR_B 2,3") # name, label, channel indices of the master

# the interface: the named one, else the first ALSA input with at least four channels
master() {
  local want="${FOUR_MIC_SOURCE:-}"
  pactl list sources short | awk -v want="$want" '$2 ~ /^alsa_input/ {
    if (want != "") { if (index($2, want)) { print $2; exit } ; next }
    for (i = 3; i <= NF; i++) if ($i ~ /^[0-9]+ch$/) { n = $i; sub(/ch/, "", n); if (n + 0 >= 4) { print $2; exit } }
  }'
}

# the master's channel names (front-left, …, aux0, …), so the pairs can name them
channel_names() { pactl list sources | awk -v src="$1" '$1 == "Name:" { on = ($2 == src) } on && /Channel Map:/ { sub(/.*Channel Map: */, ""); print; exit }'; }

# the modules this script loaded, recognised by their source names
modules() { pactl list modules short | awk '$2 == "module-remap-source" && /source_name=beams_pair_[ab]( |$)/ { print $1 }'; }

setup() {
  if [[ -n "$(modules)" ]]; then
    echo "already set up (modules $(modules | tr '\n' ' ')); run '$0 revert' first"
    exit 0
  fi
  local source names
  source="$(master)"
  [[ -n "$source" ]] || { echo "no 4-channel input found (set FOUR_MIC_SOURCE=<part of its name>)" >&2; exit 1; }
  IFS=, read -r -a names <<<"$(channel_names "$source")"
  [[ "${#names[@]}" -ge 4 ]] || { echo "$source has fewer than four channels" >&2; exit 1; }
  for pair in "${pairs[@]}"; do
    read -r name label indices <<<"$pair"
    IFS=, read -r i j <<<"$indices"
    pactl load-module module-remap-source source_name="$name" source_properties="device.description=$label" master="$source" \
      master_channel_map="${names[$i]},${names[$j]}" channel_map=front-left,front-right remix=no >/dev/null || { revert; exit 1; }
    echo "$label: ${names[$i]},${names[$j]} of $source"
  done
}

revert() {
  local found
  found="$(modules)"
  [[ -n "$found" ]] || { echo "nothing to revert"; return 0; }
  while read -r module; do
    pactl unload-module "$module" && echo "unloaded module $module"
  done <<<"$found"
}

status() { pactl list sources short | grep -E 'beams_pair_[ab]' || echo "no pair sources"; }

case "${1:-}" in
  setup) setup ;;
  revert) revert ;;
  status) status ;;
  *)
    echo "usage: $0 setup|revert|status" >&2
    exit 2
    ;;
esac
