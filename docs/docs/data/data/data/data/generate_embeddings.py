import json
from pathlib import Path

from sentence_transformers import SentenceTransformer


INPUT_FILE = Path("data/bug_chunks.json")
OUTPUT_FILE = Path("data/embedded_chunks.json")

MODEL_NAME = "all-MiniLM-L6-v2"


def generate_embeddings():
    """
    Generate vector embeddings for historical bug chunks.
    """

    if not INPUT_FILE.exists():
        print(f"Input file not found: {INPUT_FILE}")
        print("Run chunk_dataset.py first.")
        return

    print("Loading bug chunks...")

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        chunks = json.load(file)

    print(f"Chunks loaded: {len(chunks)}")

    print(f"Loading embedding model: {MODEL_NAME}")

    model = SentenceTransformer(MODEL_NAME)

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    print("Generating embeddings...")

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    embedded_chunks = []

    for chunk, embedding in zip(chunks, embeddings):

        embedded_chunks.append({
            "bug_id": chunk["bug_id"],
            "source": chunk["source"],
            "chunk_type": chunk["chunk_type"],
            "text": chunk["text"],
            "embedding": embedding.tolist()
        })

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            embedded_chunks,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"Embeddings generated for {len(embedded_chunks)} chunks."
    )

    print(
        f"Saved embeddings to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    generate_embeddings()
