from typing import List, Dict, Any, Optional
import os
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
                              history: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Generate a response using Gemini with context from the knowledge graph.
        
        Args:
            question: User's question
            context: Relevant context from knowledge graph
            history: Chat history for context
            
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

QUESTION: {question}

ANSWER: """
        
        # Generate response using the client
        response = client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        return response.text
    
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