from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from common import (
    ARTIFACTS_DIR,
    ensure_dirs,
    save_json,
)

from tool_helpers import basic_performance_payload


def main() -> None:
    ensure_dirs()

    data = load_breast_cancer()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = pd.Series(data.target, name="target")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=5,
        min_samples_leaf=3,
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

    joblib.dump(model, ARTIFACTS_DIR / "baseline_model.joblib")
    X_train.to_csv("artifacts/baseline_X_train.csv", index=False)
    X_test.to_csv("artifacts/baseline_X_test.csv", index=False)
    y_train.to_csv("artifacts/baseline_y_train.csv", index=False)
    y_test.to_csv("artifacts/baseline_y_test.csv", index=False)
    save_json(ARTIFACTS_DIR / "baseline_metadata.json", metadata)
    save_json(ARTIFACTS_DIR / "baseline_performance.json", performance)

    print("Baseline model saved.")
    print(f"Artifacts directory: {ARTIFACTS_DIR.resolve()}")
    print("Performance:")
    print(performance)


if __name__ == "__main__":
    main()
