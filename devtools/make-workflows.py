#!/usr/bin/env python3
"""The live `:::gr4` workflows of the experiment slides: workflows/exp1-claps.grc, exp1b-lowpass.grc, exp2-noise-tone.grc
(OpenDigitizer's simulation or the microphones, 96 kS/s) and exp6-chirps.grc (the recorded take
media/exp6-chirps-recorded.wav from make-demo-data.py, or the live ping and its echoes).
Re-run after a change: python3 devtools/make-workflows.py

They use only the blocks today's gr4-present viewer registers (src/app/LiveGraph.cpp); what is still missing in GR4,
OpenDigitizer and the viewer is listed in claude_gr4_demo_report.md.

One channel's trigger serves all four: microphone 1's Schmitt trigger tags its stream; that stream minus itself is a
zero which carries the tag, and adding it to microphones 2-4 puts the same tag on theirs (GR4 forwards tags from every
input to every output), so the four snapshots share one time axis and the arrival differences can be read off it.

Connections to the trigger and the snapshots name their ports (`in`, `out`): GR4 main 02d6a41 (#881) puts event ports
first, so an index there would silently name an event port; by name the graphs load on the old and the new GR4."""
import argparse
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "workflows"
OUT.mkdir(exist_ok=True)
FS = 48000   # samples per second; the live experiments 1-3 set 96000 (author, round 56), experiment 4 replays 48 kHz takes


def S(seconds):
    """a duration in samples at the current FS (every window, hold-off and history below is a time, not a count)"""
    return round(seconds * FS)
MICS = 4
FILTERS_IN_VIEWER = True    # the public viewer registers every GR4 block since gr4-present 74ab5a4 (2026-11-12), BasicFilterProto among them;
                            # False: experiment 1 runs without its 20 Hz high-pass and 1b's standby plays a take filtered offline
MIC_COLOURS = [0xF2F2F2, 0xFDB342, 0x268BD2, 0x859900]   # chalk, then the deck's first three series colours — the ones
                                                         # OpenDigitizer's LocalisationChart draws its hyperbolae in
# The line of four microphones, uniform (author, 2026-11-13): 1 m apart for the talk (a 3 m base, a ~10 x 10 m room,
# the ranging charts a 5 x 5 m area), 0.2 m apart for testing at a desk. Both live in every workflow: a `spacing` choice
# in the toolbar sets the geometry, as OpenDigitizer's XtraLocalisationLine sample does (element positions of the
# simulation, the locators and the chart, the chart's area, the correlation's reach, the simulated source's path);
# `--spacing 0.2` makes 0.2 m the default. Uniform rather than non-redundant (0, 0.5, 2, 3 m): PairDelayArrivals dates
# every arrival against mic 1 (pairs 1-2, 1-3, 1-4, one peak each), so the full base is always a measured pair — only a
# locator that weighs all six pairs together (SRP-PHAT) would profit. make-demo-data.py synthesises its takes for 1 m.
GEOMETRIES = {
    "1 m": dict(spacing=1.0, roi=[-2.5, 2.5, -0.1, 5.0],        # 5 x 5 m, from -0.1 so the microphones stay in sight
                max_lag=9.375e-3,                                # s: > pair 1-4's 8.75 ms (3 m at 343 m/s)
                drum=([0.4, 2.0], [1.2, 0.6]), fork=([0.0, 2.0], [0.8, 0.4])),   # the simulated source's circle: centre, extent
    "0.2 m": dict(spacing=0.2, roi=[-1.0, 1.0, -0.05, 1.3],
                  max_lag=2.0e-3,                                # s: > pair 1-4's 1.75 ms (0.6 m)
                  drum=([0.2, 0.7], [0.35, 0.15]), fork=([0.15, 0.7], [0.3, 0.15])),
}
_cli = argparse.ArgumentParser(description="the live workflows of the experiment slides")
_cli.add_argument("--spacing", choices=["1", "0.2"], default="1", help="the default microphone spacing in m (the toolbar switches)")
DEFAULT = "1 m" if _cli.parse_args().spacing == "1" else "0.2 m"
GEOMETRY = GEOMETRIES[DEFAULT]


def mic_x(spacing):
    return [round(spacing * (k - (MICS - 1) / 2), 4) for k in range(MICS)]


def positions(spacing):
    return Raw("!!float64 [" + ", ".join(f"[{x}, 0.0, 0.0]" for x in mic_x(spacing)) + "]")


MIC_X = mic_x(GEOMETRY["spacing"])
RANGING_ROI = GEOMETRY["roi"]


class Raw(str):
    """a YAML value written as is (a flow list, a tagged value), not quoted"""
F32 = "float32"


def block(kind, name, comment=None, **parameters):
    lines = [f"  - id: {kind}", "    parameters:", f"      name: {name}"]
    for key, value in parameters.items():
        if isinstance(value, bool):
            value = "true" if value else "false"
        elif isinstance(value, str) and not isinstance(value, Raw) and (value in ("", "-", "+", "*", "/") or any(c in value for c in ":,#")):
            value = f'"{value}"'
        lines.append(f"      {key}: {value}")
    if comment:
        lines[2] += f" # {comment}"
    return "\n".join(lines)


def control(name, label, unit, value, lo, hi, step, target):
    return block("DigitizerUi::ImControlNumber", name, label=label, unit=unit, value=value, min=lo, max=hi, step=step,
                 style="slider", target_map=target)


def sink(name, label, dataset=False, **extra):
    kind = f"opendigitizer::ImPlotSink<gr::DataSet<{F32}>>" if dataset else f"opendigitizer::ImPlotSink<{F32}>"
    return block(kind, name, signal_name=label, **extra)


class Graph:
    def __init__(self, recorded, take=None, sim=None, live=False, shaken=None, ping=False):
        """recorded: a take played at the wall clock (experiment 4); `ping`: with it, an `input` control that switches
        the four channels to the microphones and the speaker from the take's microphone 1 to the live ping (the
        `speakerSource` switch, group 1, fed by the caller); sim: PointSourceAudio settings — a simulated source
        on the line of microphones, continuously, and an `input` control that switches the four channels to the
        microphones (two browser stereo sources, devtools/four-mics-browser-pairs.sh), as OpenDigitizer's
        XtraLocalisationLine sample does (author, round 55: no standby, no restart, the positions shift); `live`: start on
        the microphones rather than the simulation (author, round 56: slide 8); `shaken` = dict(level, f_env, band): the
        simulation's shakers — Gaussian noise, independent per microphone, band-passed, its amplitude swelling with one
        sine for all four (author, round 56: slide 8, 500 Hz – 8 kHz), added to the simulated channels only"""
        self.blocks, self.connections, self.sources = [], [], []
        self.recorded = recorded
        self.ping = ping
        self.sim = sim is not None
        if sim is not None:
            names = Raw("[" + ", ".join(f'"mic {k + 1}"' for k in range(MICS)) + "]")
            self.blocks += [
                block("gr::basic::ClockSource", "clock", "paces the simulation", sample_rate=FS, chunk_size=1024, n_samples_max=0),
                block("opendigitizer::localisation::PointSourceAudio", "simulatedMicrophones", "a source moving in front of the line",
                      element_positions=Raw("!!float64 [" + ", ".join(f"[{x}, 0.0, 0.0]" for x in MIC_X) + "]"),
                      sample_rate=FS, tag_interval=600.0, **sim),
                block("opendigitizer::video::BrowserMicrophonePairs", "soundcard",
                      "four microphones from two browser stereo sources (devtools/four-mics-browser-pairs.sh)",
                      pair_a="BEAMS_PAIR_A", pair_b="BEAMS_PAIR_B", sample_rate=float(FS), align="once"),
                block("gr::basic::Switch<float32>", "source", "simulation (group 0) or microphones (group 1)",
                      n_groups=2, n_channels=MICS, group=Raw(f"!!uint32 {1 if live else 0}")),
                "  - id: DigitizerUi::ImControlDevice\n    parameters:\n      name: input\n      label: input\n"
                f"      value: {'BEAMS_PAIR_A' if live else 'simulation'}\n"
                "      choices: [\"simulation\"]\n      target_map: \"soundcard:pair_a\"\n      choice_values:\n        simulation:\n"
                "          \"source:group\": !!uint32 0\n      device_values:\n        \"source:group\": !!uint32 1",
                "  - id: DigitizerUi::ImControlDevice\n    parameters:\n      name: pairB\n      label: pair B\n      target_map: \"soundcard:pair_b\"",
            ]
            self.connections.append("[ clock, 0, simulatedMicrophones, 0 ]")
            for k in range(MICS):
                self.connections.append(f"[ soundcard, [0, {k}], source, [0, {k + MICS}] ]")
                if shaken is None:
                    self.connections.append(f"[ simulatedMicrophones, [0, {k}], source, [0, {k}] ]")
            if shaken is not None:
                level, f_env, (f_low, f_high) = shaken["level"], shaken["f_env"], shaken["band"]
                self.blocks += [
                    block(f"gr::basic::SignalGenerator<{F32}>", "shakerSwell", "the shakers' swell: level · (1 + sin), one for all four",
                          signal_type="Sin", frequency=f_env, amplitude=level, offset=level, sample_rate=FS, chunk_size=480),
                    control("shakers", "sim. noise", "FS", level, 0, 0.5, 0.01, "shakerSwell:amplitude;shakerSwell:offset"),   # the label says it is simulated (author)
                ]
                for k in range(MICS):
                    self.blocks += [
                        block(f"gr::basic::SignalGenerator<{F32}>", f"hiss{k}", f"mic {k + 1}'s own noise", signal_type="GaussianNoise",
                              amplitude=1.0, seed=Raw(f"!!uint64 {1918 + k}"), sample_rate=FS, chunk_size=480),
                        block(f"gr::filter::BasicFilterProto<{F32}, gr::Resampling<1, 1, false>>", f"hissBand{k}", filter_type="IIR",
                              filter_response="BANDPASS", iir_design_method="BUTTERWORTH", filter_order=4, f_low=float(f_low),
                              f_high=float(f_high), sample_rate=FS),
                        block(f"gr::blocks::math::Multiply<{F32}, std::multiplies<{F32}>>", f"shaken{k}", n_inputs=2),
                        block(f"gr::blocks::math::Add<{F32}, std::plus<{F32}>>", f"withShakers{k}", n_inputs=2),
                    ]
                    self.connections += [f"[ hiss{k}, 0, hissBand{k}, 0 ]", f"[ hissBand{k}, 0, shaken{k}, [0, 0] ]",
                                         f"[ shakerSwell, 0, shaken{k}, [0, 1] ]",
                                         f"[ simulatedMicrophones, [0, {k}], withShakers{k}, [0, 0] ]", f"[ shaken{k}, 0, withShakers{k}, [0, 1] ]",
                                         f"[ withShakers{k}, 0, source, [0, {k}] ]"]
            self.pre = {}
            return
        if recorded:
            self.blocks += [
                block(f"gr::basic::SignalGenerator<{F32}>", "wallClock", "silent, paces the file at the wall clock",
                      signal_type="Const", amplitude=0, sample_rate=FS, chunk_size=480),
                block(f"gr::blocks::fileio::WavSource<{F32}>", "recording", "its start tag dates the take for the trigger",
                      uri=take, repeat=True, trigger_name="TAKE_START"),
                block(f"gr::present::blocks::Deinterleave<{F32}>", "channels", n_channels=MICS),
                block(f"gr::audio::AudioSink<{F32}>", "speaker", "the live ping or the take's microphone 1 to the room" if ping
                      else "microphone 1 to the room", req_sample_rate=FS, n_inputs=1),
            ]
            self.connections.append("[ recording, 0, channels, 0 ]")
            if ping:   # one list switches both: the four channels (take or microphones) and what the speaker plays
                self.blocks += [
                    block("opendigitizer::video::BrowserMicrophonePairs", "soundcard",
                          "four microphones from two browser stereo sources (devtools/four-mics-browser-pairs.sh)",
                          pair_a="BEAMS_PAIR_A", pair_b="BEAMS_PAIR_B", sample_rate=float(FS), align="once"),
                    block("gr::basic::Switch<float32>", "source", "the take (group 0) or the microphones (group 1)",
                          n_groups=2, n_channels=MICS, group=Raw("!!uint32 0")),
                    block("gr::basic::Switch<float32>", "speakerSource", "the take's microphone 1 (group 0) or the live ping (group 1)",
                          n_groups=2, n_channels=1, group=Raw("!!uint32 0")),
                    "  - id: DigitizerUi::ImControlDevice\n    parameters:\n      name: input\n      label: input\n"
                    "      value: recorded\n      choices: [\"recorded\"]\n      target_map: \"soundcard:pair_a\"\n      choice_values:\n"
                    "        recorded:\n          \"source,speakerSource:group\": !!uint32 0\n      device_values:\n"
                    "        \"source,speakerSource:group\": !!uint32 1",
                    "  - id: DigitizerUi::ImControlDevice\n    parameters:\n      name: pairB\n      label: pair B\n      target_map: \"soundcard:pair_b\"",
                ]
                self.connections += ["[ channels, [0, 0], speakerSource, [0, 0] ]", "[ speakerSource, [0, 0], speaker, 0 ]"]
            else:
                self.connections.append("[ channels, [0, 0], speaker, 0 ]")
            # every channel paced alike: the same tags, so the four triggers date their events on one time base
            for k in range(MICS):
                self.blocks.append(block(f"gr::blocks::math::Add<{F32}, std::plus<{F32}>>", f"paced{k}", n_inputs=2))
                self.connections += [f"[ channels, [0, {k}], paced{k}, [0, 0] ]", f"[ wallClock, 0, paced{k}, [0, 1] ]"]
                if ping:
                    self.connections += [f"[ paced{k}, 0, source, [0, {k}] ]", f"[ soundcard, [0, {k}], source, [0, {k + MICS}] ]"]
        else:   # Chrome captures two channels per source: devtools/four-mics-browser-pairs.sh splits the interface into
                # two stereo sources, OpenDigitizer's BrowserMicrophonePairs re-aligns them into four (author, 2026-11-13); `align: once` (OpenDigitizer b44a908, gr4-present v0.1.0) holds
                # the first agreed shift: at 1 m spacing the first microphones of the two pairs are 2 m apart, beyond what the
                # continuous estimate resolves (> 1.6 m at 48 kHz, > 0.7 m at 96 kHz); the shift is published as `lag`
            self.blocks.append(block("opendigitizer::video::BrowserMicrophonePairs", "mics",
                                     "four microphones from two browser stereo sources (devtools/four-mics-browser-pairs.sh)",
                                     pair_a="BEAMS_PAIR_A", pair_b="BEAMS_PAIR_B", sample_rate=float(FS), align="once"))
        self.pre = {}   # microphone k's stream after the optional filters, the trigger's and the traces' input

    def filters(self, highpass=None, lowpass=None, lowpass_slider=None, band=None):
        """Per microphone: an optional IIR high-pass (2nd order, takes out DC and the interface's saturation/clamping
        transient), an optional 4th-order IIR low-pass whose cut-off one slider sets for all four, or an optional
        4th-order IIR band-pass `band` = (f_low, f_high) whose edges the waterfall's range handles set (experiment 1b)."""
        for k in range(MICS):
            stream = self.raw(k)
            for name, response, order, f in (("hp", "HIGHPASS", 2, highpass), ("lp", "LOWPASS", 4, lowpass), ("bp", "BANDPASS", 4, band)):
                if f is None:
                    continue
                edges = dict(f_low=f[0], f_high=f[1]) if isinstance(f, tuple) else dict(f_low=f)
                self.blocks.append(block(f"gr::filter::BasicFilterProto<{F32}, gr::Resampling<1, 1, false>>", f"{name}{k}",
                                         filter_type="IIR", filter_response=response, iir_design_method="BUTTERWORTH",
                                         filter_order=order, **edges, sample_rate=FS))
                self.connections.append(f"[ {stream}, {name}{k}, 0 ]")
                stream = f"{name}{k}, 0"
            self.pre[k] = stream
        if lowpass is not None and lowpass_slider:
            lo, hi, step = lowpass_slider
            self.blocks.append(control("lowpass", "low-pass", "Hz", lowpass, lo, hi, step,
                                       ",".join(f"lp{k}" for k in range(MICS)) + ":f_low"))

    def rectified(self, highpass=None):
        """The triggers' input per microphone (author, round 56): |x| of the filtered stream, after an optional
        high-pass (2nd-order Butterworth) — both polarities count, so a hit whose first swing is negative fires at
        once, and rumble, ventilation and hum stay below the threshold. The traces and the correlation keep the
        signal itself. Returns the four rectified streams' (block, port)."""
        streams = []
        for k in range(MICS):
            source = self.stream(k)
            if highpass:
                self.blocks.append(block(f"gr::filter::BasicFilterProto<{F32}, gr::Resampling<1, 1, false>>", f"trigHp{k}",
                                         filter_type="IIR", filter_response="HIGHPASS", iir_design_method="BUTTERWORTH",
                                         filter_order=2, f_low=float(highpass), sample_rate=FS))
                self.connections.append(f"[ {source}, trigHp{k}, 0 ]")
                source = f"trigHp{k}, 0"
            self.blocks.append(block(f"gr::blocks::type::converter::Abs<{F32}>", f"rect{k}", f"|mic {k + 1}| for the triggers"))
            self.connections.append(f"[ {source}, rect{k}, 0 ]")
            streams.append(f"rect{k}, 0")
        return streams

    def stream(self, k):
        return self.pre.get(k, self.raw(k))

    def raw(self, k):
        """Microphone k's stream before the trigger: simulated or live (the switch), recorded from the paced file."""
        if self.sim or self.ping:
            return f"source, [0, {k}]"
        if self.recorded:
            return f"paced{k}, 0"
        return f"mics, [0, {k}]"

    def triggered(self, threshold, n_pre, n_post, holdoff, offsets=None, continuous=None, trigger_on=None, controls=True,
                  hysteresis=None, marks=None):
        """Microphone 1's trigger, shared by the four snapshots; returns the four tagged streams' (block, port).
        `offsets` (FS) lift each trace by a constant (AddConst), a stacked "mountain range" view with
        mic 1 on top; `continuous` (samples) adds a streaming sink per microphone for the running traces;
        `trigger_on` (block, port): the stream the trigger watches instead of microphone 1's (experiment 4: the matched
        filter's output — radar detects after the matched filter; experiments 1 and 2: the first microphone to cross),
        the four traces stay the raw microphones; `marks`: per microphone a zero that carries that microphone's own
        trigger tag, added to its trace, so each trace shows where it triggered beside the common anchor."""
        source = trigger_on or self.stream(0)
        self.blocks += [
            block(f"gr::blocks::trigger::SchmittTriggerNoInterpolation<{F32}>", "trigger",
                  ("on the matched filter's output" if "matched" in trigger_on else "on the first microphone to cross")
                  if trigger_on else "on microphone 1",
                  threshold=threshold, hysteresis=round(threshold / 5, 3) if hysteresis is None else hysteresis,
                  edge="rising", dead_time=holdoff,
                  trigger_name_rising="RISING", sample_rate=FS),
            block(f"gr::blocks::math::Multiply<{F32}, std::multiplies<{F32}>>", "tagOnly", "zero, carrying the trigger tag", n_inputs=2)
            if self.recorded else
            block(f"opendigitizer::Arithmetic<{F32}>", "tagOnly", "zero, carrying the trigger tag", operation="-"),
        ]
        self.connections.append(f"[ {source}, trigger, in ]")
        if self.recorded:   # times the silent wall clock: zero, and paced
            self.connections += ["[ trigger, out, tagOnly, [0, 0] ]", "[ wallClock, 0, tagOnly, [0, 1] ]"]
        else:
            self.connections += ["[ trigger, out, tagOnly, 0 ]", f"[ {source}, tagOnly, 1 ]"]
        tagged = ["trigger, out"]
        if trigger_on:   # microphone 1's trace: its stream with the trigger's tag (and its own mark)
            inputs = 2
            self.connections += [f"[ {self.stream(0)}, tagged0, [0, 0] ]", "[ tagOnly, 0, tagged0, [0, 1] ]"]
            if marks:
                self.connections.append(f"[ {marks[0]}, tagged0, [0, {inputs}] ]")
                inputs += 1
            self.blocks.append(block(f"gr::blocks::math::Add<{F32}, std::plus<{F32}>>", "tagged0", n_inputs=inputs))
            tagged = ["tagged0, 0"]
        for k in range(1, MICS):
            inputs = 2
            self.connections += [f"[ {self.stream(k)}, tagged{k}, [0, 0] ]", f"[ tagOnly, 0, tagged{k}, [0, 1] ]"]
            if marks:
                self.connections.append(f"[ {marks[k]}, tagged{k}, [0, {inputs}] ]")
                inputs += 1
            self.blocks.append(block(f"gr::blocks::math::Add<{F32}, std::plus<{F32}>>", f"tagged{k}", n_inputs=inputs))
            tagged.append(f"tagged{k}, 0")
        # the lift: a constant added per sample, no second clock (round 57: paced Const generators added in made each
        # running trace lag by its generator's start, ~60 ms apart, where the true spread is a few ms)
        for k in range(MICS if offsets else 0):
            self.blocks.append(block(f"gr::blocks::math::AddConst<{F32}, std::plus<{F32}>>", f"lifted{k}", "the trace's lift",
                                     value=float(offsets[k])))
            self.connections.append(f"[ {tagged[k]}, lifted{k}, 0 ]")
            tagged[k] = f"lifted{k}, 0"
        for k in range(MICS):
            self.blocks += [
                block(f"gr::basic::StreamToDataSet<{F32}>", f"snapshot{k}", filter="RISING", n_pre=n_pre, n_post=n_post,
                      holdoff_samples=holdoff),
                sink(f"mic{k + 1}", f"mic {k + 1}", dataset=True, dataset_index=0, signal_unit="FS", n_history=1, color=MIC_COLOURS[k]),
            ]
            self.connections += [f"[ {tagged[k]}, snapshot{k}, in ]", f"[ snapshot{k}, out, mic{k + 1}, in ]"]
            self.sources.append(f"mic{k + 1}")
            if continuous:
                self.blocks.append(sink(f"run{k + 1}", f"mic {k + 1}", signal_unit="FS", n_history=continuous, color=MIC_COLOURS[k]))
                self.connections.append(f"[ {tagged[k]}, run{k + 1}, 0 ]")
                self.sources.append(f"run{k + 1}")
        if controls:   # the hold-off slider is gone (author, round 56: the toolbar was full); the hold-off stays as set
            self.blocks.append(control("threshold", "threshold", "FS", threshold, 0, 1, 0.01, "trigger:threshold"))
        return tagged

    def ranging(self, threshold, holdoff, min_confidence=2.0, max_lag=None, onsets=None, hysteresis=None,
                window=(0.010, 0.050), correlation=None, view_z=None):
        """Experiment 1's map, live, as OpenDigitizer's correlation layer does it: a level trigger per microphone cuts
        a window of all four channels around each hit (MultiChannelRecorder), the pairs of neighbouring channels are
        cross-correlated (their delays independent of the channels' levels — a drum's slow rise fools a plain threshold
        when the levels differ), the confident delays are associated and solved by the DelayLocator; the
        LocalisationChart draws the hyperbolae (pairs 1-2, 2-3, 3-4), where they cross, and the position. Noise from
        the shakers correlates with nothing: the hyperbolae vanish, until the band-pass (experiment 1b) removes it."""
        names = Raw("[" + ", ".join(f'"mic {k + 1}"' for k in range(MICS)) + "]")
        positions = Raw("!!float64 [" + ", ".join(f"[{x}, 0.0, 0.0]" for x in MIC_X) + "]")
        # max_lag: the geometry's (GEOMETRIES), more than pair 1-4's delay — PairDelayArrivals dates all against mic 1;
        # under N/2 = 1440 of the 2880-sample window; the `spacing` choice resets it
        max_lag = S(GEOMETRY["max_lag"]) if max_lag is None else max_lag
        # `onsets`: the triggers' input per microphone (rectified(): |high-pass| or |band-pass|), else the stream itself;
        # `window` (s before, after the first onset); `correlation`: PairCrossCorrelation's weighting and band
        correlation = dict(weighting="none", f_min=100.0, f_max=10000.0) | (correlation or {})
        for k in range(MICS):
            self.blocks.append(block(f"gr::blocks::trigger::LevelTrigger<{F32}>", f"onset{k}", f"mic {k + 1}'s hits",
                                     trigger_name=f"mic {k + 1}", threshold=threshold,
                                     hysteresis=round(threshold / 2, 3) if hysteresis is None else hysteresis,
                                     edge="rising", dead_time=float(holdoff), dead_time_unit="samples"))
            self.connections += [f"[ {onsets[k] if onsets else self.stream(k)}, onset{k}, 0 ]", f"[ onset{k}, 0, window, 0 ]",
                                 f"[ {self.stream(k)}, window, [1, {k}] ]"]
        self.blocks += [
            block(f"gr::blocks::trigger::MultiChannelRecorder<{F32}>", "window", "all four channels around a hit",
                  n_inputs=MICS, n_pre=S(window[0]), n_post=S(window[1]), retrigger="ignore", holdoff=round(holdoff / FS, 3),
                  emit_partial=False, history=0.5),   # s it may reach back: the onsets come through filters and rectifiers,
                                                      # later than the data; the default (twice the window) refused short windows
            block(f"opendigitizer::localisation::DataSetToTensor<{F32}>", "frames"),
            block(f"gr::localisation::PairCrossCorrelation<{F32}>", "correlation", max_lag=max_lag, **correlation),
            block(f"gr::localisation::PairDelay<{F32}>", "delays", max_lag=max_lag),
            block(f"opendigitizer::localisation::PairDelayArrivals<{F32}>", "arrivals", receiver_names=names, min_confidence=min_confidence),
            block("opendigitizer::localisation::DelayLocator", "locator", "the delays of one hit, solved for the drum",
                  receiver_names=names, element_positions=positions, roi=Raw(str(RANGING_ROI)),
                  **({} if view_z is None else dict(view_z=float(view_z)))),
            block("opendigitizer::ImPlotSink<gr::pmt::ValueMap>", "ranged", signal_name="ranging", color=0xF2F2F2),
        ]
        self.connections += ["[ window, 1, frames, 0 ]", "[ frames, 0, correlation, 0 ]", "[ correlation, 0, delays, 0 ]",
                             "[ delays, 0, arrivals, 0 ]", "[ arrivals, 0, locator, 0 ]", "[ arrivals, 0, ranged, 0 ]",
                             "[ locator, 0, ranged, 0 ]"]
        self.sources.append("ranged")

    def running(self, n_history, offsets):
        """The four microphones as they run, the last `n_history` samples redrawn continuously, stacked by `offsets`
        (experiment 3, author round 56: a tone has no edge to trigger on)"""
        for k in range(MICS):
            self.blocks += [
                block(f"gr::blocks::math::AddConst<{F32}, std::plus<{F32}>>", f"lifted{k}", "the trace's lift",
                      value=float(offsets[k])),
                sink(f"run{k + 1}", f"mic {k + 1}", signal_unit="FS", n_history=n_history, color=MIC_COLOURS[k]),
            ]
            self.connections += [f"[ {self.stream(k)}, lifted{k}, 0 ]", f"[ lifted{k}, 0, run{k + 1}, 0 ]"]
            self.sources.append(f"run{k + 1}")

    def ranging_continuous(self, size=None, min_confidence=1.0, band=(100.0, 10000.0), weighting="none"):
        """ranging() on untriggered frames: all four channels every `size` samples (StreamsToTensor), correlated,
        dated by PairDelayArrivals' frame_period — OpenDigitizer's continuous layer (XtraLocalisationLine). The block
        names are ranging()'s, so the `spacing` choice and the chart treat both alike."""
        names = Raw("[" + ", ".join(f'"mic {k + 1}"' for k in range(MICS)) + "]")
        size = size or S(5120 / 48000)   # 0.107 s, as OpenDigitizer's continuous layer
        self.blocks += [
            block(f"gr::basic::StreamsToTensor<{F32}>", "frames", f"all four channels, every {size} samples", n_ports=MICS, size=size),
            block(f"gr::localisation::PairCrossCorrelation<{F32}>", "correlation", max_lag=S(GEOMETRY["max_lag"]), weighting=weighting,
                  f_min=float(band[0]), f_max=float(band[1])),
            block(f"gr::localisation::PairDelay<{F32}>", "delays", max_lag=S(GEOMETRY["max_lag"])),
            block(f"opendigitizer::localisation::PairDelayArrivals<{F32}>", "arrivals", receiver_names=names,
                  min_confidence=min_confidence, frame_period=round(size / FS, 6)),
            block("opendigitizer::localisation::DelayLocator", "locator", "every frame's delays, solved",
                  receiver_names=names, element_positions=positions(GEOMETRY["spacing"]), roi=Raw(str(RANGING_ROI))),
            block("opendigitizer::ImPlotSink<gr::pmt::ValueMap>", "ranged", signal_name="ranging", color=0xF2F2F2),
        ]
        self.connections += [f"[ {self.stream(k)}, frames, [1, {k}] ]" for k in range(MICS)]
        self.connections += ["[ frames, 0, correlation, 0 ]", "[ correlation, 0, delays, 0 ]", "[ delays, 0, arrivals, 0 ]",
                             "[ arrivals, 0, locator, 0 ]", "[ arrivals, 0, ranged, 0 ]", "[ locator, 0, ranged, 0 ]"]
        self.sources.append("ranged")

    def pair_correlations_continuous(self, size=None, pairs=((0, 2), (0, 1), (0, 3)), band=(100.0, 10000.0), weighting="none"):
        """pair_correlations() on untriggered frames of two channels, every `size` samples — same sinks and colours"""
        size = size or S(5120 / 48000)
        correlators = []
        for i, j in pairs:
            tag = f"{i + 1}{j + 1}"
            self.blocks += [
                block(f"gr::basic::StreamsToTensor<{F32}>", f"frames{tag}", f"mic {i + 1} and mic {j + 1}, every {size} samples",
                      n_ports=2, size=size),
                block(f"gr::localisation::PairCrossCorrelation<{F32}>", f"correlation{tag}", max_lag=S(GEOMETRY["max_lag"]),
                      weighting=weighting, f_min=float(band[0]), f_max=float(band[1])),
                block(f"opendigitizer::ImPlotSink<gr::Tensor<{F32}>>", f"lags{tag}", signal_name=f"mic {i + 1} · mic {j + 1}"),
            ]
            self.connections += [f"[ {self.stream(i)}, frames{tag}, [1, 0] ]", f"[ {self.stream(j)}, frames{tag}, [1, 1] ]",
                                 f"[ frames{tag}, 0, correlation{tag}, 0 ]", f"[ correlation{tag}, 0, lags{tag}, 0 ]"]
            self.sources.append(f"lags{tag}")
            correlators.append(f"correlation{tag}")
        return correlators

    def pair_correlations(self, holdoff, pairs=((0, 2), (0, 1), (0, 3))):
        """The correlation of mic 1 with each other microphone, one sink per pair (author, round 56: slide 17, beneath
        the coloured traces): a two-channel window per pair, cut on the same hits as ranging()'s, correlated alike.
        One sink each, because OpenDigitizer's TensorRowsChart draws all rows of one sink in one colour; separate
        sinks take the chart's colours in turn — blue, orange, green — so the order 1-3, 1-2, 1-4 gives each curve the
        hue of its far microphone's trace (mic 3 blue, mic 2 orange, mic 4 green). Returns the correlation blocks."""
        correlators = []
        for i, j in pairs:
            tag = f"{i + 1}{j + 1}"
            self.blocks += [
                block(f"gr::blocks::trigger::MultiChannelRecorder<{F32}>", f"window{tag}", f"mic {i + 1} and mic {j + 1} around a hit",
                      n_inputs=2, n_pre=S(0.010), n_post=S(0.050), retrigger="ignore", holdoff=round(holdoff / FS, 3), emit_partial=False),
                block(f"opendigitizer::localisation::DataSetToTensor<{F32}>", f"frames{tag}"),
                block(f"gr::localisation::PairCrossCorrelation<{F32}>", f"correlation{tag}", max_lag=S(GEOMETRY["max_lag"]),
                      weighting="none", f_min=100.0, f_max=10000.0),
                block(f"opendigitizer::ImPlotSink<gr::Tensor<{F32}>>", f"lags{tag}", signal_name=f"mic {i + 1} · mic {j + 1}"),
            ]
            self.connections += [f"[ onset{k}, 0, window{tag}, 0 ]" for k in range(MICS)]
            self.connections += [f"[ {self.stream(i)}, window{tag}, [1, 0] ]", f"[ {self.stream(j)}, window{tag}, [1, 1] ]",
                                 f"[ window{tag}, 1, frames{tag}, 0 ]", f"[ frames{tag}, 0, correlation{tag}, 0 ]",
                                 f"[ correlation{tag}, 0, lags{tag}, 0 ]"]
            self.sources.append(f"lags{tag}")
            correlators.append(f"correlation{tag}")
        return correlators

    def phase_layer(self, f0):
        """OpenDigitizer's phase layer (XtraLocalisationLine): a narrow band around f0 per microphone, an envelope trigger
        on microphone 1, a frame of all four, their cross-spectra and the phase slope across the band → the delays →
        the DelayLocator → the `phase` sink, drawn beside the correlation estimate in the ranging chart"""
        names = Raw("[" + ", ".join(f'"mic {k + 1}"' for k in range(MICS)) + "]")
        for k in range(MICS):
            self.blocks.append(block(f"gr::filter::BasicFilterProto<{F32}, gr::Resampling<1, 1, false>>", f"band{k}",
                                     filter_type="IIR", filter_response="BANDPASS", iir_design_method="BUTTERWORTH",
                                     filter_order=2, f_low=f0 - 40, f_high=f0 + 40, sample_rate=FS))
            self.connections += [f"[ {self.raw(k)}, band{k}, 0 ]", f"[ band{k}, 0, phaseFrames, [1, {k}] ]"]
        self.blocks += [
            block(f"gr::blocks::type::converter::Abs<{F32}>", "rectify0"),
            block(f"gr::filter::BasicFilterProto<{F32}, gr::Resampling<1, 1, false>>", "smooth0", filter_type="IIR",
                  filter_response="LOWPASS", iir_design_method="BUTTERWORTH", filter_order=2, f_low=50.0, sample_rate=FS),
            block(f"gr::blocks::trigger::LevelTrigger<{F32}>", "envelopeTrigger0", "the strike, on microphone 1's envelope",
                  trigger_name="mic 1", threshold=0.1, hysteresis=0.05, edge="rising", dead_time=float(S(0.4)), dead_time_unit="samples"),
            block(f"gr::basic::StreamsToTensor<{F32}>", "phaseFrames", n_ports=MICS, size=S(0.05), n_pre=S(1268 / 48000),
                  holdoff_samples=S(0.4), filter=""),
            block(f"gr::blocks::fft::STFT<{F32}>", "phaseSpectra"),
            block(f"gr::localisation::PairCrossSpectra<{F32}>", "phaseCross"),
            block(f"gr::localisation::PhaseSlopeDelay<{F32}>", "phaseSlope", f_min=f0 - 5, f_max=f0 + 5, sample_rate=float(FS)),
            block(f"opendigitizer::localisation::PairDelayArrivals<{F32}>", "phaseArrivals", receiver_names=names),
            block("opendigitizer::localisation::DelayLocator", "phaseLocator", receiver_names=names,
                  element_positions=Raw("!!float64 [" + ", ".join(f"[{x}, 0.0, 0.0]" for x in MIC_X) + "]"), roi=Raw(str(RANGING_ROI))),
            block("opendigitizer::ImPlotSink<gr::pmt::ValueMap>", "phase", signal_name="phase", color=0xFFC94D),
        ]
        self.connections += ["[ band0, 0, rectify0, 0 ]", "[ rectify0, 0, smooth0, 0 ]", "[ smooth0, 0, envelopeTrigger0, 0 ]",
                             "[ envelopeTrigger0, 0, phaseFrames, 0 ]", "[ phaseFrames, 0, phaseSpectra, 0 ]",
                             "[ phaseSpectra, 0, phaseCross, 0 ]", "[ phaseCross, 0, phaseSlope, 0 ]", "[ phaseSlope, 0, phaseArrivals, 0 ]",
                             "[ phaseArrivals, 0, phaseLocator, 0 ]", "[ phaseArrivals, 0, phase, 0 ]", "[ phaseLocator, 0, phase, 0 ]"]
        self.sources.append("phase")

    def spectrum(self, stream, label="mic 1 spectrum"):
        self.blocks += [
            block(f"gr::blocks::fft::FFT<{F32}, gr::DataSet<{F32}>>", "FFT", fft_size=4096 * FS // 48000, sample_rate=FS,
                  output_in_db=True, signal_name=label),
            sink("spectrum", label, dataset=True, dataset_index=0, abscissa_quantity="frequency", abscissa_unit="Hz",
                 signal_quantity="magnitude", signal_unit="dB"),
        ]
        self.connections += [f"[ {stream}, FFT, 0 ]", "[ FFT, 0, spectrum, 0 ]"]
        self.sources.append("spectrum")

    def write(self, name, header, layout, plots):
        text = "".join(f"# {line}\n" for line in header.strip().splitlines())
        text += "blocks:\n" + "\n".join(self.blocks) + "\nconnections:\n"
        text += "".join(f"  - {c}\n" for c in self.connections)
        text += "dashboard:\n  layout: Free\n  windowLayout:\n    floatingWindows: { }\n"
        text += f"    dockSpace: {plots.split(chr(10))[0].split('name: ')[1]}\n" if layout is None else "    dockSpace:\n" + layout
        text += "  sources:\n" + "".join(f"    - name: {s}\n      block: {s}\n" for s in self.sources)
        text += "  plots:\n" + plots
        (OUT / name).write_text(text)
        print(f"{name}: {len(self.blocks)} blocks, {len(self.connections)} connections")


def triggered_plot(title, sources, n_history, y, legend=True, tags=False, name=None, every_tag=False):
    """`tags`: draw the trigger tag as a marker (experiments 1 and 2: where the trigger fired, in both views); `name`:
    the chart's block name, so a choice can address its settings (e.g. "running:n_history")"""
    lo, hi = (-y, y) if not isinstance(y, tuple) else y
    return (f"    - name: {title}\n      type: XYChart\n      parameters:\n" + (f"        name: {name}\n" if name else "")
            + f"        show_legend: {'true' if legend else 'false'}\n"
            f"        show_tags: {'true' if tags else 'false'}\n"
            + ("        tags_of_every_signal: true # each signal's tags in its colour: where each microphone triggered\n" if every_tag else "")
            + f"        n_history: {n_history}\n        max_history_count: 1\n"
            f"      axes:\n        - axis: X\n          min: NaN\n          max: NaN\n"
            f"        - axis: Y\n          min: {lo}\n          max: {hi}\n      sources:\n"
            + "".join(f"        - {s}\n" for s in sources))


def spectrum_plot(title, f_max, band=None, targets=None):
    """the magnitude over its waterfall; `band` = (f_low, f_high) adds the shaded range whose handles, dragged, send
    their edges to `targets` (as waterfall_plot)"""
    extra = ""
    if band:
        extra = (f"        range_style: both\n        range_min: {band[0]}\n        range_max: {band[1]}\n        range_min_width: 20\n"
                 "        show_range_labels: false # its f₋/f₊ glyphs are missing from the chart font: 'f?'\n"
                 f"        range_color: {0xFF8A8A} # 0xFF8A8A, as on experiment 2's waterfall\n"
                 f"        range_min_targets: \"{targets[0]}\"\n        range_max_targets: \"{targets[1]}\"\n")
    return (f"    - name: {title}\n      type: opendigitizer::charts::SpectrumView\n      parameters:\n" + extra +
            "        show_max_hold: true\n        show_average: true\n        decay_tau_frames: 60\n"
            "        n_history: 59 # spectra in the waterfall: 5 s at 11.7 a second\n"
            "        colormap: ImPlotColormap_Viridis\n        top_pane_ratio: 0.5\n      axes:\n"
            f"        - axis: X\n          min: 0\n          max: {f_max}\n          scale: Linear\n          format: MetricInline\n"
            "        - axis: Y\n          min: -120\n          max: -20\n        - axis: Z\n          min: -110\n          max: -30\n"
            "      sources:\n        - spectrum\n")


def waterfall_plot(title, f_max, band=None, targets=None, name=None):
    """The heatmap alone (no magnitude pane); `band` = (f_low, f_high) draws the shaded range whose handles, dragged,
    send their edges to `targets` = (low targets, high targets), 'BlockA,BlockB:setting' each."""
    text = (f"    - name: {title}\n      type: opendigitizer::charts::WaterfallPlot\n      parameters:\n"
            + (f"        name: {name}\n" if name else "") + "        show_legend: false\n        n_history: 59 # spectra: 5 s at 11.7 a second\n        colormap: ImPlotColormap_Viridis\n")
    if band:
        text += (f"        range_style: both\n        range_min: {band[0]}\n        range_max: {band[1]}\n        range_min_width: 50\n"
                 "        show_range_labels: false # its f₋/f₊ glyphs are missing from the chart font: 'f?'\n"
                 f"        range_color: {0xFF8A8A} # 0xFF8A8A, the drum's red on the map\n"
                 f"        range_min_targets: \"{targets[0]}\"\n        range_max_targets: \"{targets[1]}\"\n")
    return (text + "      axes:\n"
            f"        - axis: X\n          min: 0\n          max: {f_max}\n          scale: Linear\n          format: MetricInline\n"
            "        - axis: Z\n          min: -110\n          max: -30\n      sources:\n        - spectrum\n")


def ranging_plot(title, sources=("ranged",), view_z=None):
    """OpenDigitizer's LocalisationChart for the four microphones on a line: the hyperbolae of neighbouring pairs,
    their crossing and the DelayLocator's position, the delay written on each curve; no legend, no grid."""
    names = "[" + ", ".join(f'"mic {k + 1}"' for k in range(MICS)) + "]"
    positions = "!!float64 [" + ", ".join(f"[{x}, 0.0, 0.0]" for x in MIC_X) + "]"
    return (f"    - name: {title}\n      type: opendigitizer::charts::LocalisationChart\n      parameters:\n"
            "        name: ranging # the `spacing` choice's target\n"
            f"        receiver_names: {names}\n        element_positions: {positions}\n        roi: {RANGING_ROI}\n"
            "        show_legend: false\n        show_grid: false\n        show_curve_labels: false # the drawn map beside it writes the delays\n        show_status: true\n"
            + ("" if view_z is None else f"        view_z: {float(view_z)}\n")
            + "      sources:\n" + "".join(f"        - {src}\n" for src in sources))


def dock(tree, indent=6):
    """a dockSpace from ("h"|"v", first, second, ratio) tuples and pane names; in an hsplit the ratio is the first
    (left) pane's share, in a vsplit the second (bottom) pane's; a name no plot carries leaves its pane empty"""
    pad = " " * indent
    if isinstance(tree, str):
        return f'"{tree}"'
    kind, first, second, ratio = tree
    def child(sub):
        return ("\n" + dock(sub, indent + 4)) if not isinstance(sub, str) else " " + dock(sub)
    return (f"{pad}{kind}split:\n{pad}  first:{child(first)}\n{pad}  second:{child(second)}\n"
            f"{pad}  ratio: !!float32 {ratio}")


# The region spans the slide (author, 2026-11-13: the ranging where the drawn map was, the traces at their full width
# on the right): a region draws its whole dashboard in one rectangle, so the pane under the left column's picture holds
# a placeholder chart that the picture covers — its box says `{frame layer=above}` (gr4-present 28c5abe: a box drawn
# over the live charts). ImGui drops an empty dock pane, hence a chart there, never a missing name.
LEFT = 0.3385          # the left column's share of the region: 0.3143 of the slide, the traces keep 0.6143
RANGING_BOTTOM = 0.44  # the picture's share of the left column, under the ranging chart


def placeholder_plot(title):
    """a chart without sources for the pane under a picture (`layer=above` covers it)"""
    return (f"    - name: {title}\n      type: XYChart\n      parameters:\n        show_legend: false\n"
            "      axes:\n        - axis: X\n          min: 0\n          max: 1\n        - axis: Y\n          min: 0\n          max: 1\n"
            "      sources: []\n")


def split(kind, first, second, ratio):
    return (f"      {kind}:\n        first: \"{first}\"\n        second: \"{second}\"\n"
            f"        ratio: !!float32 {ratio}\n")


MICS_PLOTTED = [f"mic{k + 1}" for k in range(MICS)]
RECORDED = "recorded take, synthetic until the set-up is recorded (devtools/make-demo-data.py), played as the "

# experiments 1 and 1b: a low drum (or a clap), the audience's shakers drowning it; 1b adds the 4th-order low-pass
OFFSETS = [0.9, 0.3, -0.3, -0.9]   # mic 1 on top: the stacked traces read like a mountain range, the arrivals step down
RUN_PLOTS = [f"run{k + 1}" for k in range(MICS)]
# the simulated source of experiments 1–3 (OpenDigitizer's PointSourceAudio): a drum-like click (a 3 ms raised cosine,
# its energy below ~300 Hz) every half second, circling in front of the line; `shakers` is its uncorrelated noise
def _circle(kind):
    """the simulated source's path: an ellipse (PointSourceAudio's `circle` takes the first extent as its radius and
    ignores the second; round 56 found the sources running on circles of 1.2 and 0.8 m)"""
    centre, extent = GEOMETRY[kind]
    return dict(source_position=Raw(f"[{centre[0]}, {centre[1]}, 0.0]"), source_motion="ellipse", motion_extent=Raw(str(extent)))


SIM_DRUM = dict(**_circle("drum"),
                motion_period=20.0, period=0.6, pulse_width=0.001, tone_frequency=0.0, amplitude=0.8)   # 0.6 s: beyond the 0.5 s dead time   # 1 ms: energy to ~1 kHz, a stick on a drum
SIM_FORK = dict(**_circle("fork"),
                motion_period=20.0, period=1.0, pulse_width=0.4, tone_frequency=160.0, amplitude=0.6)


def shakers(noise):
    return control("shakers", "sim. noise", "FS", noise, 0, 0.6, 0.01, "simulatedMicrophones:noise")   # simulated, not real shakers (author)


def spacing_choice(kind, locators=("locator",), correlators=()):
    """the toolbar's `spacing`: 1 m (the talk) or 0.2 m (a desk) — the element positions of the simulation, the
    locators and the chart, the area, the correlation's reach and the simulated source's circle (`kind`: drum, fork)"""
    lines = ["  - id: DigitizerUi::ImControlChoice", "    parameters:", "      name: spacing", "      label: spacing",
             f'      value: "{DEFAULT}"', "      choices: [" + ", ".join(f'"{k}"' for k in GEOMETRIES) + "]", "      choice_values:"]
    located = ",".join(locators)
    for key, geo in GEOMETRIES.items():
        centre, extent = geo[kind]
        lines += [f'        "{key}":',
                  f'          "simulatedMicrophones,{located},ranging:element_positions": {positions(geo["spacing"])}',
                  f'          "{located},ranging:roi": {geo["roi"]}',
                  f'          "{",".join(("correlation", "delays") + tuple(correlators))}:max_lag": !!uint32 {S(geo["max_lag"])}',
                  f'          "simulatedMicrophones:source_position": [{centre[0]}, {centre[1]}, 0.0]',
                  f'          "simulatedMicrophones:motion_extent": {extent}']
    return "\n".join(lines)


# experiments 1-3 run at 96 kHz (author, round 56: tested before; leaves room above 24 kHz)
FS = 96000
RUN_HISTORY = 2.0   # s of the running traces on slides 7 and 8 (author, round 56; it was 1 s)
TRACE_Y = (-2.0, 2.0)   # the time-domain plots of slides 7 and 8 (author, 2026-11-13; it was ±1.4)
# the triggers of slides 7 and 8 (author, round 56): on |high-pass 100 Hz| (slide 8: |band-pass|), one
# slider from 0.01 to 0.1 for all five (the display trigger and the four onsets), a small fixed hysteresis below the
# slider's lowest step, and a 0.5 s time-out after each trigger (author: a loud clap's ringing would fire it again)
TRIGGER = dict(threshold=0.5, hysteresis=0.004, holdoff=0.5)   # author, round 57: 0.5 FS
TRIGGER_HP = 100.0   # Hz: above rumble, ventilation and hum, below a drum stick's attack


def threshold_slider():
    return control("threshold", "threshold", "FS", TRIGGER["threshold"], 0.01, 1.0, 0.005,
                   "trigger:threshold;" + ",".join(f"onset{k}" for k in range(MICS)) + ":threshold")


def dead_time_slider():
    """the time-out after a trigger (author, round 56: programmable; a loud clap's ringing would fire it again):
    the display trigger, the four onsets and the four snapshots alike — in samples, since the snapshots take
    their hold-off only in samples (48000 = 0.5 s at 96 kS/s)"""
    return control("deadTime", "dead time", "samples", S(TRIGGER["holdoff"]), S(0.1), S(2.0), S(0.05),
                   "trigger:dead_time;" + ",".join(f"onset{k}" for k in range(MICS)) + ":dead_time;"
                   + ",".join(f"snapshot{k}" for k in range(MICS)) + ":holdoff_samples")


def rectified_triggers(g, highpass):
    """slides 7 and 8 (author, round 56): the triggers on the rectified streams. The snapshots are
    cut around one anchor for all four, the FIRST microphone to cross (a Schmitt trigger on the maximum of the four
    |x|), so each trace keeps its own arrival time; and each trace carries its own microphone's trigger tag (its
    onset trigger tags its pass-through output; that minus its input is a zero with the tag, added to the trace), drawn
    in its colour beside the anchor. ranging() makes the onsets `onset<k>` these marks come from."""
    rect = g.rectified(highpass)
    g.blocks.append(block(f"gr::blocks::math::Max<{F32}, gr::blocks::math::Maximum<{F32}>>", "firstHit", "the four |x|: whichever crosses first", n_inputs=MICS))
    g.connections += [f"[ {rect[k]}, firstHit, [0, {k}] ]" for k in range(MICS)]
    marks = []
    for k in range(MICS):
        g.blocks.append(block(f"opendigitizer::Arithmetic<{F32}>", f"mark{k}", f"zero, carrying mic {k + 1}'s own trigger tag",
                              operation="-"))
        g.connections += [f"[ onset{k}, out, mark{k}, 0 ]", f"[ {rect[k]}, mark{k}, 1 ]"]
        marks.append(f"mark{k}, 0")
    g.triggered(threshold=TRIGGER["threshold"], n_pre=S(0.010), n_post=S(0.050), holdoff=S(TRIGGER["holdoff"]),
                offsets=OFFSETS, continuous=S(RUN_HISTORY), trigger_on="firstHit, 0", controls=False,
                hysteresis=TRIGGER["hysteresis"], marks=marks)
    return rect

# experiment 1: the drum, its four arrivals, the ranging — and the shakers (raise them: the trigger fires on the hiss)
g = Graph(False, sim=dict(SIM_DRUM, noise=0.02))
g.blocks += [shakers(0.02), spacing_choice("drum")]
g.filters(highpass=20 if FILTERS_IN_VIEWER else None)
rect = rectified_triggers(g, TRIGGER_HP)
g.ranging(threshold=TRIGGER["threshold"], holdoff=S(TRIGGER["holdoff"]), onsets=rect, hysteresis=TRIGGER["hysteresis"])
g.blocks += [threshold_slider(), dead_time_slider()]
g.write("exp1-claps.grc",
        "experiment 1, Bragg's problem at the laptop: four microphones on a line, 96 kS/s — simulated (OpenDigitizer's\n"
        "PointSourceAudio: a drum-like click every half second, circling in front of the line) or, with the input switch,\n"
        "the microphones (devtools/four-mics-browser-pairs.sh); the shakers slider adds noise; a 20 Hz high-pass per\n"
        "channel; the triggers watch |high-pass 100 Hz| (one threshold slider, 0.01-0.1); the running traces (2 s) and\n"
        "60 ms around every hit, cut on microphone 1's trigger, stacked, the trigger tags shown; the ranging left",
        dock(("h", ("v", "Ranging", "Under the picture", RANGING_BOTTOM),
              ("v", "Four microphones, running", "Four microphones, triggered on the first", 0.5), LEFT)) + "\n",
        ranging_plot("Ranging") + placeholder_plot("Under the picture")
        + triggered_plot("Four microphones, running", RUN_PLOTS, S(RUN_HISTORY), TRACE_Y, legend=False, tags=True)
        + triggered_plot("Four microphones, triggered on the first", MICS_PLOTTED, S(0.060), TRACE_Y, legend=False, tags=True, every_tag=True))

BAND = (30, 5500)   # the band-pass at the start: wide open, the shakers pass and fire the trigger
F_VIEW = 6300       # the waterfall's span; not a round number, so the last tick label (6 kHz) is not cut at the region's edge
# experiment 2: the same, the shakers on, and a band-pass on every channel whose edges the waterfall's handles drag
# (author, round 56) the microphones first; the simulation's shakers swell and fade: band-passed 500 Hz – 8 kHz noise,
# independent per microphone, its level 0.1 · (1 + sin 2π·0.5 Hz·t) — the slider sets the 0.1
SHAKEN = dict(level=0.1, f_env=0.5, band=(500, 8000))
g = Graph(False, sim=dict(SIM_DRUM, noise=0.02), live=True, shaken=SHAKEN)
g.blocks.append(spacing_choice("drum"))
g.filters(band=BAND)
rect = rectified_triggers(g, None)   # |band-pass|: narrowing the band takes the shakers out of the triggers too
g.ranging(threshold=TRIGGER["threshold"], holdoff=S(TRIGGER["holdoff"]), onsets=rect, hysteresis=TRIGGER["hysteresis"])
g.blocks += [threshold_slider(), dead_time_slider()]
g.spectrum(g.raw(0), "mic 1, unfiltered")
bands = tuple(",".join(f"bp{k}" for k in range(MICS)) + f":{edge}" for edge in ("f_low", "f_high"))
g.write("exp1b-lowpass.grc",
        "experiment 2: the same drum, the shakers on — the microphones first (the input switch: the simulation, whose\n"
        "shakers are band-passed 500 Hz – 8 kHz noise swelling and fading every 2 s), now through a\n"
        "4th-order band-pass on every channel: drag the shaded band's upper edge down onto the drum — the hiss leaves\n"
        "the traces, the trigger fires on the drum again: Tucker's hot-wire microphone in software",
        dock(("h", ("v", "Ranging", "Under the picture", RANGING_BOTTOM),
              ("v", "Four microphones, running",
               ("v", "Four microphones, triggered on the first", "Waterfall, mic 1 unfiltered", 0.5), 0.6667), LEFT)) + "\n",
        ranging_plot("Ranging") + placeholder_plot("Under the picture")
        + triggered_plot("Four microphones, running", RUN_PLOTS, S(RUN_HISTORY), TRACE_Y, legend=False, tags=True)
        + triggered_plot("Four microphones, triggered on the first", MICS_PLOTTED, S(0.060), TRACE_Y, legend=False, tags=True, every_tag=True)
        + waterfall_plot("Waterfall, mic 1 unfiltered", F_VIEW, BAND, bands))

# experiment 3: the tuning fork — a 440 Hz tone, struck once a second; two estimates in one chart: the correlation of
# a window cut on each strike (the claps' method: its peaks repeat every period, a ghost) and OpenDigitizer's phase
# layer (a narrow band, the cross-spectra's phase slope: the delay from the phase). Right (author, 2026-11-13): the
# waterfall alone and the pair correlation itself — for a tone a cosine, its peaks one period apart: the phase says
# where within a period, not which period (the window must hold pair 1-4's ±8.75 ms, several periods)
TONE_BAND = (30, 2400)
# the tone (the phase layer's band follows; one 20 Hz STFT bin, so a multiple of 20 Hz): the phase of pair 1-j holds
# its delay while |r1 - rj| < λ/2 — for the outer pair (3 m) within ~±21° of straight ahead at 160 Hz (λ/2 = 1.07 m:
# the circling source stays inside), within ~±7° at 440 Hz, the fork (λ/2 = 0.39 m: it leaves the cone, the gold
# estimate jumps to ghosts and comes back); unambiguous from every direction only below c/2L = 343/(2 · 3 m) ≈ 57 Hz
# The third choice, "24 kHz" (author, round 56): a free-running ultrasonic emitter, unmodulated, its frequency wandering —
# the microphones hear the same wandering tone, delayed, so their correlation hardly feels the wander. λ = 14.3 mm: the
# correlation becomes fringes 41.7 µs apart that slide as the emitter moves (an acoustic interferometer, Decca's lanes on
# a desk); the ranging has ~70 cycles across 1 m to choose from — ghosts. The choice also re-aims what the eye needs: the
# band-pass and the waterfall to 22.5–25.5 / 22–26 kHz, the running traces to 0.5 ms (12 cycles), the plotted
# correlations to ±0.5 ms (12 fringes), the correlation unweighted (PHAT would whiten one narrow line among ~400 noise
# bins); the phase layer and the ranging stay on, and show why one wavelength is not enough.
CORRELATORS = "correlation,correlation13,correlation12,correlation14"
PLOTTED_CORRELATORS = "correlation13,correlation12,correlation14"
BAND_PASS = ",".join(f"bp{k}" for k in range(MICS))
PHASE_BANDS = ",".join(f"band{k}" for k in range(MICS))


def _choice(f, phase_band, slope_band, correlation_band, weighting, band_pass, view, running, plotted_lag):
    values = {
        "simulatedMicrophones:tone_frequency": f"{f:.1f}",
        f"{PHASE_BANDS}:f_low": f"!!float32 {phase_band[0]:.1f}", f"{PHASE_BANDS}:f_high": f"!!float32 {phase_band[1]:.1f}",
        "phaseSlope:f_min": f"!!float32 {slope_band[0]:.1f}", "phaseSlope:f_max": f"!!float32 {slope_band[1]:.1f}",
        f"{CORRELATORS}:f_min": f"!!float32 {correlation_band[0]:.1f}", f"{CORRELATORS}:f_max": f"!!float32 {correlation_band[1]:.1f}",
        f"{CORRELATORS}:weighting": weighting,
        f"{BAND_PASS}:f_low": f"!!float32 {band_pass[0]:.1f}", f"{BAND_PASS}:f_high": f"!!float32 {band_pass[1]:.1f}",
        "waterfall:x_auto_scale": "false",   # else the dashboard's axis wins over x_min/x_max (WaterfallPlot)
        "waterfall:x_min": f"{view[0]:.1f}", "waterfall:x_max": f"{view[1]:.1f}",
        "waterfall:range_min": f"{band_pass[0]:.1f}", "waterfall:range_max": f"{band_pass[1]:.1f}",
        "running:n_history": f"!!uint32 {running}", f"{PLOTTED_CORRELATORS}:max_lag": f"!!uint32 {plotted_lag}",
    }
    return "".join(f'          "{key}": {value}\n' for key, value in values.items())


def _tone(f):   # a tone the phase can follow: PHAT over f ± 40 Hz, the band-pass and the view of experiment 3
    return _choice(f, (f - 40, f + 40), (f - 5, f + 5), (f - 40, f + 40), "phat", TONE_BAND, (0, 2450), S(0.030),
                   S(GEOMETRY["max_lag"]))


EMITTER = _choice(24000.0, (23000, 25000), (23500, 24500), (22000, 26000), "none", (22500, 25500), (22000, 25900),
                  S(0.0005), S(0.00055))   # 25.9 kHz and ±0.55 ms: the last tick labels stay inside the charts
TONE_CHOICE = ("  - id: DigitizerUi::ImControlChoice\n    parameters:\n      name: tone\n      label: tone\n      value: \"160 Hz\"\n"
               "      choices: [\"160 Hz\", \"440 Hz\", \"24 kHz\"]\n      choice_values:\n"
               "        \"160 Hz\":\n" + _tone(160.0) + "        \"440 Hz\":\n" + _tone(440.0)
               + "        \"24 kHz\":\n" + EMITTER.rstrip("\n"))
def correlation_plot(title, sources=("lags",)):
    """OpenDigitizer's TensorRowsChart: one trace per row of each source (here one pair per source, see
    pair_correlations) over the lag, ±max_lag, lag 0 in the middle (as the XtraLocalisationLine sample); no legend"""
    return (f"    - name: {title}\n      type: opendigitizer::charts::TensorRowsChart\n      parameters:\n"
            "        lag_columns: true\n        show_legend: false\n        show_grid: false\n"
            "      sources:\n" + "".join(f"        - {src}\n" for src in sources))


# (author, round 56) continuous: the traces run (the last 30 ms), the correlation and the white estimate every 5120
# samples (0.107 s) without a trigger; the gold phase estimate stays on the strike, its trigger level a slider; the
# simulated fork rings almost without a break (pulse_width = period: a raised-cosine swell every second)
g = Graph(False, sim=dict(SIM_FORK, noise=0.02, pulse_width=1.0))
g.blocks.append(TONE_CHOICE)
g.filters(band=TONE_BAND)
g.running(S(0.030), OFFSETS)
# PHAT over f0 ± 40 Hz (the tone choice moves it): the correlation a cosine of constant height whatever the swell —
# OpenDigitizer's "fork 440 Hz" preset — and robust in a room
FORK_BAND = (120.0, 200.0)
g.ranging_continuous(band=FORK_BAND, weighting="phat")
PAIRS = g.pair_correlations_continuous(band=FORK_BAND, weighting="phat")
g.phase_layer(f0=160.0)
# averaging (author, round 56): PairCrossCorrelation's `averages` (GR4 02d6a41) sums the cross- and auto-spectra of A
# consecutive frames before the weighting — frame-to-frame averaging before the peak is picked, √A less noise, one result
# per A frames (0.107 s · A); PairDelayArrivals dates untagged results by frame_period, so it follows. Not for the gold
# phase estimate (one frame per strike; PairCrossSpectra does not average).
FRAME = S(5120 / 48000)
AVERAGING = ("  - id: DigitizerUi::ImControlChoice\n    parameters:\n      name: averaging\n      label: averaging\n"
             "      value: \"off\"\n      choices: [\"off\", \"×4\", \"×10\"]\n      choice_values:\n"
             + "".join(f'        "{label}":\n          "{CORRELATORS}:averages": !!uint32 {frames}\n'
                       f'          "arrivals:frame_period": {frames * FRAME / FS:.6f}\n'
                       for label, frames in (("off", 1), ("×4", 4), ("×10", 10))).rstrip("\n"))
g.blocks += [spacing_choice("fork", ("locator", "phaseLocator")),   # the plotted correlations' reach is the tone choice's
             control("threshold", "threshold", "FS", 0.1, 0, 1, 0.01, "envelopeTrigger0:threshold"), AVERAGING]
g.spectrum(g.raw(0), "mic 1, unfiltered")
tone_targets = tuple(",".join(f"bp{k}" for k in range(MICS)) + f":{edge}" for edge in ("f_low", "f_high"))
g.write("exp2-noise-tone.grc",
        "experiment 3 (slide `exp2`): the tuning fork — simulated (a struck 160 Hz tone, circling; 440 Hz or a 24 kHz\n"
        "emitter with the tone choice) or the microphones;\n"
        "the ranging chart shows both estimates: the continuous correlation (white, every 0.107 s) and the phase layer\n"
        "(gold, on each strike, its level the threshold slider); right the four microphones as they run (the last 30 ms,\n"
        "coloured, stacked), beneath them each one's correlation with mic 1, continuously (in the same hue: a cosine, its\n"
        "peaks one period apart), and microphone 1's waterfall with the band-pass handles",
        dock(("h", ("v", "Ranging", "Under the picture", RANGING_BOTTOM),
              ("v", "Four microphones, running",
               ("v", "Correlation with mic 1", "Waterfall, mic 1 unfiltered", 0.5), 0.6667), LEFT)) + "\n",
        ranging_plot("Ranging", ("ranged", "phase")) + placeholder_plot("Under the picture")
        + triggered_plot("Four microphones, running", RUN_PLOTS, S(0.030), (-1.4, 1.4), legend=False, tags=False, name="running")
        + correlation_plot("Correlation with mic 1", ("lags13", "lags12", "lags14"))
        + waterfall_plot("Waterfall, mic 1 unfiltered", 2450, TONE_BAND, tone_targets, name="waterfall"))

# experiment 4 (slide `exp6`): the chirp and the receiver that knows it — the matched filter, live (GR4's
# gr::filter::Correlator against the emitted chirp), the trigger on its output (radar detects after the matched filter)
def chirp_reference():
    """the emitted chirp (media/chirp-1-8khz.wav, its first 20 ms), scaled by 1/its energy: the filter's peak then reads
    the received chirp's amplitude relative to the emitted one, and white noise comes out ~10x (20 dB) smaller"""
    import wave
    import numpy as np
    with wave.open(str(OUT.parent / "media" / "chirp-1-8khz.wav")) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(float) / 32767
    c = x[:int(0.02 * FS)]
    return c / np.dot(c, c)


FS = 48000   # experiment 4 replays 48 kHz files (the chirp, the take)
REFERENCE = Raw("!!float32 [" + ", ".join(f"{v:.6g}" for v in chirp_reference()) + "]")
# one graph (author, 2026-11-14): the rehearsal take by default; on the microphones the speaker pings the chirp into the
# room, and the matched filter's trace, triggered on the direct path, shows every echo after it — a radar's A-scope,
# ~5.8 ms per metre to a reflector and back, whatever the browser's output-to-input latency
if True:
    g = Graph(True, "media/exp6-chirps-recorded.wav", ping=True)
    g.blocks += [
        block(f"gr::blocks::fileio::WavSource<{F32}>", "chirp", "the known waveform, 1-8 kHz in 20 ms, once a second",
              uri="media/chirp-1-8khz.wav", repeat=True, trigger_name=""),
        block(f"gr::basic::SignalGenerator<{F32}>", "noise", "broadband, from the speaker: bury the chirp", signal_type="GaussianNoise",
              amplitude=0, sample_rate=FS, chunk_size=480),
        block(f"gr::blocks::math::Add<{F32}, std::plus<{F32}>>", "mix", n_inputs=2),
        control("noiseLevel", "noise", "FS", 0, 0, 0.5, 0.01, "noise:amplitude"),
    ]
    g.connections += ["[ chirp, 0, mix, [0, 0] ]", "[ noise, 0, mix, [0, 1] ]", "[ mix, 0, speakerSource, [0, 1] ]"]
    g.blocks += [
        block(f"gr::filter::Correlator<{F32}>", "matched", "microphone 1 against the emitted chirp: the matched filter",
              reference=REFERENCE, lags=480),
        block(f"gr::basic::StreamToDataSet<{F32}>", "mfSnapshot", filter="RISING", n_pre=480, n_post=1440, holdoff_samples=24000),
        sink("mf", "matched filter, mic 1", dataset=True, dataset_index=0, signal_unit="a.u.", n_history=1, color=MIC_COLOURS[0]),
    ]
    g.connections += [f"[ {g.raw(0)}, matched, in ]", "[ trigger, out, mfSnapshot, in ]", "[ mfSnapshot, out, mf, in ]"]
    g.sources.append("mf")
    tagged = g.triggered(threshold=0.2, n_pre=480, n_post=1440, holdoff=24000, offsets=OFFSETS, trigger_on="matched, out")
    g.ranging(threshold=0.15, holdoff=24000)
    g.spectrum(g.raw(0))
    g.write("exp6-chirps.grc",
            "experiment 4 (slide `exp6`), by default the " + RECORDED + "\n"
            "chirp once a second, the room noise rising until the chirp is gone from the traces; on the microphones (the input\n"
            "switch) the speaker pings the same chirp, a noise slider buries it, and the matched filter's trace shows the direct\n"
            "path, then each echo (~5.8 ms per metre)\n"
            + "the matched filter (gr::filter::Correlator against the emitted chirp) compresses microphone 1's chirp to one\n"
              "0.15 ms peak; the trigger watches that peak, so the snapshots keep coming when the chirp has vanished\n"
              "in the noise; the ranging left, the four snapshots, the matched filter's output and the waterfall right",
            dock(("h", ("v", "Ranging", "Under the picture", RANGING_BOTTOM),
                  ("v", "Four microphones, triggered on the matched filter",
                   ("v", "Matched filter, mic 1", "Waterfall, mic 1", 0.5), 0.6667), LEFT)) + "\n",
            ranging_plot("Ranging") + placeholder_plot("Under the picture")
            + triggered_plot("Four microphones, triggered on the matched filter", MICS_PLOTTED, 1920, (-1.4, 1.4), legend=False)
            + triggered_plot("Matched filter, mic 1", ["mf"], 1920, (-0.4, 1.4), legend=False)
            + waterfall_plot("Waterfall, mic 1", 9700))   # not a round number: the last tick label (9 kHz) is not cut
