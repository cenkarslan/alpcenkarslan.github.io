"""Videoya eşlik eden sentezlenmiş ses zemini (telifsiz, 60 sn, 48 kHz stereo).
Video sessiz izlendiğinde de anlaşılır; bu yalnızca atmosfer katmanıdır."""
import wave
from pathlib import Path
import numpy as np

SR, DUR = 48000, 60.0
t = np.arange(int(SR * DUR)) / SR
rng = np.random.default_rng(3)
out = np.zeros((2, t.size))

def env(a, b, fi=0.5, fo=0.5):
    e = np.clip((t - a) / max(fi, 1e-3), 0, 1) * np.clip((b - t) / max(fo, 1e-3), 0, 1)
    return e * ((t >= a) & (t <= b))

def lowpass(x, k):
    y = np.empty_like(x); acc = 0.0
    for i in range(0, x.size, 4096):  # blok halinde tek kutuplu filtre
        seg = x[i:i + 4096]
        z = np.empty_like(seg)
        for j, v in enumerate(seg):
            acc += k * (v - acc); z[j] = acc
        y[i:i + 4096] = z
    return y

# 1) zemin drone: 0–55 sn, bölüme göre tonalite kayar
lfo = 0.6 + 0.4 * np.sin(2 * np.pi * 0.07 * t)
for f, g, pan in [(55, .16, 0), (82.4, .09, .3), (110.6, .05, -.3), (164.8, .025, .5)]:
    s = np.sin(2 * np.pi * f * t + 0.3 * np.sin(2 * np.pi * 0.11 * t)) * g * lfo * env(0, 55.4, 1.5, 1.2)
    out[0] += s * (1 - pan) / 1.2; out[1] += s * (1 + pan) / 1.2

# 2) hava/hışırtı
air = lowpass(rng.standard_normal(t.size), 0.02) * 0.05
out += air * env(0, 59.5, 2, 1.5)

# 3) bölüm geçiş vuruşları
for hit in [0.15, 6.0, 15.0, 25.0, 35.0, 46.0, 55.1]:
    m = t >= hit; d = t[m] - hit
    boom = np.sin(2 * np.pi * (48 + 30 * np.exp(-d * 12)) * d) * np.exp(-d * 2.8) * .45
    out[:, m] += boom

# 4) hook kesmeleri: kısa tıklar
for c in [0.95, 1.38, 2.05, 2.48, 3.0, 3.7, 4.4, 5.1]:
    m = (t >= c) & (t < c + .08); d = t[m] - c
    out[:, m] += rng.standard_normal(d.size) * np.exp(-d * 80) * .12

# 5) Petrov: radar ping'leri + alarm
for p in np.arange(15.2, 21.8, 2 * np.pi / 2.2):
    m = (t >= p) & (t < p + 1.2); d = t[m] - p
    out[:, m] += np.sin(2 * np.pi * 1180 * d) * np.exp(-d * 6) * .05
for b in np.arange(16.85, 20.3, .5):
    m = (t >= b) & (t < b + .22); d = t[m] - b
    tone = np.sin(2 * np.pi * (740 if int((b - 16.85) / .5) % 2 else 880) * d) * np.minimum(1, d * 60) * np.minimum(1, (.22 - d) * 60)
    out[:, m] += tone * .045

# 6) veri merkezi uğultusu (25–35)
hum = sum(np.sin(2 * np.pi * 50 * k * t) / k for k in (1, 2, 3, 5)) * .05 * env(25.3, 35.2, 1.5, .6)
out += hum

# 7) savaş: hızlanan tıklar (döngü hızı)
pos, period = 38.6, 2.2 / 4
while pos < 45.9:
    m = (t >= pos) & (t < pos + .03); d = t[m] - pos
    out[:, m] += np.sin(2 * np.pi * 2400 * d) * np.exp(-d * 200) * .10
    k = np.clip((pos - 38.6) / 7.0, 0, 1) ** 3
    period = (2.2 + (0.18 - 2.2) * k) / 4
    pos += period
riser = np.sin(2 * np.pi * (60 + 80 * np.clip((t - 39) / 7, 0, 1) ** 2) * t) * .06 * env(39, 46.0, 3, .2)
out += riser

# 8) kapanış akoru (55–60)
for f, g in [(110, .08), (164.8, .06), (220, .05), (329.6, .03)]:
    out += np.sin(2 * np.pi * f * t) * g * env(56.6, 59.95, .4, 2.0)

out /= np.max(np.abs(out)) / 0.55
pcm = (out.T * 32767).astype("<i2")
p = Path(__file__).with_name("soundtrack.wav")
with wave.open(str(p), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("ses →", p)
