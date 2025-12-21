# Design Document: Agent Simplification with LangChain

## Overview

This design outlines the migration from class-based agents to LangChain's `create_agent` function. The goal is to simplify the codebase by removing custom agent classes and leveraging LangChain's built-in agent creation patterns. Each agent (Scanner, Fixer, Validator) will be converted to use functional composition with tools and prompts.

## Architecture

### Current Architecture (Class-Based)

```
BaseAgent (Abstract Class)
├── ScannerAgent
├── FixerAgent
└── ValidatorAgent

Each agent:
- Inherits from BaseAgent
- Implements execute() method
- Contains AI client instance
- Handles JSON parsing
- Manages timing and logging
```

### New Architecture (Functional with LangChain)

```
Agent Creation Functions
├── create_scanner_agent()
├── create_fixer_agent()
└── create_validator_agent()

Each function:
- Uses LangChain's create_agent()
- Defines tools for the agent
- Provides prompt template
- Returns configured agent executor
```

### Key Changes

1. **Remove Classes**: Delete BaseAgent, ScannerAgent, FixerAgent, ValidatorAgent classes
2. **Add Agent Factories**: Create factory functions that return LangChain agents
3. **Define Tools**: Create tool functions for each agent's capabilities
4. **Simplify Nodes**: Update node functions to use new agent creation pattern
5. **Maintain Compatibility**: Keep same input/output formats for seamless integration

## Components and Interfaces

### 1. Agent Tools Module (`app/agents/tools/`)

Each agent will have dedicated tool functions:

**Scanner Tools** (`scanner_tools.py`):
```python
from langchain.tools import tool
from typing import Dict, Any

@tool
def analyze_code(code: str, language: str, context: str = "") -> Dict[str, Any]:
    """
    Analyze code for syntax errors, runtime errors, and warnings.
    
    Args:
        code: The source code to analyze
        language: Programming language (e.g., 'python', 'javascript')
        context: Optional context about the code
        
    Returns:
        Dictionary with errors, warnings, and quality score
    """
    # Implementation calls AI model with structured prompt
    pass
```

**Fixer Tools** (`fixer_tools.py`):
```python
@tool
def fix_code_errors(code: str, errors: list, language: str) -> Dict[str, Any]:
    """
    Generate fixes for identified code errors.
    
    Args:
        code: The original buggy code
        errors: List of errors from scanner
        language: Programming language
        
    Returns:
        Dictionary with fixed code and change details
    """
    pass
```

**Validator Tools** (`validator_tools.py`):
```python
@tool
def validate_fixes(original_code: str, fixed_code: str, 
                   errors: list, changes: list, language: str) -> Dict[str, Any]:
    """
    Validate that code fixes are correct and complete.
    
    Args:
        original_code: The original buggy code
        fixed_code: The fixed code
        errors: Original errors from scanner
        changes: Changes made by fixer
        language: Programming language
        
    Returns:
        Dictionary with validation status and recommendations
    """
    pass
```

### 2. Agent Creation Module (`app/agents/agent_factory.py`)

Factory functions for creating agents:

```python
from langchain.agents import create_agent, AgentExecutor
from langchain_groq import ChatGroq
from app.agents.tools.scanner_tools import analyze_code
from app.agents.tools.fixer_tools import fix_code_errors
from app.agents.tools.validator_tools import validate_fixes
from app.core.prompts import SCANNER_PROMPT, FIXER_PROMPT, VALIDATOR_PROMPT

def create_scanner_agent() -> AgentExecutor:
    """Create and return a Scanner agent using LangChain."""
    llm = ChatGroq(model="llama-3.1-70b-versatile", temperature=0.2)
    tools = [analyze_code]
    
    agent = create_agent(
        llm=llm,
        tools=tools,
        prompt=SCANNER_PROMPT
    )
    
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

def create_fixer_agent() -> AgentExecutor:
    """Create and return a Fixer agent using LangChain."""
    llm = ChatGroq(model="llama-3.1-70b-versatile", temperature=0.4)
    tools = [fix_code_errors]
    
    agent = create_agent(
        llm=llm,
        tools=tools,
        prompt=FIXER_PROMPT
    )
    
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

def create_validator_agent() -> AgentExecutor:
    """Create and return a Validator agent using LangChain."""
    llm = ChatGroq(model="llama-3.1-70b-versatile", temperature=0.2)
    tools = [validate_fixes]
    
    agent = create_agent(
        llm=llm,
        tools=tools,
        prompt=VALIDATOR_PROMPT
    )
    
    return AgentExecutor(agent=agent, tools=tools, verbose=True)
```

### 3. Updated Node Functions (`app/graphs/nodes.py`)

Simplified node functions using agent factories:

```python
from app.agents.agent_factory import (
    create_scanner_agent,
    create_fixer_agent,
    create_validator_agent
)

# Singleton instances
_scanner_agent = None
_fixer_agent = None
_validator_agent = None

def get_scanner_agent():
    global _scanner_agent
    if _scanner_agent is None:
        _scanner_agent = create_scanner_agent()
    return _scanner_agent

async def scanner_node(state: DebugState) -> Dict[str, Any]:
    """Scanner node using LangChain agent."""
    agent = get_scanner_agent()
    
    # Invoke agent with state data
    result = await agent.ainvoke({
        "code": state["code"],
        "language": state["language"],
        "context": state.get("context", "")
    })
    
    # Extract and format results
    return {
        "errors": result["errors"],
        "warnings": result["warnings"],
        # ... rest of state updates
    }
```

### 4. Prompt Templates (`app/core/prompts.py`)

Centralized prompt templates for agents:

```python
from langchain.prompts import ChatPromptTemplate

SCANNER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert code analyzer.
    
Analyze the provided code for:
- Syntax errors
- Runtime errors  
- Warnings and code smells

Return structured JSON with errors, warnings, and quality score."""),
    ("human", """Analyze this {language} code:

```{language}
{code}
```

{context}""")
])

FIXER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert code fixer.
    
Fix the identified errors while:
- Preserving original intent
- Making minimal changes
- Following best practices

Return structured JSON with fixed code and changes."""),
    ("human", """Fix this {language} code:

```{language}
{code}
```

Errors to fix:
{errors}""")
])

VALIDATOR_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert code validator.
    
Validate that fixes:
- Resolve all errors
- Don't introduce new issues
- Follow best practices

Return structured JSON with validation status."""),
    ("human", """Validate these fixes:

Original:
```{language}
{original_code}
```

Fixed:
```{language}
{fixed_code}
```

Changes: {changes}""")
])
```

## Data Models

### Tool Input/Output Schemas

All tools will use Pydantic models for validation:

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class AnalyzeCodeInput(BaseModel):
    code: str = Field(description="Source code to analyze")
    language: str = Field(description="Programming language")
    context: Optional[str] = Field(default="", description="Optional context")

class AnalyzeCodeOutput(BaseModel):
    errors: List[ErrorDetail]
    warnings: List[WarningDetail]
    code_quality_score: float
    analysis_summary: str
    is_runnable: bool

# Similar models for Fixer and Validator
```

### Agent Invocation Format

Agents will be invoked with dictionaries and return dictionaries:

```python
# Input
input_data = {
    "code": "def add(a):\n    return a + b",
    "language": "python",
    "context": ""
}

# Output
output_data = {
    "errors": [...],
    "warnings": [...],
    "code_quality_score": 6.5,
    "analysis_summary": "Found 1 error",
    "is_runnable": False
}
```



## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property 1: Tool invocation returns structured results
*For any* tool and valid input parameters, invoking the tool should return a structured dictionary with expected fields.
**Validates: Requirements 2.4**

### Property 2: Agent prompt formatting
*For any* agent and valid state values, executing the agent should properly format the prompt template with those values.
**Validates: Requirements 3.5**

### Property 3: Output format compatibility
*For any* valid input to an agent, the new LangChain-based agent should return results in the same format as the class-based implementation.
**Validates: Requirements 4.2**

### Property 4: State transition preservation
*For any* valid input state to the workflow graph, the state transitions and conditional logic should match the original implementation.
**Validates: Requirements 4.3**

### Property 5: Error handling consistency
*For any* error condition during agent execution, the system should handle it gracefully and update state with error information.
**Validates: Requirements 4.4**

### Property 6: End-to-end equivalence
*For any* code input to the debugging workflow, the new implementation should produce output identical to the class-based implementation.
**Validates: Requirements 4.5**

### Property 7: Logging consistency
*For any* agent operation, the logging output should follow the same patterns and include the same information as the original implementation.
**Validates: Requirements 5.4**

### Property 8: Agent determinism
*For any* input to an agent, executing the agent multiple times with the same LLM responses should produce consistent output.
**Validates: Requirements 6.4**

### Property 9: Backward compatibility during migration
*For any* migrated agent, it should work correctly with existing node functions and produce expected outputs.
**Validates: Requirements 7.3**

## Error Handling

### Tool Execution Errors

- Tools should catch exceptions and return structured error responses
- Errors should include error type, message, and context
- Failed tool calls should not crash the agent

### Agent Invocation Errors

- Invalid inputs should be validated before agent execution
- LLM API failures should be caught and logged
- Timeout errors should be handled gracefully

### JSON Parsing Errors

- Tools should handle malformed JSON from LLM responses
- Fallback parsing strategies (markdown extraction) should be attempted
- Clear error messages should be provided for debugging

## Testing Strategy

### Unit Tests

Unit tests will verify individual components:

1. **Tool Function Tests**
   - Test each tool with valid inputs
   - Test error handling with invalid inputs
   - Verify output structure matches schema

2. **Agent Creation Tests**
   - Verify agents are created with correct components
   - Test that tools are properly registered
   - Verify prompt templates are correctly configured

3. **Prompt Template Tests**
   - Test template formatting with various inputs
   - Verify all placeholders are replaced
   - Test edge cases (empty strings, special characters)

### Integration Tests

Integration tests will verify agent behavior in context:

1. **Agent Execution Tests**
   - Test each agent with realistic inputs
   - Verify output format matches expectations
   - Test error scenarios

2. **Node Function Tests**
   - Test node functions with new agents
   - Verify state updates are correct
   - Test error propagation

3. **End-to-End Tests**
   - Run complete workflow with new agents
   - Compare outputs with class-based implementation
   - Test various code samples and error conditions

### Migration Validation Tests

Tests to ensure smooth migration:

1. **Compatibility Tests**
   - Test that new agents work with existing code
   - Verify API contracts are maintained
   - Test backward compatibility

2. **Equivalence Tests**
   - Compare outputs between old and new implementations
   - Test with same inputs to both versions
   - Verify identical behavior

## Implementation Notes

### Migration Order

1. **Phase 1: Scanner Agent**
   - Create scanner tools
   - Create scanner agent factory
   - Update scanner node
   - Test thoroughly

2. **Phase 2: Fixer Agent**
   - Create fixer tools
   - Create fixer agent factory
   - Update fixer node
   - Test thoroughly

3. **Phase 3: Validator Agent**
   - Create validator tools
   - Create validator agent factory
   - Update validator node
   - Test thoroughly

4. **Phase 4: Cleanup**
   - Remove BaseAgent class
   - Remove old agent classes
   - Update documentation
   - Final integration tests

### Key Considerations

1. **Singleton Pattern**: Maintain singleton pattern for agent instances to avoid recreating agents on each request
2. **Async Support**: Ensure all agent invocations use `ainvoke` for async compatibility
3. **Logging**: Preserve existing logging patterns for debugging and monitoring
4. **Error Messages**: Maintain clear, actionable error messages
5. **Performance**: Monitor performance to ensure no regression from class-based approach

### Dependencies

- `langchain` - Core LangChain library
- `langchain-groq` - Groq LLM integration
- `langchain-core` - Core abstractions and tools
- Existing dependencies (pydantic, fastapi, etc.) remain unchanged

### File Changes Summary

**New Files:**
- `app/agents/tools/scanner_tools.py`
- `app/agents/tools/fixer_tools.py`
- `app/agents/tools/validator_tools.py`
- `app/agents/agent_factory.py`

**Modified Files:**
- `app/graphs/nodes.py` - Update to use new agent factories
- `app/core/prompts.py` - Add LangChain prompt templates

**Deleted Files:**
- `app/agents/base_agent.py`
- `app/agents/scanner_agent.py`
- `app/agents/fixer_agent.py`
- `app/agents/validator_agent.py`

**Unchanged Files:**
- `app/models/schemas.py` - All schemas remain the same
- `app/api/routes/debug.py` - API endpoints unchanged
- `app/graphs/states.py` - State definitions unchanged
- `app/graphs/workflow.py` - Workflow structure unchanged
