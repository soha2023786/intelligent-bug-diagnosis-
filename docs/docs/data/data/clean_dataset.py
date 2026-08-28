import pandas as pd
from pathlib import Path


# Input and output files
INPUT_FILE = Path("data/sample_bug_reports.csv")
OUTPUT_FILE = Path("data/cleaned_bug_reports.csv")


def clean_text(value):
    """
    Clean and standardize text fields.
    """
    if pd.isna(value):
        return ""

    value = str(value)

    # Remove unnecessary spaces
    value = " ".join(value.split())

    return value.strip()


def clean_dataset():
    """
    Load historical bug reports, clean the data,
    remove invalid records, and save the standardized dataset.
    """

    print("Loading historical bug dataset...")

    if not INPUT_FILE.exists():
        print(f"Input file not found: {INPUT_FILE}")
        return

    df = pd.read_csv(INPUT_FILE)

    print(f"Records loaded: {len(df)}")

    # Standardize column names
    df.columns = [
        column.strip().lower().replace(" ", "_")
        for column in df.columns
    ]

    # Required fields
    required_columns = [
        "bug_id",
        "source",
        "title",
        "description"
    ]

    # Check required columns
    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        print("Missing required columns:", missing_columns)
        return

    # Clean text columns
    text_columns = [
        "bug_id",
        "source",
        "title",
        "description",
        "component",
        "status",
        "resolution",
        "comments"
    ]

    for column in text_columns:
        if column in df.columns:
            df[column] = df[column].apply(clean_text)

    # Remove records without title or description
    df = df[
        (df["title"] != "") &
        (df["description"] != "")
    ]

    # Remove duplicate bug IDs
    df = df.drop_duplicates(
        subset=["bug_id"],
        keep="first"
    )

    # Create standardized combined text
    df["combined_text"] = (
        "Title: " + df["title"] +
        "\nDescription: " + df["description"] +
        "\nComponent: " + df["component"] +
        "\nStatus: " + df["status"] +
        "\nResolution: " + df["resolution"] +
        "\nComments: " + df["comments"]
    )

    # Save cleaned dataset
    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"Cleaned records: {len(df)}")
    print(f"Saved cleaned dataset to: {OUTPUT_FILE}")


if __name__ == "__main__":
    clean_dataset()
