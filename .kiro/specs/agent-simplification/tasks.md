# Implementation Plan

- [ ] 1. Set up tools infrastructure
  - Create tools directory structure
  - Set up tool decorators and base utilities
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [ ] 2. Implement Scanner Agent with LangChain
  - Create scanner tool functions
  - Define scanner prompt template
  - Create scanner agent factory using create_agent
  - Update scanner node to use new agent
  - _Requirements: 1.1, 1.2, 2.1, 3.1, 3.2, 4.1_

- [ ]* 2.1 Write unit tests for scanner tools
  - Test analyze_code tool with valid inputs
  - Test error handling with invalid inputs
  - Verify output structure matches schema
  - _Requirements: 2.4, 6.2_

- [ ]* 2.2 Write integration tests for scanner agent
  - Test agent execution with realistic code samples
  - Verify output format matches old implementation (Property 3)
  - Test error scenarios
  - _Requirements: 4.2, 6.1_

- [ ]* 2.3 Write property test for scanner output compatibility
  - **Property 3: Output format compatibility**
  - **Validates: Requirements 4.2**

- [ ] 3. Implement Fixer Agent with LangChain
  - Create fixer tool functions
  - Define fixer prompt template
  - Create fixer agent factory using create_agent
  - Update fixer node to use new agent
  - _Requirements: 1.1, 1.2, 2.2, 3.1, 3.2, 4.1_

- [ ] 3.1 Write unit tests for fixer tools
  - Test fix_code_errors tool with valid inputs
  - Test with various error types
  - Verify output structure
  - _Requirements: 2.4, 6.2_

- [ ] 3.2 Write integration tests for fixer agent
  - Test agent execution with buggy code
  - Verify fixes are applied correctly
  - Test edge cases (no errors, multiple errors)
  - _Requirements: 4.2, 6.1_

- [ ] 3.3 Write property test for fixer output compatibility
  - **Property 3: Output format compatibility**
  - **Validates: Requirements 4.2**

- [ ] 4. Implement Validator Agent with LangChain
  - Create validator tool functions
  - Define validator prompt template
  - Create validator agent factory using create_agent
  - Update validator node to use new agent
  - _Requirements: 1.1, 1.2, 2.3, 3.1, 3.2, 4.1_

- [ ]* 4.1 Write unit tests for validator tools
  - Test validate_fixes tool with valid inputs
  - Test validation logic
  - Verify output structure
  - _Requirements: 2.4, 6.2_

- [ ]* 4.2 Write integration tests for validator agent
  - Test agent execution with original and fixed code
  - Verify validation results
  - Test approval and rejection scenarios
  - _Requirements: 4.2, 6.1_

- [ ]* 4.3 Write property test for validator output compatibility
  - **Property 3: Output format compatibility**
  - **Validates: Requirements 4.2**

- [ ] 5. Checkpoint - Verify all agents work independently
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 6. Update LangGraph integration
  - Update all node functions to use new agent factories
  - Ensure singleton pattern is maintained
  - Verify async invocation with ainvoke
  - Test state transitions
  - _Requirements: 4.1, 4.3, 4.4_

- [ ]* 6.1 Write property test for state transition preservation
  - **Property 4: State transition preservation**
  - **Validates: Requirements 4.3**

- [ ]* 6.2 Write property test for error handling consistency
  - **Property 5: Error handling consistency**
  - **Validates: Requirements 4.4**

- [ ] 7. End-to-end testing
  - Run complete workflow with new agents
  - Compare outputs with class-based implementation
  - Test with various code samples
  - Verify all error scenarios work
  - _Requirements: 4.5, 5.1, 5.2_

- [ ]* 7.1 Write property test for end-to-end equivalence
  - **Property 6: End-to-end equivalence**
  - **Validates: Requirements 4.5**

- [ ]* 7.2 Write property test for logging consistency
  - **Property 7: Logging consistency**
  - **Validates: Requirements 5.4**

- [ ]* 7.3 Write property test for agent determinism
  - **Property 8: Agent determinism**
  - **Validates: Requirements 6.4**

- [ ] 8. Cleanup and documentation
  - Remove BaseAgent class
  - Remove old agent class files (scanner_agent.py, fixer_agent.py, validator_agent.py)
  - Update documentation to reflect new architecture
  - Update README and architecture docs
  - _Requirements: 1.3, 7.4, 7.5_

- [ ] 9. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
