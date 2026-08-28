
from pathlib import Path
import gzip
import joblib
import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "turbidity_model.pkl.gz"
DATA_PATH = BASE_DIR / "data" / "river_features.csv"


# ============================================================
# LOAD SAVED MODEL PACKAGE
# ============================================================

def load_model_info():

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    with gzip.open(MODEL_PATH, "rb") as model_file:
        model_data = joblib.load(model_file)

    if not isinstance(model_data, dict):
        raise ValueError(
            "Unexpected model file format."
        )

    if "model" not in model_data:
        raise KeyError(
            "Saved model does not contain 'model'."
        )

    if "features" not in model_data:
        raise KeyError(
            "Saved model does not contain 'features'."
        )

    return model_data


# ============================================================
# LOAD ACTUAL ML MODEL
# ============================================================

def load_model():

    model_data = load_model_info()

    return model_data["model"]


# ============================================================
# PREDICT TURBIDITY FROM SUPPLIED DATA
# ============================================================

def predict_turbidity(data):

    model_data = load_model_info()

    model = model_data["model"]
    features = model_data["features"]

    if isinstance(data, dict):

        data = pd.DataFrame([data])

    elif not isinstance(data, pd.DataFrame):

        raise TypeError(
            "Input must be a dictionary or pandas DataFrame."
        )

    missing_features = [
        feature
        for feature in features
        if feature not in data.columns
    ]

    if missing_features:

        raise ValueError(
            "Missing required features: "
            + ", ".join(missing_features)
        )

    X = data[features]

    prediction = model.predict(X)

    return float(prediction[0])


# ============================================================
# PREDICT LATEST TURBIDITY
# ============================================================

def predict_latest():

    # --------------------------------------------------------
    # Check dataset
    # --------------------------------------------------------

    if not DATA_PATH.exists():

        raise FileNotFoundError(
            f"Feature dataset not found: {DATA_PATH}"
        )

    data = pd.read_csv(DATA_PATH)

    if data.empty:

        raise ValueError(
            "Feature dataset is empty."
        )

    # --------------------------------------------------------
    # Load model and stored features
    # --------------------------------------------------------

    model_data = load_model_info()

    model = model_data["model"]
    features = model_data["features"]

    # --------------------------------------------------------
    # Verify required columns
    # --------------------------------------------------------

    missing_features = [
        feature
        for feature in features
        if feature not in data.columns
    ]

    if missing_features:

        raise ValueError(
            "Feature dataset is missing required columns: "
            + ", ".join(missing_features)
        )

    # --------------------------------------------------------
    # Use latest available row
    # --------------------------------------------------------

    latest_row = data.iloc[[-1]]

    X = latest_row[features]

    # --------------------------------------------------------
    # Generate prediction
    # --------------------------------------------------------

    prediction = model.predict(X)

    predicted_turbidity = float(prediction[0])

    # --------------------------------------------------------
    # Get current turbidity
    # --------------------------------------------------------

    if "Turbidity" in latest_row.columns:

        current_turbidity = float(
            latest_row["Turbidity"].iloc[0]
        )

    elif "turbidity" in latest_row.columns:

        current_turbidity = float(
            latest_row["turbidity"].iloc[0]
        )

    else:

        raise KeyError(
            "The dataset does not contain a Turbidity column."
        )

    # --------------------------------------------------------
    # Get timestamp
    # --------------------------------------------------------

    timestamp_column = None

    for column in data.columns:

        if column.lower() == "timestamp":

            timestamp_column = column
            break

    if timestamp_column is None:

        raise KeyError(
            "The dataset does not contain a Timestamp column."
        )

    timestamp = latest_row[
        timestamp_column
    ].iloc[0]

    # --------------------------------------------------------
    # IMPORTANT:
    # Return the structure expected by advisor.py
    # --------------------------------------------------------

    return {

        "timestamp": timestamp,

        "current_turbidity": current_turbidity,

        "predicted_turbidity": predicted_turbidity

    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("TURBIDITY MODEL TEST")
    print("=" * 60)

    model_data = load_model_info()

    print("Model loaded successfully.")

    print(
        "Stored features:",
        model_data["features"]
    )

    print(
        "Target:",
        model_data["target"]
    )

    result = predict_latest()

    print("\n========== LATEST PREDICTION ==========")

    print(
        "Timestamp:",
        result["timestamp"]
    )

    print(
        "Current Turbidity:",
        result["current_turbidity"],
        "NTU"
    )

    print(
        "Predicted Turbidity:",
        result["predicted_turbidity"],
        "NTU"
    )

    print("\n" + "=" * 60)
    print("PREDICTION TEST SUCCESSFUL")
    print("=" * 60)

