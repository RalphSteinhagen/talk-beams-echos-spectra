#!/usr/bin/env python3
"""The audio of experiment 4: the chirp the live graph plays (media/chirp-1-8khz.wav) and its recorded take
(media/exp6-chirps-recorded.wav, 4 channels, 48 kS/s, 16 bit). Re-run after changing a parameter:
python3 devtools/make-demo-data.py
Geometry as the design document's Experiment 1-6 (§20)."""
import numpy as np
import wave
from pathlib import Path

MEDIA = Path(__file__).resolve().parent.parent / "media"
FS = 48000.0
C = 343.0

# four microphones on a line, 1 m apart (a 3 m base along x, like a sound-ranging base), the source in front of
# it (y > 0), 2.5 m from the centre at 60 degrees; a line fixes the source up to its mirror image behind the base
mics = np.array([[-1.5, 0.0], [-0.5, 0.0], [0.5, 0.0], [1.5, 0.0]])   # 1 m apart, a 3 m base (author, 2026-11-13; was 0.2 m)
src = 2.5 * np.array([np.cos(np.radians(60)), np.sin(np.radians(60))])
dist = np.linalg.norm(mics - src, axis=1)
tau = dist / C


# the chirp: 1-8 kHz in 20 ms
tc = np.arange(0, 0.02, 1 / FS)
chirp = np.sin(2 * np.pi * (1000 * tc + (7000 / (2 * 0.02)) * tc**2))


def write_wav(name, frames):
    pcm = np.clip(np.round(np.atleast_2d(frames.T).T * 32767), -32768, 32767).astype("<i2")
    with wave.open(str(MEDIA / name), "wb") as w:
        w.setnchannels(pcm.shape[1])
        w.setsampwidth(2)
        w.setframerate(int(FS))
        w.writeframes(pcm.tobytes())
    print(f"{name}: {pcm.shape[1]} channels, {pcm.shape[0] / FS:.1f} s, peak {np.abs(frames).max():.2f} FS")


def geometry(position):
    r = np.linalg.norm(mics - position, axis=1)
    return r / C - (r / C).min() + 0.002, r.min() / r   # delays (the nearest microphone 2 ms in), gains


# experiments 5/6: the chirp of the matched-filter slide, 1-8 kHz in 20 ms, once a second, buried in room noise
period = int(FS)
emitted = np.zeros(period)
emitted[:chirp.size] = chirp * np.hanning(chirp.size) ** 0.25   # tapered ends, no click
write_wav("chirp-1-8khz.wav", 0.5 * emitted)
# the take of experiment 4 (round 52): 8 s, the chirp once a second, each microphone's copy circularly delayed by its
# fractional time of flight (the loop repeats without a seam) and scaled by 1/r; the room noise (uncorrelated per
# microphone, its own generator) rises from 2 s to 7 s until the chirp is gone from the traces — the matched filter
# still finds it (its output noise is ~20 dB lower)
spec8, f8 = np.fft.rfft(0.3 * np.tile(emitted, 8)), np.fft.rfftfreq(8 * period, 1 / FS)
d8, g8 = geometry(src)
loop8 = np.column_stack([np.fft.irfft(spec8 * np.exp(-2j * np.pi * f8 * d), 8 * period) * gk for d, gk in zip(d8, g8)])
t8 = np.arange(loop8.shape[0]) / FS
noise_level = 0.02 + 0.16 * np.clip((t8 - 2) / 5, 0, 1)
write_wav("exp6-chirps-recorded.wav", loop8 + noise_level[:, None] * np.random.default_rng(6).standard_normal(loop8.shape))

print("source at", src.round(3), "m; delays [ms]", (tau * 1e3).round(3), "; TDOA vs mic1 [ms]", ((tau - tau[0]) * 1e3).round(3))
