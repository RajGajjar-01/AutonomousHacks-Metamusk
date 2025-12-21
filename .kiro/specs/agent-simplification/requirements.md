# Requirements Document

## Introduction

This document outlines the requirements for simplifying the agent architecture in the code debugging system by migrating from class-based agents to LangChain's `create_react_agent` function. The goal is to reduce complexity, improve maintainability, and align with LangChain best practices while preserving all existing functionality.

## Glossary

- **Agent**: An AI-powered component that performs a specific task (scanning, fixing, or validating code)
- **LangChain**: A framework for developing applications powered by language models
- **create_agent**: LangChain's built-in function for creating agents with tools and prompts
- **Tool**: A function that an agent can call to perform specific actions
- **Scanner Agent**: Agent responsible for analyzing code and identifying errors
- **Fixer Agent**: Agent responsible for generating fixes for identified errors
- **Validator Agent**: Agent responsible for validating that fixes are correct
- **LangGraph**: Framework for building stateful, multi-agent workflows
- **Node Function**: A function in LangGraph that processes state and returns updates

## Requirements

### Requirement 1

**User Story:** As a developer, I want agents to be implemented using LangChain's standard patterns, so that the codebase is easier to understand and maintain.

#### Acceptance Criteria

1. WHEN the system initializes agents THEN the system SHALL use LangChain's `create_agent` function for all agent creation
2. WHEN an agent is created THEN the system SHALL define the agent using a language model, tools list, and prompt template
3. WHEN the codebase is reviewed THEN the system SHALL contain no class-based agent implementations (BaseAgent, ScannerAgent, FixerAgent, ValidatorAgent classes)
4. WHEN agents are instantiated THEN the system SHALL use functional composition instead of object-oriented inheritance
5. WHEN the agent architecture is examined THEN the system SHALL follow LangChain's recommended patterns and conventions

### Requirement 2

**User Story:** As a developer, I want each agent to have clearly defined tools, so that agent capabilities are explicit and testable.

#### Acceptance Criteria

1. WHEN the Scanner Agent is created THEN the system SHALL define a tool for code analysis that accepts code and language parameters
2. WHEN the Fixer Agent is created THEN the system SHALL define a tool for code fixing that accepts code, language, and error information
3. WHEN the Validator Agent is created THEN the system SHALL define a tool for validation that accepts original code, fixed code, and previous outputs
4. WHEN a tool is invoked THEN the system SHALL execute the tool function and return structured results
5. WHEN tools are defined THEN the system SHALL include clear docstrings describing inputs, outputs, and behavior

### Requirement 3

**User Story:** As a developer, I want agent prompts to be clearly separated from agent logic, so that prompts can be easily modified and tested.

#### Acceptance Criteria

1. WHEN an agent is created THEN the system SHALL use a dedicated prompt template for that agent
2. WHEN a prompt template is defined THEN the system SHALL include placeholders for dynamic inputs (code, errors, language)
3. WHEN prompts are stored THEN the system SHALL maintain them in a centralized location (app/core/prompts.py)
4. WHEN prompts are updated THEN the system SHALL not require changes to agent creation code
5. WHEN an agent executes THEN the system SHALL format the prompt template with current state values

### Requirement 4

**User Story:** As a developer, I want the LangGraph integration to work seamlessly with simplified agents, so that the workflow remains functional.

#### Acceptance Criteria

1. WHEN a node function calls an agent THEN the system SHALL invoke the agent using LangChain's standard invocation pattern
2. WHEN an agent completes execution THEN the system SHALL return results in the same format as before
3. WHEN the graph executes THEN the system SHALL maintain all existing state transitions and conditional logic
4. WHEN errors occur THEN the system SHALL handle them gracefully and update state appropriately
5. WHEN the workflow completes THEN the system SHALL produce output identical to the class-based implementation

### Requirement 5

**User Story:** As a developer, I want minimal changes to the existing codebase, so that the refactoring is low-risk and easy to review.

#### Acceptance Criteria

1. WHEN the refactoring is complete THEN the system SHALL preserve all existing API endpoints and request/response formats
2. WHEN the refactoring is complete THEN the system SHALL maintain all existing state schemas and data structures
3. WHEN the refactoring is complete THEN the system SHALL keep all existing utility functions and helpers unchanged
4. WHEN the refactoring is complete THEN the system SHALL preserve all existing logging and error handling patterns
5. WHEN the refactoring is complete THEN the system SHALL require changes only to agent files and node functions

### Requirement 6

**User Story:** As a developer, I want each agent to be independently testable, so that I can verify agent behavior in isolation.

#### Acceptance Criteria

1. WHEN an agent is created THEN the system SHALL allow the agent to be invoked directly with test inputs
2. WHEN an agent tool is defined THEN the system SHALL allow the tool to be tested independently
3. WHEN tests are written THEN the system SHALL support mocking the language model for deterministic testing
4. WHEN an agent executes THEN the system SHALL produce consistent output for the same inputs
5. WHEN debugging THEN the system SHALL provide clear visibility into agent reasoning and tool calls

### Requirement 7

**User Story:** As a developer, I want the migration to be done incrementally, so that I can validate each agent independently before moving to the next.

#### Acceptance Criteria

1. WHEN migrating agents THEN the system SHALL convert one agent at a time (Scanner, then Fixer, then Validator)
2. WHEN an agent is migrated THEN the system SHALL verify it works correctly before proceeding to the next agent
3. WHEN an agent is migrated THEN the system SHALL maintain backward compatibility with existing node functions
4. WHEN all agents are migrated THEN the system SHALL remove the BaseAgent class and related infrastructure
5. WHEN the migration is complete THEN the system SHALL update all documentation to reflect the new architecture
