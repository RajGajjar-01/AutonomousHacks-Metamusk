"""Test individual agents"""
import sys
import os
import asyncio

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.agents.scanner_agent import ScannerAgent
from app.agents.fixer_agent import FixerAgent
from app.agents.validator_agent import ValidatorAgent
from app.core.logger import get_logger

logger = get_logger()

# Test code with intentional error
TEST_CODE = """
def add(a):
    return a + b
"""

async def test_scanner():
    """Test Scanner Agent"""
    print("\n" + "=" * 60)
    print("TESTING SCANNER AGENT")
    print("=" * 60)
    
    try:
        scanner = ScannerAgent()
        result = await scanner.execute({
            "request_id": "test-001",
            "code": TEST_CODE,
            "language": "python"
        })
        
        print(f"Status: {result.get('status')}")
        print(f"Errors found: {result.get('total_errors')}")
        print(f"Warnings found: {result.get('total_warnings')}")
        
        if result.get('errors'):
            print("\nErrors:")
            for error in result['errors']:
                print(f"  - {error.get('message')}")
        
        print("✓ Scanner Agent is working!")
        return True, result
    except Exception as e:
        print(f"✗ Scanner Agent failed: {str(e)}")
        return False, None

async def test_fixer(scanner_result):
    """Test Fixer Agent"""
    print("\n" + "=" * 60)
    print("TESTING FIXER AGENT")
    print("=" * 60)
    
    if not scanner_result:
        print("✗ Skipping (Scanner failed)")
        return False, None
    
    try:
        fixer = FixerAgent()
        result = await fixer.execute({
            "request_id": "test-001",
            "original_code": TEST_CODE,
            "language": "python",
            "scanner_output": scanner_result
        })
        
        print(f"Status: {result.get('status')}")
        print(f"Changes made: {result.get('total_changes')}")
        print(f"\nFixed code:\n{result.get('fixed_code')}")
        
        print("✓ Fixer Agent is working!")
        return True, result
    except Exception as e:
        print(f"✗ Fixer Agent failed: {str(e)}")
        return False, None

async def test_validator(scanner_result, fixer_result):
    """Test Validator Agent"""
    print("\n" + "=" * 60)
    print("TESTING VALIDATOR AGENT")
    print("=" * 60)
    
    if not scanner_result or not fixer_result:
        print("✗ Skipping (Previous agents failed)")
        return False, None
    
    try:
        validator = ValidatorAgent()
        result = await validator.execute({
            "request_id": "test-001",
            "original_code": TEST_CODE,
            "fixed_code": fixer_result.get('fixed_code'),
            "language": "python",
            "scanner_output": scanner_result,
            "fixer_output": fixer_result
        })
        
        print(f"Status: {result.get('status')}")
        print(f"Validation: {result.get('validation_status')}")
        print(f"Confidence: {result.get('confidence_score')}")
        
        print("✓ Validator Agent is working!")
        return True, result
    except Exception as e:
        print(f"✗ Validator Agent failed: {str(e)}")
        return False, None

async def main():
    """Main test function"""
    print("\n🤖 AGENT TESTING\n")
    print(f"Test code:\n{TEST_CODE}")
    
    scanner_ok, scanner_result = await test_scanner()
    fixer_ok, fixer_result = await test_fixer(scanner_result)
    validator_ok, validator_result = await test_validator(scanner_result, fixer_result)
    
    print("\n" + "=" * 60)
    print("FINAL RESULT")
    print("=" * 60)
    
    if scanner_ok and fixer_ok and validator_ok:
        print("✓ All agents are working correctly!")
        return 0
    else:
        print("✗ Some agents failed.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
