from __future__ import annotations

import joblib
import numpy as np
import pandas as pd

from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from common import ARTIFACTS_DIR, ensure_dirs, save_json
from tool_helpers import basic_performance_payload


def add_batch_artifact(
    X: pd.DataFrame,
    y: pd.Series,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Create a batch_id that is associated with the target.

    In the real world, this could be::
    - hospital_id
    - lab_id
    - scanner_id
    - collection_batch
    - data_source
    """
    rng = np.random.default_rng(random_state)

    X_new = X.copy()

    batch = []

    for label in y:
        if label == 1:
            # For benign  batch_A / batch_B
            batch.append(rng.choice(["batch_A", "batch_B", "batch_C"], p=[0.65, 0.25, 0.10]))
        else:
            # For malignant  batch_C / batch_D
            batch.append(rng.choice(["batch_A", "batch_B", "batch_C"], p=[0.05, 0.20, 0.75]))

    X_new["batch"] = batch

    return X_new


def main() -> None:
    ensure_dirs()

    data = load_breast_cancer()

    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = pd.Series(data.target, name="target")

    X = add_batch_artifact(X, y, random_state=42)

    X = pd.get_dummies(
        X,
        columns=["batch"],
        drop_first=False,
        dtype=int,
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        min_samples_leaf=1,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    metadata = {
        "dataset": "sklearn.datasets.load_breast_cancer",
        "task": "binary classification",
        "target_names": list(data.target_names),
        "feature_names": list(X.columns),
        "model_type": "RandomForestClassifier",
        "model_params": model.get_params(),
    }

    performance = basic_performance_payload(
        model=model,
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test,
        target_names=list(data.target_names),
    )

    joblib.dump(model, ARTIFACTS_DIR / "batch_artifact_model.joblib")

    X_train.to_csv(ARTIFACTS_DIR / "batch_artifact_X_train.csv", index=False)
    X_test.to_csv(ARTIFACTS_DIR / "batch_artifact_X_test.csv", index=False)
    y_train.to_csv(ARTIFACTS_DIR / "batch_artifact_y_train.csv", index=False)
    y_test.to_csv(ARTIFACTS_DIR / "batch_artifact_y_test.csv", index=False)

    save_json(ARTIFACTS_DIR / "batch_artifact_metadata.json", metadata)
    save_json(ARTIFACTS_DIR / "batch_artifact_performance.json", performance)

    print("Batch artifact model saved.")
    print(f"Artifacts directory: {ARTIFACTS_DIR.resolve()}")
    print("Performance:")
    print(performance)


if __name__ == "__main__":
    main()