# XAI

**Library and method table**

| Library | LIME | pdp plots | shap values | permutation importance | Sensitivity Analysis | Counterfactual Explanations | integrated gradients | 	Layer-wise Relevance Propagation | Scalable Bayesian Rule Lists | other methods |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| eli5 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0| 0 | 0 |
| pdpbox | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0| 0 | 0 |
| shap | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0| 0 | 0 |
| deeplift | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0| 0 | 1 |
| SALib | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0| 0 | 0 |
| LIME | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0| 0 | 0 |
| interpretML | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 0| 0 | 0 |
| dice-ml | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0| 0 | 0 |
| interpret-text | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0| 0 | 0 |
| treeinterpreter | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0| 0 | 0 |
| graphviz | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0| 0 | 1 |
| captum | 1 | 0 | 1 | 0 | 0 | 0 | 1 | 1| 0 | 1 |
| skater | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 1| 0 | 0 |
| transformers-interpret | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| bertviz | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| alibi | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 0| 0 | 0 |

If everything is 0 in the line, it means that no explicit name of the method used has been found

**Library and data table**


| Библиотека | Тексты	| Изображения |	Звук	| Табличные данные	| Графовые данные	| Генетические данные |
| --- | --- | --- | --- | --- | --- | --- |
| eli5	| 1	| 1	| 0	| 1	| 1	| 0 |
| pdpbox	| 0	| 0	| 0	| 0	| 0	| 0 |
| shap	| 1	| 1	| 0	| 1	| 0	| 0 |
| deeplift	| 1	| 1	| 0	| 0	| 0	| 1 |
| LIME	| 1	| 1	| 0	| 1	| 0	| 0 |
| SALib |	0	|	0	| 0| 1| 0 | 0 |
| librosa	| 0	| 0	| 1	| 0	| 0	| 0 |
| interpretML	| 1	| 1	| 1	| 1	| 0	| 0 |
| dice-ml 	| 0	| 0	| 0	| 1	| 0	| 0 |
| interpret-text	| 1	| 0	| 0	| 0	| 0	| 0 |
| treeinterpreter	| 0	| 0	| 0	| 1	| 0	| 0 |
| captum | 1 | 1 | 0 | 1 | 0 | 0 |
| skater	| 1	| 1	| 0	| 1	| 0	| 0 |
| transformers-interpret | 1	| 1	| 0	| 0	| 0	| 0 |
| bertviz	| 1	| 0	| 0	| 0	| 0	| 0 |
| GNNExplainer |0	| 0	| 0	| 0	| 1	| 0 |
| alibi	| 1	| 1	| 0	| 1	| 0	| 0 |
| PGExplainer	| 0	| 0	| 0	| 0	| 1	| 0 | 
