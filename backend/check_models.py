import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not found in environment variables")
    exit(1)

genai.configure(api_key=api_key)

print(f"Checking available models for key: {api_key[:5]}...")

try:
    print("\n--- Available Models ---")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Name: {m.name}")
            print(f"Display Name: {m.display_name}")
            print("-" * 20)
            
    print("\nCheck complete.")
except Exception as e:
    print(f"\nError listing models: {e}")
