import pandas as pd
import logging

from common.config import settings

RAW_DATA_DIR = settings.RAW_DATA_DIR
PROCESSED_DATA_DIR = settings.PROCESSED_DATA_DIR

logger = logging.getLogger("medical_report_app")


# -----------------------------
# Load all questionnaires once
# -----------------------------
def load_questionnaires():
    logger.info("Loading questionnaire datasets...")

    return {
        "diq": pd.read_sas(RAW_DATA_DIR / "DIQ_G.XPT"),
        "bpq": pd.read_sas(RAW_DATA_DIR / "BPQ_G.XPT"),
        "kiq": pd.read_sas(RAW_DATA_DIR / "KIQ_U_G.XPT"),
        "cdq": pd.read_sas(RAW_DATA_DIR / "CDQ_G.XPT"),
    }


# -----------------------------
# Diabetes Label
# -----------------------------
def build_diabetes_labels(diq: pd.DataFrame) -> pd.DataFrame:
    df = diq[["SEQN", "DIQ010"]].copy()

    df = df.query("DIQ010 in [1, 2]").copy()

    df["diabetes"] = (df["DIQ010"] == 1).astype(int)

    return df[["SEQN", "diabetes"]]


# -----------------------------
# Hypertension Label
# -----------------------------
def build_hypertension_labels(bpq: pd.DataFrame) -> pd.DataFrame:
    df = bpq[["SEQN", "BPQ020"]].copy()

    df = df.query("BPQ020 in [1, 2]").copy()

    df["hypertension"] = (df["BPQ020"] == 1).astype(int)

    return df[["SEQN", "hypertension"]]


# -----------------------------
# Kidney Label
# -----------------------------
def build_kidney_labels(kiq: pd.DataFrame) -> pd.DataFrame:
    df = kiq[["SEQN", "KIQ022"]].copy()

    df = df.query("KIQ022 in [1, 2]").copy()

    df["kidney_disease"] = (df["KIQ022"] == 1).astype(int)

    return df[["SEQN", "kidney_disease"]]



# -----------------------------
# Final Labels Dataset
# -----------------------------
def build_labels_dataset() -> pd.DataFrame:
    logger.info("Building labels dataset...")

    data = load_questionnaires()

    diabetes = build_diabetes_labels(data["diq"])
    hypertension = build_hypertension_labels(data["bpq"])
    kidney = build_kidney_labels(data["kiq"])

    labels = (
        diabetes
        .merge(hypertension, on="SEQN", how="inner")
        .merge(kidney, on="SEQN", how="inner")
    )

    logger.info(f"Labels dataset shape: {labels.shape}")

    return labels


# -----------------------------
# Main
# -----------------------------
def main() -> None:
    labels_df = build_labels_dataset()

    labels_df.to_csv(
        PROCESSED_DATA_DIR / "labels_dataset_v1.csv",
        index=False,
    )

    logger.info("Labels saved successfully")


if __name__ == "__main__":
    main()