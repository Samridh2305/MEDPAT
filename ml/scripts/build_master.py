import pandas as pd

from common.config import settings

PROCESSED_DATA_DIR = settings.PROCESSED_DATA_DIR


def build_master_dataset() -> pd.DataFrame:
    features = pd.read_csv(
        PROCESSED_DATA_DIR / "final_dataset_v1.csv"
    )

    labels = pd.read_csv(
        PROCESSED_DATA_DIR / "labels_dataset_v1.csv"
    )

    return features.merge(
        labels,
        on="SEQN",
        how="left",
    )


def main() -> None:
    master = build_master_dataset()

    print(master.head())
    print(master.shape)

    master.to_csv(
        PROCESSED_DATA_DIR / "master_dataset_v1.csv",
        index=False,
    )

if __name__ == "__main__":
    main()