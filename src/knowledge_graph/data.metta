;; Sample FAQ entries with related concepts
(FAQ "What is a knowledge graph?" 
     "A knowledge graph is a network of entities, their properties, and relationships between them. It helps organize and connect information in a structured way."
     "Basics"
     "knowledge_representation data_structure graph_database semantic_web")

(FAQ "How does the chatbot use the knowledge graph?"
     "The chatbot uses the knowledge graph to understand relationships between concepts, find relevant context, and provide more accurate and detailed answers by leveraging connected information."
     "Usage"
     "chatbot knowledge_graph context_awareness semantic_search")

(FAQ "Can I add new information to the knowledge graph?"
     "Yes, you can add new FAQs, entities, and relationships through the API endpoints. The knowledge graph updates in real-time to incorporate new information."
     "Usage"
     "api knowledge_management real_time_updates data_entry")

;; Sample entities with metadata
(Entity "KnowledgeGraph" "Concept")
(Property "KnowledgeGraph" "definition" 
         "A structured representation of knowledge" 
         "source: academic_literature confidence: 0.95")
(Property "KnowledgeGraph" "purpose" 
         "To organize and connect information" 
         "source: technical_documentation confidence: 0.9")

(Entity "ChatbotSystem" "System")
(Property "ChatbotSystem" "type" 
         "FAQ Assistant" 
         "version: 1.0 status: active")
(Property "ChatbotSystem" "capability" 
         "Natural language understanding" 
         "framework: gemini confidence: 0.85")

(Entity "MeTTa" "Technology")
(Property "MeTTa" "type" 
         "Knowledge representation language" 
         "version: latest source: official_docs")
(Property "MeTTa" "purpose" 
         "Graph-based knowledge storage and querying" 
         "source: technical_spec confidence: 0.9")

(Entity "Gemini" "Technology")
(Property "Gemini" "type" 
         "Large Language Model" 
         "version: 2.0 provider: Google")
(Property "Gemini" "version" 
         "2.0" 
         "release_date: 2024 status: active")
(Property "Gemini" "provider" 
         "Google" 
         "source: official reliability: high")

;; Sample relationships with context
(Relationship "ChatbotSystem" "uses" "KnowledgeGraph" 
             "core_component integration_level: high")
(Relationship "ChatbotSystem" "uses" "MeTTa" 
             "for_knowledge_representation confidence: 0.9")
(Relationship "ChatbotSystem" "uses" "Gemini" 
             "for_natural_language_understanding confidence: 0.95")
(Relationship "KnowledgeGraph" "implementedIn" "MeTTa" 
             "primary_implementation confidence: 0.9")

;; Sample categories with descriptions
(Category "Basics" "Root" 
         "Fundamental concepts and definitions")
(Category "Usage" "Root" 
         "How to use and interact with the system")
(Category "Technical" "Root" 
         "Technical details and implementation specifics")

;; Sample synonyms with confidence scores
(Synonym "KnowledgeGraph" "KG" 0.95)
(Synonym "KnowledgeGraph" "Knowledge Base" 0.85)
(Synonym "ChatbotSystem" "FAQ Assistant" 0.9)
(Synonym "MeTTa" "Meta Language" 0.8)

;; Sample context relationships with weights
(Context "KnowledgeGraph" "semantic_search" 0.9)
(Context "KnowledgeGraph" "data_storage" 0.8)
(Context "ChatbotSystem" "user_interaction" 0.95)
(Context "MeTTa" "graph_processing" 0.9) 