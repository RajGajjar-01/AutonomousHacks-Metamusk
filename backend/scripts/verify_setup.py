"""Verify backend setup and dependencies"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.config import get_settings
from app.core.logger import get_logger

logger = get_logger()

def verify_environment():
    """Verify environment variables"""
    settings = get_settings()
    
    print("=" * 60)
    print("ENVIRONMENT VERIFICATION")
    print("=" * 60)
    
    checks = {
        "Gemini API Key": bool(settings.gemini_api_key and settings.gemini_api_key != "your_gemini_api_key_here"),
        "Groq API Key": bool(settings.groq_api_key),
        "Host": bool(settings.host),
        "Port": bool(settings.port),
    }
    
    for check, status in checks.items():
        status_str = "✓ PASS" if status else "✗ FAIL"
        print(f"{check:.<40} {status_str}")
    
    print("=" * 60)
    
    all_passed = all(checks.values())
    if all_passed:
        print("✓ All checks passed!")
    else:
        print("✗ Some checks failed. Please check your .env file.")
    
    return all_passed

def verify_imports():
    """Verify all required imports"""
    print("\n" + "=" * 60)
    print("IMPORT VERIFICATION")
    print("=" * 60)
    
    imports = {
        "FastAPI": "fastapi",
        "Pydantic": "pydantic",
        "Groq": "groq",
        "Google GenAI": "google.generativeai",
        "HTTPX": "httpx",
    }
    
    results = {}
    for name, module in imports.items():
        try:
            __import__(module)
            results[name] = True
            print(f"{name:.<40} ✓ PASS")
        except ImportError:
            results[name] = False
            print(f"{name:.<40} ✗ FAIL")
    
    print("=" * 60)
    
    all_passed = all(results.values())
    if all_passed:
        print("✓ All imports successful!")
    else:
        print("✗ Some imports failed. Run: pip install -r requirements.txt")
    
    return all_passed

def verify_structure():
    """Verify directory structure"""
    print("\n" + "=" * 60)
    print("STRUCTURE VERIFICATION")
    print("=" * 60)
    
    required_dirs = [
        "app/api",
        "app/api/routes",
        "app/agents",
        "app/agents/tools",
        "app/graphs",
        "app/core",
        "app/models",
        "app/utils",
        "scripts",
        "data/checkpoints",
        "logs",
    ]
    
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    results = {}
    for dir_path in required_dirs:
        full_path = os.path.join(base_path, dir_path)
        exists = os.path.exists(full_path)
        results[dir_path] = exists
        status_str = "✓ PASS" if exists else "✗ FAIL"
        print(f"{dir_path:.<40} {status_str}")
    
    print("=" * 60)
    
    all_passed = all(results.values())
    if all_passed:
        print("✓ All directories exist!")
    else:
        print("✗ Some directories missing.")
    
    return all_passed

if __name__ == "__main__":
    print("\n🔍 BACKEND SETUP VERIFICATION\n")
    
    env_ok = verify_environment()
    imports_ok = verify_imports()
    structure_ok = verify_structure()
    
    print("\n" + "=" * 60)
    print("FINAL RESULT")
    print("=" * 60)
    
    if env_ok and imports_ok and structure_ok:
        print("✓ Setup verification PASSED!")
        print("\nYou can now start the server with:")
        print("  cd backend && python -m app.main")
        sys.exit(0)
    else:
        print("✗ Setup verification FAILED!")
        print("\nPlease fix the issues above before starting the server.")
        sys.exit(1)
