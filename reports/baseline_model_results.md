# Baseline model results

## Setup

- Responses retained: 139.
- Outcome: exploratory total across five symptom-frequency items, scored 0 to 15.
- Inputs: age group, screen-time category, sleep category, break frequency, primary device, and vision correction.
- Validation: five-fold group cross-validation. Identical input-and-outcome rows were assigned to the same group.
- Duplicate-like responses were retained, as requested.

## Cross-validation results

Metrics are fold means ± standard deviations from the run completed in the project environment.

| Model | MAE, score points | RMSE, score points | R² |
|---|---:|---:|---:|
| Mean baseline | 2.63 ± 0.27 | 3.18 ± 0.31 | -0.03 ± 0.03 |
| Ridge regression | 2.40 ± 0.32 | 2.88 ± 0.34 | 0.15 ± 0.13 |
| Random Forest | 2.47 ± 0.33 | 2.96 ± 0.31 | 0.11 ± 0.12 |

## Interpretation

Ridge regression had the lowest average MAE and RMSE. Its MAE was 0.23 score points lower than the mean-only baseline. This is a modest improvement, and the fold-to-fold variation is substantial relative to the difference between Ridge and Random Forest. Keep Ridge as the current candidate for further exploration, not as a validated screening model.

## Ridge permutation importance

Importance is the increase in held-out MAE after shuffling one input. Higher positive values mean that the fitted Ridge model relied more on that feature in these folds.

| Input | Mean MAE increase | SD across folds | Folds with positive importance |
|---|---:|---:|---:|
| Sleep category | 0.086 | 0.146 | 3/5 |
| Vision correction | 0.077 | 0.097 | 4/5 |
| Screen-time category | 0.041 | 0.020 | 5/5 |
| Primary device | 0.032 | 0.019 | 5/5 |
| Age group | 0.018 | 0.059 | 3/5 |
| Breaks per hour category | 0.015 | 0.038 | 3/5 |

Sleep category had the largest average importance, but its fold-to-fold variation was larger than its mean. Primary device had a small positive value in every fold. These results do not identify a stable individual risk factor. Treat the ranking as exploratory model reliance, not as a causal or medical explanation.

These values come from the current training script, which uses the same clipped predictions for permutation scoring as it uses for the reported error metrics.

The outcome is a project-created score, not a validated clinical measure. Results describe associations in this small, mostly 19–24-year-old sample. They do not establish that screen habits cause symptoms or support medical risk claims.

The training script also reports held-out-fold permutation importance for Ridge. Interpret it as how much this fitted model relies on a feature, not as a causal effect.
