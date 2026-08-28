from vector_store import search_similar_bugs


def build_rag_context(query, top_k=3):
    """
    Retrieve similar historical bugs and
    build context for the RAG pipeline.
    """

    results = search_similar_bugs(
        query,
        top_k=top_k
    )

    if not results:
        return "No relevant historical defects were found."

    context_parts = []

    for index, result in enumerate(results, start=1):

        context = (
            f"Historical Defect {index}\n"
            f"Bug ID: {result['bug_id']}\n"
            f"Source: {result['source']}\n"
            f"Chunk Type: {result['chunk_type']}\n"
            f"Similarity Score: {result['similarity']}\n"
            f"Information: {result['text']}\n"
        )

        context_parts.append(context)

    return "\n".join(context_parts)


def retrieve_historical_context(
    bug_description,
    top_k=3
):
    """
    Retrieve relevant historical defect information
    for a newly submitted bug.
    """

    if not bug_description.strip():
        return "Bug description cannot be empty."

    return build_rag_context(
        bug_description,
        top_k=top_k
    )


if __name__ == "__main__":

    print("RAG Historical Defect Retrieval")
    print("=" * 50)

    query = input(
        "Enter the new bug description: "
    )

    context = retrieve_historical_context(
        query,
        top_k=3
    )

    print("\nRetrieved RAG Context")
    print("=" * 50)
    print(context)
