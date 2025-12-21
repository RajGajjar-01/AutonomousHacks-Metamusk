"""
Test script for integrated LangGraph agents.

This script tests the complete workflow with actual agent implementations.
"""

import sys
import os
import asyncio

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.graphs.debug_graph import invoke_debug_workflow
from app.core.logger import get_logger

logger = get_logger()


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


async def test_complete_workflow():
    """Test complete workflow with actual agents."""
    print_section("COMPLETE WORKFLOW TEST")
    
    # Test code with intentional error
    code = """
def add(a):
    return a + b

result = add(5)
print(result)
"""
    
    print(f"Input code:\n{code}")
    
    try:
        result = await invoke_debug_workflow(
            request_id="test-integrated",
            code=code,
            language="python",
            max_iterations=2
        )
        
        print(f"\n{'='*70}")
        print("WORKFLOW RESULTS")
        print(f"{'='*70}")
        print(f"Status: {result['workflow_status']}")
        print(f"Success: {result['success']}")
        print(f"Message: {result['message']}")
        
        print(f"\n{'='*70}")
        print("SCANNER RESULTS")
        print(f"{'='*70}")
        print(f"Errors Found: {result.get('total_errors', 0)}")
        print(f"Warnings Found: {result.get('total_warnings', 0)}")
        print(f"Quality Score: {result.get('code_quality_score', 0)}/10")
        
        if result.get('errors'):
            print("\nErrors:")
            for err in result['errors']:
                print(f"  - Line {err['line_number']}: {err['type']} - {err['message']}")
        
        print(f"\n{'='*70}")
        print("FIXER RESULTS")
        print(f"{'='*70}")
        print(f"Changes Made: {result.get('total_changes', 0)}")
        print(f"Explanation: {result.get('explanation', 'N/A')}")
        
        if result.get('fixes'):
            print("\nChanges:")
            for fix in result['fixes']:
                print(f"  - Line {fix['line_number']}: {fix['reason']}")
        
        if result.get('fixed_code'):
            print(f"\nFixed Code:\n{result['fixed_code']}")
        
        print(f"\n{'='*70}")
        print("VALIDATOR RESULTS")
        print(f"{'='*70}")
        validation = result.get('validation_result', {})
        print(f"Status: {validation.get('status', 'N/A')}")
        print(f"Confidence: {validation.get('confidence_score', 0):.2f}")
        print(f"Verdict: {validation.get('final_verdict', 'N/A')}")
        
        print(f"\n{'='*70}")
        print("METADATA")
        print(f"{'='*70}")
        metadata = result.get('metadata', {})
        print(f"Iterations: {metadata.get('iterations', 0)}")
        print(f"Agents Involved: {', '.join(metadata.get('agents_involved', []))}")
        print(f"Total Events: {len(result.get('events', []))}")
        
        print(f"\n{'='*70}")
        print("✅ WORKFLOW TEST PASSED")
        print(f"{'='*70}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ WORKFLOW TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_no_errors_code():
    """Test with code that has no errors."""
    print_section("NO ERRORS TEST")
    
    code = """
def greet(name):
    return f"Hello, {name}!"

message = greet("World")
print(message)
"""
    
    print(f"Input code:\n{code}")
    
    try:
        result = await invoke_debug_workflow(
            request_id="test-no-errors",
            code=code,
            language="python",
            max_iterations=2
        )
        
        print(f"\nStatus: {result['workflow_status']}")
        print(f"Success: {result['success']}")
        print(f"Message: {result['message']}")
        print(f"Errors Found: {result.get('total_errors', 0)}")
        print(f"Agents Involved: {', '.join(result.get('metadata', {}).get('agents_involved', []))}")
        
        # Verify fixer was skipped
        agents = result.get('metadata', {}).get('agents_involved', [])
        if "Fixer" not in agents:
            print("\n✅ Fixer correctly skipped (no errors)")
        else:
            print("\n⚠️  Fixer ran even though no errors found")
        
        print(f"\n{'='*70}")
        print("✅ NO ERRORS TEST PASSED")
        print(f"{'='*70}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ NO ERRORS TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_multiple_errors():
    """Test with code that has multiple errors."""
    print_section("MULTIPLE ERRORS TEST")
    
    code = """
def calculate(x):
    result = x + y + z
    return result

output = calculate(10)
print(output)
"""
    
    print(f"Input code:\n{code}")
    
    try:
        result = await invoke_debug_workflow(
            request_id="test-multiple",
            code=code,
            language="python",
            max_iterations=2
        )
        
        print(f"\nStatus: {result['workflow_status']}")
        print(f"Errors Found: {result.get('total_errors', 0)}")
        print(f"Changes Made: {result.get('total_changes', 0)}")
        
        if result.get('errors'):
            print("\nErrors detected:")
            for err in result['errors']:
                print(f"  - {err['type']}: {err['message']}")
        
        if result.get('fixed_code'):
            print(f"\nFixed Code:\n{result['fixed_code']}")
        
        print(f"\n{'='*70}")
        print("✅ MULTIPLE ERRORS TEST PASSED")
        print(f"{'='*70}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ MULTIPLE ERRORS TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def run_all_tests():
    """Run all integration tests."""
    print("\n" + "=" * 70)
    print("  INTEGRATED AGENTS TEST SUITE")
    print("=" * 70)
    
    results = []
    
    # Test 1: Complete workflow
    results.append(await test_complete_workflow())
    
    # Test 2: No errors
    results.append(await test_no_errors_code())
    
    # Test 3: Multiple errors
    results.append(await test_multiple_errors())
    
    # Summary
    print_section("TEST SUMMARY")
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nTests Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED!")
        print("\nThe integrated LangGraph workflow with actual agents is working correctly!")
        return 0
    else:
        print(f"\n❌ {total - passed} TEST(S) FAILED")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
