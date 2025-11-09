"""Base agent class."""

from abc import ABC, abstractmethod
from typing import Any, Optional
from ..utils import get_logger


class BaseAgent(ABC):
    """Base class for all agents."""
    
    def __init__(self, name: str, config: Optional[dict] = None):
        """Initialize base agent."""
        self.name = name
        self.config = config or {}
        self.logger = get_logger(name)
    
    @abstractmethod
    def process(self, input_data: Any) -> Any:
        """Process input and return output."""
        pass
    
    def log_info(self, message: str):
        """Log info message."""
        self.logger.info(f"[{self.name}] {message}")
    
    def log_error(self, message: str):
        """Log error message."""
        self.logger.error(f"[{self.name}] {message}")
    
    def log_warning(self, message: str):
        """Log warning message."""
        self.logger.warning(f"[{self.name}] {message}")
