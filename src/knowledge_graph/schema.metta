;; Define the basic entity types
(= (Entity $name $type) (HasType $name $type))

;; Define relationships between entities
(= (Relationship $from $type $to) (HasRelation $from $type $to))

;; Define properties for entities
(= (Property $entity $key $value) (HasProperty $entity $key $value))

;; Define FAQ entries
(= (FAQ $question $answer $category) (HasFAQ $question $answer $category))

;; Define category hierarchies
(= (Category $name $parent) (HasParent $name $parent))

;; Define synonyms for better matching
(= (Synonym $term $equivalent) (HasSynonym $term $equivalent))

;; Define context relationships
(= (Context $entity $context) (HasContext $entity $context))

;; Helper function to get all properties of an entity
(= (GetProperties $entity)
   (match &self (Property $entity $key $value)
          (Property $key $value)))

;; Helper function to get related entities
(= (GetRelated $entity)
   (match &self (Relationship $entity $type $to)
          (Related $to $type)))

;; Helper function to get FAQs by category
(= (GetFAQsByCategory $category)
   (match &self (FAQ $question $answer $category)
          (FAQEntry $question $answer))) 