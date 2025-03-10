Google Gen AI SDK
pypi

https://github.com/googleapis/python-genai

google-genai is an initial Python client library for interacting with Google’s Generative AI APIs.

Google Gen AI Python SDK provides an interface for developers to integrate Google’s generative models into their Python applications. It supports the Gemini Developer API and Vertex AI APIs.

Installation
pip install google-genai
Imports
from google import genai
from google.genai import types
Create a client
Please run one of the following code blocks to create a client for different services (Gemini Developer API or Vertex AI). Feel free to switch the client and run all the examples to see how it behaves under different APIs.

# Only run this block for Gemini Developer API
client = genai.Client(api_key='GEMINI_API_KEY')
# Only run this block for Vertex AI API
client = genai.Client(
    vertexai=True, project='your-project-id', location='us-central1'
)
(Optional) Using environment variables:

You can create a client by configuring the necessary environmental variables. Configuration setup instructions depends on whether the user is using the ML Dev Gemini API or the Vertex AI Gemini API.

Gemini Developer API: Set GOOGLE_API_KEY as shown below:

export GOOGLE_API_KEY='your-api-key'
Vertex AI Gemini API: Set GOOGLE_GENAI_USE_VERTEXAI, GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION, as shown below:

export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_PROJECT='your-project-id'
export GOOGLE_CLOUD_LOCATION='us-central1'
client = genai.Client()
API Selection
By default, the SDK uses the beta API endpoints provided by Google to support preview features in the APIs. The stable API endpoints can be selected by setting the API version to v1.

To set the API version use http_options. For example, to set the API version to v1 for Vertex AI:

client = genai.Client(
    vertexai=True,
    project='your-project-id',
    location='us-central1',
    http_options=types.HttpOptions(api_version='v1')
)
To set the API version to v1alpha for the Gemini Developer API:

# Only run this block for Gemini Developer API
client = genai.Client(
    api_key='GEMINI_API_KEY',
    http_options=types.HttpOptions(api_version='v1alpha')
)
Types
Parameter types can be specified as either dictionaries(TypedDict) or Pydantic Models. Pydantic model types are available in the types module.

Models
The client.models modules exposes model inferencing and model getters.

Generate Content
with text content
response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents='Why is the sky blue?'
)
print(response.text)
with uploaded file (Gemini API only)
download the file in console.

!wget -q https://storage.googleapis.com/generativeai-downloads/data/a11.txt
python code.

file = client.files.upload(file='a11.txt')
response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=['Could you summarize this file?', file]
)
print(response.text)
How to structure contents argument for generate_content
The SDK always converts the inputs to the contents argument into list[types.Content]. The following shows some common ways to provide your inputs.

Provide a list[types.Content]
This is the canonical way to provide contents, SDK will not do any conversion.

Provide a types.Content instance
contents = types.Content(
role='user',
parts=[types.Part.from_text(text='Why is the sky blue?')]
)
SDK converts this to

[
types.Content(
    role='user',
    parts=[types.Part.from_text(text='Why is the sky blue?')]
)
]
Provide a string
contents='Why is the sky blue?'
The SDK will assume this is a text part, and it converts this into the following:

[
types.UserContent(
    parts=[
    types.Part.from_text(text='Why is the sky blue?')
    ]
)
]
Where a types.UserContent is a subclass of types.Content, it sets the role field to be user.

Provide a list of string
The SDK assumes these are 2 text parts, it converts this into a single content, like the following:

[
types.UserContent(
    parts=[
    types.Part.from_text(text='Why is the sky blue?'),
    types.Part.from_text(text='Why is the cloud white?'),
    ]
)
]
Where a types.UserContent is a subclass of types.Content, the role field in types.UserContent is fixed to be user.

Provide a function call part
contents = types.Part.from_function_call(
name='get_weather_by_location',
args={'location': 'Boston'}
)
The SDK converts a function call part to a content with a model role:

[
types.ModelContent(
    parts=[
    types.Part.from_function_call(
        name='get_weather_by_location',
        args={'location': 'Boston'}
    )
    ]
)
]
Where a types.ModelContent is a subclass of types.Content, the role field in types.ModelContent is fixed to be model.

Provide a list of function call parts
contents = [
types.Part.from_function_call(
    name='get_weather_by_location',
    args={'location': 'Boston'}
),
types.Part.from_function_call(
    name='get_weather_by_location',
    args={'location': 'New York'}
),
]
The SDK converts a list of function call parts to the a content with a model role:

[
types.ModelContent(
    parts=[
    types.Part.from_function_call(
        name='get_weather_by_location',
        args={'location': 'Boston'}
    ),
    types.Part.from_function_call(
        name='get_weather_by_location',
        args={'location': 'New York'}
    )
    ]
)
]
Where a types.ModelContent is a subclass of types.Content, the role field in types.ModelContent is fixed to be model.

Provide a non function call part
contents = types.Part.from_uri(
file_uri: 'gs://generativeai-downloads/images/scones.jpg',
mime_type: 'image/jpeg',
)
The SDK converts all non function call parts into a content with a user role.

[
types.UserContent(parts=[
    types.Part.from_uri(
    file_uri: 'gs://generativeai-downloads/images/scones.jpg',
    mime_type: 'image/jpeg',
    )
])
]
Provide a list of non function call parts
contents = [
types.Part.from_text('What is this image about?'),
types.Part.from_uri(
    file_uri: 'gs://generativeai-downloads/images/scones.jpg',
    mime_type: 'image/jpeg',
)
]
The SDK will convert the list of parts into a content with a user role

[
types.UserContent(
    parts=[
    types.Part.from_text('What is this image about?'),
    types.Part.from_uri(
        file_uri: 'gs://generativeai-downloads/images/scones.jpg',
        mime_type: 'image/jpeg',
    )
    ]
)
]
Mix types in contents
You can also provide a list of types.ContentUnion. The SDK leaves items of types.Content as is, it groups consecutive non function call parts into a single types.UserContent, and it groups consecutive function call parts into a single types.ModelContent.

If you put a list within a list, the inner list can only contain types.PartUnion items. The SDK will convert the inner list into a single types.UserContent.

System Instructions and Other Configs
The output of the model can be influenced by several optional settings available in generate_content’s config parameter. For example, the variability and length of the output can be influenced by the temperature and max_output_tokens respectively.

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='high',
    config=types.GenerateContentConfig(
        system_instruction='I say high, you say low',
        max_output_tokens=3,
        temperature=0.3,
    ),
)
print(response.text)
Typed Config
All API methods support Pydantic types for parameters as well as dictionaries. You can get the type from google.genai.types.

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=types.Part.from_text(text='Why is the sky blue?'),
    config=types.GenerateContentConfig(
        temperature=0,
        top_p=0.95,
        top_k=20,
        candidate_count=1,
        seed=5,
        max_output_tokens=100,
        stop_sequences=['STOP!'],
        presence_penalty=0.0,
        frequency_penalty=0.0,
    ),
)

print(response.text)

