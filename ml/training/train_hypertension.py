import joblib
import pandas as pd
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from common.config import settings
from common.logger_config import logger
from ml.config import FEATURES

PROCESSED_DATA_DIR = settings.PROCESSED_DATA_DIR
MODEL_DIR=settings.MODEL_DIR

def load_dataset() -> pd.DataFrame:
    return pd.read_csv(
        PROCESSED_DATA_DIR / "master_dataset_v1.csv"
    )


def train_hypertension_model() -> None:
    master = load_dataset()

    hypertension_df = master.dropna(
        subset=["hypertension"]
    )

    X = hypertension_df[FEATURES]
    y = hypertension_df["hypertension"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    neg = (y_train == 0).sum()
    pos = (y_train == 1).sum()

    scale_pos_weight = neg / pos

    logger.info(
        "Training samples=%s, Positive=%s, Negative=%s",
        len(y_train),
        pos,
        neg,
    )

    logger.info(
        "Calculated scale_pos_weight=%.2f",
        scale_pos_weight,
    )

    model = XGBClassifier(
        n_estimators=500,
        max_depth=4,
        learning_rate=0.2,
        scale_pos_weight=scale_pos_weight,
        random_state=42,
    )

    logger.info("Training hypertension model")

    model.fit(
        X_train,
        y_train,
    )

    predictions = model.predict(X_test)

    logger.info(
        "\n%s",
        classification_report(
            y_test,
            predictions,
        ),
    )

    cm = confusion_matrix(
        y_test,
        predictions,
    )

    logger.info(
        "Confusion Matrix:\n%s",
        cm,
    )

    importance = (
        pd.DataFrame(
            {
                "feature": FEATURES,
                "importance": model.feature_importances_,
            }
        )
        .sort_values(
            "importance",
            ascending=False,
        )
    )

    logger.info(
        "Feature Importance:\n%s",
        importance,
    )

    joblib.dump(
    model,
    filename=MODEL_DIR / "hypertension_model.pkl",
    )

    logger.info(
        "Model saved to %s",
        MODEL_DIR / "hypertension_model.pkl",
    )

if __name__ == "__main__":
    train_hypertension_model()