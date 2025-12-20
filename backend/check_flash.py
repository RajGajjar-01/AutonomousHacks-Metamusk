
import google.generativeai as genai
from dotenv import load_dotenv
import os
import sys

# Set encoding to utf-8 for stdout
sys.stdout.reconfigure(encoding='utf-8')

load_dotenv(dotenv_path="backend/.env")
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

print("---START---")
try:
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content("Hello")
    print("models/gemini-1.5-flash: OK")
except Exception as e:
    print(f"models/gemini-1.5-flash: FAIL - {e}")

try:
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Hello")
    print("gemini-1.5-flash: OK")
except Exception as e:
    print(f"gemini-1.5-flash: FAIL - {e}")
print("---END---")
