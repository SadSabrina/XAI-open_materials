from __future__ import annotations

import json

from langchain.agents import create_agent
from langchain.tools import tool

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

PREFIX = "baseline" #"batch_artifact"

art = load_artifacts(prefix=PREFIX)
model = art["model"]
X_train = art["X_train"]
X_test = art["X_test"]
y_train = art["y_train"]
y_test = art["y_test"]
metadata = art["metadata"]
target_names = metadata["target_names"]




@tool
def model_performance() -> str:
    """Return train/test model performance and generalization gap."""
    return json.dumps(
        basic_performance_payload(model, X_train, X_test, y_train, y_test, target_names),
        indent=2,
        ensure_ascii=False,
    )


@tool
def sanity_checks() -> str:
    """Run basic sanity checks for data shape, missing values, duplicates and class balance."""
    return json.dumps(
        sanity_checks_payload(X_train, X_test, y_train, y_test),
        indent=2,
        ensure_ascii=False,
    )


@tool
def feature_importance(top_k: int = 15) -> str:
    """Return top-k impurity-based feature importances from the model."""
    return json.dumps(
        feature_importance_payload(model, list(X_train.columns), top_k=top_k),
        indent=2,
        ensure_ascii=False,
    )


@tool
def shap_explanation(top_k: int = 15, row_index: int = 0) -> str:
    """Return global and local SHAP explanations for the model."""
    return json.dumps(
        shap_payload(model, X_train, X_test, top_k=top_k, row_index=row_index),
        indent=2,
        ensure_ascii=False,
    )


@tool
def explain_single_prediction(row_index: int = 0) -> str:
    """Return a compact local explanation for one test row using prediction probabilities and top global features."""
    return json.dumps(
        local_prediction_payload(model, X_test, row_index, target_names),
        indent=2,
        ensure_ascii=False,
    )


def main() -> None:
    llm = make_llm(model_name="openai/gpt-oss-120b:free", temperature=0)

    agent = create_agent(
        model=llm,
        tools=[
            model_performance,
            sanity_checks,
            feature_importance,
            shap_explanation,
            explain_single_prediction,
        ],
        system_prompt="""
                        You are an interpretability agent for a tabular ML model.
                        """,
    )

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": """
                    Analyze the trained model.
                    Important: call each tool at most once and then stop.
                    """,
                                                    }
                                                ]
                                            },
        config={"recursion_limit": 12},
    )

    final = result["messages"][-1].content
    path = write_report(f"02_naive_agent_report_zero_shot_{PREFIX}.md", final)
    print(final)
    print(f"\nReport saved to: {path}")


if __name__ == "__main__":
    main()
