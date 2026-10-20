
import xml.etree.ElementTree as ET

# Parse XML file
tree = ET.parse("webdata.xml")
root = tree.getroot()

# Extract page titles, topics, and links
pages = {}
graph = {}

for page in root.findall("page"):
    page_id = page.get("id")
    title = page.findtext("title", default="Untitled")
    topic = page.get("topic", "")
    links = [link.text.strip() for link in page.findall("link")
             if link.text and link.text.strip()]

    pages[page_id] = {"title": title, "topic": topic}
    graph[page_id] = links

# Remove links to pages not present in the XML
for page in graph:
    graph[page] = [link for link in graph[page] if link in pages]

# Display the directed web graph
print("===== WEB GRAPH =====")
for page, links in graph.items():
    print(f"{page} -> {links}")

# Select the topic
topic = input("\nEnter topic (AI or Sports): ").strip().lower()

# Initialize topic-specific PageRank
n = len(pages)
d = 0.85
iterations = 100

if n == 0:
    print("No pages found in the XML file.")
else:
    # Give higher initial preference to pages matching the topic
    matching = [
        page for page in pages
        if pages[page]["topic"].lower() == topic
    ]

    if not matching:
        print("No pages found for this topic.")
    else:
        rank = {
            page: (1 / len(matching) if page in matching else 0)
            for page in pages
        }

        # Calculate topic-specific PageRank
        for _ in range(iterations):
            new_rank = {}

            for page in pages:
                score = (1 - d) * (
                    1 / len(matching) if page in matching else 0
                )

                for source in pages:
                    if graph[source]:
                        if page in graph[source]:
                            score += (
                                d * rank[source] / len(graph[source])
                            )
                    else:
                        # Distribute rank from pages with no outgoing links
                        score += d * rank[source] / n

                new_rank[page] = score

            rank = new_rank

        # Display results in descending order
        print(f"\n===== PAGERANK FOR TOPIC: {topic.upper()} =====")

        for page, score in sorted(
            rank.items(), key=lambda item: item[1], reverse=True
        ):
            print(
                f"{page} - {pages[page]['title']}: {score:.4f}"
            )
