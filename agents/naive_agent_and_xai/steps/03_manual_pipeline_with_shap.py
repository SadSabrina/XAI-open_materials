from __future__ import annotations

import json

from agents.naive_agent_and_xai.steps.common import (
    load_artifacts,
    write_report,
)

from agents.naive_agent_and_xai.steps.agent import make_llm

from agents.naive_agent_and_xai.steps.tool_helpers import (
    basic_performance_payload,
    feature_importance_payload,
    local_prediction_payload,
    sanity_checks_payload,
    shap_payload,
        )

PREFIX = "batch_artifact"

def main() -> None:
    art = load_artifacts(prefix=PREFIX)
    model = art["model"]
    X_train = art["X_train"]
    X_test = art["X_test"]
    y_train = art["y_train"]
    y_test = art["y_test"]
    metadata = art["metadata"]
    target_names = metadata["target_names"]

    performance = basic_performance_payload(
        model, X_train, X_test, y_train, y_test, target_names
    )
    checks = sanity_checks_payload(X_train, X_test, y_train, y_test)
    importance = feature_importance_payload(model, metadata["feature_names"], top_k=15)
    shap_info = shap_payload(model, X_train, X_test, top_k=15, row_index=0)
    local = local_prediction_payload(model, X_test, row_index=0, target_names=target_names)

    llm = make_llm(model_name="openai/gpt-oss-120b:free", temperature=0)

    prompt = f"""
You are an interpretability agent for a tabular ML model.

Write a careful interpretability report using only the provided tool outputs.

Do not overclaim causality.
Separate observed evidence from hypotheses.
Mention limitations and possible failure modes.

MODEL METADATA:
{json.dumps(metadata, indent=2, ensure_ascii=False)}

MODEL PERFORMANCE:
{json.dumps(performance, indent=2, ensure_ascii=False)}

SANITY CHECKS:
{json.dumps(checks, indent=2, ensure_ascii=False)}

FEATURE IMPORTANCE:
{json.dumps(importance, indent=2, ensure_ascii=False)}

SHAP:
{json.dumps(shap_info, indent=2, ensure_ascii=False)}

LOCAL PREDICTION:
{json.dumps(local, indent=2, ensure_ascii=False)}

Required sections:
1. Short summary
2. Performance
3. Sanity checks
4. Global interpretation
5. SHAP interpretation
6. Local explanation
7. Limitations
8. What to check next
"""

    response = llm.invoke(prompt)
    final = response.content

    path = write_report(f"03_manual_pipeline_report_{PREFIX}.md", final)
    print(final)
    print(f"\nReport saved to: {path}")


if __name__ == "__main__":
    main()
