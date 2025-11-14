# ------------------------------------------------------------
#  model_router_demo.py
# ------------------------------------------------------------
import os
import json
from typing import List, Dict

from dotenv import load_dotenv
from openai import AzureOpenAI, APIError, RateLimitError

import base64
import requests  # For fetching image URLs


# ------------------------------------------------------------
# 1. Load environment variables
# ------------------------------------------------------------
load_dotenv()                     # expects AZURE_OPENAI_API_KEY & AZURE_OPENAI_ENDPOINT

client = AzureOpenAI(
    api_key=os.getenv("MODEL_ROUTER_AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("MODEL_ROUTERAZURE_OPENAI_ENDPOINT"),
    api_version="2024-12-01-preview",   # keep the preview version that supports the router
)

ROUTER_DEPLOYMENT = "model-router"

# ------------------------------------------------------------
# 2. Prompts that exercise different model strengths
# ------------------------------------------------------------
prompts: List[Dict[str, str]] = [
    # 1. Ultra-simple fact → usually GPT-3.5-turbo
    {
        "role": "user",
        "content": "What is the capital of France?"
    },

    # 2. Short reasoning + math → often GPT-4o-mini
    {
        "role": "user",
        "content": "A car travels 120 km in 2 hours. What is its average speed in km/h? Show the calculation step-by-step."
    },

    # 3. Multi-step planning → usually GPT-4o (o-series)
    {
        "role": "user",
        "content": (
            "Plan a 5-day business trip to Berlin for 2 people. "
            "Include flights from London, 4-star hotel, daily meeting schedule, "
            "and a €1,500 total budget. List every expense."
        )
    },

    # 4. Creative / long-form writing → often GPT-4o or a larger model
    {
        "role": "user",
        "content": (
            "Write a 400-word short story about a time-travelling barista who accidentally "
            "serves coffee to Albert Einstein in 1905. Keep the tone humorous."
        )
    },
]

system_msg = {"role": "system", "content": "You are a helpful assistant."}


# ------------------------------------------------------------
# 3. Helper: call the router and pretty-print the result
# ------------------------------------------------------------
def call_router(messages: List[Dict[str, str]]) -> None:
    try:
        response = client.chat.completions.create(
            model=ROUTER_DEPLOYMENT,
            messages=messages,
            max_tokens=4096,
            temperature=0.7,
            top_p=0.95,
        )

        choice = response.choices[0]
        content = choice.message.content.strip()
        routed_model = getattr(choice.message, "model", response.model)  # router injects it here
        usage = response.usage

        print("\n" + "=" * 80)
        print(f"Prompt: {messages[-1]['content'][:70]}...")
        print(f"Routed model: {routed_model}")
        print(f"Tokens → prompt: {usage.prompt_tokens} | completion: {usage.completion_tokens} | total: {usage.total_tokens}")
        print("-" * 80)
        print(f"Answer:\n{content}")
        print("=" * 80 + "\n")

    except (APIError, RateLimitError) as e:
        print(f"\nAPI error for prompt: {messages[-1]['content'][:50]}... → {e}\n")




# Client setup
client_custom = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

client_audio = AzureOpenAI(
    api_key=os.getenv("AUDIO_AZURE_OPENAI_API_KEY"),
    api_version="2025-03-01-preview",
    azure_endpoint=os.getenv("AUDIO_AZURE_OPENAI_ENDPOINT")
)

# Deployments (update with your Azure deployments)
DEPLOYMENTS = {
    "simple": "gpt-4o-mini",  # Lightweight for facts
    "complex": "gpt-4o-2",  # Advanced for reasoning (vision-capable)
    "whisper": "gpt-4o-transcribe-diarize",  # For audio transcription
    "image": "gpt-4.1-mini" # for Image
}


def select_model(prompt: str) -> str:
    """
    Custom selection logic (inspired by Copilot Camp strategies):
    - Length < 50 chars or no reasoning keywords → simple model
    - Else → complex model
    - Images always → complex (vision-capable)
    """
    length = len(prompt)
    reasoning_keywords = ["plan", "analyze", "explain why", "compare", "budget"]
    if "image" in prompt.lower() or "[IMAGE:" in prompt:
        return DEPLOYMENTS["complex"]
    if length < 50 or not any(keyword in prompt.lower() for keyword in reasoning_keywords):
        return DEPLOYMENTS["simple"]
    return DEPLOYMENTS["complex"]


def transcribe_audio(audio_file_path: str) -> str:
    """
    Transcribe MP3 audio to text using Azure OpenAI Whisper.
    Assumes audio_file_path is a local MP3 file (<25MB).
    """
    try:
        with open(audio_file_path, "rb") as audio_file:
            transcript = client_audio.audio.transcriptions.create(
                model=DEPLOYMENTS["whisper"],
                file=audio_file,
                response_format="text"  # Or "json" for structured output
            )
        return transcript
    except Exception as e:
        return f"Transcription error: {str(e)}"


def extract_image_text(image_url_or_path: str, is_url: bool = True) -> str:
    """
    Extract text from an image using GPT-4o vision (multimodal).
    - If URL: Fetches and base64-encodes.
    - If path: Encodes local file.
    Prompts the model to "extract all visible text".
    """
    # Encode image to base64
    if is_url:
        # Fetch image from URL
        response = requests.get(image_url_or_path)
        image_data = base64.b64encode(response.content).decode('utf-8')
        print(f"image_data:: {image_data}")
        mime_type = response.headers.get('content-type', 'image/jpeg')
        print(f"mime_type :: {mime_type}")
    else:
        # Load from local path
        with open(image_url_or_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        mime_type = 'image/jpeg'  # Assume JPEG; adjust if needed

    # Vision message format
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text",
                 "text": "Extract and list all visible text from this image accurately. If no text, say 'No text detected'."},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{image_data}"
                    }
                }
            ]
        }
    ]

    response = client_custom.chat.completions.create(
        model=DEPLOYMENTS["image"],  # Must be vision-capable like gpt-4o
        messages=messages,
        max_tokens=1000,
        temperature=0.3  # Low for accurate extraction
    )

    return response.choices[0].message.content.strip()


def custom_router(messages: List[Dict]) -> Dict:
    """
    Enhanced router: Handles text, audio, or image inputs.
    - Detects special formats: [AUDIO: path] or [IMAGE: url/path]
    - For media, bypasses text routing and calls dedicated functions.
    """
    user_content = messages[-1]["content"]

    # Check for audio
    if "[AUDIO:" in user_content.upper():
        audio_path = user_content.split("[AUDIO:")[1].split("]")[0].strip()
        transcribed_text = transcribe_audio(audio_path)
        return {
            "content": f"Transcribed Audio Text: {transcribed_text}",
            "selected_model": "gpt-4o-transcribe-diarize",
            "reason": f"Audio input detected: {audio_path}"
        }

    # Check for image
    if "[IMAGE:" in user_content.upper():
        image_input = user_content.split("[IMAGE:")[1].split("]")[0].strip()
        is_url = image_input.startswith("http")
        print(f"image_input : {image_input}, is_url: {is_url}")
        extracted_text = extract_image_text(image_input, is_url=is_url)
        return {
            "content": f"Extracted Image Text: {extracted_text}",
            "selected_model": DEPLOYMENTS["image"],
            "reason": f"Image input detected: {image_input} (URL: {is_url})"
        }

    # Fallback to text routing
    selected_model = select_model(user_content)
    response = client_custom.chat.completions.create(
        model=selected_model,
        messages=messages,
        temperature=0.7,
        top_p=0.95
    )
    return {
        "content": response.choices[0].message.content,
        "selected_model": selected_model,
        "reason": f"Prompt length: {len(user_content)}, Keywords detected: {any(kw in user_content.lower() for kw in ['plan', 'analyze'])}"
    }


# Tests



# ------------------------------------------------------------
# 4. Run the demo
# ------------------------------------------------------------
if __name__ == "__main__":
    inc = 0
    for idx, user_msg in enumerate(prompts, start=1):
        messages = [system_msg, user_msg]
        inc = inc + 1
        print(f"\n--- Running test #{inc} ---")

        call_router(messages)


    system_msg = {"role": "system", "content": "You are a helpful assistant."}

    # Text prompts (original)
    text_prompts = [
        {"role": "user", "content": "What's the capital of France?"},
        {"role": "user",
         "content": "Plan a 7-day trip to Paris for a family of 4, including budget breakdowns, activities, and contingencies for rain. Assume a $2000 total budget."}
    ]

    # New media tests (uncomment and update paths/URLs)
    media_prompts = [
        {"role": "user", "content": "[AUDIO: C:\\Users\\1036383\\Documents\\checktext.mp3]"},
        # Transcribe local MP3
        {"role": "user", "content": "[IMAGE: C:\\Users\\1036383\\Documents\\plan.jpg]"}
        # Extract from URL (replace with real URL)
        # Or local: {"role": "user", "content": "[IMAGE: /path/to/local_image.jpg]"}
    ]

    prompts = text_prompts + media_prompts  # Combine for full test

    for i, user_msg in enumerate(prompts, 1):
        inc = inc + 1
        messages = [system_msg, user_msg]
        result = custom_router(messages)
        print(f"\n--- Test {inc}: {user_msg['content'][:50]}... ---")
        print(f"Selected Model/Method: {result['selected_model']}")
        print(f"Reason: {result['reason']}")
        print(f"Response: {result['content']}")
        print("-" * 80)
