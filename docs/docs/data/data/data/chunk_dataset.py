import pandas as pd
from pathlib import Path
import json


INPUT_FILE = Path("data/cleaned_bug_reports.csv")
OUTPUT_FILE = Path("data/bug_chunks.json")


def create_chunks(row):
    """
    Create meaningful text chunks from a historical bug report.
    """

    chunks = []

    bug_id = row.get("bug_id", "")
    source = row.get("source", "")
    title = row.get("title", "")
    description = row.get("description", "")
    component = row.get("component", "")
    status = row.get("status", "")
    resolution = row.get("resolution", "")
    comments = row.get("comments", "")

    # Chunk 1: Bug description
    if title or description:
        chunks.append({
            "bug_id": bug_id,
            "source": source,
            "chunk_type": "description",
            "text": (
                f"Bug Title: {title}\n"
                f"Bug Description: {description}"
            )
        })

    # Chunk 2: Component information
    if component:
        chunks.append({
            "bug_id": bug_id,
            "source": source,
            "chunk_type": "component",
            "text": f"Affected Component: {component}"
        })

    # Chunk 3: Resolution information
    if status or resolution:
        chunks.append({
            "bug_id": bug_id,
            "source": source,
            "chunk_type": "resolution",
            "text": (
                f"Bug Status: {status}\n"
                f"Resolution: {resolution}"
            )
        })

    # Chunk 4: Comments
    if comments:
        chunks.append({
            "bug_id": bug_id,
            "source": source,
            "chunk_type": "comments",
            "text": f"Historical Comments: {comments}"
        })

    return chunks


def chunk_dataset():
    """
    Load cleaned historical bug reports and
    divide them into retrieval-friendly text chunks.
    """

    print("Loading cleaned dataset...")

    if not INPUT_FILE.exists():
        print(f"Input file not found: {INPUT_FILE}")
        print("Run clean_dataset.py first.")
        return

    df = pd.read_csv(INPUT_FILE)

    all_chunks = []

    for _, row in df.iterrows():
        chunks = create_chunks(row)
        all_chunks.extend(chunks)

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            all_chunks,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"Bug reports processed: {len(df)}")
    print(f"Chunks created: {len(all_chunks)}")
    print(f"Saved chunks to: {OUTPUT_FILE}")


if __name__ == "__main__":
    chunk_dataset()
