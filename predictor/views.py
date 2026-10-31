import json
from pathlib import Path

import joblib
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "titanic_model.pkl"
FEATURE_COLUMNS = ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"]

_model = None

def get_model():
    global _model
    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                "titanic_model.pkl was not found. Place it beside manage.py."
            )
        # Only load pickle/joblib files that you created or trust.
        _model = joblib.load(MODEL_PATH)
    return _model

def home(request):
    return render(request, "predictor/home.html")

@require_POST
def predict(request):
    try:
        data = json.loads(request.body or "{}")

        passenger = {
            "Pclass": int(data["Pclass"]),
            "Sex": str(data["Sex"]).lower(),
            "Age": float(data["Age"]),
            "SibSp": int(data["SibSp"]),
            "Parch": int(data["Parch"]),
            "Fare": float(data["Fare"]),
            "Embarked": str(data["Embarked"]).upper(),
        }

        if passenger["Pclass"] not in (1, 2, 3):
            return JsonResponse({"error": "Choose a valid passenger class."}, status=400)
        if passenger["Sex"] not in ("male", "female"):
            return JsonResponse({"error": "Choose a valid sex value."}, status=400)
        if passenger["Embarked"] not in ("C", "Q", "S"):
            return JsonResponse({"error": "Choose a valid embarkation port."}, status=400)
        if not (0 <= passenger["Age"] <= 100 and 0 <= passenger["Fare"] <= 1000):
            return JsonResponse({"error": "Age or fare is outside the supported range."}, status=400)
        if not (0 <= passenger["SibSp"] <= 10 and 0 <= passenger["Parch"] <= 10):
            return JsonResponse({"error": "Family counts must be between 0 and 10."}, status=400)

        frame = pd.DataFrame([passenger], columns=FEATURE_COLUMNS)
        model = get_model()
        prediction = int(model.predict(frame)[0])

        score = None
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(frame)[0]
            classes = list(getattr(model, "classes_", []))
            if 1 in classes:
                score = round(float(probabilities[classes.index(1)]) * 100, 1)

        return JsonResponse({
            "survived": prediction == 1,
            "score": score,
            "message": (
                "The model predicts this passenger would survive."
                if prediction == 1
                else "The model predicts this passenger would not survive."
            ),
        })
    except FileNotFoundError as exc:
        return JsonResponse({"error": str(exc)}, status=503)
    except (KeyError, ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse({"error": "Please check all passenger details and try again."}, status=400)
    except Exception:
        return JsonResponse(
            {"error": "The model could not process these details. Check that its expected features match the website."},
            status=500,
        )
