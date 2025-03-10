# Domain-Specific FAQ Chatbot with Knowledge Graph Integration

A powerful FAQ chatbot that combines MeTTa knowledge graphs with Google's Gemini 2.0 LLM for enhanced, context-aware responses. Now with multimodal capabilities and automatic knowledge extraction!

## Features

- **Knowledge Graph Integration**: Uses MeTTa for structured knowledge representation
- **LLM Integration**: Leverages Google Gemini 2.0 for natural language understanding
- **Graph RAG**: Retrieval-Augmented Generation for context-aware responses
- **Real-time Updates**: Support for adding new FAQs, entities, and relationships
- **Context-Aware Responses**: Understands relationships and hierarchies within the domain
- **REST API**: FastAPI-based endpoints for easy integration
- **Multimodal Support**: Process and respond to images and videos
- **Automatic Knowledge Extraction**: Extract entities, relationships, and FAQs from text and images

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
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

### Chat Endpoints

#### Text-Only Chat
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

#### Multimodal Chat
```http
POST /chat/multimodal
Content-Type: multipart/form-data

text: What is shown in this image?
files: [image1.jpg, image2.jpg]
history: [{"user": "Previous question", "assistant": "Previous answer"}]
```

### Knowledge Management Endpoints

#### Add FAQ Entry
```http
POST /faq
Content-Type: application/json

{
    "question": "What is...",
    "answer": "The answer is...",
    "category": "General",
    "concepts": "concept1 concept2 concept3"
}
```

#### Add Entity
```http
POST /entity
Content-Type: application/json

{
    "name": "EntityName",
    "entity_type": "Type",
    "properties": {
        "key": {
            "value": "property value",
            "metadata": "source: documentation confidence: 0.9"
        }
    }
}
```

#### Add Relationship
```http
POST /relationship
Content-Type: application/json

{
    "from_entity": "Entity1",
    "relationship_type": "RelationType",
    "to_entity": "Entity2",
    "context": "relationship_context confidence: 0.85"
}
```

### Automatic Knowledge Extraction Endpoints

#### Extract from Text
```http
POST /extract/text
Content-Type: application/json

{
    "text": "Your text content here..."
}
```

#### Extract from Document
```http
POST /extract/document
Content-Type: application/json

{
    "text": "Your long document content here..."
}
```

#### Extract from Image
```http
POST /extract/image
Content-Type: multipart/form-data

file: image.jpg
```

## Production Deployment

### Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t faq-chatbot .
   ```

2. Run the container:
   ```bash
   docker run -d -p 8000:8000 --env-file .env --name faq-chatbot faq-chatbot
   ```

### Kubernetes Deployment

1. Create a Kubernetes deployment:
   ```bash
   kubectl apply -f k8s/deployment.yaml
   ```

2. Create a service:
   ```bash
   kubectl apply -f k8s/service.yaml
   ```

3. Create a ConfigMap for environment variables:
   ```bash
   kubectl apply -f k8s/configmap.yaml
   ```

### Scaling Considerations

1. **Database Scaling**: For production environments with large knowledge graphs, consider using a dedicated graph database like Neo4j or Amazon Neptune instead of in-memory MeTTa storage.

2. **Horizontal Scaling**: Deploy multiple instances behind a load balancer for high availability and throughput.

3. **Caching**: Implement Redis or Memcached for caching frequent queries and responses.

4. **Monitoring**: Set up Prometheus and Grafana for monitoring API performance and usage.

5. **Rate Limiting**: Implement rate limiting to prevent abuse and ensure fair usage.

## Architecture

1. **Knowledge Graph Layer** (MeTTa)
   - Schema definition
   - Data storage
   - Query processing

2. **LLM Layer** (Gemini 2.0)
   - Natural language understanding
   - Response generation
   - Context integration
   - Multimodal processing

3. **Graph RAG Layer**
   - Context retrieval
   - Knowledge integration
   - Response enhancement

4. **API Layer** (FastAPI)
   - RESTful endpoints
   - Request/response handling
   - Data validation

5. **Automatic Extraction Layer**
   - Entity extraction
   - Relationship extraction
   - FAQ extraction
   - Background processing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License 