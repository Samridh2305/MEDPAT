# ml/helpers/build_features.py

import pandas as pd

from ml.config import FEATURES


def build_prediction_features(
    lab_values: dict,
) -> pd.DataFrame:

    row = {}

    for feature in FEATURES:
        row[feature] = lab_values.get(
            feature,
            0,
        )

    return pd.DataFrame([row])

# ml/helpers/lab_to_dict.py

def labs_to_feature_dict(
    labs,
) -> dict:

    values = {}

    for lab in labs:

        if (
            lab.normalized_name
            and lab.value is not None
        ):
            values[
                lab.normalized_name
            ] = lab.value

    return values