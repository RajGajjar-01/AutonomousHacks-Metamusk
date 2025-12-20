import os
import google.generativeai as genai
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    # Fallback to key in code if env fails
    api_key = "AIzaSyCOo-EHzBaKEv7-RzEwOciqia00CF9RDpc"

genai.configure(api_key=api_key)

models = []
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            models.append(m.name)
except Exception as e:
    models.append(f"Error: {str(e)}")

with open("available_models.json", "w") as f:
    json.dump(models, f, indent=2)

print(f"Found {len(models)} models.")
