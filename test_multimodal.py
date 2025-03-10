import requests
import json
import os
import sys
import argparse
from pathlib import Path

def test_multimodal_chat(image_path, question, api_url="http://localhost:8000/chat/multimodal", history=None):
    """
    Test the multimodal chat functionality by sending an image and a question.
    
    Args:
        image_path: Path to the image file
        question: Question to ask about the image
        api_url: URL of the multimodal chat API
        history: Optional chat history as a list of dictionaries with 'user' and 'assistant' keys
    """
    # Check if image exists
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at {image_path}")
        return
    
    # Prepare the multipart form data
    files = {
        'files': (os.path.basename(image_path), open(image_path, 'rb'), f'image/{Path(image_path).suffix[1:]}')
    }
    
    # Prepare history
    history_json = json.dumps(history) if history else json.dumps([])
    
    data = {
        'text': question,
        'history': history_json
    }
    
    print(f"Sending request to {api_url}...")
    print(f"Question: {question}")
    print(f"Image: {image_path}")
    if history:
        print(f"History: {len(history)} previous messages")
    
    try:
        # Send the request
        response = requests.post(api_url, files=files, data=data)
        
        # Check if request was successful
        if response.status_code == 200:
            result = response.json()
            
            # Display the response
            print("\nResponse:")
            print(f"Answer: {result.get('text', 'No text in response')}")
            
            # Display extracted entities if any
            if 'extracted_entities' in result and result['extracted_entities']:
                print("\nExtracted Entities:")
                for entity in result['extracted_entities']:
                    print(f"- {entity.get('name', 'Unnamed')} ({entity.get('type', 'Unknown type')})")
                    if 'properties' in entity and entity['properties']:
                        for prop_name, prop_value in entity['properties'].items():
                            if isinstance(prop_value, dict) and 'value' in prop_value:
                                print(f"  • {prop_name}: {prop_value['value']}")
                            else:
                                print(f"  • {prop_name}: {prop_value}")
            
            # Update and return history
            updated_history = result.get('history', [])
            if not updated_history and 'text' in result:
                # If no history in response, create it
                if history:
                    updated_history = history.copy()
                else:
                    updated_history = []
                updated_history.append({
                    'user': question,
                    'assistant': result['text']
                })
            
            return updated_history
        else:
            print(f"\nError: {response.status_code} {response.reason}")
            print(response.text)
            return None
    except Exception as e:
        print(f"\nException: {str(e)}")
        return None
    finally:
        # Close the file
        files['files'][1].close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test multimodal chat functionality")
    parser.add_argument("image_path", help="Path to the image file")
    parser.add_argument("question", help="Question to ask about the image")
    parser.add_argument("--url", default="http://localhost:8000/chat/multimodal", help="URL of the multimodal chat API")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode for multiple questions")
    
    args = parser.parse_args()
    
    if args.interactive:
        # Interactive mode
        history = []
        current_image = args.image_path
        
        print("Interactive mode. Type 'exit' to quit, 'image <path>' to change image.")
        
        # First question
        history = test_multimodal_chat(current_image, args.question, args.url, history)
        
        while True:
            user_input = input("\nEnter your next question (or command): ")
            
            if user_input.lower() == 'exit':
                break
            elif user_input.lower().startswith('image '):
                # Change the image
                new_image = user_input[6:].strip()
                if os.path.exists(new_image):
                    current_image = new_image
                    print(f"Image changed to: {current_image}")
                else:
                    print(f"Error: Image file not found at {new_image}")
                continue
            
            # Send the next question with the same image
            history = test_multimodal_chat(current_image, user_input, args.url, history)
            if not history:
                print("Error in conversation. Resetting history.")
                history = []
    else:
        # Single question mode
        test_multimodal_chat(args.image_path, args.question, args.url) 