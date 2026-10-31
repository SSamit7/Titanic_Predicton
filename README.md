# Titanic Survival Predictor

A cinematic Titanic-themed Django website 'titanic_model.pkl`.

## 1. Put your model in place

Copy `titanic_model.pkl` into the project root, beside `manage.py`.

The model must be a scikit-learn-compatible fitted pipeline and expect these columns:
`Pclass, Sex, Age, SibSp, Parch, Fare, Embarked`

The view sends a pandas DataFrame with those exact column names.

## 2. Install and run (Windows PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000/>

## 3. Notes

- The model is loaded once when Django starts.
- `predict()` determines the result. If `predict_proba()` exists, its positive-class probability is shown as a model score.
- A model score is not a guarantee or a real-world probability of survival.
- Pickle files can execute code when loaded. Only load a model file you created or trust.
- If your model uses different feature names or preprocessing, update `FEATURE_COLUMNS` and the form/view accordingly.
