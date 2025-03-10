# Hackathon Presentation Guide

This guide will help you effectively demonstrate the Domain-Specific FAQ Chatbot with Knowledge Graph Integration during your hackathon presentation.

## Preparation

1. Make sure you have:
   - A working internet connection
   - Your Gemini API key in the `.env` file
   - Some sample images ready for demonstration
   - The project code fully set up and tested

2. Recommended sample images:
   - A diagram of a graph database
   - A screenshot of code related to knowledge graphs
   - An image with text describing a technical concept
   - A photo of a technical device or component

## Starting the Demo

1. Open a terminal and navigate to the project directory
2. Activate the virtual environment:
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Start the demo:
   ```bash
   python start_demo.py
   ```
4. The demo interface should automatically open in your browser

## Demonstration Flow

### 1. Introduction (2 minutes)

- Introduce the problem: Traditional chatbots lack domain-specific depth and contextual understanding
- Explain your solution: Combining knowledge graphs with LLMs for enhanced responses
- Highlight the key features: Knowledge graph integration, multimodal capabilities, entity extraction

### 2. Basic Chat Functionality (2 minutes)

- Start with a simple domain-specific question (e.g., "What is a graph database?")
- Point out how the response includes information from the knowledge graph
- Show the "Knowledge Context" tab to demonstrate what information was used
- Highlight how the chatbot maintains conversation history

### 3. Multimodal Capabilities (3 minutes)

- Upload an image (e.g., a diagram of a graph database)
- Ask a question about the image (e.g., "What does this diagram show?")
- Point out the extracted entities in the "Extracted Entities" tab
- Show how these entities are added to the knowledge graph visualization
- Ask a follow-up question that references both the image and previous context

### 4. Knowledge Graph Visualization (2 minutes)

- Explain the knowledge graph visualization
- Show how entities and relationships are represented
- Demonstrate how the graph grows as new information is extracted
- Explain how this structured knowledge enhances the chatbot's responses

### 5. Technical Implementation (2 minutes)

- Briefly explain the architecture:
  - MeTTa for knowledge representation
  - Gemini 2.0 for LLM capabilities
  - FastAPI for the backend
  - Graph RAG for context-aware responses
- Highlight the most innovative aspects of your implementation

### 6. Q&A and Conclusion (2 minutes)

- Summarize the key benefits of your approach
- Discuss potential applications and use cases
- Answer questions from the judges

## Tips for a Successful Presentation

1. **Practice the demo flow** beforehand to ensure smooth transitions
2. **Have backup examples** ready in case something doesn't work as expected
3. **Focus on the user experience** rather than technical details unless asked
4. **Highlight the integration aspects** - how the knowledge graph and LLM work together
5. **Be prepared to explain** how your solution is different from existing chatbots
6. **Keep the demo moving** - don't spend too long on any one feature
7. **Have a "wow moment"** prepared - something that clearly demonstrates the power of your approach

## Troubleshooting

If you encounter issues during the presentation:

1. **Server not starting**: Check if another instance is already running with `lsof -i :8000`
2. **CORS errors**: Make sure the CORS middleware is properly configured in `src/main.py`
3. **Image upload issues**: Try a different image or use a smaller file
4. **API key errors**: Verify your Gemini API key is correctly set in the `.env` file
5. **Browser compatibility**: If the demo doesn't work in one browser, try another (Chrome recommended)

## After the Presentation

Be prepared to share:
- GitHub repository link
- Documentation on how to set up and run the project
- Ideas for future enhancements
- Your contact information for follow-up questions 