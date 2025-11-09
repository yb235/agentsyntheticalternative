"""Synthesis data models."""

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class CorePrinciple:
    """A core principle extracted from synthesis."""
    
    principle: str
    evidence: List[str] = field(default_factory=list)
    implications: List[str] = field(default_factory=list)
    boundary_conditions: str = ""
    confidence: float = 0.0


@dataclass
class Contradiction:
    """A contradiction between different positions."""
    
    contradiction_id: str
    description: str
    position_a: dict = field(default_factory=dict)
    position_b: dict = field(default_factory=dict)
    resolution_status: str = "unresolved"
    attempted_resolution: Optional[dict] = None


@dataclass
class SynthesisChapter:
    """Synthesis chapter for a single theme."""
    
    theme_id: str
    theme_name: str
    executive_summary: str = ""
    
    # Content
    evolution_of_thought: Dict = field(default_factory=dict)
    core_principles: List[CorePrinciple] = field(default_factory=list)
    actionable_rules: Dict = field(default_factory=lambda: {
        "do": [],
        "dont": [],
        "when_to": []
    })
    contradictions: List[Contradiction] = field(default_factory=list)
    key_quotes: List[str] = field(default_factory=list)
    second_order_implications: List[str] = field(default_factory=list)
    open_questions: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "theme_id": self.theme_id,
            "theme_name": self.theme_name,
            "executive_summary": self.executive_summary,
            "evolution_of_thought": self.evolution_of_thought,
            "core_principles": [
                {
                    "principle": p.principle,
                    "evidence": p.evidence,
                    "implications": p.implications,
                    "boundary_conditions": p.boundary_conditions,
                    "confidence": p.confidence,
                }
                for p in self.core_principles
            ],
            "actionable_rules": self.actionable_rules,
            "contradictions": [
                {
                    "contradiction_id": c.contradiction_id,
                    "description": c.description,
                    "position_a": c.position_a,
                    "position_b": c.position_b,
                    "resolution_status": c.resolution_status,
                    "attempted_resolution": c.attempted_resolution,
                }
                for c in self.contradictions
            ],
            "key_quotes": self.key_quotes,
            "second_order_implications": self.second_order_implications,
            "open_questions": self.open_questions,
        }
