import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

DATA_PATH = "data/data-processed/styles_cleaned.csv"
EMBEDDING_DIR = "data/embedding-pipeline"

# Load dataset
df = pd.read_csv(DATA_PATH)
print("Loaded", len(df), "rows")

# Create text description for embeddings
df["text"] = (
    df["gender"].fillna("") + " " +
    df["articletype"].fillna("") + " " +
    df["basecolour"].fillna("") + " " +
    df["season"].fillna("") + " " +
    df["usage"].fillna("") + " " +
    df["productdisplayname"].fillna("")
)

texts = df["text"].tolist()

print("Generating embeddings...")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(texts, show_progress_bar=True)

print("Embedding shape:", embeddings.shape)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings).astype("float32"))

# Create directory
os.makedirs(EMBEDDING_DIR, exist_ok=True)

# Save index
faiss.write_index(index, f"{EMBEDDING_DIR}/clothing_index.faiss")

# Save metadata
df.to_csv(f"{EMBEDDING_DIR}/metadata.csv", index=False)

print("Embeddings saved!")
