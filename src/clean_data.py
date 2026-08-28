from pathlib import Path
import pandas as pd
import numpy as np

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "river.csv"
OUTPUT_PATH = BASE_DIR / "data" / "river_cleaned.csv"


# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_PATH}"
    )

print("=" * 60)
print("SMART WATER QUALITY ADVISORY ASSISTANT")
print("STEP 4 - DATA CLEANING")
print("=" * 60)

print("\nLoading dataset...")

df = pd.read_csv(DATA_PATH)

print(f"Original shape: {df.shape}")


# --------------------------------------------------
# CLEAN COLUMN NAMES
# --------------------------------------------------

df.columns = (
    df.columns
    .str.strip()
    .str.replace(" ", "_")
)

print("\nAvailable columns:")
for column in df.columns:
    print(f" - {column}")


# --------------------------------------------------
# FIND TIMESTAMP COLUMN
# --------------------------------------------------

timestamp_candidates = [
    "Timestamp",
    "timestamp",
    "DateTime",
    "datetime",
    "Date",
    "date"
]

timestamp_column = None

for column in timestamp_candidates:
    if column in df.columns:
        timestamp_column = column
        break

if timestamp_column is None:
    raise ValueError(
        "Timestamp column was not found."
    )

print(f"\nTimestamp column: {timestamp_column}")


# --------------------------------------------------
# CONVERT TIMESTAMP
# --------------------------------------------------

df[timestamp_column] = pd.to_datetime(
    df[timestamp_column],
    errors="coerce"
)

invalid_timestamps = df[timestamp_column].isna().sum()

print(
    f"Invalid timestamps found: "
    f"{invalid_timestamps}"
)

df = df.dropna(
    subset=[timestamp_column]
)


# --------------------------------------------------
# REMOVE DUPLICATES
# --------------------------------------------------

duplicates = df.duplicated().sum()

print(
    f"Duplicate rows found: {duplicates}"
)

df = df.drop_duplicates()


# --------------------------------------------------
# IDENTIFY SENSOR COLUMNS
# --------------------------------------------------

possible_sensor_columns = [
    "NO3",
    "Turbidity",
    "WaterTemp",
    "Water_Temp",
    "Temperature",
    "Temp"
]

sensor_columns = [
    column
    for column in possible_sensor_columns
    if column in df.columns
]

print("\nSensor columns detected:")

for column in sensor_columns:
    print(f" - {column}")


# --------------------------------------------------
# CONVERT SENSOR VALUES TO NUMERIC
# --------------------------------------------------

for column in sensor_columns:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    print(
        f"{column}: converted to numeric"
    )


# --------------------------------------------------
# REMOVE IMPOSSIBLE NEGATIVE VALUES
# --------------------------------------------------

if "NO3" in df.columns:

    invalid_no3 = (
        df["NO3"] < 0
    ).sum()

    print(
        f"\nInvalid NO3 values (< 0): "
        f"{invalid_no3}"
    )

    df.loc[
        df["NO3"] < 0,
        "NO3"
    ] = np.nan


if "Turbidity" in df.columns:

    invalid_turbidity = (
        df["Turbidity"] < 0
    ).sum()

    print(
        f"Invalid Turbidity values (< 0): "
        f"{invalid_turbidity}"
    )

    df.loc[
        df["Turbidity"] < 0,
        "Turbidity"
    ] = np.nan


# --------------------------------------------------
# SORT BY TIMESTAMP
# --------------------------------------------------

df = df.sort_values(
    timestamp_column
).reset_index(drop=True)


# --------------------------------------------------
# CHECK MISSING VALUES
# --------------------------------------------------

print("\n========== MISSING VALUES BEFORE CLEANING ==========")

if sensor_columns:
    print(
        df[sensor_columns]
        .isna()
        .sum()
    )


# --------------------------------------------------
# INTERPOLATE SENSOR VALUES
# --------------------------------------------------

for column in sensor_columns:

    df[column] = (
        df[column]
        .interpolate(
            method="linear",
            limit_direction="both"
        )
    )


# --------------------------------------------------
# CHECK MISSING VALUES AFTER CLEANING
# --------------------------------------------------

print("\n========== MISSING VALUES AFTER CLEANING ==========")

if sensor_columns:
    print(
        df[sensor_columns]
        .isna()
        .sum()
    )


# --------------------------------------------------
# SAVE CLEANED DATASET
# --------------------------------------------------

df.to_csv(
    OUTPUT_PATH,
    index=False
)


# --------------------------------------------------
# FINAL REPORT
# --------------------------------------------------

print("\n========== CLEANING COMPLETE ==========")

print(
    f"Original rows : {25354}"
)

print(
    f"Final rows    : {len(df)}"
)

print(
    f"Final columns : {len(df.columns)}"
)

print(
    f"\nCleaned dataset saved to:"
)

print(OUTPUT_PATH)

print("\n" + "=" * 60)