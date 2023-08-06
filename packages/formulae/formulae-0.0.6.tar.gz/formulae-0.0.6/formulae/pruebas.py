# import numpy as np
import pandas as pd

# from numpy.linalg import matrix_rank

data = pd.DataFrame(
    {
        "y": np.random.normal(size=50),
        "x": np.random.normal(size=50),
        "s": ["s1"] * 25 + ["s2"] * 25,
        "g": np.random.choice(["a", "b", "c"], size=50),
    }
)

# dm = fm.design_matrices("y ~ x * g", data)
