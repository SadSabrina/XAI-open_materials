from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List

import joblib
import numpy as np
import pandas as pd

ARTIFACTS_DIR = Path("artifacts")
REPORTS_DIR = Path("reports")


def ensure_dirs() -> None:
    ARTIFACTS_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)


def save_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_artifacts(prefix: str = "baseline") -> Dict[str, Any]:
    """
    Загружает модель и данные, сохраненные обучающим скриптом.
    prefix='baseline' — обычная модель.
    prefix='overfit' — специально переобученная модель.
    """
    model = joblib.load(ARTIFACTS_DIR / f"{prefix}_model.joblib")
    X_train = pd.read_csv(ARTIFACTS_DIR / f"{prefix}_X_train.csv")
    X_test = pd.read_csv(ARTIFACTS_DIR / f"{prefix}_X_test.csv")
    y_train = pd.read_csv(ARTIFACTS_DIR / f"{prefix}_y_train.csv")["target"]
    y_test = pd.read_csv(ARTIFACTS_DIR / f"{prefix}_y_test.csv")["target"]
    metadata = load_json(ARTIFACTS_DIR / f"{prefix}_metadata.json")

    return {
        "model": model,
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "metadata": metadata,
    }


def write_report(name: str, content: str) -> Path:
    REPORTS_DIR.mkdir(exist_ok=True)
    path = REPORTS_DIR / name
    path.write_text(content, encoding="utf-8")
    return path
