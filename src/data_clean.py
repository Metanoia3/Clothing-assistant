import os
import pandas as pd

# -----------------------------
# FILE PATHS
# -----------------------------
INPUT_FILE = "data/data-processed/styles_cleaned.csv"
OUTPUT_FILE = "data/data-processed/styles_final.csv"

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv(INPUT_FILE)

print("Dataset loaded")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

# -----------------------------
# STANDARDIZE COLUMN NAMES
# -----------------------------
df.columns = df.columns.str.lower().str.strip()

# -----------------------------
# DROP DUPLICATES
# -----------------------------
before = df.shape[0]
df = df.drop_duplicates()
after = df.shape[0]

print(f"Removed {before - after} duplicate rows")

# -----------------------------
# HANDLE MISSING VALUES
# -----------------------------
for column in df.columns:
    if df[column].dtype == "object":
        df[column] = df[column].fillna("Unknown")
    else:
        df[column] = df[column].fillna(0)

# -----------------------------
# CLEAN TEXT COLUMNS
# -----------------------------
text_columns = ["gender", "mastercategory", "subcategory", "articleType", "season", "usage"]

for col in text_columns:
    if col.lower() in df.columns:
        df[col.lower()] = df[col.lower()].astype(str).str.strip().str.lower()

# -----------------------------
# REMOVE INVALID CATEGORIES
# -----------------------------
df = df[df["mastercategory"] != "unknown"]

# -----------------------------
# SAVE CLEAN DATASET
# -----------------------------
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

df.to_csv(OUTPUT_FILE, index=False)

print("Cleaned dataset saved")
print(f"Final dataset rows: {df.shape[0]}")
print(f"Saved to: {OUTPUT_FILE}")
