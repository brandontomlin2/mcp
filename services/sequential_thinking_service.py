"""
Sequential Thinking Service

A service for dynamic and reflective problem-solving through thoughts.
This service helps analyze problems through a flexible thinking process that can adapt and evolve.
"""

import os
from typing import Dict, List, Any, Optional
from loguru import logger
from utils import BaseService, ThoughtData, ThoughtResponse


class SequentialThinkingService(BaseService):
    """Service for sequential thinking and problem-solving."""
    
    def __init__(self):
        """Initialize the Sequential Thinking service."""
        self.thought_history: List[ThoughtData] = []
        self.branches: Dict[str, List[ThoughtData]] = {}
        self.disable_thought_logging = (
            os.getenv("DISABLE_THOUGHT_LOGGING", "").lower() == "true"
        )
        logger.info("Sequential Thinking Service initialized")
    
    def get_name(self) -> str:
        """Return the service name."""
        return "Sequential Thinking Service"
    
    def _validate_thought_data(self, input_data: Any) -> ThoughtData:
        """Validate and parse thought data."""
        try:
            if isinstance(input_data, dict):
                # Convert camelCase to snake_case for Python compatibility
                data = {}
                for key, value in input_data.items():
                    snake_key = self._camel_to_snake(key)
                    data[snake_key] = value
                
                return ThoughtData(**data)
            else:
                raise ValueError("Input must be a dictionary")
        except Exception as e:
            raise ValueError(f"Invalid thought data: {str(e)}")
    
    def _camel_to_snake(self, name: str) -> str:
        """Convert camelCase to snake_case."""
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    def _format_thought(self, thought_data: ThoughtData) -> str:
        """Format thought for display."""
        thought_number = thought_data.thought_number
        total_thoughts = thought_data.total_thoughts
        thought = thought_data.thought
        is_revision = thought_data.is_revision
        revises_thought = thought_data.revises_thought
        branch_from_thought = thought_data.branch_from_thought
        branch_id = thought_data.branch_id
        
        # Determine prefix and context
        if is_revision:
            prefix = "🔄 Revision"
            context = f" (revising thought {revises_thought})"
        elif branch_from_thought:
            prefix = "🌿 Branch"
            context = f" (from thought {branch_from_thought}, ID: {branch_id})"
        else:
            prefix = "💭 Thought"
            context = ""
        
        header = f"{prefix} {thought_number}/{total_thoughts}{context}"
        border_length = max(len(header), len(thought)) + 4
        border = "─" * border_length
        
        return f"""
┌{border}┐
│ {header:<{border_length-2}} │
├{border}┤
│ {thought:<{border_length-2}} │
└{border}┘"""
    
    def process_thought(self, input_data: Any) -> ThoughtResponse:
        """
        Process a thought step in the sequential thinking process.
        
        Args:
            input_data: The thought data containing the thinking step
            
        Returns:
            ThoughtResponse: The processed thought response
        """
        try:
            # Validate input data
            validated_input = self._validate_thought_data(input_data)
            
            # Adjust total thoughts if current thought exceeds it
            if validated_input.thought_number > validated_input.total_thoughts:
                validated_input.total_thoughts = validated_input.thought_number
            
            # Add to thought history
            self.thought_history.append(validated_input)
            
            # Handle branching
            if validated_input.branch_from_thought and validated_input.branch_id:
                if validated_input.branch_id not in self.branches:
                    self.branches[validated_input.branch_id] = []
                self.branches[validated_input.branch_id].append(validated_input)
            
            # Log formatted thought if logging is enabled
            if not self.disable_thought_logging:
                formatted_thought = self._format_thought(validated_input)
                logger.info(formatted_thought)
            
            # Return response
            return ThoughtResponse(
                thought_number=validated_input.thought_number,
                total_thoughts=validated_input.total_thoughts,
                next_thought_needed=validated_input.next_thought_needed,
                branches=list(self.branches.keys()),
                thought_history_length=len(self.thought_history)
            )
            
        except Exception as e:
            logger.error(f"Error processing thought: {str(e)}")
            return ThoughtResponse(
                thought_number=0,
                total_thoughts=0,
                next_thought_needed=False,
                branches=[],
                thought_history_length=len(self.thought_history),
                error=str(e),
                status="failed"
            )
    
    def get_thought_history(self) -> List[ThoughtData]:
        """Get the complete thought history."""
        return self.thought_history.copy()
    
    def get_branches(self) -> Dict[str, List[ThoughtData]]:
        """Get all branches."""
        return self.branches.copy()
    
    def clear_history(self) -> None:
        """Clear thought history and branches."""
        self.thought_history.clear()
        self.branches.clear()
        logger.info("Thought history and branches cleared")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the thinking session."""
        return {
            "total_thoughts": len(self.thought_history),
            "branches": list(self.branches.keys()),
            "branch_count": len(self.branches),
            "latest_thought_number": (
                self.thought_history[-1].thought_number 
                if self.thought_history else 0
            ),
            "latest_total_estimate": (
                self.thought_history[-1].total_thoughts 
                if self.thought_history else 0
            )
        }
