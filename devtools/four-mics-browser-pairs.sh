#!/usr/bin/env bash
# The live experiment slides read four microphones in the browser, but Chrome captures at most two channels per audio
# source: this exposes the 4-channel USB interface (here a Behringer UMC404HD) as two stereo PipeWire sources,
# BEAMS_PAIR_A (inputs 1, 2) and BEAMS_PAIR_B (inputs 3, 4), which the workflows' opendigitizer::video::BrowserMicrophonePairs
# opens and re-aligns. A miniDSP UMA16v2 (16 channels) gets the same treatment for the backup slide `camera`, but with
# its CORNER microphones, not its first four: UMA16_PAIR_A (bottom row: aux1, aux14) and UMA16_PAIR_B (top row: aux7,
# aux8), as OpenDigitizer's src/blocks/video/tools/uma16-browser-pairs.sh, from which this script is copied and widened.
# Native applications keep the interfaces' own multichannel sources either way.
#
#   setup | revert | status      for this session only (gone after re-login): pulse remap modules for whichever devices are
#                                plugged in; a pair the permanent set-up already provides is skipped
#   install | uninstall          permanent (survives a reboot, user rights only): four PipeWire loopback virtual sources in
#                                ~/.config/pipewire/pipewire.conf.d/60-browser-mic-pairs.conf, each waiting for its device
#                                (no fallback to another microphone) and relinking when it is plugged in again; restarts
#                                the user's PipeWire services
#
# FOUR_MIC_SOURCE=<substring> picks the 4-channel interface by name; install takes the full node names from the plugged-in
# devices, else FOUR_MIC_NODE / UMA16_NODE, else the author's (below).
set -euo pipefail

pairs=("beams_pair_a BEAMS_PAIR_A 0,1" "beams_pair_b BEAMS_PAIR_B 2,3") # name, label, channel indices of the interface
uma16_pairs=("uma16_pair_a UMA16_PAIR_A aux1,aux14" "uma16_pair_b UMA16_PAIR_B aux7,aux8") # name, label, channels: rows bottom, top
uma16_pattern='^alsa_input[.]usb-miniDSP_UMA16v2.*multichannel-input'
# the author's devices, for `install` while one is unplugged (the UMC404HD in PipeWire's "Pro Audio" profile: AUX0-AUX3)
default_line_node=alsa_input.usb-BEHRINGER_UMC404HD_192k-00.pro-input-0
default_uma16_node=alsa_input.usb-miniDSP_UMA16v2_00026-00.multichannel-input
conf="${XDG_CONFIG_HOME:-$HOME/.config}/pipewire/pipewire.conf.d/60-browser-mic-pairs.conf"

# the interface: the named one, else the first ALSA input with at least four channels that is not the UMA16v2
master() {
  local want="${FOUR_MIC_SOURCE:-}"
  pactl list sources short | awk -v want="$want" '$2 ~ /^alsa_input/ {
    if (want != "") { if (index($2, want)) { print $2; exit } ; next }
    if (index($2, "miniDSP_UMA16")) next
    for (i = 3; i <= NF; i++) if ($i ~ /^[0-9]+ch$/) { n = $i; sub(/ch/, "", n); if (n + 0 >= 4) { print $2; exit } }
  }'
}

uma16_master() { pactl list sources short | awk -v uma16="$uma16_pattern" '$2 ~ uma16 { print $2; exit }'; }

# the master's channel names (front-left, …, aux0, …), so the pairs can name them
channel_names() { pactl list sources | awk -v src="$1" '$1 == "Name:" { on = ($2 == src) } on && /Channel Map:/ { sub(/.*Channel Map: */, ""); print; exit }'; }

# a pulse channel name as a PipeWire position: aux0 -> AUX0, front-left -> FL, rear-right -> RR, ...
position() {
  case "$1" in
    aux*) echo "AUX${1#aux}" ;;
    mono) echo MONO ;;
    lfe) echo LFE ;;
    *) echo "$1" | awk -F- '{ s = ""; for (i = 1; i <= NF; i++) s = s toupper(substr($i, 1, 1)); print s }' ;;
  esac
}

# the modules `setup` loaded, recognised by their source names
modules() { pactl list modules short | awk '$2 == "module-remap-source" && /source_name=(beams|uma16)_pair_[ab]( |$)/ { print $1 }'; }

exists() { pactl list sources short | awk -v name="$1" '$2 == name { found = 1 } END { exit !found }'; }

# pair <name> <label> <master> <channel>,<channel>: one stereo source from two channels of the master
pair() {
  if exists "$1"; then
    echo "$2: provided already (the permanent set-up, $conf)"
    return
  fi
  pactl load-module module-remap-source source_name="$1" source_properties="device.description=$2" master="$3" \
    master_channel_map="$4" channel_map=front-left,front-right remix=no >/dev/null || { revert; exit 1; }
  echo "$2: $4 of $3"
}

setup() {
  if [[ -n "$(modules)" ]]; then
    echo "already set up (modules $(modules | tr '\n' ' ')); run '$0 revert' first"
    exit 0
  fi
  local source uma16 names found=0
  source="$(master)"
  if [[ -n "$source" ]]; then
    IFS=, read -r -a names <<<"$(channel_names "$source")"
    [[ "${#names[@]}" -ge 4 ]] || { echo "$source has fewer than four channels" >&2; exit 1; }
    for entry in "${pairs[@]}"; do
      read -r name label indices <<<"$entry"
      IFS=, read -r i j <<<"$indices"
      pair "$name" "$label" "$source" "${names[$i]},${names[$j]}"
    done
    found=1
  else
    echo "no 4-channel input found (set FOUR_MIC_SOURCE=<part of its name>): no BEAMS pairs"
  fi
  uma16="$(uma16_master)"
  if [[ -n "$uma16" ]]; then
    for entry in "${uma16_pairs[@]}"; do
      read -r name label channels <<<"$entry"
      pair "$name" "$label" "$uma16" "$channels"
    done
    found=1
  fi
  [[ "$found" -eq 1 ]] || { echo "neither a 4-channel input nor a UMA16v2 found" >&2; exit 1; }
}

revert() {
  local found
  found="$(modules)"
  [[ -n "$found" ]] || { echo "nothing to revert"; return 0; }
  while read -r module; do
    pactl unload-module "$module" && echo "unloaded module $module"
  done <<<"$found"
}

status() {
  pactl list sources short | grep -E '(beams|uma16)_pair_[ab]' || echo "no pair sources"
  [[ -f "$conf" ]] && echo "permanent: $conf" || echo "permanent: not installed"
}

# loopback <name> <label> <node> <position> <position>: one permanent virtual stereo source from two channels of the node
loopback() {
  cat <<EOF
  {   name = libpipewire-module-loopback
      args = {
          node.description = "$2"
          capture.props = {
              node.name = "capture.$1"
              audio.position = [ $4 $5 ]
              stream.dont-remix = true     # take these two channels as they are
              target.object = "$3"
              node.dont-fallback = true    # never another microphone when the device is unplugged ...
              node.linger = true           # ... but wait for it, and relink when it is plugged in again
              node.dont-move = true
              node.passive = true          # the device runs only while the pair is in use
          }
          playback.props = {
              node.name = "$1"
              node.description = "$2"
              media.class = "Audio/Source"
              audio.position = [ FL FR ]
          }
      }
  }
EOF
}

restart() {
  systemctl --user restart pipewire pipewire-pulse wireplumber
  for _ in $(seq 1 20); do pactl info >/dev/null 2>&1 && return 0; sleep 0.5; done
  echo "PipeWire did not come back: systemctl --user status pipewire" >&2
  exit 1
}

install() {
  [[ -z "$(modules)" ]] || revert # the session's remap modules would collide with the permanent sources' names
  local line uma16 names positions=(AUX0 AUX1 AUX2 AUX3)
  line="$(master)"
  line="${line:-${FOUR_MIC_NODE:-$default_line_node}}"
  if exists "$line"; then
    IFS=, read -r -a names <<<"$(channel_names "$line")"
    for k in 0 1 2 3; do positions[k]="$(position "${names[$k]}")"; done
  fi
  uma16="$(uma16_master)"
  uma16="${uma16:-${UMA16_NODE:-$default_uma16_node}}"
  mkdir -p "$(dirname "$conf")"
  {
    echo "# written by talk-beam_echoes' devtools/four-mics-browser-pairs.sh install; remove with its 'uninstall'"
    echo "# two stereo sources per microphone interface for the browser (Chrome captures two channels per source); the"
    echo "# interfaces' own sources stay as they are for native applications"
    echo "context.modules = ["
    loopback beams_pair_a BEAMS_PAIR_A "$line" "${positions[0]}" "${positions[1]}"
    loopback beams_pair_b BEAMS_PAIR_B "$line" "${positions[2]}" "${positions[3]}"
    loopback uma16_pair_a UMA16_PAIR_A "$uma16" AUX1 AUX14
    loopback uma16_pair_b UMA16_PAIR_B "$uma16" AUX7 AUX8
    echo "]"
  } >"$conf"
  echo "wrote $conf: BEAMS_PAIR_A/B = ${positions[*]} of $line; UMA16_PAIR_A/B = AUX1,AUX14 / AUX7,AUX8 of $uma16"
  restart
  status
}

uninstall() {
  [[ -f "$conf" ]] || { echo "not installed"; return 0; }
  rm -f "$conf"
  echo "removed $conf"
  restart
  status
}

case "${1:-}" in
  setup) setup ;;
  revert) revert ;;
  status) status ;;
  install) install ;;
  uninstall) uninstall ;;
  *)
    echo "usage: $0 setup|revert|status|install|uninstall" >&2
    exit 2
    ;;
esac
