# 🌟 Explainable AI (XAI) Tutorials Repository  

## **Goal**  

Hello, friends! Welcome to a repository dedicated to learning explainable artificial intelligence (XAI) methods.

This repository was created to make XAI methods accessible, understandable, and easy to use. Here, you will find practical guides to help you master key tools and approaches for applying XAI to large models. Each tutorial focuses on techniques for analyzing models to improve transparency in data processing and build trust in their decisions.

## **What’s Inside?**  

This repository offers tutorials in both Russian and English, designed to help you learn essential XAI tools.  

### Available Tutorials: 

- **LIME** [`LIME`] (Local Interpretable Model-Agnostic Explanations): explains local model behavior.  
- **YOLO** (You Only Look Once) [`yolo_nas_cam_tutorial`]: visualizes and interprets features within object detection models.  
- **GPT-2 probing** [`gpt2_probing`]: tutorial is about probing, a simple but powerful method for learning the inner workings of LLMs (Large Language Models) with GPT2 model.
- **CAM: [`CAM_yt`]**: tutorial about Class Activation Maps with YouTube [video](https://www.youtube.com/watch?v=6cOWGzv_ITQ)
- **Logit Lens Vit [`Logit Lens ViT`]:** [Logit Lens](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens) tutorial for vision model.
- **VIT and Autoencoders ['VIT_and_autoencoders']**: guide to applying AEs to hidden states (SAE coming soon).
- **Embedding geometry across architectures** [`architectures_embeddings`]: how attention masks shape representation geometry in encoder-only (BERT), decoder-only (GPT-2) and encoder-decoder (T5, BART) models — anisotropy, spectrum, intrinsic dimension, CKA — and what that means for pooling, cosine similarity and cross-model comparison. Runs on real corpora (UD English-EWT, AG News).
- **Anisotropy, PCA and false causality** [`pca_causality_pitfall`]: a post-mortem of a near-miss — how a descriptive PCA statistic almost became a "causal threshold". Covers why PC1 is a decoy under anisotropy, why perturbation size is the main confounder in `collapse`/`remove` interventions, why a replicated result can still be a method artifact, and a 7-point checklist to run before calling geometry causal. Fully synthetic, CPU-only, ground truth known by construction.
- **Latent vector fields and attractors** [`geometrical_structures`]: a walkthrough of *Navigating the Latent Space Dynamics of Neural Models* (Fumero et al., ICLR 2026) — reading an autoencoder as a dynamical system. Iterating `E ∘ D` induces a latent vector field whose attractors encode what the network learned. Covers flows vs cascades, Lipschitz/contraction conditions and where they fail on real data, basins of attraction and the thresholds that silently decide how many attractors you find, the memorisation–generalisation spectrum across bottleneck sizes, and OOD detection from trajectories. Honest partial replication: what reproduced, what did not, and why. MNIST/FashionMNIST, CPU-only.
- **RISE** [`RISE`]: perturbation-based interpretation — explaining a prediction by randomly masking the input thousands of times and weighting the masks by how much they hurt the score. Implemented from scratch.
- **LIME for time series** [`LIME_for_Time_Series`]: the same local-surrogate idea applied to ECG signals, where "a segment of the input" is a time window rather than a superpixel.
- **COLA: counterfactuals** [`COLA_contrfactuals`]: the `xai-cola` library — counterfactual explanations made sparse and actionable via joint-distribution-informed Shapley values.
- **CAM adaptation** [`cam_adaptation`]: a seminar on carrying localisation maps across architectures — CAM → Grad-CAM, from ResNet to a detector.
- **Gradient ascent** [`gradient_ascent`]: activation maximisation — synthesising the input a neuron likes most, from CNNs to CLIP.
- **Activation steering** [`steering`]: shifting LLM behaviour at inference time by adding a direction to the residual stream. Three implementations (raw hooks, `nnsight`, `pyvene`), an advanced part with `repeng` and `pyreft`, and a benchmark of the frameworks against each other.
- **SAE basics** [`SAE_basics`]: a hands-on introduction to sparse autoencoders over LLM activations with `SAELens`.
- **XAI for agents** [`agents`]: two projects — AgentSHAP, attributing an agent's answer to the tools it actually used (runs locally via Ollama, no paid API), and a comparison of naive tool-calling agents, deterministic pipelines and multi-agent systems with critique on tabular ML.

## **How to Start**  

1. **Clone the Repository**:  
   ```bash
   git clone https://github.com/SadSabrina/XAI-open_materials.git
   cd XAI-open_materials
   ```  
2. **Explore the Tutorials**: Check out the materials available in the following folders.

3. **Run the Examples**: Use Jupyter Notebook or your favorite IDE to test the examples and understand how they work.  

## **How to Contribute**  

1. **Create an Issue**: If you find a bug or want to suggest a new topic.  
2. **Contribute**: Submit a PR with your examples, improvements, or translations.  
3. **Spread the Word**: Share the repository link to help others learn about the importance of XAI.  

## 💡 **Contact & Feedback** 

If you have questions, suggestions, or want to discuss XAI, feel free to reach out:  
📧 Email: sad.sabrina.d@yandex.ru  
🔗 LinkedIn: [Sabrina Sadiekh](https://www.linkedin.com/in/sabrina-sadiekh-35181a286/)  
📢 Telegram Channel (Russian): [Just Data Blog](https://t.me/jdata_blog)  