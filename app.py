import os
from flask import Flask, jsonify, request, send_from_directory

# Everything lives in this folder. Make it the working directory so the
# relative "KG_Obesity_Artifact/..." paths inside KG_Obesity_Prediction.py
# resolve correctly no matter where the server is started from.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

from KG_Obesity_Prediction import KG_Obesity_Predict  # original module, untouched

app = Flask(__name__)

YES_NO = {"Yes", "No"}
CHOICES = {
    "Female": {"Female", "Male"},
    "Family_History": YES_NO,
    "FAVC": YES_NO,
    "SMOKE": YES_NO,
    "SCC": YES_NO,
    "CAEC": {"no", "Sometimes", "Frequently", "Always"},
    "CALC": {"no", "Sometimes", "Frequently", "Always"},
    "MTRANS": {"Car", "Cycle", "Motorbike", "Public", "Walking"},
}
# field: (min, max, must_be_whole_number)
NUMBERS = {
    "Age": (14, 100, False),
    "Height": (1.0, 2.5, False),
    "Weight": (30, 300, False),
    "FCVC": (1, 3, True),
    "NCP": (1, 4, True),
    "CH2O": (1, 3, True),
    "FAF": (0, 3, True),
    "TUE": (0, 2, True),
}


def validate(data):
    """Return (clean_dict, error_message)."""
    if not isinstance(data, dict):
        return None, "Send the form data as JSON."
    clean = {}
    for field, allowed in CHOICES.items():
        value = data.get(field)
        if value not in allowed:
            return None, f"Choose a valid option for {field}."
        clean[field] = value
    for field, (low, high, whole) in NUMBERS.items():
        try:
            number = float(data.get(field))
        except (TypeError, ValueError):
            return None, f"Enter a number for {field}."
        if not low <= number <= high:
            return None, f"{field} must be between {low} and {high}."
        clean[field] = int(number) if whole else number
    return clean, None


@app.get("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.post("/predict")
def predict():
    clean, error = validate(request.get_json(silent=True))
    if error:
        return jsonify(error=error), 400
    try:
        return jsonify(KG_Obesity_Predict(clean))
    except Exception as exc:  # keep the server alive, show a readable message
        app.logger.exception("Prediction failed")
        return jsonify(error="Prediction failed on the server.", detail=str(exc)), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
