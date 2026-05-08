# Agentic XAI with LangChain

Small project on building interpretability agents for tabular ML.

The project compares:
- naive tool-calling agents,
- deterministic/manual pipelines,
- multi-agent systems with critique.

I also simulate a batch artifact to test whether agents can detect suspicious dataset behavior.

---

# Setup

## Create environment

```bash
python -m venv agent_exp
source agent_exp/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

---

# API Configuration

Create `.env`:

```env
OPENROUTER_API_KEY=your_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

Experiments use:

```text
openai/gpt-oss-120b:free
```

via OpenRouter.

---

# Experiments

## 1. Train baseline model

```bash
python steps/01_train_model.py
```

## 2. Run naive agent

```bash
python steps/02_naive_interpretability_agent.py
```

## 3. Run manual pipeline

```bash
python steps/03_manual_pipeline_with_shap.py
```

## 4. Run multi-agent pipeline

```bash
python steps/04_multi_agent_system.py
```

---

# Batch Artifact Experiment

Train artifact model:

```bash
python steps/05_train_batch_artifact_model.py
```

Then switch:

```python
PREFIX = "batch_artifact"
```

inside pipeline scripts and rerun experiments.

---

# Main Idea

The project explores:
- interpretability with LLM agents,
- orchestration strategies,
- failure modes,
- skepticism in XAI systems.

See the analysis in `agent.ipynb`.
