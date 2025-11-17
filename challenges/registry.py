from __future__ import annotations
import numpy as np
from types import SimpleNamespace
from datasets import CITY_TEMPS, STUDENT_SCORES, SIGNALS

# Each challenge: id, title, prompt, starter, solution_hint, tests(g,l)

CHALLENGES = []

def register(ch):
    CHALLENGES.append(SimpleNamespace(**ch))

def get_challenges():
    return CHALLENGES

def get_challenge(cid: str):
    return next((c for c in CHALLENGES if c.id == cid), None)

# ---- Level 1: Column mean (NumPy basics) ----

def tests_level1(g, l):
    fn = l.get("mean_last_column")
    assert callable(fn), "Define function mean_last_column(arr)"
    arr = np.array([[1,2,3],[4,5,6],[7,8,9]], dtype=float)
    res = fn(arr)
    assert isinstance(res, (int, float, np.floating)), "Return a scalar"
    assert abs(res - 6.0) < 1e-6, "Expected mean 6.0 for last column"
    return True, "All tests passed!"

register({
    "id": "level1",
    "title": "Compute Mean of Last Column",
    "prompt": "Implement mean_last_column(arr) that returns the mean of the last column of a 2D numpy array.",
    "starter": (
        "import numpy as np\n\n"
        "def mean_last_column(arr: np.ndarray):\n"
        "    # TODO: return the mean of arr[:, -1]\n"
        "    pass\n"
    ),
    "solution_hint": "Use arr[:, -1].mean().",
    "tests": tests_level1,
})

# ---- Level 2: Z-score outlier detection ----

def tests_level2(g, l):
    fn = l.get("zscore_outliers")
    assert callable(fn), "Define function zscore_outliers(x, thr=3.0)"
    x = np.array([10, 10, 11, 10, 9, 12, 200])
    idx = fn(x, 2.5)
    assert isinstance(idx, np.ndarray) and idx.dtype == bool, "Return a boolean mask"
    outliers = x[idx]
    assert outliers.shape[0] == 1 and outliers[0] == 200, "200 must be flagged as outlier"
    return True, "All tests passed!"

register({
    "id": "level2",
    "title": "Z-score Outliers",
    "prompt": "Implement zscore_outliers(x, thr=3.0) returning a boolean mask of values considered outliers by |z| > thr.",
    "starter": (
        "import numpy as np\n\n"
        "def zscore_outliers(x: np.ndarray, thr: float = 3.0) -> np.ndarray:\n"
        "    x = np.asarray(x, dtype=float)\n"
        "    # TODO: compute z = (x - mean)/std and return |z| > thr\n"
        "    pass\n"
    ),
    "solution_hint": "Use (x - x.mean())/x.std(ddof=0) and np.abs(z) > thr.",
    "tests": tests_level2,
})

# ---- Level 3: Normalize signal (min-max) ----

def tests_level3(g, l):
    fn = l.get("minmax_normalize")
    assert callable(fn), "Define function minmax_normalize(x)"
    x = np.array([5, 10, 15], dtype=float)
    y = fn(x)
    assert isinstance(y, np.ndarray) and y.shape == x.shape, "Return ndarray of same shape"
    assert np.allclose(y, np.array([0.0, 0.5, 1.0])), "Expected [0, 0.5, 1] after min-max"
    return True, "All tests passed!"

register({
    "id": "level3",
    "title": "Min-Max Normalize",
    "prompt": "Implement minmax_normalize(x) that scales values to [0,1] using (x - min)/(max - min).",
    "starter": (
        "import numpy as np\n\n"
        "def minmax_normalize(x):\n"
        "    x = np.asarray(x, dtype=float)\n"
        "    # TODO: implement min-max normalization\n"
        "    pass\n"
    ),
    "solution_hint": "Compute mn=x.min(); mx=x.max(); return (x-mn)/(mx-mn).",
    "tests": tests_level3,
})