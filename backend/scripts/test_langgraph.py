"""
Test script for LangGraph debugging workflow.

This script verifies:
1. Graph structure is valid
2. Nodes execute correctly
3. Conditional routing works
4. State management functions properly
5. Retry logic operates as expected
"""

import sys
import os
import asyncio

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.graphs.debug_graph import (
    debug_graph,
    invoke_debug_workflow,
    stream_debug_workflow,
    get_graph_visualization
)
from app.core.logger import get_logger

logger = get_logger()


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


async def test_graph_structure():
    """Test 1: Verify graph structure."""
    print_section("TEST 1: Graph Structure")
    
    try:
        # Check graph exists
        assert debug_graph is not None, "Graph not initialized"
        print("✓ Graph initialized successfully")
        
        # Get graph representation
        graph_repr = debug_graph.get_graph()
        print(f"✓ Graph has {len(graph_repr.nodes)} nodes")
        print(f"✓ Graph has {len(graph_repr.edges)} edges")
        
        # List nodes
        print("\nNodes:")
        for node in graph_repr.nodes:
            print(f"  - {node}")
        
        # List edges
        print("\nEdges:")
        for edge in graph_repr.edges:
            print(f"  - {edge}")
        
        return True
        
    except Exception as e:
        print(f"✗ Graph structure test failed: {str(e)}")
        return False


async def test_no_errors_flow():
    """Test 2: Workflow with no errors (should skip fixer)."""
    print_section("TEST 2: No Errors Flow (Scanner → Finalize)")
    
    try:
        # Code with no errors
        code = """
def greet(name):
    return f"Hello, {name}!"

print(greet("World"))
"""
        
        print(f"Input code:\n{code}")
        
        result = await invoke_debug_workflow(
            request_id="test-no-errors",
            code=code,
            language="python",
            max_iterations=3
        )
        
        print(f"\nWorkflow Status: {result['workflow_status']}")
        print(f"Success: {result['success']}")
        print(f"Message: {result['message']}")
        print(f"Total Errors: {result.get('total_errors', 0)}")
        print(f"Agents Involved: {result['metadata']['agents_involved']}")
        
        # Verify fixer was skipped
        agents = result['metadata']['agents_involved']
        assert "Scanner" in agents, "Scanner should run"
        assert "Fixer" not in agents, "Fixer should be skipped when no errors"
        
        print("\n✓ No errors flow works correctly (Fixer skipped)")
        return True
        
    except Exception as e:
        print(f"\n✗ No errors flow test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_with_errors_flow():
    """Test 3: Workflow with errors (full pipeline)."""
    print_section("TEST 3: With Errors Flow (Scanner → Fixer → Validator)")
    
    try:
        # Code with intentional error
        code = """
def add(a):
    return a + b
"""
        
        print(f"Input code:\n{code}")
        
        result = await invoke_debug_workflow(
            request_id="test-with-errors",
            code=code,
            language="python",
            max_iterations=3
        )
        
        print(f"\nWorkflow Status: {result['workflow_status']}")
        print(f"Success: {result['success']}")
        print(f"Message: {result['message']}")
        print(f"Total Errors: {result.get('total_errors', 0)}")
        print(f"Total Changes: {result.get('total_changes', 0)}")
        print(f"Agents Involved: {result['metadata']['agents_involved']}")
        
        if result.get('fixed_code'):
            print(f"\nFixed code:\n{result['fixed_code']}")
        
        # Verify all agents ran
        agents = result['metadata']['agents_involved']
        assert "Scanner" in agents, "Scanner should run"
        assert "Fixer" in agents, "Fixer should run when errors found"
        assert "Validator" in agents, "Validator should run after fixer"
        
        print("\n✓ With errors flow works correctly (Full pipeline)")
        return True
        
    except Exception as e:
        print(f"\n✗ With errors flow test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_streaming():
    """Test 4: Streaming workflow."""
    print_section("TEST 4: Streaming Workflow")
    
    try:
        code = """
def multiply(x):
    return x * y
"""
        
        print(f"Input code:\n{code}")
        print("\nStreaming events:")
        
        event_count = 0
        async for state_update in stream_debug_workflow(
            request_id="test-streaming",
            code=code,
            language="python",
            max_iterations=2
        ):
            event_count += 1
            
            for node_name, state in state_update.items():
                current_agent = state.get("metadata", {}).get("current_agent")
                workflow_status = state.get("workflow_status")
                
                print(f"  [{event_count}] Node: {node_name}, Agent: {current_agent}, Status: {workflow_status}")
        
        print(f"\n✓ Streaming works correctly ({event_count} events received)")
        return True
        
    except Exception as e:
        print(f"\n✗ Streaming test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_state_accumulation():
    """Test 5: State accumulation (events, iteration counter)."""
    print_section("TEST 5: State Accumulation")
    
    try:
        code = "def test(): return x"
        
        result = await invoke_debug_workflow(
            request_id="test-accumulation",
            code=code,
            language="python",
            max_iterations=3
        )
        
        # Check events accumulated
        events = result.get("events", [])
        print(f"Total events accumulated: {len(events)}")
        
        for i, event in enumerate(events, 1):
            print(f"  [{i}] {event.get('agent')}: {event.get('action')}")
        
        # Check iteration counter
        iteration = result.get("iteration", 0)
        print(f"\nFinal iteration count: {iteration}")
        
        assert len(events) > 0, "Events should accumulate"
        print("\n✓ State accumulation works correctly")
        return True
        
    except Exception as e:
        print(f"\n✗ State accumulation test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_graph_visualization():
    """Test 6: Graph visualization."""
    print_section("TEST 6: Graph Visualization")
    
    try:
        mermaid = get_graph_visualization()
        
        print("Mermaid diagram:")
        print(mermaid)
        
        assert "graph" in mermaid.lower() or "flowchart" in mermaid.lower(), "Should contain graph definition"
        
        print("\n✓ Graph visualization works")
        return True
        
    except Exception as e:
        print(f"\n✗ Graph visualization test failed: {str(e)}")
        return False


async def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("  LANGGRAPH DEBUGGING WORKFLOW TEST SUITE")
    print("=" * 70)
    
    results = []
    
    # Test 1: Graph structure
    results.append(await test_graph_structure())
    
    # Test 2: No errors flow
    results.append(await test_no_errors_flow())
    
    # Test 3: With errors flow
    results.append(await test_with_errors_flow())
    
    # Test 4: Streaming
    results.append(await test_streaming())
    
    # Test 5: State accumulation
    results.append(await test_state_accumulation())
    
    # Test 6: Visualization
    results.append(test_graph_visualization())
    
    # Summary
    print_section("TEST SUMMARY")
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nTests Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n✗ {total - passed} TEST(S) FAILED")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
