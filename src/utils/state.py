"""State management and checkpointing."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Dict
from ..models import AnalyzedDocument, ThemeStructure, SynthesisChapter, ValidationReport


class StateManager:
    """Manages synthesis state and checkpointing."""
    
    def __init__(self, checkpoint_dir: str = "./checkpoints"):
        """Initialize state manager."""
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        
        self.stage = "initialized"
        self.documents = []
        self.analyzed_documents = []
        self.patterns = None
        self.themes = None
        self.synthesis_chapters = []
        self.validation_report = None
    
    def save_checkpoint(self, stage: str, data: Any):
        """Save checkpoint for current stage."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        checkpoint_file = self.checkpoint_dir / f"checkpoint_{stage}_{timestamp}.json"
        
        checkpoint_data = {
            "stage": stage,
            "timestamp": timestamp,
            "data": self._serialize_data(data)
        }
        
        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint_data, f, indent=2, ensure_ascii=False)
        
        # Also save as latest
        latest_file = self.checkpoint_dir / f"checkpoint_{stage}_latest.json"
        with open(latest_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint_data, f, indent=2, ensure_ascii=False)
        
        return checkpoint_file
    
    def load_checkpoint(self, stage: str, use_latest: bool = True) -> Optional[Dict]:
        """Load checkpoint for specified stage."""
        if use_latest:
            checkpoint_file = self.checkpoint_dir / f"checkpoint_{stage}_latest.json"
        else:
            # Find most recent checkpoint for this stage
            checkpoints = list(self.checkpoint_dir.glob(f"checkpoint_{stage}_*.json"))
            if not checkpoints:
                return None
            checkpoint_file = max(checkpoints, key=lambda p: p.stat().st_mtime)
        
        if not checkpoint_file.exists():
            return None
        
        with open(checkpoint_file, 'r', encoding='utf-8') as f:
            checkpoint_data = json.load(f)
        
        return checkpoint_data
    
    def _serialize_data(self, data: Any) -> Any:
        """Serialize data for checkpoint."""
        if isinstance(data, list):
            return [self._serialize_data(item) for item in data]
        elif hasattr(data, 'to_dict'):
            return data.to_dict()
        elif isinstance(data, dict):
            return {k: self._serialize_data(v) for k, v in data.items()}
        else:
            return data
    
    def set_stage(self, stage: str):
        """Set current stage."""
        self.stage = stage
    
    def get_stage(self) -> str:
        """Get current stage."""
        return self.stage
