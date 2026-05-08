## **Building an XAI Agent and Never Being Online Again**

Hi everyone! It seems that the collective existential crisis caused by the arrival of agents into our lives has finally settled down a bit. I’ve always loved the process of solving problems — this strangely personal little universe of reasoning, even when you already know the rule of L’Hôpital / Modus Ponens / whichever theorem made you laugh the hardest while studying.

And now, to avoid completely falling out of modern life, problems increasingly have to be solved *with someone*. And that someone is an LLM-Agent.

I work in XAI research, so among the endless stream of “agent tutorials”, this article will be a more practical attempt to answer a specific question:

> Can we build an agent for ML interpretability and finally stop staring at logistic regression coefficients at 2 a.m.?

Or, unfortunately, will we still have to think after all?

#### **A Bit of Context**

Before diving in, let’s quickly align on a few core concepts.

**Definitions:**

An *LLM Agent* is a system where a large language model acts as the main engine. Different people define agents differently, but I like to think about them as a set of roughly four components: $\{M, T, S, R\}$

where:

* $M$ — the LLM itself;
* $T$ — the set of tools the agent can call;
* $S$ — the system state: memory, action history, intermediate results;
* $R$ — the reasoning loop, i.e. the cycle of reasoning and decision-making.

The math in this article more or less ends here, but this formulation will still be useful to keep in mind.

*Explainable AI (XAI)* is a collection of methods and approaches used to analyze model behavior (both LLMs and classical ML models, although in this article we will focus only on ML). Technically, every interpretability method has its own mathematical formulation, but fortunately we do not need to go that deep today.

**Context:**

Most — alright, almost all — XAI approaches were historically designed for humans. We used to sit there and try to understand why “the thing” works. Classical ML methods like SHAP values, feature importance, and partial dependence plots assume that a human enters the interpretation loop next: someone who can think, look at plots or coefficients, and still remembers what a confidence interval is.

Any process that can be broken down step by step — unless one wrong step means the patient can no longer be stitched back together, sorry — will sooner or later be automated. Interpretability was no exception. This is how *agentic XAI* was informally born: approaches where an LLM explains a model.

There are many ways to improve an agent’s explanation:

- for a human: go for a walk and come back;
- for an LLM: run more reasoning cycles;
- for a human: find another human and brainstorm;
- for an LLM: critique its own solution.

But more does not mean better, and automatic plus fast does not automatically mean cheap and cheerful. Agents have failure modes — places where everything seems to work, but absolutely not in the way we wanted. For example: p-hacking, where an LLM agent automatically searches through analytical choices until it gets a statistically significant result; missing sanity checks, where the agent skips basic validation of the data, experiment, or model; or the one much closer to everyday work — unreliable LLM-driven annotation, where the LLM inconsistently labels data or interprets research results, creating noise, bias, or entirely fictional conclusions.

This article is meant as an example of a “proper enough” agent-based interpretability pipeline. We will:

- train a baseline model;
- add SHAP and feature attribution;
- build a naive, but still decent, interpretability agent;
- build a less naive multi-agent pipeline;
- look at a failure mode that we will construct ourselves.

Let’s go.

### **Design: the Agent**
We will use [LangChain](https://github.com/langchain-ai/langchain) — and honestly, I have yet to find anything more pleasant for this kind of work. So, instead of just looking at a simple piece of code — hooray, tautology — let’s treat this as a proper small experiment.
We will have two versions of the task.
**The first one is the baseline:** a regular model trained on the standard `breast_cancer` dataset. Here we will check whether an agentic pipeline can, in principle, produce a reasonable XAI report: evaluate model quality, inspect feature importance, compute SHAP, and provide a local explanation for one example.
**The second one is the batch artifact setting:** the same task, but with an additional feature that imitates a data collection artifact. In the real world, this could be a hospital ID, laboratory ID, device ID, measurement batch, or data source. Such a feature may correlate strongly with the target not because it carries meaningful signal, but simply because of how the data was collected. Ideally, if we are automating ML interpretation, the agent should be able to notice that.
For each task version, we will run three pipeline variants.

#### **Naive Agent**
The first variant is a naive agent — a regular tool-using agent. We will run it in two versions: one with detailed instructions and one closer to a zero-shot setup. In both cases, the agent can call functions to compute metrics, sanity checks, feature importance, SHAP, and a local explanation.
Schematically:
```text
LLM + tools + freedom of action 
(not a very constrained system prompt)
LLM + tools + freedom of action 
(constrained system prompt)

Given mostly just the system prompt as context, the agent decides:

* which tools to call;
* in what order;
* when to stop;
* how to assemble the final interpretability report.

Run:
```bash
python 02_naive_interpretability_agent.py
```
Inside, the agent gets the following tools (tool_helpers.py, agent.py):

* model_performance — computes train/test quality and the generalization gap;
* sanity_checks — checks basic properties of the data;
* feature_importance — extracts impurity-based importance from the forest;
* shap_explanation — computes global/local SHAP;
* explain_single_prediction — explains one model prediction.

From the LangChain perspective, this is just a tool-calling pipeline: the LLM receives a task, calls functions, and gradually builds a reasoning trace. From the XAI perspective, these tools cover the necessary and sufficient analysis for a random forest in this setup.

*Note:*
If you look at the code, pay attention to the recursion_limit parameter. It limits the number of iterations the agent can take. Because an agent is like a Sunday before Monday: the last donut is never really the last one. In our case, we explicitly limit the number of steps in the config and protect ourselves from buying new pants:

```python
config={"recursion_limit": 12}
```

The goal of this step is to see what happens if we give an LLM agent tools and say: “Analyze the model.” This is the simplest and most natural scenario. The questions are: how did the agent use the tools? Did it respect the instructions? Did it notice suspicious features?

#### **Manual Agent Pipeline**

The second variant is a manual pipeline. Here all tools are executed deterministically, and the LLM receives the already computed results and only writes the report.

This experiment is a baseline, but now for the agent pipeline itself. We remove part of the autonomy — in fancier terms, we remove the orchestration layer — and get reproducibility: the same checks, the same evidence, the same inputs.

```bash
LLM + context + analysis task
(summarization + interpretation + writing)
```

Run:

```bash
python 03_manual_pipeline_with_shap.py
```
The question here is: does a fixed order of checks help avoid missing important details, or is the “go figure it out yourself” mode good enough?

#### **Multi-Agent Pipeline**

The third variant, as you may have unexpectedly guessed, consists of three agents. One is the analyst, one is the critic, and one is the reporting officer. Office roles define themselves: the analyst performs the initial interpretation of the model, the critic searches for weak points such as overfitting, leakage, suspicious features, overclaiming, and missing sanity checks, and the reporter assembles the final text. All roles are defined through system prompts.

Run:
```bash
python 04_multi_agent_system.py
```

The idea here is role separation. If one agent simultaneously analyzes, critiques, and writes the final report, it can easily miss its own mistakes. A multi-agent pipeline makes criticism part of the process. And don’t pretend you’ve never had a rubber duck on your desk.

The key questions here are: did the critic-agent catch the batch artifact, and did the final report improve?

#### **Note: XAI Design**

> Why do we give the agent exactly these tools — not fewer and not more? 

This follows from the task setup. We are working with a RandomForestClassifier, so we use several ways to interpret the model: internal and external methods, as well as local and global levels. Each has its own limitations, but this pair is enough for our experiment.

For a random forest, feature_importance is impurity-based importance: it measures how much a feature helped reduce uncertainty when splitting the trees. The method is fast, built-in, and gives a good global picture of what the model relies on on average. Its caveats are also well known: importance can be unstable for correlated features, and features with many unique values — also called high-cardinality features — may receive artificially inflated importance.

SHAP values are an external method based on the idea of fairly distributing the “payout” among features. Simplifying a bit, we estimate feature contributions by adding and removing them from coalitions. SHAP also gives us two levels: contribution to a specific model prediction, and global SHAP, which averages contributions over the dataset. SHAP has its own caveats: values are sensitive to the data distribution, correlated features, and the chosen background distribution. A good agent should be aware of that too.

Finally, we use local and global explanations because they answer different questions.

* global interpretation → what the model learned on average;
* local interpretation → why the model made a specific decision for one object.

Now, armed with this baggage, let’s see what the agents produce in each setup.

### **Analysis**

After running the scripts sequentially, we end up with 7 runs, and the `reports/` and `artifacts/` folders start filling up with outputs.
Before running the agent scripts, make sure to set the prefix for the experiment you want to analyze, and train the models first:

```bash
python 01_train_model.py
python 05_batch_exp.py
```
After that, the artifacts/ folder will contain:

* the trained model;
* train/test data;
* metadata;
* baseline performance metrics.

These artifacts are then passed to the agents as their working context.

### **Baseline**

Let’s look at the file produced by the naive agent on the `baseline` setup with the naive prompt: `reports/02_naive_agent_report_zero_shot_baseline.md`.
As we can see, the report does have sections. The structure declared by the agent is roughly:

```text
sanity checks → metrics → feature importance → SHAP
```
However, the agent broke on SHAP. For the sake of experimental cleanliness, we will not try to fix it here — but we should definitely note it.

So, the good news is that even without detailed instructions, the agent used the tools sequentially and produced a structured report — still embryonic, but a report nonetheless.

The bad news is that the quality remained fairly superficial. A broken SHAP section would not be acceptable in real life. There are two possible explanations here: either the agent’s capabilities were not enough, or the instructions were insufficient. Let’s try to fix the second part and give the agent more context.

### **Baseline + System Prompt**

The naive agent with a detailed system prompt is already noticeably better than the zero-shot version. It starts interpreting the results: connects feature importance with the clinical meaning of features, compares impurity-based importance and SHAP, discusses the generalization gap and limitations of the test set.

In my opinion, the agent does a great job with limitations: potential collinearity, single-model view, feature-importance bias — and, overall, points 1–6 are well justified.

However, there are still downsides. For example, in section 3, the global interpretation, the agent states:

These are known clinically to be strong discriminators between malignant and benign breast lesions.

This is generally reasonable and may even be true, but the agent slightly oversteps its mandate here. We did not ask it to play doctor. Let’s forgive it and move on to a more linear version, where the agent’s task is only summarization.

### **Baseline + System Prompt + Controlled Tool Calling**

Life has already taught us a few lessons, so let’s ask the agent for good sections right away:

1. Short summary — what kind of model this is and whether it can generally be trusted.
2. Performance — model quality: train/test metrics, generalization gap, classification errors.
3. Sanity checks — basic data checks.
4. Global interpretation — global model interpretation via feature importance: what the model learned “on average”.
5. SHAP interpretation — global and local SHAP explanations: which features contribute to predictions.
6. Local explanation — analysis of one specific object and the reasons behind its prediction.
7. Limitations — limitations of the interpretation and potential threats to validity.
8. What to check next — additional checks, experiments, or validation steps worth running later.

In this setup, one particularly interesting thing the agent produced was a disclaimer:

Prepared by the interpretability analysis agent, using only the supplied model diagnostics.

And honestly, this is great. Models often produce disclaimers, and sometimes those disclaimers are exactly what saves us from forgetting critical thinking.

The rest of this run is also good: the agent did not start hallucinating and separated performance, SHAP, local explanations, and limitations fairly carefully. Moreover, it again — unsurprisingly, since it is the same model — correctly raised issues like feature-importance bias, potential collinearity, calibration, and external validation.

At the same time — hooray, now we can nitpick. The agent recommends next steps, and some of them are genuinely useful: calibration and PDP/ICE plots are reasonable suggestions. But PCA is less obviously needed here: if the goal is interpretability, we could inspect correlations more directly and keep the original feature space readable. Will an external critic fix this?

### **Multi-Agent Pipeline + System Prompt**

Recall that instead of one agent that simultaneously analyzes the model, writes conclusions, and checks itself, we split the roles:

* the analyst-agent interprets the model;
* the critic-agent looks for weak spots;
* the reporter-agent assembles the final narrative.

From the report, it is clear that the critic strongly lowers the “seriousness” and confidence of the conclusions. In human terms, it behaves like the annoying skeptic in the room — which is exactly who you need when analyzing data and models.

The critic also sees all the issues mentioned earlier and expands on them extensively. This is both a strength and a weakness: the report becomes more careful, but also harder to read and easier to get lost in.

So, we saw that role separation does improve the interpretability pipeline. But at the same time, we also:

* increased complexity;
* increased latency;
* increased reasoning cost;
* and added quite a bit of water.


### **Let’s Inject an Obvious Bug: Batch Artifact**

To wrap things up, let’s move to our tricky scenario. In the real world, this artifact could be anything — from a hospital ID to a scanner type. By construction, we know that such features are dangerous: this is leakage-like behavior, and using it as a meaningful predictor is not okay.

Let’s see what the agents say.

After running the scripts, we again get three report files.

```
reports/02_naive_agent_report_batch_artifact.md
reports/03_manual_pipeline_report_batch_artifact.md
reports/04_multi_agent_report_batch_artifact.md
```
The result turned out to be surprisingly good: all three pipelines noticed the problem. Even the naive agent fairly quickly started suspecting that `collection_batch` does not look like a domain feature, but rather like a data collection artifact.

The main difference was not *whether* the issue was detected, but how the pipelines talked about it.

The manual pipeline stayed relatively dry and focused. The multi-agent pipeline, on the other hand, went full paranoia mode: it suggested group-aware validation, checking performance across batches, and treating the feature as a possible acquisition artifact. The reporter-agent later cleaned this up a bit, but still — we got a lot of extra text, plus even reproducibility code at the end.

So the good news is: the agents did catch the batch artifact.

The less good news is: the more complex the pipeline became, the more verbose the explanation became too.

### **Conclusions**

So, by this point we have seen several things in action.

First, even relatively simple agentic XAI pipelines are already capable of producing fairly reasonable interpretability reports. It is also worth remembering that all experiments above were run using the free `gpt-oss-120b` model through OpenRouter. In other words, we did not use a frontier model or some specialized research agent. A fairly standard open-weight LLM turned out to be capable of supporting a complete interpretability workflow for tabular ML.

Second, the orchestration layer affects interpretation quality no less than the XAI methods themselves.

* the naive agent turned out to be simple, functional, but rather overconfident;
* the manual pipeline was more sequential and grounded, but sacrificed some automation;
* the multi-agent pipeline became broader and more cautious, but also noticeably more verbose.

The critic-agent genuinely improved the reports: it raised issues like collinearity, calibration, leakage, and limits of interpretation much more frequently. But at the same time, it became clear how easily agents start overconstructing narratives, and that “more reasoning” does not always mean “better reasoning”. The batch artifact experiment demonstrated this nicely: all pipelines detected the problem, but the most complex pipeline was not necessarily the cleanest one.

#### **Limitations**

Earlier, we defined an agent as a system of four components. Naturally, changing any of them — partially or completely — affects the outcome of the experiment.

This means it is important to:

1. design tools for XAI systems carefully;
2. choose a strong backbone model;
3. structure system state thoughtfully;
4. guide the reasoning loop intentionally.

Overall, building an agent that explains a model is no longer particularly difficult. Building an agent that understands when its explanation should *not* be trusted is much harder.

And may no one ever ask us to explain *why* the agent decided to call a particular tool.

Thanks for reading and for your time!

More tutorials and experiments are published on the blog:  
[Telegram blog](https://t.me/jdata_blog)

and on GitHub:  
[GitHub repository](https://github.com/SadSabrina/XAI-open_materials/tree/main)

Good luck — and may your agents occasionally agree to work *for* you instead of against you.

— *Your Data Author*