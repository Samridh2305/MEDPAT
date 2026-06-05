import pandas as pd

from common.config import settings

RAW_DATA_DIR = settings.RAW_DATA_DIR
PROCESSED_DATA_DIR = settings.PROCESSED_DATA_DIR


def load_questionnaires() -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
]:
    diq = pd.read_sas(RAW_DATA_DIR / "DIQ_G.XPT")
    bpq = pd.read_sas(RAW_DATA_DIR / "BPQ_G.XPT")
    kiq = pd.read_sas(RAW_DATA_DIR / "KIQ_U_G.XPT")
    cdq = pd.read_sas(RAW_DATA_DIR / "CDQ_G.XPT")

    return diq, bpq, kiq, cdq


def build_diabetes_labels() -> pd.DataFrame:
    diq = pd.read_sas(RAW_DATA_DIR / "DIQ_G.XPT")

    diabetes = (
        diq[["SEQN", "DIQ010", ]].query("DIQ010 in [1, 2]")
    )

    diabetes["diabetes"] = (
            diabetes["DIQ010"] == 1
    ).astype(int)

    return diabetes[
        [
            "SEQN",
            "diabetes",
        ]
    ]


def build_hypertension_labels() -> pd.DataFrame:
    bpq = pd.read_sas(RAW_DATA_DIR / "BPQ_G.XPT")

    hypertension = (
        bpq[["SEQN", "BPQ020", ]].query("BPQ020 in [1, 2]")
    )

    hypertension["hypertension"] = (
            hypertension["BPQ020"] == 1
    ).astype(int)

    return hypertension[
        [
            "SEQN",
            "hypertension",
        ]
    ]


def build_kidney_labels() -> pd.DataFrame:
    kiq = pd.read_sas(RAW_DATA_DIR / "KIQ_U_G.XPT")

    kidney = (
        kiq[["SEQN", "KIQ022", ]].query("KIQ022 in [1, 2]")
    )

    kidney["kidney_disease"] = (
            kidney["KIQ022"] == 1
    ).astype(int)

    return kidney[
        [
            "SEQN",
            "kidney_disease",
        ]
    ]


def build_cardiovascular_labels() -> pd.DataFrame:
    cdq = pd.read_sas(RAW_DATA_DIR / "CDQ_G.XPT")

    cardiovascular = (
        cdq[["SEQN", "CDQ001", ]].query("CDQ001 in [1, 2]")
    )

    cardiovascular["cardiovascular"] = (
            cardiovascular["CDQ001"] == 1
    ).astype(int)

    return cardiovascular[
        [
            "SEQN",
            "cardiovascular",
        ]
    ]


def build_labels_dataset() -> pd.DataFrame:
    diabetes = build_diabetes_labels()
    hypertension = build_hypertension_labels()
    kidney = build_kidney_labels()
    cardiovascular = build_cardiovascular_labels()

    return (
        diabetes
        .merge(
            hypertension,
            on="SEQN",
            how="outer",
        )
        .merge(
            kidney,
            on="SEQN",
            how="outer",
        )
        .merge(
            cardiovascular,
            on="SEQN",
            how="outer",
        )
    )


def main() -> None:
    labels_df = build_labels_dataset()

    print(labels_df.head())
    print(labels_df.shape)

    labels_df.to_csv(
        PROCESSED_DATA_DIR / "labels_dataset_v1.csv",
        index=False,
    )


if __name__ == "__main__":
    main()
