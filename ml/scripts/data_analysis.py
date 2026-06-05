import pandas as pd

from common.config import settings
from ml.config import LAB_RENAME_MAP, LAB_COLUMNS

RAW_DATA_DIR = settings.RAW_DATA_DIR
PROCESSED_DATA_DIR = settings.PROCESSED_DATA_DIR


def load_lab_datasets() -> tuple[pd.DataFrame, ...]:
    cbc = pd.read_sas(RAW_DATA_DIR / "CBC_G.XPT")
    biopro = pd.read_sas(RAW_DATA_DIR / "BIOPRO_G.XPT")
    ghb = pd.read_sas(RAW_DATA_DIR / "GHB_G.XPT")
    hdl = pd.read_sas(RAW_DATA_DIR / "HDL_G.XPT")
    tchol = pd.read_sas(RAW_DATA_DIR / "TCHOL_G.XPT")
    alb_cr = pd.read_sas(RAW_DATA_DIR / "ALB_CR_G.XPT")
    apob = pd.read_sas(RAW_DATA_DIR / "APOB_G.XPT")
    bpx = pd.read_sas(RAW_DATA_DIR / "BPX_G.XPT")
    paq = pd.read_sas(RAW_DATA_DIR / "PAQ_G.XPT")
    trigly = pd.read_sas(RAW_DATA_DIR / "TRIGLY_G.XPT")
    vid = pd.read_sas(RAW_DATA_DIR / "VID_G.XPT")
    ucosmo = pd.read_sas(RAW_DATA_DIR / "UCOSMO_G.XPT")

    return cbc, biopro, ghb, hdl, tchol, alb_cr, apob, bpx, paq, trigly, vid, ucosmo


def build_lab_dataset() -> pd.DataFrame:
    cbc, biopro, ghb, hdl, tchol = load_lab_datasets()

    master = (
        cbc
        .merge(biopro, on="SEQN")
        .merge(ghb, on="SEQN")
        .merge(hdl, on="SEQN")
        .merge(tchol, on="SEQN")
    )

    return (
        master[LAB_COLUMNS]
        .rename(columns=LAB_RENAME_MAP)
        .dropna()
    )

def load_demographics() -> pd.DataFrame:
    demo = pd.read_sas(RAW_DATA_DIR / "DEMO_G.XPT")

    return demo[
        [
            "SEQN",
            "RIDAGEYR",
            "RIAGENDR",
            "RIDRETH1",
        ]
    ].rename(
        columns={
            "RIDAGEYR": "age",
            "RIAGENDR": "gender",
            "RIDRETH1": "race",
        }
    )


def build_final_dataset() -> pd.DataFrame:
    labs = build_lab_dataset()
    demographics = load_demographics()

    return labs.merge(
        demographics,
        on="SEQN",
        how="inner",
    )


def main() -> None:
    final_df = build_final_dataset()

    print(final_df.head())
    print(final_df.shape)

    final_df.to_csv(
        PROCESSED_DATA_DIR / "final_dataset_v1.csv",
        index=False,
    )


if __name__ == "__main__":
    main()
