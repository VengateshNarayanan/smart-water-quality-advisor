from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "river_features.csv"
MODEL_PATH = BASE_DIR / "models" / "turbidity_model.pkl"


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Feature dataset not found: {DATA_PATH}"
    )

print("=" * 60)
print("SMART WATER QUALITY ADVISORY ASSISTANT")
print("STEP 6 - MODEL TRAINING")
print("=" * 60)

print("\nLoading feature dataset...")

df = pd.read_csv(DATA_PATH)

print(f"Dataset shape: {df.shape}")


# --------------------------------------------------
# SORT BY TIME
# --------------------------------------------------

df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    errors="coerce"
)

df = df.sort_values(
    "Timestamp"
).reset_index(drop=True)


# --------------------------------------------------
# TARGET
# --------------------------------------------------

TARGET = "Turbidity"

if TARGET not in df.columns:
    raise ValueError(
        f"Target column '{TARGET}' not found."
    )


# --------------------------------------------------
# FEATURES
# --------------------------------------------------

FEATURES = [
    "NO3",
    "hour",
    "day",
    "day_of_week",
    "month",
    "day_of_year",
    "hour_sin",
    "hour_cos",
    "month_sin",
    "month_cos",
    "turbidity_lag_1",
    "turbidity_lag_3",
    "turbidity_lag_6",
    "turbidity_lag_12",
    "turbidity_rolling_mean_3",
    "turbidity_rolling_mean_6",
    "turbidity_rolling_std_6",
]


# --------------------------------------------------
# CHECK FEATURES
# --------------------------------------------------

missing_features = [
    feature
    for feature in FEATURES
    if feature not in df.columns
]

if missing_features:
    raise ValueError(
        "Missing features:\n"
        + "\n".join(missing_features)
    )


# --------------------------------------------------
# REMOVE MISSING VALUES
# --------------------------------------------------

df = df.dropna(
    subset=FEATURES + [TARGET]
).reset_index(drop=True)


# --------------------------------------------------
# TIME-SERIES SPLIT
# --------------------------------------------------

# 80% historical data -> training
# 20% latest data      -> testing

split_index = int(len(df) * 0.80)

train_df = df.iloc[:split_index]
test_df = df.iloc[split_index:]


X_train = train_df[FEATURES]
y_train = train_df[TARGET]

X_test = test_df[FEATURES]
y_test = test_df[TARGET]


# --------------------------------------------------
# DISPLAY SPLIT INFORMATION
# --------------------------------------------------

print("\n========== TIME-SERIES SPLIT ==========")

print(f"Training rows: {len(train_df)}")
print(f"Testing rows : {len(test_df)}")

print(
    f"\nTraining period:"
    f"\n{train_df['Timestamp'].min()}"
    f"\n→ {train_df['Timestamp'].max()}"
)

print(
    f"\nTesting period:"
    f"\n{test_df['Timestamp'].min()}"
    f"\n→ {test_df['Timestamp'].max()}"
)


# --------------------------------------------------
# TRAIN RANDOM FOREST
# --------------------------------------------------

print("\n========== TRAINING MODEL ==========")

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=15,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

model.fit(
    X_train,
    y_train
)

print("Random Forest training completed.")


# --------------------------------------------------
# PREDICTION
# --------------------------------------------------

print("\nGenerating predictions...")

predictions = model.predict(
    X_test
)


# --------------------------------------------------
# EVALUATION
# --------------------------------------------------

mae = mean_absolute_error(
    y_test,
    predictions
)

mse = mean_squared_error(
    y_test,
    predictions
)

rmse = mse ** 0.5

r2 = r2_score(
    y_test,
    predictions
)


print("\n========== MODEL PERFORMANCE ==========")

print(f"MAE  : {mae:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"R²   : {r2:.4f}")


# --------------------------------------------------
# FEATURE IMPORTANCE
# --------------------------------------------------

print("\n========== FEATURE IMPORTANCE ==========")

importance = pd.DataFrame(
    {
        "Feature": FEATURES,
        "Importance": model.feature_importances_
    }
).sort_values(
    "Importance",
    ascending=False
)

print(
    importance.to_string(index=False)
)


# --------------------------------------------------
# SAVE MODEL
# --------------------------------------------------

MODEL_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

joblib.dump(
    {
        "model": model,
        "features": FEATURES,
        "target": TARGET
    },
    MODEL_PATH
)

print("\n========== MODEL SAVED ==========")

print(
    f"Model saved to:\n{MODEL_PATH}"
)

print("\n" + "=" * 60)
print("TASK A MODEL TRAINING COMPLETE")
print("=" * 60)