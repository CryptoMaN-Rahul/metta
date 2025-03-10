from typing import List, Dict, Any, Optional, Union, BinaryIO
import os
import base64
from pathlib import Path
import mimetypes
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini client
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

class GeminiLLM:
    def __init__(self, model_name: str = 'gemini-2.0-flash'):
        """Initialize Gemini LLM with specified model."""
        self.model_name = model_name
        
    async def generate_response(self, 
                              question: str, 
                              context: List[Dict[str, Any]], 
                              history: Optional[List[Dict[str, str]]] = None,
                              media_files: Optional[List[Dict[str, Any]]] = None) -> str:
        """
        Generate a response using Gemini with context from the knowledge graph.
        
        Args:
            question: User's question
            context: Relevant context from knowledge graph
            history: Chat history for context
            media_files: List of media files (images, videos, etc.)
            
        Returns:
            str: Generated response
        """
        # Format context for the prompt
        context_str = self._format_context(context)
        
        # Format chat history if provided
        history_str = self._format_history(history) if history else ""
        
        # Construct the prompt with enhanced instructions
        prompt = f"""You are a domain-specific FAQ chatbot powered by a knowledge graph. Your goal is to provide accurate, 
contextual, and insightful answers based on the provided information.

CONTEXT INFORMATION:
{context_str}

CHAT HISTORY:
{history_str}

INSTRUCTIONS:
1. Use the provided context to answer the question accurately
2. If multiple pieces of information are relevant, synthesize them into a coherent response
3. If you find relationships between concepts in the context, explain them
4. Include relevant examples or definitions when they help clarify the answer
5. If the context includes category hierarchies or synonyms, use them to provide more comprehensive answers
6. When confidence scores or weights are provided, prioritize information accordingly
7. If you're not completely certain about something, acknowledge the uncertainty
8. If the context doesn't contain enough information to answer fully, say so
9. If media files are provided, analyze and describe them in your response

QUESTION: {question}

ANSWER: """
        
        # Prepare contents for the API call
        contents = []
        
        # Add text prompt
        contents.append(prompt)
        
        # Add media files if provided
        if media_files:
            for media_file in media_files:
                if media_file['type'] == 'image':
                    # Add image to contents
                    contents.append(self._create_image_part(media_file['data'], media_file['mime_type']))
                elif media_file['type'] == 'video':
                    # For videos, we can extract frames or use the thumbnail
                    # This is a simplified approach - in production, you'd want to extract key frames
                    if 'thumbnail' in media_file:
                        contents.append(self._create_image_part(media_file['thumbnail'], 'image/jpeg'))
        
        # Generate response using the client
        response = client.models.generate_content(
            model=self.model_name,
            contents=contents
        )
        return response.text
    
    def _create_image_part(self, image_data: Union[str, bytes, BinaryIO], mime_type: str = None) -> Dict:
        """Create an image part for the Gemini API."""
        if isinstance(image_data, str):
            # If it's a file path
            if Path(image_data).exists():
                with open(image_data, "rb") as f:
                    image_bytes = f.read()
                if not mime_type:
                    mime_type = mimetypes.guess_type(image_data)[0]
            # If it's a base64 string
            else:
                image_bytes = base64.b64decode(image_data)
                mime_type = mime_type or "image/jpeg"  # Default to JPEG if not specified
        elif isinstance(image_data, bytes):
            image_bytes = image_data
            mime_type = mime_type or "image/jpeg"  # Default to JPEG if not specified
        else:
            # Assume it's a file-like object
            image_bytes = image_data.read()
            mime_type = mime_type or "image/jpeg"  # Default to JPEG if not specified
            
        # Create image part using the Gemini API
        return genai.types.Part.from_data(
            data=image_bytes,
            mime_type=mime_type
        )
    
    def _format_context(self, context: List[Dict[str, Any]]) -> str:
        """Format knowledge graph context into a structured string."""
        sections = []
        
        # Process FAQs
        faqs = [item['faq'] for item in context if 'faq' in item]
        if faqs:
            faq_section = "RELEVANT FAQs:\n" + "\n\n".join([
                f"Q: {faq['question']}\n"
                f"A: {faq['answer']}\n"
                f"Category: {faq.get('category', 'General')}\n"
                f"Match Type: {faq.get('match_type', 'direct')}"
                for faq in faqs
            ])
            sections.append(faq_section)
        
        # Process Entities
        entities = [item['entity'] for item in context if 'entity' in item]
        if entities:
            entity_section = "RELEVANT ENTITIES:\n" + "\n\n".join([
                f"Entity: {entity['name']} (Type: {entity['type']})\n"
                f"Properties:\n" + "\n".join([
                    f"- {key}: {value['value']} "
                    f"(Metadata: {value['metadata']})"
                    for key, value in entity['properties'].items()
                ]) + "\n"
                f"Relationships:\n" + "\n".join([
                    f"- {rel['to']} ({rel['type']}) "
                    f"Context: {rel['context']}"
                    for rel in entity['relations']
                ])
                for entity in entities
            ])
            sections.append(entity_section)
        
        # Process Category Hierarchies
        hierarchies = [item['category_hierarchy'] for item in context if 'category_hierarchy' in item]
        if hierarchies:
            hierarchy_section = "CATEGORY HIERARCHIES:\n" + "\n".join([
                f"Category: {h['category']}\n"
                f"Parent: {h['parent']}\n"
                f"Description: {h['description']}"
                for h in hierarchies
            ])
            sections.append(hierarchy_section)
        
        # Process Context Relationships
        context_rels = [item['context_relationship'] for item in context if 'context_relationship' in item]
        if context_rels:
            context_section = "CONTEXTUAL RELATIONSHIPS:\n" + "\n".join([
                f"- {rel['context']} (Weight: {rel['weight']})"
                for rel in context_rels
            ])
            sections.append(context_section)
        
        return "\n\n".join(sections)
    
    def _format_history(self, history: List[Dict[str, str]]) -> str:
        """Format chat history into a structured string."""
        if not history:
            return ""
            
        return "Previous conversation:\n" + "\n\n".join([
            f"User: {h['user']}\n"
            f"Assistant: {h['assistant']}"
            for h in history
        ]) 