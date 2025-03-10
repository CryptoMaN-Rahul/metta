

Problem Statement 1
INFO

This problem statement is shared by SingularityNET - title sponsor for HackIndia 2025.


Project: Domain-Specific FAQ Chatbot with Knowledge Graph Integration
Overview
Traditional chatbots often rely solely on predefined responses or general-purpose AI models, leading to shallow answers that lack domain-specific depth. They struggle to understand complex relationships, hierarchies, and contextual dependencies within a specialized field. This results in inaccurate or incomplete responses, making them unreliable for industry-specific use cases.

Challenge
Develop a domain-specific FAQ chatbot that:
Integrates a knowledge graph for real-time contextual understanding.
Understands relationships, hierarchies, and dependencies within a domain.
Provides insightful, structured, and fact-enriched answers beyond standalone AI models.
Supports real-time updates as new knowledge is added to the graph.
Enhances responses with definitions, examples, and contextual references from structured data.
Key Features
Conversational AI + Knowledge Graph: Combines NLP (LLM) with structured data. (DONT USE NLP , STRICTLY USE AN LLM ->Google Gen AI SDK

The new Google Gen AI SDK provides a unified interface to Gemini 2.0 through both the Gemini Developer API and Vertex AI (the Gemini Enterprise API). With a few exceptions, code that runs on one platform will run on both. The Gen AI SDK also supports the Gemini 1.5 models.

Python
The Google Gen AI SDK for Python is available on PyPI and GitHub.

To learn more, see the Python SDK reference.

Quickstart
1. Install the SDK


pip install google-genai
2. Import the library


from google import genai
3. Create a client


client = genai.Client(api_key='GEMINI_API_KEY')
4. Generate content


response = client.models.generate_content(
    model='gemini-2.0-flash', contents='How does RLHF work?'
)
print(response.text)
)
Context-Aware Answers: Leverages relationships and hierarchies for deeper insights.
Real-Time Data Access: Fetches the latest domain-specific facts dynamically.
Adaptive Learning: Updates the knowledge graph with new insights over time.
Multi-Format Support: Responds with text, images, links, and interactive elements.
Impact
This chatbot will transform industry-specific FAQs by providing more accurate, contextual, and enriched responses. It will enable businesses to automate complex queries, improve customer support, and enhance knowledge management through AI-powered intelligence.

Learning outcomes
Knowledge base querying with MeTTa
MeTTa-Python integration
Graph RAG (Retrieval-Augmented Generation)
Ready to Build It? 🚀
Take on the challenge of redefining chatbot intelligence with MeTTa’s graph integration. Show us how your chatbot can truly understand and adapt to your domain!🤖💡🔍

________________


