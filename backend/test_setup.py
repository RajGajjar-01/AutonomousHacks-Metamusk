"""
Quick test script to verify backend setup
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 50)
print("Backend Configuration Test")
print("=" * 50)

# Check API Keys
groq_key = os.getenv("GROQ_API_KEY", "")
gemini_key = os.getenv("GEMINI_API_KEY", "")
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN", "")

print("\n✓ API Keys Status:")
print(f"  GROQ_API_KEY: {'✓ Set' if groq_key else '✗ Missing'}")
print(f"  GEMINI_API_KEY: {'✓ Set' if gemini_key else '✗ Missing (optional)'}")
print(f"  HUGGINGFACEHUB_API_TOKEN: {'✓ Set' if hf_token else '✗ Missing (optional)'}")

# Test imports
print("\n✓ Testing imports...")
try:
    from app.agents.scanner import scanner_agent
    print("  Scanner agent: ✓")
except Exception as e:
    print(f"  Scanner agent: ✗ {e}")

try:
    from app.agents.fixer import fixer_agent
    print("  Fixer agent: ✓")
except Exception as e:
    print(f"  Fixer agent: ✗ {e}")

try:
    from app.agents.validator import validator_agent
    print("  Validator agent: ✓")
except Exception as e:
    print(f"  Validator agent: ✗ {e}")

try:
    from app.agents.base import GroqChatModel, get_fallback_model
    print("  Base models: ✓")
except Exception as e:
    print(f"  Base models: ✗ {e}")

print("\n" + "=" * 50)
print("If all checks pass, the backend should work!")
print("=" * 50)
