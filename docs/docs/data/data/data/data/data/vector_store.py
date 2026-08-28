import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


EMBEDDED_FILE = Path("data/embedded_chunks.json")

MODEL_NAME = "all-MiniLM-L6-v2"


def load_embeddings():
    """Load embedded historical bug chunks."""

    if not EMBEDDED_FILE.exists():
        print(f"File not found: {EMBEDDED_FILE}")
        print("Run generate_embeddings.py first.")
        return []

    with open(
        EMBEDDED_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def cosine_similarity(vector_a, vector_b):
    """Calculate cosine similarity between two vectors."""

    vector_a = np.array(vector_a)
    vector_b = np.array(vector_b)

    denominator = (
        np.linalg.norm(vector_a) *
        np.linalg.norm(vector_b)
    )

    if denominator == 0:
        return 0.0

    return float(
        np.dot(vector_a, vector_b) / denominator
    )


def search_similar_bugs(query, top_k=3):
    """
    Find historical bug chunks that are
    semantically similar to the user query.
    """

    chunks = load_embeddings()

    if not chunks:
        return []

    model = SentenceTransformer(MODEL_NAME)

    # Convert query into an embedding
    query_embedding = model.encode(query).tolist()

    results = []

    for chunk in chunks:

        similarity = cosine_similarity(
            query_embedding,
            chunk["embedding"]
        )

        results.append({
            "bug_id": chunk["bug_id"],
            "source": chunk["source"],
            "chunk_type": chunk["chunk_type"],
            "text": chunk["text"],
            "similarity": round(similarity, 4)
        })

    # Sort by highest similarity
    results.sort(
        key=lambda item: item["similarity"],
        reverse=True
    )

    return results[:top_k]


if __name__ == "__main__":

    query = input(
        "Enter a bug description to search: "
    )

    results = search_similar_bugs(
        query,
        top_k=3
    )

    print("\nSimilar Historical Bugs")
    print("=" * 50)

    if not results:
        print("No results found.")

    for result in results:

        print(f"\nBug ID: {result['bug_id']}")
        print(f"Source: {result['source']}")
        print(f"Type: {result['chunk_type']}")
        print(
            f"Similarity: {result['similarity']}"
        )
        print(f"Text: {result['text']}")
