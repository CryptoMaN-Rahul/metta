import requests
import json

# Sample document about knowledge graphs and their applications
document = """
Knowledge Graphs: A Comprehensive Overview

Knowledge graphs are a powerful way to represent and organize information in a structured format. They consist of entities (nodes) and relationships (edges) that connect these entities. This structure allows for complex queries and insights that would be difficult to obtain from traditional databases.

Key Components:
1. Entities: These are the nodes in the graph, representing real-world objects, concepts, or ideas. Examples include people, places, products, or abstract concepts.
2. Relationships: These are the edges connecting entities, representing how entities relate to each other. Examples include "is_part_of", "works_for", or "created_by".
3. Properties: These are attributes that provide additional information about entities or relationships.

Applications of Knowledge Graphs:
- Semantic Search: Enhancing search capabilities by understanding the meaning and context of queries.
- Recommendation Systems: Providing personalized recommendations based on relationships between entities.
- Question Answering: Enabling more accurate and contextual answers to complex questions.
- Data Integration: Combining data from multiple sources into a unified view.
- Fraud Detection: Identifying suspicious patterns and connections in financial transactions.

Popular Knowledge Graph Implementations:
- Google Knowledge Graph: Powers Google's search results with factual information.
- Facebook's Social Graph: Maps relationships between users, pages, and content.
- Amazon's Product Graph: Connects products, customers, and preferences.
- Microsoft's Academic Graph: Links academic publications, authors, and institutions.

Building a Knowledge Graph:
1. Data Collection: Gather relevant data from various sources.
2. Entity Extraction: Identify entities from the collected data.
3. Relationship Extraction: Determine how entities are related to each other.
4. Knowledge Integration: Combine extracted knowledge into a coherent graph.
5. Knowledge Validation: Verify the accuracy and consistency of the graph.
6. Knowledge Enrichment: Add additional information to enhance the graph.

Challenges in Knowledge Graph Development:
- Data Quality: Ensuring the accuracy and completeness of the data.
- Scalability: Managing large volumes of entities and relationships.
- Maintenance: Keeping the graph up-to-date as new information becomes available.
- Interoperability: Ensuring compatibility with different systems and standards.

Future Trends:
- Integration with AI: Combining knowledge graphs with machine learning for more intelligent systems.
- Decentralized Knowledge Graphs: Distributing knowledge across multiple systems for better resilience.
- Multimodal Knowledge Graphs: Incorporating different types of data (text, images, videos) into a unified graph.
- Temporal Knowledge Graphs: Representing how knowledge changes over time.

Conclusion:
Knowledge graphs represent a significant advancement in how we organize and utilize information. By explicitly modeling relationships between entities, they enable more sophisticated analysis and insights than traditional data structures. As technology continues to evolve, knowledge graphs will play an increasingly important role in various domains, from search engines to artificial intelligence systems.
"""

# API endpoint
url = "http://localhost:8000/extract/document"

# Request headers
headers = {
    "Content-Type": "application/json"
}

# Request payload
payload = {
    "text": document
}

# Send POST request
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Print response
print("Status Code:", response.status_code)
print("Response:")
print(json.dumps(response.json(), indent=2))

# Now query about knowledge graphs
query_url = "http://localhost:8000/chat"
query_payload = {
    "text": "What are the key components and applications of knowledge graphs?",
    "history": []
}

query_response = requests.post(query_url, headers=headers, data=json.dumps(query_payload))
print("\nQuery Response:")
print(json.dumps(query_response.json(), indent=2)) 