**Interpretability Report – Tabular Classification Model**  

---

### 1. Performance  

| Metric (test set) | Value |
|-------------------|-------|
| **Accuracy** | **0.965** (96.5 %) |
| **Precision (malignant)** | 0.962 |
| **Recall (malignant)** | 0.943 |
| **F1‑score (malignant)** | 0.952 |
| **Precision (benign)** | 0.967 |
| **Recall (benign)** | 0.978 |
| **F1‑score (benign)** | 0.972 |
| **Confusion matrix** (rows = true, columns = predicted) | <pre>[[50, 3],   # true benign → 50 correct, 3 mis‑classified as malignant<br> [ 2, 88]]  # true malignant → 2 mis‑classified as benign, 88 correct</pre> |
| **Test set size** | 143 samples (33 features) |
| **Training accuracy** | 1.00 (perfect) |

*Interpretation*: The model attains very high discrimination on the held‑out test data, with only 5 errors (3 false positives, 2 false negatives). The balanced precision/recall for both classes suggests it is not heavily biased toward one class.

---

### 2. Sanity Checks  

| Check | Result |
|-------|--------|
| Missing values (train / test) | 0 / 0 |
| Duplicate rows (train / test) | 0 / 0 |
| Test shape | (143 rows × 33 columns) |
| Class balance (train) | 0 ≈ 37 % class 0, 63 % class 1 |
| Class balance (test) | 0 ≈ 37 % class 0, 63 % class 1 |

*Interpretation*: The data are clean (no missing or duplicate records) and the class distribution is consistent between training and test sets, reducing concerns about sampling bias.

---

### 3. Global Interpretation (Feature‑Importance from the model)  

The top 15 impurity‑based importance scores (higher = more influence on splits):

| Rank | Feature | Importance |
|------|---------|------------|
| 1 | **worst radius** | 0.130 |
| 2 | **worst concave points** | 0.107 |
| 3 | **worst perimeter** | 0.099 |
| 4 | **mean concave points** | 0.094 |
| 5 | **worst area** | 0.088 |
| 6 | **mean perimeter** | 0.063 |
| 7 | **mean radius** | 0.052 |
| 8 | **mean concavity** | 0.045 |
| 9 | **mean area** | 0.045 |
|10 | **worst concavity** | 0.036 |
|11 | **batch_batch_C** (categorical batch indicator) | 0.035 |
|12 | **area error** | 0.035 |
|13 | **batch_batch_A** | 0.024 |
|14 | **worst compactness** | 0.017 |
|15 | **worst texture** | 0.015 |

*Interpretation*: The model relies heavily on the “worst” (i.e., largest) measurements of tumor geometry (radius, perimeter, area, concave points) and several “mean” shape descriptors. Batch‑related variables also appear, indicating some systematic variation across data collection batches.

---

### 4. SHAP Interpretation (Global & Local)  

**Global SHAP (mean absolute SHAP values)** – the ranking is very similar to impurity importance, confirming that the same features drive predictions:

| Rank | Feature | Mean | |SHAP| |
|------|---------|-----------|
| 1 | worst radius | 0.0528 |
| 2 | worst area | 0.0500 |
| 3 | worst concave points | 0.0479 |
| 4 | worst perimeter | 0.0454 |
| 5 | mean concave points | 0.0359 |
| … | … | … |

Thus, the model’s decisions are consistently explained by the “worst” tumor measurements, with batch indicators and area error also contributing.

**Local SHAP for row index = 7** (prediction probability not shown by the tool, but SHAP values indicate direction):

| Feature | Value (row 7) | SHAP value | Effect on prediction |
|---------|---------------|------------|----------------------|
| worst radius | 22.32 | **‑0.099** | pushes toward the *benign* class |
| worst area | 1538 | **‑0.085** | pushes toward benign |
| worst perimeter | 148.2 | **‑0.070** | pushes toward benign |
| mean area | 1138 | **‑0.046** | pushes toward benign |
| mean radius | 19.0 | **‑0.038** | pushes toward benign |
| mean perimeter | 123.4 | **‑0.038** | pushes toward benign |
| area error | 81.23 | **‑0.036** | pushes toward benign |
| mean concave points | 0.05627 | **‑0.030** | pushes toward benign |
| batch_batch_A | 0 | **‑0.024** | pushes toward benign |
| worst concavity | 0.3207 | **‑0.020** | pushes toward benign |
| batch_batch_C | 0 | **+0.019** | slight push toward malignant |
| radius error | 0.6896 | **‑0.012** | pushes toward benign |
| perimeter error | 5.216 | **‑0.012** | pushes toward benign |
| mean smoothness | 0.08217 | **+0.011** | slight push toward malignant |
| worst smoothness | 0.1021 | **+0.007** | slight push toward malignant |

*Overall direction*: The majority of the top‑ranking features have **negative** SHAP values, indicating that for this patient the model leans toward the **benign** class. The net sum of SHAP values (not provided) would be needed to compute the exact predicted probability, but the pattern is clear.

---

### 5. Local Explanation (row index = 7) – compact view  

| Feature | Value | Contribution (SHAP) |
|---------|-------|---------------------|
| worst radius | 22.32 | –0.099 |
| worst area | 1538 | –0.085 |
| worst perimeter | 148.2 | –0.070 |
| mean area | 1138 | –0.046 |
| mean radius | 19.0 | –0.038 |
| mean perimeter | 123.4 | –0.038 |
| area error | 81.23 | –0.036 |
| mean concave points | 0.0563 | –0.030 |
| batch_batch_A | 0 | –0.024 |
| worst concavity | 0.321 | –0.020 |
| batch_batch_C | 0 | +0.019 |
| radius error | 0.690 | –0.012 |
| perimeter error | 5.22 | –0.012 |
| mean smoothness | 0.0822 | +0.011 |
| worst smoothness | 0.102 | +0.007 |

**Narrative**: The patient’s tumor exhibits relatively *smaller* “worst” measurements (radius, area, perimeter) compared with typical malignant cases, and these measurements dominate the explanation, pulling the prediction toward benign. Minor positive contributions from batch C and smoothness features are insufficient to overturn the overall benign tendency.

---

### 6. Limitations  

| Aspect | Why it matters |
|--------|----------------|
| **Training‑test gap** | Training accuracy is 100 % while test accuracy is 96.5 %; the gap suggests possible over‑fitting, especially given the small test set (143 rows). |
| **Single‑run metrics** | Only one split is reported; performance may vary with different random seeds or cross‑validation folds. |
| **Feature‑importance method** | Impurity‑based importance can be biased toward features with many distinct values; SHAP values mitigate this but are still model‑specific. |
| **Batch effects** | Batch indicators appear among top features, hinting that systematic differences between data collection batches influence predictions. If batches correlate with outcome, the model may be learning artefacts rather than true pathology. |
| **Interpretability scope** | SHAP explanations are local approximations; they do not prove causal relationships, only association with the model’s decision surface. |
| **Missing clinical context** | The model uses only numeric tumor descriptors; no patient‑level covariates (age, genetics, etc.) are considered, limiting real‑world applicability. |
| **Binary‑class SHAP note** | SHAP values are reported for class 1 (malignant). Negative values therefore indicate a push toward the opposite class (benign). |

**Bottom line**: The model shows strong predictive performance and its decisions are driven primarily by the “worst” geometric tumor features, consistent with medical intuition that larger, more irregular tumors are more likely malignant. However, the perfect training score, presence of batch‑related importance, and reliance on a single train‑test split caution against assuming the model will generalize flawlessly to new hospitals or populations without further validation.