"""Render one piece as the device's ring tone file: mono 24 kHz 16-bit (a small speaker plays nothing above 12 kHz).
  SCORES=scores2 uv run --no-project --with numpy --with scipy --with soxr python export.py <sfz> <piece prefix> <out.wav>"""
import sys
import wave

import numpy as np
import soxr

import render

piano = render.Piano(sys.argv[1])
name, fn = next(p for p in render.scores.PIECES + getattr(render.scores, 'CHIMES', []) if p[0].startswith(sys.argv[2]))
x = render.render(piano, fn).mean(axis=1)
x = soxr.resample(x, render.SR, 24000)
pcm = (np.clip(x, -1, 1) * 32767).astype(np.int16)
with wave.open(sys.argv[3], 'wb') as w:
    w.setnchannels(1), w.setsampwidth(2), w.setframerate(24000), w.writeframes(pcm.tobytes())
print(name, f'{len(x) / 24000:.1f} s')
