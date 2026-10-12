# ML Methodology and Evaluation

## Objective and Target

The task is binary classification: estimate whether an order will be delivered late.

The target variable, `is_late`, is derived by comparing the actual delivery timestamp with the estimated delivery timestamp. The precise target-generation rule and handling of missing timestamps are defined by the feature-engineering code.

A predicted probability is a risk estimate, not a guarantee.

## Feature Groups

The current model input schema includes:

- Customer and seller state.
- Number of items, products, and sellers.
- Total price, freight, payment value, product weight, and product volume.
- Product category and payment type.
- Number of payments and maximum payment installments.
- Purchase hour, day of the week, month, and year.
- Order approval delay and estimated delivery days.

The feature pipeline and training code are the definitive specifications for the model inputs. The target variable must never be passed as an inference feature.

## Training Approach

The project uses a fitted preprocessing pipeline and an XGBoost classifier, with hyperparameter tuning through `RandomizedSearchCV`.

The training workflow includes preprocessing, train/test splitting, model selection, hyperparameter tuning, and evaluation.

**Data validation was skipped in the current implementation.** A separate automated data-validation stage is not claimed as completed.

For reproducibility, the training configuration should record:

- Train/test split and random seed.
- Stratification and cross-validation strategy.
- Hyperparameter search space and number of trials.
- Scoring metric.
- Selected hyperparameters and classification threshold.
- Dependency versions and model artifact version.

Preprocessing should be fitted on training data only. The saved fitted pipeline should be reused during inference to keep transformations consistent.

## Reported Evaluation

The following metrics were recorded from the reported held-out evaluation run.

| Metric | Score |
|---|---:|
| Accuracy | 0.8072458 |
| Precision | 0.2298043 |
| Recall | 0.5853035 |
| F1-score | 0.3300306 |
| F2-score | 0.4470037 |
| ROC-AUC | 0.7856269 |

Confirm that these values correspond to the final saved pipeline and held-out test set before presenting them as final results.

### Interpretation

- **Accuracy (~80.7%):** Measures overall correctness but can be misleading when classes are imbalanced.
- **Precision (~23.0%):** Around 23% of orders predicted as late were actually late in the evaluated sample, assuming class 1 is the positive class.
- **Recall (~58.5%):** The model identified around 58.5% of actual late-delivery cases in the evaluated sample.
- **F1-score (~0.330):** Balances precision and recall.
- **F2-score (~0.447):** Gives more weight to recall than precision.
- **ROC-AUC (~0.786):** Measures the model's ability to rank positive cases above negative cases across thresholds. It does not guarantee that predicted probabilities are well calibrated.

The operating threshold should reflect the relative costs of false positives and false negatives. A false positive can trigger an unnecessary intervention, while a false negative can leave a genuinely late order unflagged.

## SHAP Explanations

The explanation service reuses the fitted pipeline's `preprocessor` and `best_model` steps, transforms a representative background sample, and uses `TreeExplainer` configured for probability output and interventional feature perturbation.

- Positive SHAP values push the model's late-delivery probability upward relative to the baseline.
- Negative SHAP values push it downward.
- The baseline plus all SHAP contributions should approximately reconstruct the model's predicted probability when the explainer is configured and evaluated consistently.
- The API returns only the top-ranked contributions. These values alone will not generally sum to the final probability because other contributions are omitted.
- One-hot-encoded feature names may be less readable than the original business features.

SHAP is a model-attribution technique, not proof of causation. Feature correlations and the choice of background sample can affect the explanations.

## Limitations and Next Experiments

- Precision is relatively low at the reported operating point.
- Historical patterns may not represent current logistics behavior.
- Unseen categories or changes in the data distribution can affect predictions.
- LLM explanations add latency and may vary; they should be grounded in the actual prediction and SHAP output.
- Consider evaluating PR-AUC, inspecting the confusion matrix, selecting a threshold based on business costs, checking probability calibration, and reviewing false positives and false negatives.
- Consider grouping one-hot SHAP contributions into original business fields.
- Add automated data validation and data-quality checks as a future improvement.
- Consider monitoring data drift after deployment.
