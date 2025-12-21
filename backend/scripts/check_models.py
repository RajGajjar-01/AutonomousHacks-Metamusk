"""Check AI model availability and connectivity"""
import sys
import os
import asyncio

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.ai_clients import gemini_client, groq_client
from app.core.logger import get_logger

logger = get_logger()

async def test_gemini():
    """Test Gemini API connectivity"""
    print("\n" + "=" * 60)
    print("TESTING GEMINI API")
    print("=" * 60)
    
    try:
        response = await gemini_client.generate(
            "Respond with exactly: {'status': 'ok'}",
            temperature=0.0
        )
        print(f"Response: {response[:100]}...")
        print("✓ Gemini API is working!")
        return True
    except Exception as e:
        print(f"✗ Gemini API failed: {str(e)}")
        return False

async def test_groq():
    """Test Groq API connectivity"""
    print("\n" + "=" * 60)
    print("TESTING GROQ API")
    print("=" * 60)
    
    try:
        response = await groq_client.generate(
            "Respond with exactly: {'status': 'ok'}",
            temperature=0.0
        )
        print(f"Response: {response[:100]}...")
        print("✓ Groq API is working!")
        return True
    except Exception as e:
        print(f"✗ Groq API failed: {str(e)}")
        return False

async def main():
    """Main test function"""
    print("\n🤖 AI MODEL CONNECTIVITY TEST\n")
    
    gemini_ok = await test_gemini()
    groq_ok = await test_groq()
    
    print("\n" + "=" * 60)
    print("FINAL RESULT")
    print("=" * 60)
    
    if gemini_ok and groq_ok:
        print("✓ All AI models are accessible!")
        return 0
    else:
        print("✗ Some AI models are not accessible.")
        print("\nPlease check your API keys in .env file:")
        if not gemini_ok:
            print("  - GEMINI_API_KEY")
        if not groq_ok:
            print("  - GROQ_API_KEY")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
