
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="backend/.env")

api_key = os.getenv("GEMINI_API_KEY")
api_key="AIzaSyAgZ5LF8elH7k4t2YGczGA8r03jWslW-TM"
if not api_key:
    print("No API Key found")
    exit(1)

genai.configure(api_key=api_key)

try:
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content("Hello, this is a test.")
    print("Success! Response:", response.text)
except Exception as e:
    print("Error with models/gemini-1.5-flash:", e)
    
try:
    model2 = genai.GenerativeModel("gemini-1.5-flash")
    response2 = model2.generate_content("Hello, this is a test 2.")
    print("Success with short name! Response:", response2.text)
except Exception as e:
    print("Error with gemini-1.5-flash:", e)
