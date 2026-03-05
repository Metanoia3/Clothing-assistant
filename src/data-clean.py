import os
import pandas as pd

unprocessed = "data/data-raw/styles.csv"
images_folder = "data/data-raw/images"
processed = "data/processed/styles_cleaned.csv"

df = pd.read_csv(unprocessed, on_bad_lines="skip")
print(f"Loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns")

df.columns = df.columns.str.lower()

df = df.dropna(subset=["mastercategory", "subcategory"])
df["season"] = df["season"].fillna("Unknown")
df["usage"] = df["usage"].fillna("Unknown")

def image_exists(article_id):
    # Image filename is usually <id>.jpg
    img_path = os.path.join(images_folder, f"{article_id}.jpg")
    return os.path.exists(img_path)

df["image_exists"] = df["id"].apply(image_exists)

# Keep only rows with valid images
df = df[df["image_exists"] == True]

# Drop helper column
df = df.drop(columns=["image_exists"])

print(f"After cleaning, {df.shape[0]} rows remain")# Keep only rows with valid images
df = df[df["image_exists"] == True]

os.makedirs(os.path.dirname(processed), exist_ok=True)
df.to_csv(processed, index=False)

print(f"Cleaned dataset saved to {processed}")