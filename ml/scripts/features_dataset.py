import logging

import numpy as np
import pandas as pd

from common.config import settings
from ml.config import LAB_COLUMNS, LAB_RENAME_MAP, CLINICAL_RENAME_MAP

RAW_DATA_DIR = settings.RAW_DATA_DIR

logger = logging.getLogger("medical_report_app")


def build_clinical_features() -> pd.DataFrame:
    logger.info("Building clinical features...")

    alb_cr = pd.read_sas(RAW_DATA_DIR / "ALB_CR_G.XPT")
    apob = pd.read_sas(RAW_DATA_DIR / "APOB_G.XPT")
    bpx = pd.read_sas(RAW_DATA_DIR / "BPX_G.XPT")
    paq = pd.read_sas(RAW_DATA_DIR / "PAQ_G.XPT")
    trigly = pd.read_sas(RAW_DATA_DIR / "TRIGLY_G.XPT")
    vid = pd.read_sas(RAW_DATA_DIR / "VID_G.XPT")
    ucosmo = pd.read_sas(RAW_DATA_DIR / "UCOSMO_G.XPT")

    # -------------------------
    # Blood Pressure
    # -------------------------
    bp_features = pd.DataFrame({
        "SEQN": bpx["SEQN"],
        "avg_sys_bp": bpx[["BPXSY1", "BPXSY2", "BPXSY3", "BPXSY4"]].mean(axis=1),
        "avg_dia_bp": bpx[["BPXDI1", "BPXDI2", "BPXDI3", "BPXDI4"]].mean(axis=1),
        "pulse_rate": bpx["BPXPLS"],
    })

    bp_features["hypertension_stage1"] = (
            (bp_features["avg_sys_bp"] >= 130) |
            (bp_features["avg_dia_bp"] >= 80)
    ).astype(int)

    bp_features["hypertension_stage2"] = (
            (bp_features["avg_sys_bp"] >= 140) |
            (bp_features["avg_dia_bp"] >= 90)
    ).astype(int)

    # -------------------------
    # Kidney
    # -------------------------
    kidney_features = (
        alb_cr[["SEQN", "URDACT"]]
        .rename(columns=CLINICAL_RENAME_MAP)
    )

    kidney_features = kidney_features.merge(
        ucosmo[["SEQN", "URXOAV"]].rename(
            columns={
                "URXOAV": CLINICAL_RENAME_MAP["URXOAV"]
            }
        ),
        on="SEQN",
        how="left",
    )

    # -------------------------
    # Lipids
    # -------------------------
    lipid_features = (
        trigly[["SEQN", "LBXTR", "LBDLDL"]]
        .rename(columns=CLINICAL_RENAME_MAP)
    )

    lipid_features = lipid_features.merge(
        apob[["SEQN", "LBXAPB"]].rename(
            columns={
                "LBXAPB": CLINICAL_RENAME_MAP["LBXAPB"]
            }
        ),
        on="SEQN",
        how="left",
    )

    # Safe derived feature (important fix)
    lipid_features["tg_ldl_ratio"] = np.where(
        lipid_features["ldl"] > 0,
        lipid_features["triglycerides"] / lipid_features["ldl"],
        np.nan
    )

    # -------------------------
    # Vitamin D
    # -------------------------
    vitamin_features = (
        vid[["SEQN", "LBXVIDMS"]]
        .rename(columns=CLINICAL_RENAME_MAP)
    )

    vitamin_features["vitamin_d_deficient"] = (
            vitamin_features["vitamin_d"] < 20
    ).astype(int)

    # -------------------------
    # Activity
    # -------------------------
    activity_cols = ["PAQ605", "PAQ620", "PAQ635", "PAQ650"]

    activity_binary = paq[activity_cols].replace({
        1: 1,
        2: 0,
        7: np.nan,
        9: np.nan,
    })

    activity = pd.DataFrame({
        "SEQN": paq["SEQN"],
        "activity_score": activity_binary.fillna(0).sum(axis=1)
    })

    # -------------------------
    # Final merge
    # -------------------------
    clinical = (
        bp_features
        .merge(kidney_features, on="SEQN", how="left")
        .merge(lipid_features, on="SEQN", how="left")
        .merge(vitamin_features, on="SEQN", how="left")
        .merge(activity, on="SEQN", how="left")
    )

    logger.info(f"Clinical features shape: {clinical.shape}")

    return clinical


def load_lab_datasets() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    return (
        pd.read_sas(RAW_DATA_DIR / "CBC_G.XPT"),
        pd.read_sas(RAW_DATA_DIR / "BIOPRO_G.XPT"),
        pd.read_sas(RAW_DATA_DIR / "GHB_G.XPT"),
        pd.read_sas(RAW_DATA_DIR / "HDL_G.XPT"),
        pd.read_sas(RAW_DATA_DIR / "TCHOL_G.XPT"),
    )


def build_lab_dataset() -> pd.DataFrame:
    cbc, biopro, ghb, hdl, tchol = load_lab_datasets()

    lab_df = (
        cbc
        .merge(biopro, on="SEQN")
        .merge(ghb, on="SEQN")
        .merge(hdl, on="SEQN")
        .merge(tchol, on="SEQN")
    )

    labs = lab_df[LAB_COLUMNS].rename(columns=LAB_RENAME_MAP)

    logger.info(f"Lab dataset shape: {labs.shape}")

    return labs


# -------------------------
# Demographics
# -------------------------
def load_demographics() -> pd.DataFrame:
    demo = pd.read_sas(RAW_DATA_DIR / "DEMO_G.XPT")

    return demo[
        ["SEQN", "RIDAGEYR", "RIAGENDR", "RIDRETH1"]
    ].rename(
        columns={
            "RIDAGEYR": "age",
            "RIAGENDR": "gender",
            "RIDRETH1": "race",
        }
    )


def main():
    clinical = build_clinical_features()
    labs = build_lab_dataset()
    demographics = load_demographics()
    logger.info(clinical.head())
    logger.info(labs.head())
    logger.info(demographics.head())


if __name__ == "__main__":
    main()
