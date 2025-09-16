"""
Sequential Thinking Tool Provider

MCP tool definitions for sequential thinking functionality.
"""

from typing import Dict, Any
from loguru import logger
from utils import BaseToolProvider
from services.sequential_thinking_service import SequentialThinkingService


class SequentialThinkingToolProvider(BaseToolProvider):
    """Tool provider for Sequential Thinking MCP tools."""
    
    def __init__(self, mcp, service: SequentialThinkingService):
        """Initialize the Sequential Thinking tool provider."""
        super().__init__(mcp, service)
        logger.info("Sequential Thinking Tool Provider initialized")
    
    def _register_tools(self):
        """Register Sequential Thinking tools with the MCP server."""
        
        @self.mcp.tool()
        async def sequential_thinking(
            thought: str,
            next_thought_needed: bool,
            thought_number: int,
            total_thoughts: int,
            is_revision: bool = False,
            revises_thought: int = None,
            branch_from_thought: int = None,
            branch_id: str = None,
            needs_more_thoughts: bool = None
        ) -> Dict[str, Any]:
            """
            A detailed tool for dynamic and reflective problem-solving through thoughts.
            
            This tool helps analyze problems through a flexible thinking process that can adapt and evolve.
            Each thought can build on, question, or revise previous insights as understanding deepens.

            When to use this tool:
            - Breaking down complex problems into steps
            - Planning and design with room for revision
            - Analysis that might need course correction
            - Problems where the full scope might not be clear initially
            - Problems that require a multi-step solution
            - Tasks that need to maintain context over multiple steps
            - Situations where irrelevant information needs to be filtered out

            Key features:
            - You can adjust total_thoughts up or down as you progress
            - You can question or revise previous thoughts
            - You can add more thoughts even after reaching what seemed like the end
            - You can express uncertainty and explore alternative approaches
            - Not every thought needs to build linearly - you can branch or backtrack
            - Generates a solution hypothesis
            - Verifies the hypothesis based on the Chain of Thought steps
            - Repeats the process until satisfied
            - Provides a correct answer

            Parameters explained:
            - thought: Your current thinking step, which can include:
              * Regular analytical steps
              * Revisions of previous thoughts
              * Questions about previous decisions
              * Realizations about needing more analysis
              * Changes in approach
              * Hypothesis generation
              * Hypothesis verification
            - next_thought_needed: True if you need more thinking, even if at what seemed like the end
            - thought_number: Current number in sequence (can go beyond initial total if needed)
            - total_thoughts: Current estimate of thoughts needed (can be adjusted up/down)
            - is_revision: A boolean indicating if this thought revises previous thinking
            - revises_thought: If is_revision is true, which thought number is being reconsidered
            - branch_from_thought: If branching, which thought number is the branching point
            - branch_id: Identifier for the current branch (if any)
            - needs_more_thoughts: If reaching end but realizing more thoughts needed

            You should:
            1. Start with an initial estimate of needed thoughts, but be ready to adjust
            2. Feel free to question or revise previous thoughts
            3. Don't hesitate to add more thoughts if needed, even at the "end"
            4. Express uncertainty when present
            5. Mark thoughts that revise previous thinking or branch into new paths
            6. Ignore information that is irrelevant to the current step
            7. Generate a solution hypothesis when appropriate
            8. Verify the hypothesis based on the Chain of Thought steps
            9. Repeat the process until satisfied with the solution
            10. Provide a single, ideally correct answer as the final output
            11. Only set next_thought_needed to false when truly done and a satisfactory answer is reached
            """
            try:
                # Prepare input data
                input_data = {
                    "thought": thought,
                    "nextThoughtNeeded": next_thought_needed,
                    "thoughtNumber": thought_number,
                    "totalThoughts": total_thoughts,
                    "isRevision": is_revision,
                    "revisesThought": revises_thought,
                    "branchFromThought": branch_from_thought,
                    "branchId": branch_id,
                    "needsMoreThoughts": needs_more_thoughts
                }
                
                # Process the thought
                response = self.service.process_thought(input_data)
                
                # Return the response as a dictionary
                return {
                    "thought_number": response.thought_number,
                    "total_thoughts": response.total_thoughts,
                    "next_thought_needed": response.next_thought_needed,
                    "branches": response.branches,
                    "thought_history_length": response.thought_history_length,
                    "error": response.error,
                    "status": response.status or "success"
                }
                
            except Exception as e:
                logger.error(f"Error in sequential_thinking tool: {str(e)}")
                return {
                    "error": str(e),
                    "status": "failed"
                }
        
        @self.mcp.tool()
        async def get_thought_summary() -> Dict[str, Any]:
            """
            Get a summary of the current thinking session.
            
            Returns information about the thought history, branches, and current state.
            """
            try:
                summary = self.service.get_summary()
                return summary
            except Exception as e:
                logger.error(f"Error getting thought summary: {str(e)}")
                return {
                    "error": str(e),
                    "status": "failed"
                }
        
        @self.mcp.tool()
        async def clear_thought_history() -> Dict[str, str]:
            """
            Clear the thought history and branches.
            
            This will reset the thinking session to start fresh.
            """
            try:
                self.service.clear_history()
                return {
                    "status": "success",
                    "message": "Thought history and branches cleared"
                }
            except Exception as e:
                logger.error(f"Error clearing thought history: {str(e)}")
                return {
                    "error": str(e),
                    "status": "failed"
                }
