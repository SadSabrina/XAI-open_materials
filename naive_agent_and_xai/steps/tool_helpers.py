from __future__ import annotations


from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix



def basic_performance_payload(model: Any, X_train: pd.DataFrame, X_test: pd.DataFrame,
                              y_train: pd.Series, y_test: pd.Series,
                              target_names: List[str]) -> Dict[str, Any]:
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)

    train_acc = accuracy_score(y_train, train_pred)
    test_acc = accuracy_score(y_test, test_pred)

    return {
        "train_accuracy": round(float(train_acc), 4),
        "test_accuracy": round(float(test_acc), 4),
       # "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
        "classification_report_test": classification_report(
            y_test,
            test_pred,
            target_names=target_names,
            output_dict=True,
            zero_division=0,
        ),
        "confusion_matrix_test": confusion_matrix(y_test, test_pred).tolist(),
    }


def sanity_checks_payload(X_train: pd.DataFrame, X_test: pd.DataFrame,
                          y_train: pd.Series, y_test: pd.Series) -> Dict[str, Any]:
    return {
        "missing_values_train": int(X_train.isna().sum().sum()),
        "missing_values_test": int(X_test.isna().sum().sum()),
        "duplicate_rows_train": int(X_train.duplicated().sum()),
        "duplicate_rows_test": int(X_test.duplicated().sum()),
     #   "train_shape": list(X_train.shape),
        "test_shape": list(X_test.shape),
        "class_balance_train": {
            str(k): round(float(v), 4)
            for k, v in y_train.value_counts(normalize=True).sort_index().items()
        },
        "class_balance_test": {
            str(k): round(float(v), 4)
            for k, v in y_test.value_counts(normalize=True).sort_index().items()
        },
    }


def feature_importance_payload(model: Any, feature_names: List[str], top_k: int = 15) -> Dict[str, Any]:
    if not hasattr(model, "feature_importances_"):
        return {
            "error": "Model does not expose feature_importances_.",
            "hint": "Use permutation importance or SHAP instead.",
        }

    ranked = sorted(
        zip(feature_names, model.feature_importances_),
        key=lambda x: x[1],
        reverse=True,
    )[:top_k]

    return {
        "top_features": [
            {"feature": name, "importance": round(float(score), 6)}
            for name, score in ranked
        ]
    }


def local_prediction_payload(model: Any, X_test: pd.DataFrame, row_index: int,
                             target_names: List[str], top_k: int = 10) -> Dict[str, Any]:
    if row_index < 0 or row_index >= len(X_test):
        return {"error": f"row_index must be between 0 and {len(X_test) - 1}"}

    row = X_test.iloc[[row_index]]
    pred = int(model.predict(row)[0])

    payload: Dict[str, Any] = {
        "row_index": row_index,
        "predicted_class_id": pred,
        "predicted_class_name": target_names[pred],
    }

    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(row)[0]
        payload["probabilities"] = {
            target_names[i]: round(float(p), 6) for i, p in enumerate(proba)
        }

    if hasattr(model, "feature_importances_"):
        ranked = sorted(
            zip(X_test.columns, model.feature_importances_, row.iloc[0].values),
            key=lambda x: x[1],
            reverse=True,
        )[:top_k]
        payload["top_global_features_for_this_row"] = [
            {
                "feature": name,
                "global_importance": round(float(imp), 6),
                "row_value": round(float(value), 6),
            }
            for name, imp, value in ranked
        ]

    return payload


def shap_payload(model: Any, X_background: pd.DataFrame, X_explain: pd.DataFrame,
                 top_k: int = 15, row_index: int = 0) -> Dict[str, Any]:
    """
    Returns a compact SHAP payload.

    We use shap for trees.TreeExplainer.
    For binary classification, SHAP can have different output formats:
     - list[array] by class;
    - array of dimensions [n_samples, n_features, n_classes];
    - array [n_samples, n_features].
    Therefore, we normalize the result. 
    """
    try:
        import shap
    except ImportError:
        return {"error": "shap is not installed. Run pip install shap"}

    background = X_background.sample(
        min(100, len(X_background)), random_state=42
    )

    explain_data = X_explain.iloc[: min(50, len(X_explain))]

    try:
        explainer = shap.TreeExplainer(model, data=background)
        shap_values = explainer.shap_values(explain_data)
    except Exception as e:
        return {"error": f"SHAP failed: {type(e).__name__}: {e}"}

    # Normalize SHAP values to [n_samples, n_features] for the positive class if possible.
    if isinstance(shap_values, list):
        values = shap_values[1] if len(shap_values) > 1 else shap_values[0]
    else:
        arr = np.array(shap_values)
        if arr.ndim == 3:
            values = arr[:, :, 1] if arr.shape[2] > 1 else arr[:, :, 0]
        else:
            values = arr

    mean_abs = np.abs(values).mean(axis=0)
    ranked_idx = np.argsort(mean_abs)[::-1][:top_k]

    global_top = [
        {
            "feature": str(explain_data.columns[i]),
            "mean_abs_shap": round(float(mean_abs[i]), 6),
        }
        for i in ranked_idx
    ]

    row_index = min(row_index, len(explain_data) - 1)
    row_values = values[row_index]
    local_idx = np.argsort(np.abs(row_values))[::-1][:top_k]

    local_top = [
        {
            "feature": str(explain_data.columns[i]),
            "shap_value": round(float(row_values[i]), 6),
            "feature_value": round(float(explain_data.iloc[row_index, i]), 6),
        }
        for i in local_idx
    ]

    return {
        "note": "For binary classification, SHAP values are reported for class index 1 when available.",
        "global_top_features": global_top,
        "local_explanation": {
            "row_index": row_index,
            "top_features": local_top,
        },
    }

