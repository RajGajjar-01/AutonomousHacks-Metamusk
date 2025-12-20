from typing import Dict, Any, AsyncGenerator
from datetime import datetime
import time
import json
import asyncio
from app.agents.scanner_agent import ScannerAgent
from app.agents.fixer_agent import FixerAgent
from app.agents.validator_agent import ValidatorAgent
from app.utils.logger import get_logger

logger = get_logger()

class StreamingOrchestrator:
    """Orchestrates the multi-agent workflow with real-time streaming"""
    
    def __init__(self):
        self.scanner = ScannerAgent()
        self.fixer = FixerAgent()
        self.validator = ValidatorAgent()
        self.max_iterations = 3
    
    async def execute_workflow_streaming(
        self, 
        request_id: str,
        code: str,
        language: str,
        context: str = None
    ) -> AsyncGenerator[str, None]:
        """
        Execute workflow with real-time SSE streaming
        
        Yields JSON events for each step:
        - agent_start: Agent begins processing
        - agent_complete: Agent finished with results
        - workflow_complete: All done with final result
        - error: If something goes wrong
        """
        logger.info(f"Streaming Orchestrator - Starting workflow for {request_id}")
        start_time = time.time()
        
        workflow_result = {
            "request_id": request_id,
            "workflow_status": "in_progress",
            "success": False,
            "message": "",
            "original_code": code,
            "final_code": None,
            "language": language,
            "context": context,
            "scanner_result": None,
            "fixer_result": None,
            "validator_result": None,
            "workflow_metadata": {
                "iterations": 0,
                "agents_involved": [],
                "start_time": datetime.utcnow().isoformat() + "Z"
            },
            "summary": {}
        }
        
        def create_event(event_type: str, data: dict) -> str:
            """Create SSE event string"""
            return f"data: {json.dumps({'type': event_type, **data})}\n\n"
        
        try:
            iteration = 0
            current_code = code
            
            while iteration < self.max_iterations:
                iteration += 1
                
                # ========== SCANNER AGENT ==========
                yield create_event("agent_start", {
                    "agent": "Scanner",
                    "message": "Scanning code for errors...",
                    "iteration": iteration
                })
                await asyncio.sleep(0.1)  # Small delay for UI to update
                
                scanner_input = {
                    "request_id": request_id,
                    "code": current_code,
                    "language": language,
                    "context": context
                }
                scanner_output = await self.scanner.execute_with_timing(scanner_input)
                workflow_result["scanner_result"] = scanner_output
                
                yield create_event("agent_complete", {
                    "agent": "Scanner",
                    "result": scanner_output,
                    "message": f"Found {scanner_output.get('total_errors', 0)} errors, {scanner_output.get('total_warnings', 0)} warnings"
                })
                await asyncio.sleep(0.1)
                
                # Check if any errors found
                if scanner_output.get("total_errors", 0) == 0:
                    workflow_result.update({
                        "workflow_status": "completed",
                        "success": True,
                        "message": "No errors found in code!",
                        "final_code": current_code
                    })
                    break
                
                # ========== FIXER AGENT ==========
                yield create_event("agent_start", {
                    "agent": "Fixer",
                    "message": "Fixing detected errors...",
                    "iteration": iteration
                })
                await asyncio.sleep(0.1)
                
                fixer_input = {
                    "request_id": request_id,
                    "original_code": current_code,
                    "language": language,
                    "scanner_output": scanner_output
                }
                fixer_output = await self.fixer.execute_with_timing(fixer_input)
                workflow_result["fixer_result"] = fixer_output
                fixed_code = fixer_output.get("fixed_code", current_code)
                
                yield create_event("agent_complete", {
                    "agent": "Fixer",
                    "result": fixer_output,
                    "message": f"Applied {fixer_output.get('total_changes', 0)} fixes"
                })
                await asyncio.sleep(0.1)
                
                # ========== VALIDATOR AGENT ==========
                yield create_event("agent_start", {
                    "agent": "Validator",
                    "message": "Validating fixes...",
                    "iteration": iteration
                })
                await asyncio.sleep(0.1)
                
                validator_input = {
                    "request_id": request_id,
                    "original_code": code,
                    "fixed_code": fixed_code,
                    "language": language,
                    "scanner_output": scanner_output,
                    "fixer_output": fixer_output
                }
                validator_output = await self.validator.execute_with_timing(validator_input)
                workflow_result["validator_result"] = validator_output
                
                yield create_event("agent_complete", {
                    "agent": "Validator",
                    "result": validator_output,
                    "message": f"Validation: {validator_output.get('validation_status', 'unknown')}"
                })
                await asyncio.sleep(0.1)
                
                # ========== DECISION ==========
                validation_status = validator_output.get("validation_status", "approved")
                
                if validation_status == "approved":
                    workflow_result.update({
                        "workflow_status": "completed",
                        "success": True,
                        "message": "Code successfully debugged and validated!",
                        "final_code": fixed_code
                    })
                    break
                elif validation_status == "needs_revision" and iteration < self.max_iterations:
                    current_code = fixed_code
                    yield create_event("iteration", {
                        "message": f"Needs revision, starting iteration {iteration + 1}...",
                        "iteration": iteration + 1
                    })
                    continue
                else:
                    workflow_result.update({
                        "workflow_status": "completed_with_warnings",
                        "success": True,
                        "message": "Code fixed (validation incomplete)",
                        "final_code": fixed_code
                    })
                    break
            
            # Calculate final summary
            workflow_result["workflow_metadata"]["iterations"] = iteration
            workflow_result["workflow_metadata"]["total_time"] = round(time.time() - start_time, 2)
            workflow_result["workflow_metadata"]["end_time"] = datetime.utcnow().isoformat() + "Z"
            workflow_result["workflow_metadata"]["agents_involved"] = ["Scanner", "Fixer", "Validator"]
            workflow_result["summary"] = self._generate_summary(workflow_result)
            
            # Final complete event
            yield create_event("workflow_complete", {
                "result": workflow_result,
                "message": workflow_result["message"]
            })
            
        except Exception as e:
            logger.error(f"Streaming Orchestrator - Error: {str(e)}")
            yield create_event("error", {
                "message": f"Workflow error: {str(e)}",
                "request_id": request_id
            })
    
    def _generate_summary(self, workflow_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate workflow summary"""
        scanner = workflow_result.get("scanner_result", {}) or {}
        fixer = workflow_result.get("fixer_result", {}) or {}
        validator = workflow_result.get("validator_result", {}) or {}
        
        return {
            "errors_found": scanner.get("total_errors", 0),
            "errors_fixed": len(fixer.get("changes", [])),
            "warnings_found": scanner.get("total_warnings", 0),
            "validation_score": validator.get("confidence_score", 0),
            "code_quality_before": scanner.get("code_quality_score", 0),
            "improvement_percentage": validator.get("comparison", {}).get("improvement_percentage", 100),
            "final_status": workflow_result["workflow_status"]
        }


# Keep the old orchestrator for non-streaming endpoint
class WorkflowOrchestrator(StreamingOrchestrator):
    """Non-streaming orchestrator for backwards compatibility"""
    
    async def execute_workflow(
        self, 
        request_id: str,
        code: str,
        language: str,
        context: str = None
    ) -> Dict[str, Any]:
        """Execute workflow and return final result"""
        result = None
        async for event in self.execute_workflow_streaming(request_id, code, language, context):
            # Parse the SSE data
            if event.startswith("data: "):
                data = json.loads(event[6:].strip())
                if data["type"] == "workflow_complete":
                    result = data["result"]
                elif data["type"] == "error":
                    result = {
                        "request_id": request_id,
                        "workflow_status": "failed",
                        "success": False,
                        "message": data["message"]
                    }
        return result
