from __future__ import annotations
import numpy as np

# Small, in-memory datasets for missions
CITY_TEMPS = np.array([
    ["Warsaw",  3.0,  5.0,  9.0, 15.0, 18.0, 20.0],
    ["Krakow",  2.0,  6.0, 10.0, 16.0, 19.0, 21.0],
    ["Gdansk",  1.0,  4.0,  8.0, 14.0, 17.0, 19.0],
], dtype=object)

STUDENT_SCORES = np.array([
    ["Alice", 78, 82, 91],
    ["Bob",   65, 70, 68],
    ["Cara",  90, 88, 95],
    ["Dan",   55, 60, 58],
])

SIGNALS = {
    "sine_short": np.sin(np.linspace(0, 6.283, 100)),
    "noisy": np.sin(np.linspace(0, 6.283, 100)) + 0.25*np.random.RandomState(42).normal(size=100),
}