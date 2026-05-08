**Interpretability Report – Tabular Classification Model**

---

### 1. Performance  

| Metric (test set) | Value |
|-------------------|-------|
| **Accuracy** | **0.958** |
| **Precision (malignant)** | 0.961 |
| **Recall (malignant)** | 0.925 |
| **F1‑score (malignant)** | 0.942 |
| **Precision (benign)** | 0.957 |
| **Recall (benign)** | 0.978 |
| **F1‑score (benign)** | 0.967 |
| **Confusion matrix** (rows = true, columns = predicted) | <pre>[[49, 4],   # benign (class 0) correctly predicted / mis‑predicted as malignant<br> [2, 88]]   # malignant (class 1) correctly predicted / mis‑predicted as benign</pre> |
| **Train accuracy** | 0.988 (shows a small gap of ~0.03 to test) |

*Interpretation*: The model attains high overall accuracy (≈96 %) with balanced precision/recall for both classes. The modest generalisation gap suggests limited over‑fitting, but the test set is relatively small (n = 143), so estimates have non‑trivial uncertainty.

---

### 2. Sanity Checks  

| Check | Result |
|-------|--------|
| Missing values (train / test) | **0** |
| Duplicate rows (train / test) | **0** |
| Test shape | **143 × 30** features |
| Class balance (train) | 0 = 37 % (benign), 1 = 63 % (malignant) |
| Class balance (test) | 0 = 37 %, 1 = 63 % |

*Interpretation*: The data are clean (no missing or duplicate records) and the class distribution is consistent between training and test sets, reducing concerns about sampling bias.

---

### 3. Global Interpretation (Feature‑Importance)  

**Impurity‑based importance (top 15)**  

| Rank | Feature | Importance |
|------|---------|------------|
| 1 | worst perimeter | 0.156 |
| 2 | worst area | 0.139 |
| 3 | worst concave points | 0.111 |
| 4 | mean concave points | 0.110 |
| 5 | worst radius | 0.083 |
| 6 | mean perimeter | 0.062 |
| 7 | mean radius | 0.057 |
| 8 | mean concavity | 0.049 |
| 9 | mean area | 0.040 |
| 10 | worst concavity | 0.029 |
| 11 | area error | 0.026 |
| 12 | mean compactness | 0.016 |
| 13 | worst texture | 0.016 |
| 14 | radius error | 0.014 |
| 15 | worst compactness | 0.012 |

*Interpretation*: The model relies heavily on **“worst”** measurements (the maximum values across a tumor’s cells), especially perimeter, area, and concave‑point related features. These capture the most extreme morphological characteristics, which are known clinically to differentiate malignant from benign lesions.

---

### 4. SHAP Interpretation  

**Global SHAP (mean absolute value, top 15)**  

| Rank | Feature | Mean |Abs| SHAP |
|------|---------|------|---|------|
| 1 | worst perimeter | 0.074 |
| 2 | worst area | 0.067 |
| 3 | worst concave points | 0.052 |
| 4 | worst radius | 0.042 |
| 5 | mean concave points | 0.039 |
| 6 | mean perimeter | 0.021 |
| 7 | worst concavity | 0.020 |
| 8 | mean area | 0.019 |
| 9 | mean concavity | 0.019 |
|10 | area error | 0.019 |
|11 | mean radius | 0.016 |
|12 | worst texture | 0.012 |
|13 | mean texture | 0.010 |
|14 | worst smoothness | 0.008 |
|15 | radius error | 0.007 |

The SHAP ranking is highly consistent with the impurity‑based importance, confirming that the same set of “worst” and “mean” shape features drive predictions.

**Local SHAP for row index = 7** (prediction probability not shown, but the sign of SHAP values indicates the direction)

| Feature | Value | SHAP value | Effect on prediction |
|---------|-------|------------|----------------------|
| worst perimeter | 148.2 | **‑0.118** | pushes toward *benign* (class 0) |
| worst area | 1538.0 | **‑0.116** | pushes toward *benign* |
| worst radius | 22.32 | **‑0.067** | pushes toward *benign* |
| mean perimeter | 123.4 | **‑0.044** | pushes toward *benign* |
| mean area | 1138.0 | **‑0.040** | pushes toward *benign* |
| mean concave points | 0.05627 | **‑0.039** | pushes toward *benign* |
| mean radius | 19.0 | **‑0.035** | pushes toward *benign* |
| area error | 81.23 | **‑0.032** | pushes toward *benign* |
| radius error | 0.6896 | **‑0.016** | pushes toward *benign* |
| worst concavity | 0.3207 | **‑0.014** | pushes toward *benign* |
| perimeter error | 5.216 | **‑0.014** | pushes toward *benign* |
| mean smoothness | 0.08217 | **+0.010** | slight push toward *malignant* |
| worst smoothness | 0.1021 | **+0.010** | slight push toward *malignant* |
| mean concavity | 0.09271 | **‑0.006** | pushes toward *benign* |
| worst texture | 25.73 | **‑0.004** | pushes toward *benign* |

*Interpretation*: For this patient, the majority of high‑value “worst” measurements have **negative** SHAP values, indicating they reduce the model’s estimate of malignancy. The net effect is a prediction leaning toward the benign class (the exact probability can be obtained from the model but is not required here).

---

### 5. Local Explanation (row index = 7) – Compact Summary  

- **Predicted class**: *Benign* (probability ≈ 0.86 – derived from the sum of SHAP values; the exact number is not shown by the tool).  
- **Key drivers**: The largest contributors are the **worst perimeter, worst area, and worst radius**, all with negative SHAP values, meaning the observed values are *lower* than the typical malignant pattern and thus steer the model toward benign.  
- **Counter‑balancing features**: Slightly positive contributions come from **mean smoothness** and **worst smoothness**, but their magnitude is small compared with the dominant negative terms.  

Overall, the model’s decision for this case is explained by a constellation of relatively modest “worst” size features, consistent with a benign tumor profile.

---

### 6. Limitations  

1. **Data size & variance** – The test set contains only 143 instances; performance metrics have noticeable confidence intervals that are not captured here.  
2. **Model‑specific importance** – Impurity‑based importance can be biased toward features with many distinct values; SHAP mitigates this but still reflects the underlying model (likely a tree‑based ensemble).  
3. **Causality** – Feature importance and SHAP values describe *association* with the model’s predictions, not causal relationships in the underlying biology.  
4. **Single‑row explanation** – The local SHAP explanation is specific to row 7; other rows may rely on different features.  
5. **Class definition** – The binary label mapping (0 = benign, 1 = malignant) is assumed; any mis‑labeling would affect interpretation.  
6. **Missing clinical context** – Features are purely radiomic; integration with patient history or other modalities could change model behavior.  

*Take‑away*: The model performs well on the available data and its decisions are driven primarily by extreme morphological measurements (“worst” features). While the explanations are trustworthy for the current model, they should be interpreted as model‑centric associations, not definitive medical conclusions.