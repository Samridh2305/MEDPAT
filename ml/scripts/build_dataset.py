import logging

import pandas as pd

from common.config import settings
from ml.services.kidney_filtration_rate import calculate_egfr
from ml.scripts.features_dataset import build_clinical_features, build_lab_dataset, load_demographics
from ml.scripts.label_dataset import build_labels_dataset

RAW_DATA_DIR = settings.RAW_DATA_DIR
PROCESSED_DATA_DIR = settings.PROCESSED_DATA_DIR

logger = logging.getLogger("medical_report_app")


# -------------------------
# Master Dataset Builder
# -------------------------
def build_master_dataset() -> pd.DataFrame:
    logger.info("Building Master dataset...")

    labs = build_lab_dataset()
    clinical = build_clinical_features()
    demographics = load_demographics()
    labels = build_labels_dataset()

    master_df = (
        labels
        .merge(labs, on="SEQN", how="inner")
        .merge(clinical, on="SEQN", how="left")
        .merge(demographics, on="SEQN", how="left")
    )

    master_df["egfr"] = calculate_egfr(
        creatinine=master_df["creatinine"],
        age=master_df["age"],
        gender=master_df["gender"],
    )

    logger.info(f"Master dataset shape: {master_df.shape}")

    return master_df


# -------------------------
# Main
# -------------------------
def main() -> None:
    master_df = build_master_dataset()

    logger.info(master_df.head())

    logger.info(
        master_df.isnull()
        .mean()
        .sort_values(ascending=False)
    )
    logger.info(
        f"Duplicate SEQN count: "
        f"{master_df['SEQN'].duplicated().sum()}"
    )

    logger.info(
        f"Rows with labels: {len(master_df)}"
    )
    master_df.to_csv(
        PROCESSED_DATA_DIR / "master_dataset_v1.csv",
        index=False,
    )

    logger.info("Training dataset saved successfully")


if __name__ == "__main__":
    main()
