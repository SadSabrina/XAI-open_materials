from __future__ import annotations

import json

from common import (
    load_artifacts,
    write_report,
)

from agent import make_llm

from tool_helpers import (
    basic_performance_payload,
    feature_importance_payload,
    local_prediction_payload,
    sanity_checks_payload,
    shap_payload,
        )

def invoke_role(llm, role_name: str, system_instruction: str, payload: str) -> str:
    prompt = f"""
Role: {role_name}

{system_instruction}

Input:
{payload}
"""
    return llm.invoke(prompt).content

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

    measurements = {
        "metadata": metadata,
        "performance": basic_performance_payload(
            model, X_train, X_test, y_train, y_test, target_names
        ),
        "sanity_checks": sanity_checks_payload(X_train, X_test, y_train, y_test),
        "feature_importance": feature_importance_payload(
            model, metadata["feature_names"], top_k=15
        ),
        "shap": shap_payload(model, X_train, X_test, top_k=15, row_index=0),
        "local_prediction": local_prediction_payload(
            model, X_test, row_index=0, target_names=target_names
        ),
    }

    llm = make_llm(model_name="openai/gpt-oss-120b:free", temperature=0)

    measurements_text = json.dumps(measurements, indent=2, ensure_ascii=False)

    analyst_report = invoke_role(
        llm=llm,
        role_name="Analyst Agent",
        system_instruction="""
You analyze ML model evidence.

Task:
- Explain what the model appears to learn.
- Use performance, feature importance, SHAP and local prediction.
- Do not discuss policy or style.
- Do not overclaim causality.
- Be concise and evidence-based.
""",
        payload=measurements_text,
    )

    critic_report = invoke_role(
        llm=llm,
        role_name="Critic Agent",
        system_instruction="""
You are a skeptical reviewer of an interpretability report.

Task:
- Look for overclaiming.
- Look for missing sanity checks.
- Look for signs of overfitting or weak generalization.
- Look for causal claims that are not justified.
- Look for places where SHAP or feature importance may be unstable.
- Produce a list of concrete criticisms and recommended fixes.
""",
        payload=json.dumps(
            {
                "measurements": measurements,
                "analyst_report": analyst_report,
            },
            indent=2,
            ensure_ascii=False,
        ),
    )

    reporter_report = invoke_role(
        llm=llm,
        role_name="Reporter Agent",
        system_instruction="""
You write the final article-ready interpretability report.

Use:
- the raw measurements,
- the analyst report,
- the critic report.

Final report requirements:
1. Short summary
2. What the model learned
3. Evidence from global importance and SHAP
4. Local explanation
5. Reliability and sanity checks
6. Critic's concerns
7. Limitations
8. Next experiments

Be precise. Separate evidence from interpretation.
""",
        payload=json.dumps(
            {
                "measurements": measurements,
                "analyst_report": analyst_report,
                "critic_report": critic_report,
            },
            indent=2,
            ensure_ascii=False,
        ),
    )

    final = f"""# Multi-agent Interpretability Report

## Analyst Agent

{analyst_report}

---

## Critic Agent

{critic_report}

---

## Reporter Agent Final Report

{reporter_report}
"""

    path = write_report(f"04_multi_agent_report_{PREFIX}.md", final)
    print(final)
    print(f"\nReport saved to: {path}")


if __name__ == "__main__":
    main()
