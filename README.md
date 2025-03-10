# Domain-Specific FAQ Chatbot with Knowledge Graph Integration

A powerful FAQ chatbot that combines MeTTa knowledge graphs with Google's Gemini 2.0 LLM for enhanced, context-aware responses.

## Features

- **Knowledge Graph Integration**: Uses MeTTa for structured knowledge representation
- **LLM Integration**: Leverages Google Gemini 2.0 for natural language understanding
- **Graph RAG**: Retrieval-Augmented Generation for context-aware responses
- **Real-time Updates**: Support for adding new FAQs, entities, and relationships
- **Context-Aware Responses**: Understands relationships and hierarchies within the domain
- **REST API**: FastAPI-based endpoints for easy integration

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```bash
   # Create .env file
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

1. Start the server:
   ```bash
   python src/main.py
   ```

2. The API will be available at `http://localhost:8000`

## API Endpoints

### Chat Endpoint
```http
POST /chat
Content-Type: application/json

{
    "text": "What is...",
    "history": [
        {
            "user": "Previous question",
            "assistant": "Previous answer"
        }
    ]
}
```

### Add FAQ Entry
```http
POST /faq
Content-Type: application/json

{
    "question": "What is...",
    "answer": "The answer is...",
    "category": "General"
}
```

### Add Entity
```http
POST /entity
Content-Type: application/json

{
    "name": "EntityName",
    "entity_type": "Type",
    "properties": {
        "key": "value"
    }
}
```

### Add Relationship
```http
POST /relationship
Content-Type: application/json

{
    "from_entity": "Entity1",
    "relationship_type": "RelationType",
    "to_entity": "Entity2"
}
```

## Knowledge Graph Schema

The knowledge graph is built using MeTTa and supports:
- Entities with properties
- Relationships between entities
- FAQ entries with categories
- Category hierarchies
- Synonyms for better matching
- Context relationships

## Architecture

1. **Knowledge Graph Layer** (MeTTa)
   - Schema definition
   - Data storage
   - Query processing

2. **LLM Layer** (Gemini 2.0)
   - Natural language understanding
   - Response generation
   - Context integration

3. **Graph RAG Layer**
   - Context retrieval
   - Knowledge integration
   - Response enhancement

4. **API Layer** (FastAPI)
   - RESTful endpoints
   - Request/response handling
   - Data validation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License 