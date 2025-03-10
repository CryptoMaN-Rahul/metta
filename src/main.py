import os
from typing import List, Dict, Optional, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from chat.llm import GeminiLLM
from chat.rag import GraphRAG

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Domain-Specific FAQ Chatbot",
    description="A chatbot that combines knowledge graphs with LLM for enhanced FAQ responses",
    version="1.0.0"
)

# Initialize components
llm = GeminiLLM()
rag = GraphRAG()

# Load knowledge base
@app.on_event("startup")
async def startup_event():
    """Load knowledge base on startup."""
    try:
        rag.load_knowledge_base(
            "src/knowledge_graph/schema.metta",
            "src/knowledge_graph/data.metta"
        )
    except Exception as e:
        print(f"Error loading knowledge base: {e}")

# Pydantic models for request/response validation
class Question(BaseModel):
    text: str
    history: Optional[List[Dict[str, str]]] = None

class Answer(BaseModel):
    text: str
    context: List[Dict]

class FAQEntry(BaseModel):
    question: str
    answer: str
    category: str

class PropertyValue(BaseModel):
    value: str
    metadata: str

class Entity(BaseModel):
    name: str
    entity_type: str
    properties: Optional[Dict[str, PropertyValue]] = None

class Relationship(BaseModel):
    from_entity: str
    relationship_type: str
    to_entity: str
    context: Optional[str] = ""

@app.post("/chat", response_model=Answer)
async def chat(question: Question):
    """
    Get an answer to a question using the knowledge graph and LLM.
    """
    try:
        # Query knowledge graph for context
        context = rag.query_context(question.text)
        
        # Generate response using LLM with context
        response = await llm.generate_response(
            question=question.text,
            context=context,
            history=question.history
        )
        
        return Answer(text=response, context=context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/faq")
async def add_faq(faq: FAQEntry):
    """Add a new FAQ entry to the knowledge graph."""
    try:
        rag.add_faq(faq.question, faq.answer, faq.category)
        return {"message": "FAQ added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/entity")
async def add_entity(entity: Entity):
    """Add a new entity to the knowledge graph."""
    try:
        properties_dict = {
            key: {"value": prop.value, "metadata": prop.metadata}
            for key, prop in entity.properties.items()
        } if entity.properties else None
        
        rag.add_entity(entity.name, entity.entity_type, properties_dict)
        return {"message": "Entity added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/relationship")
async def add_relationship(relationship: Relationship):
    """Add a new relationship between entities."""
    try:
        rag.add_relationship(
            relationship.from_entity,
            relationship.relationship_type,
            relationship.to_entity,
            relationship.context
        )
        return {"message": "Relationship added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 