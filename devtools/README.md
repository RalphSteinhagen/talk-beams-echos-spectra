# Presenting the deck

How to show the talk and set up its live demonstrations; the overview is in the [README](../README.md).

## The deck

`talk.md` is a [gr4-present](https://github.com/RalphSteinhagen/gr4-present) deck (`entry:` in `index.yml`): 21
slides, then the backups and the references. The arc: Maxwell and Hertz, the Braggs and X-rays → 1914–1918, a real
problem (where is that gun?) → experiments 1 and 2, sound ranging and Tucker's microphone live → one problem, many
disguises → Widerøe, the betatron, radio navigation, the "Battle of the Beams", signals you did not mean to send →
pulses or spectra, experiment 3 (a tuning fork's phase) → the klystron loop, the people → Schottky noise, the MIM,
experiment 4 (a chirp below the noise) → not a tree but a braid → learn from it twice. Speaker notes are in each
slide's `:::notes`; historical claims are cited, or marked `[verify]` there.

```bash
./serve.sh            # serves this folder on :8000 and opens a viewer on it
./serve.sh -p 8001    # another port; --no-open only serves
```

The live regions of the experiment slides need a viewer built with OpenDigitizer: the pinned one of the live slides
(`viewer:` in `zenodo.yml`), or gr4-present's public full viewer,
`https://ralphsteinhagen.github.io/gr4-present/?presentation=http://localhost:8000` (a local `WASM-Minimal` build draws
an empty frame). Chrome asks once for *Local network access* to `localhost`; allow it (the lock icon in the address
bar). *Load* in the viewer's side menu (`Ctrl+O`) opens the folder from disk instead; tick *follow edits* to reload on
every change. Present fullscreen (F11) in the viewer's dark theme: the layout is exact at 16:9.

**Without a network: the pinned viewer locally.** `index.wasm` is ~190 MB, and `./serve.sh` alone opens gr4-present's
public viewer, or a local `WASM-Minimal` build without live regions. `devtools/present-offline.sh` keeps the pinned full
viewer (`viewer/<commit>/VERSION`) in `~/.cache/beams-echoes-viewer/`, fetched and checked once while online, links this
deck beside it and serves both on port 8090, where Chrome keeps its device grants, then opens Chrome on the deck;
`--view <slide id>` starts on a slide, `--help` says more:

```bash
devtools/present-offline.sh            # http://localhost:8090/?presentation=beams&theme=dark
```

**The four microphones.** Experiments 1 and 3 (slides `exp1`, `exp2`) start on a simulated source (OpenDigitizer's
PointSourceAudio), experiment 2 (slide `lowpass`) and the backups `camera` and `gains` on the microphones; the toolbar's
`input` switches between them, experiment 4 plays its recorded take. Microphones that are missing, refused or silent for
1.5 s (an unplugged interface's loopback pair delivers exact zeros) put `input` on `simulation` until they deliver
again; `simulation` picked by hand stays. The spacing is a toolbar choice too, `spacing`: 1 m (the talk, a 3 m line) or
0.2 m (a desk); `python3 devtools/make-workflows.py --spacing 0.2` makes 0.2 m the default for testing — regenerate
without the option before the talk. The browser captures at most two channels per audio source, so before the talk (and
after every login or re-plugging) split the 4-channel interface (here a Behringer UMC404HD, PipeWire profile "Pro
Audio") into two stereo sources, then allow the microphone when Chrome asks and pick `BEAMS_PAIR_A` in `input` (`pair B`
already names `BEAMS_PAIR_B`; slides `lowpass` and `gains` start on it):

```bash
devtools/four-mics-browser-pairs.sh setup      # BEAMS_PAIR_A = inputs 1, 2; BEAMS_PAIR_B = inputs 3, 4
devtools/four-mics-browser-pairs.sh status
devtools/four-mics-browser-pairs.sh revert     # afterwards: back to the default set-up
devtools/four-mics-browser-pairs.sh install    # or once, permanently (survives a reboot; `uninstall` removes it)
```

The 16-channel miniDSP UMA16v2 is split too, for the backup slide `camera` (OpenDigitizer's acoustic camera, after the
close) — with its corner microphones, not its first four: `UMA16_PAIR_A` (bottom row, aux1/aux14) and `UMA16_PAIR_B`
(top row, aux7/aux8), as OpenDigitizer's `uma16-browser-pairs.sh`; the toolbar picks the camera and the two pairs.
`install` writes the four pairs as PipeWire loopback virtual sources to
`~/.config/pipewire/pipewire.conf.d/60-browser-mic-pairs.conf` (user rights, no root) and restarts the user's PipeWire
services: each pair waits for its interface, never falls back to another microphone, relinks when the interface is
plugged in again, and the interfaces' own multichannel sources stay as they are for native applications; `setup` then
skips the pairs that exist already. The backup slide `gains` matches the four pre-amplifier gains before the talk: the microphones bundled before
one speaker, its `test noise` raised, each pre-amplifier turned until its offset to mic 1 reads 0.0 dB.


**The FM radio** (backup slide `fmradio`, after `camera`): an RTL-SDR dongle, tuned to 102.0 MHz. Click the toolbar's
`Connect RTL-SDR` and pick the dongle in Chrome's USB chooser; until then the slide shows a recorded screenshot. On
Linux Chrome needs write access to the dongle (e.g. the `rtlsdr` group) and the kernel's DVB driver blacklisted
(`dvb_usb_rtl28xxu`). The radio plays on the browser's default output; `pavucontrol` (Playback) moves it elsewhere.

## Layout

| path | content |
| --- | --- |
| `index.yml`, `talk.md` | the deck: masters, fonts and sizes once, then one `#` heading per slide, `:::notes` with bullet cues |
| `figures/` | the chalkboard masters (`devtools/make-masters.py`, from tables in cm, the board texture `chalk-*.jpg` embedded), the diagrams (`devtools/make-figures.py`) and the title panorama (`devtools/make-montage.py`) |
| `media/` | photographs, drawings, the Armistice clip and the portraits (`media/portraits/`), each with its source and licence in `media/CREDITS.md` or `media/portraits/PORTRAITS.md`; on a slide a picture carries only its reference number |
| `fonts/`, `effects/` | Patrick Hand and Patrick Hand SC (SIL Open Font License); the GREMLIN slide's wave-packet background |
| `workflows/*.grc` | the live `:::gr4` regions, from `devtools/make-workflows.py`: `exp1-claps`, `exp1b-lowpass`, `exp2-noise-tone` (the simulation or the microphones, 96 kS/s), `exp6-chirps` (the matched filter, 48 kS/s: the recorded take from `devtools/make-demo-data.py`, or the live ping and its echoes); the backups' `acoustic-camera` (OpenDigitizer's browser sample, the UMA16v2) `gain-match` (the pre-amplifier gains) and `fm-radio` (OpenDigitizer's FM radio, an RTL-SDR dongle) |
| `devtools/` | the generators above, `serve.mjs` (gr4-present's server), `shoot.mjs` (screenshots at 1600×900), `check-workflows.py` (every workflow parameter against its block's settings, since GR4 drops an unknown one silently), `four-mics-browser-pairs.sh`, `present-offline.sh` (the pinned viewer and this deck, offline) |
| `zenodo.yml`, `scripts/`, `viewer/` | the Zenodo record of the talk and its tools; the viewer pin of the live slides (below) |
| `.github/workflows/` | `pages.yml` (the live slides), `zenodo-talks.yml` (the Zenodo record) |
| `CLAUDE.md` (`AGENTS.md`), `CORE_*.md`, `.claude/commands/` | guidance for coding agents: GR4's rules, as in OpenDigitizer |
