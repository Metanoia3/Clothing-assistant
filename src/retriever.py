import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer

# Paths
INDEX_PATH = "data/embedding-pipeline/clothing_index.faiss"
METADATA_PATH = "data/embedding-pipeline/clothing_metadata.csv"

# Load vector database
index = faiss.read_index(INDEX_PATH)

# Load metadata
df = pd.read_csv(METADATA_PATH)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_documents(query: str, k: int = 5) -> list[str]:
    """
    Retrieve the most relevant clothing items for a query.
    """

    # Convert query to embedding
    query_embedding = model.encode([query])

    # Search FAISS
    distances, indices = index.search(query_embedding, k)

    results = []

    for idx in indices[0]:

        row = df.iloc[idx]

        description = (
            f"{row['productdisplayname']} "
            f"{row['articletype']} "
            f"{row['basecolour']} "
            f"{row['season']} "
            f"{row['usage']}"
        )

        results.append(description)

    return results

# test
if __name__ == "__main__":

    query = "casual summer shirt"

    docs = retrieve_documents(query)

    for d in docs:
        print(d)
