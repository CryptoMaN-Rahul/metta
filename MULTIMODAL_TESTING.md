# Testing Multimodal Functionality

This guide explains how to test the multimodal capabilities of the FAQ chatbot.

## Prerequisites

- The chatbot server is running at http://localhost:8000
- You have a Gemini API key (for direct API testing)
- You have Python installed with the required packages

## Option 1: Using the Backend API (Recommended)

This approach uses our backend API to handle the image processing and Gemini API calls.

### Using the HTML Form

1. Open the `test_multimodal_backend.html` file in your browser
2. Enter your question in the "Question" field
3. Upload an image using the file selector
4. Click "Submit" to send the request
5. The response will be displayed below the form
6. Your chat history will be maintained and displayed
7. Entities extracted from the image will be shown in a separate section

### Using the Python Script

```bash
# Install required packages
pip install requests

# Run the script with an image and a question
python test_multimodal.py path/to/your/image.jpg "What is in this image?"

# Run in interactive mode to maintain conversation history
python test_multimodal.py path/to/your/image.jpg "What is in this image?" --interactive
```

In interactive mode, you can:
- Continue the conversation with follow-up questions
- Change the image by typing `image path/to/new/image.jpg`
- Exit by typing `exit`

## Option 2: Direct Gemini API Integration

This approach communicates directly with the Gemini API, bypassing our backend.

### Using the HTML Form

1. Open the `test_multimodal_direct.html` file in your browser
2. Enter your Gemini API key in the "Gemini API Key" field
3. Enter your question in the "Question" field
4. Upload an image using the file selector
5. Click "Submit" to send the request
6. The response will be displayed below the form

## How It Works

### Backend API Approach

1. The image is uploaded to our server
2. Our server processes the image and extracts relevant entities
3. Extracted entities are added to the knowledge graph
4. The server enhances the query with extracted entity information
5. The knowledge graph is queried for relevant context
6. The server sends the image, enhanced query, and context to Gemini API
7. Gemini processes the image, query, and context and returns a response
8. The response is returned to the client along with:
   - Extracted entities
   - Updated chat history
   - Knowledge graph context

### Direct API Approach

1. The image is uploaded directly to Gemini's file storage API
2. The file URI is obtained from the upload response
3. A request is sent to Gemini's generateContent API with the file URI and question
4. Gemini processes the image and question and returns a response
5. The response is displayed to the user

## Knowledge Graph Integration

The multimodal functionality is fully integrated with our knowledge graph:

1. **Entity Extraction**: Entities are automatically extracted from uploaded images
2. **Knowledge Graph Updates**: Extracted entities are added to the knowledge graph
3. **Context Enhancement**: Responses are enhanced with knowledge graph context
4. **Query Augmentation**: User queries are enhanced with extracted entity information

## Chat History

The system maintains chat history across interactions:

1. Previous messages are stored and sent with each new request
2. The LLM uses this history to provide contextual responses
3. The history is displayed in the UI for reference
4. In the Python script's interactive mode, history is maintained across multiple questions

## Troubleshooting

### CORS Issues

If you encounter CORS issues with the direct API approach, you may need to use a CORS proxy or run the HTML file from a local server.

### API Key Issues

Make sure your Gemini API key has access to the multimodal capabilities. You can check this in the Google AI Studio.

### File Size Limitations

Gemini has file size limitations. If your image is too large, try resizing it before uploading.

### Entity Extraction Failures

If entity extraction fails, the system will still process the image and question, but without the benefit of extracted entities.

## Example Images to Test

Here are some suggestions for images to test with:

1. A photograph of a landmark (e.g., "What landmark is this?")
2. A diagram or chart (e.g., "Explain this diagram")
3. A screenshot of code (e.g., "What does this code do?")
4. A photograph of an object (e.g., "What is this object?")
5. A photograph with text (e.g., "What does the text in this image say?")

Try asking follow-up questions about the same image to test the chat history functionality. 