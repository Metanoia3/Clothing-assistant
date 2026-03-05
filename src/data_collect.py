import os
import pandas as pd

# -----------------------------
# CONFIG
# -----------------------------
RAW_CSV = "data/data-raw/styles.csv"
IMAGE_FOLDER = "data/data-raw/images"
PROCESSED_CSV = "data/data-processed/styles_cleaned.csv"

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv(RAW_CSV, on_bad_lines="skip")
print(f"Loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns")

# -----------------------------
# Detect ID column for images
# -----------------------------
possible_id_cols = ["id", "articleid", "article_id", "ArticleId"]
IMAGE_ID_COL = None
for col in possible_id_cols:
    if col in df.columns:
        IMAGE_ID_COL = col
        break

if IMAGE_ID_COL is None:
    raise ValueError("Could not find a column for image IDs. Please check your CSV.")

print(f"Using '{IMAGE_ID_COL}' as image ID column")

# -----------------------------
# Standardize column names
# -----------------------------
df.columns = df.columns.str.lower()

# -----------------------------
# Remove rows missing critical info
# -----------------------------
critical_cols = ["mastercategory", "subcategory"]
for col in critical_cols:
    if col not in df.columns:
        raise ValueError(f"Critical column '{col}' not found in CSV")
df = df.dropna(subset=critical_cols)

# Fill optional columns
for col in ["season", "usage"]:
    if col in df.columns:
        df[col] = df[col].fillna("Unknown")
    else:
        df[col] = "Unknown"

# -----------------------------
# Validate images
# -----------------------------
def image_exists(article_id):
    img_path = os.path.join(IMAGE_FOLDER, f"{article_id}.jpg")
    return os.path.exists(img_path)

df["image_exists"] = df[IMAGE_ID_COL].apply(image_exists)

# Keep only rows with valid images
df = df[df["image_exists"] == True]

# Drop helper column
df = df.drop(columns=["image_exists"])

print(f"After cleaning, {df.shape[0]} rows remain")

# -----------------------------
# Save cleaned CSV
# -----------------------------
os.makedirs(os.path.dirname(PROCESSED_CSV), exist_ok=True)
df.to_csv(PROCESSED_CSV, index=False)
print(f"Cleaned dataset saved to {PROCESSED_CSV}")
