"""Configuration management."""

import os
from typing import Dict, Any, Optional
from pathlib import Path
import json


class Config:
    """Configuration container."""
    
    def __init__(self, config_dict: Optional[Dict[str, Any]] = None):
        """Initialize configuration."""
        self._config = config_dict or {}
        self._load_defaults()
        self._load_env_vars()
    
    def _load_defaults(self):
        """Load default configuration values."""
        defaults = {
            "llm": {
                "provider": "openai",
                "model": "gpt-4",
                "temperature": 0.7,
                "max_tokens": 2000,
            },
            "processing": {
                "parallel_workers": 4,
                "batch_size": 10,
            },
            "stages": {
                "deconstruction": {"enabled": True},
                "pattern_recognition": {"enabled": True},
                "categorization": {"enabled": True},
                "synthesis": {"enabled": True, "depth": "standard"},
                "validation": {"enabled": True},
            },
            "output": {
                "format": "markdown",
                "destination": "./output",
            },
            "checkpoints": {
                "enabled": True,
                "directory": "./checkpoints",
            }
        }
        
        # Merge defaults with existing config
        for key, value in defaults.items():
            if key not in self._config:
                self._config[key] = value
    
    def _load_env_vars(self):
        """Load configuration from environment variables."""
        # LLM API keys
        if "OPENAI_API_KEY" in os.environ:
            self._config.setdefault("llm", {})["openai_api_key"] = os.environ["OPENAI_API_KEY"]
        
        if "ANTHROPIC_API_KEY" in os.environ:
            self._config.setdefault("llm", {})["anthropic_api_key"] = os.environ["ANTHROPIC_API_KEY"]
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key."""
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value."""
        keys = key.split(".")
        config = self._config
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        config[keys[-1]] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return self._config.copy()


# Global configuration instance
_config: Optional[Config] = None


def load_config(config_path: Optional[str] = None) -> Config:
    """Load configuration from file or create default."""
    global _config
    
    config_dict = {}
    if config_path and Path(config_path).exists():
        with open(config_path, 'r') as f:
            config_dict = json.load(f)
    
    _config = Config(config_dict)
    return _config


def get_config() -> Config:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = load_config()
    return _config
