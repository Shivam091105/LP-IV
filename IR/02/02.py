# PageRank Algorithm

# Directed graph: each page links to the listed pages
graph = {
    "A": ["B", "C"],
    "B": ["C"],
    "C": ["A"],
    "D": ["C"]
}

damping_factor = 0.85
iterations = 100

# Initialize equal rank for every page
pages = list(graph.keys())
n = len(pages)
rank = {page: 1 / n for page in pages}

# Calculate PageRank iteratively
for _ in range(iterations):
    new_rank = {}

    for page in pages:
        # Random teleportation probability
        score = (1 - damping_factor) / n

        # Rank contribution from incoming links
        for source in pages:
            if page in graph[source]:
                score += (
                    damping_factor
                    * rank[source]
                    / len(graph[source])
                )

        new_rank[page] = score

    rank = new_rank

# Display results in descending order
print("===== PAGERANK RESULTS =====")

for page, score in sorted(
    rank.items(), key=lambda item: item[1], reverse=True
):
    print(f"Page {page}: {score:.4f}")
