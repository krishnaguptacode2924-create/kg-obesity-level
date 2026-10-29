# Obesity Level Predictor

A web app that predicts a person's obesity level from body measurements, eating habits and lifestyle. A Random Forest model sits behind a Flask API, and a single-page UI is served from the same app, so the whole project deploys as one service.

**Predicted categories:** Insufficient Weight, Normal Weight, Overweight Level I, Overweight Level II, Obesity Type I, Obesity Type II, Obesity Type III.

> This is a statistical estimate, not a medical diagnosis.

## Dataset

- Source 1: https://www.kaggle.com/datasets/tathagatbanerjee/obesity-dataset-uci-ml
- Source 2: https://www.kaggle.com/datasets/jayitabhattacharyya/estimation-of-obesity-levels-uci-dataset

## Model

Three Random Forest models were trained and compared. **Model 3 is the one used in the app.**


| Model | Features | Accuracy |
|---|---|---|
| Model 1 | All features | 95.5% |
| Model 2 | No Height/Weight | 86.6% |
| Model 3 | BMI instead of Height/Weight | **98.6%** |

- **Model 3 is best.** The classes are defined by BMI thresholds, so giving the model BMI directly hands it the answer. Model 1 has the same information but must approximate `Weight / Height²` with many splits on two separate columns, which costs about 3 points of accuracy.
- **Model 1** is strong for the same reason, just less efficient. Its weakest classes are the ones whose BMI boundaries sit close to a neighbouring class.
- **Model 2** reaches about 87% using only lifestyle and demographic features, with no body measurements. It mostly confuses neighbouring classes.

**Model 3 results (test set, 418 samples):** accuracy 0.986, macro F1 0.98, weighted F1 0.99.

**Features (15):** `Female`, `Age`, `BMI`, `Family_History`, `FAVC`, `FCVC`, `NCP`, `CAEC`, `SMOKE`, `CH2O`, `SCC`, `FAF`, `TUE`, `CALC`, `MTRANS`

The user enters Height and Weight, and the prediction module computes BMI as `Weight / Height²`.

## Inputs

| Field | Accepted values |
|---|---|
| Female | `Female`, `Male` |
| Age | 14 to 100 (years) |
| Height | 1.0 to 2.5 (metres) |
| Weight | 30 to 300 (kg) |
| Family_History, FAVC, SMOKE, SCC | `Yes`, `No` |
| FCVC (vegetables) | 1 Never, 2 Sometimes, 3 Always |
| NCP (main meals) | 1 to 4 |
| CAEC (snacking) | `no`, `Sometimes`, `Frequently`, `Always` |
| CH2O (water) | 1 under 1 L, 2 1 to 2 L, 3 over 2 L |
| FAF (activity) | 0 none, 1 1 to 2 days, 2 2 to 4 days, 3 4 to 5 days |
| TUE (devices) | 0 0 to 2 h, 1 3 to 5 h, 2 over 5 h |
| CALC (alcohol) | `no`, `Sometimes`, `Frequently`, `Always` |
| MTRANS | `Car`, `Cycle`, `Motorbike`, `Public`, `Walking` |

## Project structure

```
KG_Obesity/
├── app.py                     Flask API, also serves the UI
├── index.html                 UI (CSS and JS inline)
├── KG_Obesity_Prediction.py   Prediction module
├── KG_Obesity_Artifact/       Trained model and encoders (.joblib)
├── requirements.txt
├── render.yaml                Render deployment config
└── README.md
```

All paths are relative, so the project runs the same locally and on Render.


## Tech stack

Python, scikit-learn, pandas, joblib, Flask, gunicorn, HTML/CSS/JavaScript, Render
