from pathlib import Path
import joblib
import pandas as pd


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "river_features.csv"
MODEL_PATH = BASE_DIR / "models" / "turbidity_model.pkl"


# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model not found: {MODEL_PATH}"
    )

model_data = joblib.load(MODEL_PATH)

model = model_data["model"]
FEATURES = model_data["features"]


# --------------------------------------------------
# PREDICTION FUNCTION
# --------------------------------------------------

def predict_latest():

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Feature dataset not found: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["Timestamp"]
    )

    df = df.sort_values(
        "Timestamp"
    ).reset_index(drop=True)

    # Latest available observation
    latest = df.iloc[-1]

    # Prepare model input
    X_latest = pd.DataFrame(
        [latest[FEATURES].values],
        columns=FEATURES
    )

    # Forecast
    prediction = model.predict(
        X_latest
    )[0]

    return {
        "timestamp": latest["Timestamp"],
        "current_turbidity": float(
            latest["Turbidity"]
        ),
        "predicted_turbidity": float(
            prediction
        )
    }


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    result = predict_latest()

    print("=" * 60)
    print("LATEST TURBIDITY FORECAST")
    print("=" * 60)

    print(
        f"\nTimestamp:"
        f" {result['timestamp']}"
    )

    print(
        f"Current Turbidity:"
        f" {result['current_turbidity']:.4f} NTU"
    )

    print(
        f"Predicted Turbidity:"
        f" {result['predicted_turbidity']:.4f} NTU"
    )

    print("\nPrediction completed successfully.")