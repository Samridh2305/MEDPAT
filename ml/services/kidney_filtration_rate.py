import numpy as np
import pandas as pd


def calculate_egfr(
    creatinine: pd.Series,
    age: pd.Series,
    gender: pd.Series,
) -> pd.Series:
    """
    CKD-EPI 2021 equation.
    gender:
        1 = Male
        2 = Female
    """

    kappa = np.where(gender == 2, 0.7, 0.9)
    alpha = np.where(gender == 2, -0.241, -0.302)
    female_factor = np.where(gender == 2, 1.012, 1.0)

    egfr = (
        142
        * np.minimum(creatinine / kappa, 1) ** alpha
        * np.maximum(creatinine / kappa, 1) ** (-1.200)
        * (0.9938 ** age)
        * female_factor
    )

    return egfr