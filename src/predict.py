
from pathlib import Path
import gzip
import joblib
import pandas as pd


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "turbidity_model.pkl.gz"


# ============================================================
# MODEL FEATURES
# ============================================================

FEATURES = [
    "Conductivity",
    "Dissolved Oxygen",
    "pH",
    "WaterTemp",
    "NO3",
]


# ============================================================
# LOAD COMPRESSED MODEL
# ============================================================

def load_model():
    """
    Load the trained scikit-learn model from
    the compressed .pkl.gz file.
    """

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    with gzip.open(MODEL_PATH, "rb") as model_file:
        model = joblib.load(model_file)

    return model


# ============================================================
# PREDICT TURBIDITY
# ============================================================

def predict_turbidity(data):
    """
    Predict turbidity using the trained model.

    Parameters
    ----------
    data : dict or pandas.DataFrame
        Input sensor/feature values.

    Returns
    -------
    float
        Predicted turbidity value.
    """

    model = load_model()

    # --------------------------------------------------------
    # Convert dictionary input to DataFrame
    # --------------------------------------------------------

    if isinstance(data, dict):
        data = pd.DataFrame([data])

    elif not isinstance(data, pd.DataFrame):
        raise TypeError(
            "Input must be a dictionary or pandas DataFrame."
        )

    # --------------------------------------------------------
    # Validate required features
    # --------------------------------------------------------

    missing_features = [
        feature
        for feature in FEATURES
        if feature not in data.columns
    ]

    if missing_features:
        raise ValueError(
            "Missing required features: "
            + ", ".join(missing_features)
        )

    # --------------------------------------------------------
    # Select features in correct order
    # --------------------------------------------------------

    X = data[FEATURES]

    # --------------------------------------------------------
    # Generate prediction
    # --------------------------------------------------------

    prediction = model.predict(X)

    return float(prediction[0])


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_data = {
        "Conductivity": 250.0,
        "Dissolved Oxygen": 7.5,
        "pH": 7.2,
        "WaterTemp": 24.0,
        "NO3": 2.0,
    }

    prediction = predict_turbidity(test_data)

    print("=" * 60)
    print("TURBIDITY PREDICTION TEST")
    print("=" * 60)
    print(f"Predicted Turbidity: {prediction:.4f} NTU")

