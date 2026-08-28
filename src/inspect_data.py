from pathlib import Path
import pandas as pd

# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "river.csv"

# Verify dataset exists
if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found at: {DATA_PATH}\n"
        "Make sure river.csv is inside the data folder."
    )

print("=" * 60)
print("SMART WATER QUALITY ADVISORY ASSISTANT")
print("=" * 60)

print(f"\nDataset found: {DATA_PATH}")
print("Loading dataset...")

# Load dataset
df = pd.read_csv(DATA_PATH)

print("\n========== DATASET LOADED SUCCESSFULLY ==========")

# Shape
print("\n========== SHAPE ==========")
print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")

# Columns
print("\n========== COLUMNS ==========")
for i, column in enumerate(df.columns, start=1):
    print(f"{i}. {column}")

# First rows
print("\n========== FIRST 5 ROWS ==========")
print(df.head().to_string())

# Data types
print("\n========== DATA TYPES ==========")
print(df.dtypes.to_string())

# Missing values
print("\n========== MISSING VALUES ==========")
missing = df.isnull().sum()

for column, count in missing.items():
    print(f"{column}: {count}")

# Duplicate rows
print("\n========== DUPLICATE ROWS ==========")
print(f"Duplicates: {df.duplicated().sum()}")

# Numerical summary
print("\n========== NUMERICAL SUMMARY ==========")
print(df.describe().T.to_string())

print("\n" + "=" * 60)
print("DATASET INSPECTION COMPLETE")
print("=" * 60)