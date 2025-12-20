#!/usr/bin/env python3
"""
Quick test script to verify backend setup
"""
import os
from dotenv import load_dotenv

load_dotenv()

def check_setup():
    print("=" * 50)
    print("Backend Setup Check")
    print("=" * 50)
    
    # Check Python version
    import sys
    print(f"\n✓ Python version: {sys.version.split()[0]}")
    
    # Check environment variables
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    groq_key = os.getenv("GROQ_API_KEY", "")
    
    print(f"\n{'✓' if gemini_key else '✗'} GEMINI_API_KEY: {'Set' if gemini_key else 'NOT SET'}")
    print(f"{'✓' if groq_key else '✗'} GROQ_API_KEY: {'Set (optional)' if groq_key else 'NOT SET (optional)'}")
    
    # Check required packages
    print("\nChecking required packages...")
    required_packages = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("pydantic", "pydantic"),
        ("google-generativeai", "google.generativeai"),
        ("groq", "groq"),
        ("httpx", "httpx"),
        ("python-dotenv", "dotenv")
    ]
    
    missing_packages = []
    for package_name, import_name in required_packages:
        try:
            __import__(import_name.replace("-", "_").split(".")[0])
            print(f"  ✓ {package_name}")
        except ImportError:
            print(f"  ✗ {package_name} - MISSING")
            missing_packages.append(package_name)
    
    # Summary
    print("\n" + "=" * 50)
    if not gemini_key:
        print("⚠️  WARNING: GEMINI_API_KEY not set in .env")
        print("   Please add your API key to backend/.env")
    
    if missing_packages:
        print(f"⚠️  WARNING: Missing packages: {', '.join(missing_packages)}")
        print("   Run: pip install -r requirements.txt")
    
    if gemini_key and not missing_packages:
        print("✓ Backend setup looks good!")
        print("\nTo start the server, run:")
        print("  ./start.sh")
        print("  or")
        print("  uvicorn app.main:app --reload")
    
    print("=" * 50)

if __name__ == "__main__":
    check_setup()
