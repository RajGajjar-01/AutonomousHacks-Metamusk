"""
Quick test script to verify LangGraph setup.

Run this after installing dependencies to ensure everything works.
"""

import sys
import os
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.graphs.debug_graph import invoke_debug_workflow


async def main():
    print("\n🚀 Quick LangGraph Test\n")
    print("=" * 60)
    
    # Test code with an error
    test_code = """
def add(a):
    return a + b
"""
    
    print("Testing with code:")
    print(test_code)
    print("=" * 60)
    
    try:
        result = await invoke_debug_workflow(
            request_id="quick-test",
            code=test_code,
            language="python",
            max_iterations=2
        )
        
        print("\n✅ WORKFLOW COMPLETED\n")
        print(f"Status: {result['workflow_status']}")
        print(f"Success: {result['success']}")
        print(f"Message: {result['message']}")
        print(f"\nErrors Found: {result.get('total_errors', 0)}")
        print(f"Changes Made: {result.get('total_changes', 0)}")
        print(f"Agents Involved: {', '.join(result['metadata']['agents_involved'])}")
        
        if result.get('fixed_code'):
            print(f"\nFixed Code:\n{result['fixed_code']}")
        
        print("\n" + "=" * 60)
        print("✅ LangGraph is working correctly!")
        print("=" * 60)
        
        return 0
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
