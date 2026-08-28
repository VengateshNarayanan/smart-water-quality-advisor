from pathlib import Path
import pandas as pd
import numpy as np

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_PATH = BASE_DIR / "data" / "river_cleaned.csv"
OUTPUT_PATH = BASE_DIR / "data" / "river_features.csv"


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

if not INPUT_PATH.exists():
    raise FileNotFoundError(
        f"Cleaned dataset not found: {INPUT_PATH}"
    )

print("=" * 60)
print("SMART WATER QUALITY ADVISORY ASSISTANT")
print("STEP 5 - FEATURE ENGINEERING")
print("=" * 60)

print("\nLoading cleaned dataset...")

df = pd.read_csv(INPUT_PATH)

print(f"Dataset shape: {df.shape}")


# --------------------------------------------------
# TIMESTAMP
# --------------------------------------------------

timestamp_column = "Timestamp"

if timestamp_column not in df.columns:
    raise ValueError(
        f"{timestamp_column} column not found."
    )

df[timestamp_column] = pd.to_datetime(
    df[timestamp_column],
    errors="coerce"
)

df = df.dropna(
    subset=[timestamp_column]
)

df = df.sort_values(
    timestamp_column
).reset_index(drop=True)


# --------------------------------------------------
# TEMPORAL FEATURES
# --------------------------------------------------

print("\nCreating temporal features...")

df["hour"] = df[timestamp_column].dt.hour

df["day"] = df[timestamp_column].dt.day

df["day_of_week"] = (
    df[timestamp_column].dt.dayofweek
)

df["month"] = (
    df[timestamp_column].dt.month
)

df["day_of_year"] = (
    df[timestamp_column].dt.dayofyear
)


# --------------------------------------------------
# CYCLICAL TIME FEATURES
# --------------------------------------------------

# Hour is cyclical: 23:00 is close to 00:00
df["hour_sin"] = np.sin(
    2 * np.pi * df["hour"] / 24
)

df["hour_cos"] = np.cos(
    2 * np.pi * df["hour"] / 24
)

# Month is cyclical
df["month_sin"] = np.sin(
    2 * np.pi * df["month"] / 12
)

df["month_cos"] = np.cos(
    2 * np.pi * df["month"] / 12
)


# --------------------------------------------------
# TURBIDITY LAG FEATURES
# --------------------------------------------------

if "Turbidity" not in df.columns:
    raise ValueError(
        "Turbidity column not found."
    )

print("Creating Turbidity lag features...")

df["turbidity_lag_1"] = (
    df["Turbidity"].shift(1)
)

df["turbidity_lag_3"] = (
    df["Turbidity"].shift(3)
)

df["turbidity_lag_6"] = (
    df["Turbidity"].shift(6)
)

df["turbidity_lag_12"] = (
    df["Turbidity"].shift(12)
)


# --------------------------------------------------
# ROLLING STATISTICS
# --------------------------------------------------

print("Creating rolling statistics...")

df["turbidity_rolling_mean_3"] = (
    df["Turbidity"]
    .rolling(window=3)
    .mean()
)

df["turbidity_rolling_mean_6"] = (
    df["Turbidity"]
    .rolling(window=6)
    .mean()
)

df["turbidity_rolling_std_6"] = (
    df["Turbidity"]
    .rolling(window=6)
    .std()
)


# --------------------------------------------------
# NO3 FEATURES
# --------------------------------------------------

if "NO3" in df.columns:

    print("Creating NO3 features...")

    df["no3_lag_1"] = (
        df["NO3"].shift(1)
    )

    df["no3_rolling_mean_3"] = (
        df["NO3"]
        .rolling(window=3)
        .mean()
    )


# --------------------------------------------------
# WATER TEMPERATURE FEATURES
# --------------------------------------------------

temperature_column = None

for column in [
    "WaterTemp",
    "Water_Temp",
    "Temperature",
    "Temp"
]:

    if column in df.columns:
        temperature_column = column
        break


if temperature_column:

    print(
        f"Using temperature column: "
        f"{temperature_column}"
    )

    df["temperature_lag_1"] = (
        df[temperature_column].shift(1)
    )


# --------------------------------------------------
# REMOVE ROWS CREATED BY LAG/ROLLING OPERATIONS
# --------------------------------------------------

before = len(df)

df = df.dropna().reset_index(drop=True)

after = len(df)

print(
    f"\nRows removed because of "
    f"lag/rolling features: {before - after}"
)


# --------------------------------------------------
# SAVE FEATURE DATASET
# --------------------------------------------------

df.to_csv(
    OUTPUT_PATH,
    index=False
)


# --------------------------------------------------
# REPORT
# --------------------------------------------------

print("\n========== FEATURE ENGINEERING COMPLETE ==========")

print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")

print("\nFeatures created:")

for column in df.columns:
    print(f" - {column}")

print(
    f"\nFeature dataset saved to:\n"
    f"{OUTPUT_PATH}"
)

print("=" * 60)