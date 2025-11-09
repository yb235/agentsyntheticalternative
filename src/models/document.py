"""Document data models."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass(frozen=True)
class Document:
    """Raw document input."""
    
    document_id: str
    filename: str
    content: str
    date_created: Optional[datetime] = None
    metadata: dict = field(default_factory=dict)


@dataclass
class ActionableRules:
    """Actionable rules extracted from document."""
    
    do: List[str] = field(default_factory=list)
    dont: List[str] = field(default_factory=list)
    when: List[dict] = field(default_factory=list)


@dataclass
class TriggeringContext:
    """Context that triggered the document."""
    
    emotional_state: Optional[str] = None
    market_condition: Optional[str] = None
    triggering_event: Optional[str] = None


@dataclass
class AnalyzedDocument:
    """Analyzed document with extracted structured data."""
    
    document_id: str
    filename: str
    original_content: str
    date_created: Optional[datetime] = None
    
    # Extracted information
    core_principle: str = ""
    actionable_rules: ActionableRules = field(default_factory=ActionableRules)
    triggering_context: TriggeringContext = field(default_factory=TriggeringContext)
    evidence: List[str] = field(default_factory=list)
    contradictions: List[dict] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    
    # Metadata
    quality_score: float = 0.0
    emotional_valence: Optional[str] = None
    document_type: Optional[str] = None
    confidence: float = 0.0
    reasoning: str = ""
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "document_id": self.document_id,
            "filename": self.filename,
            "date_created": self.date_created.isoformat() if self.date_created else None,
            "core_principle": self.core_principle,
            "actionable_rules": {
                "do": self.actionable_rules.do,
                "dont": self.actionable_rules.dont,
                "when": self.actionable_rules.when,
            },
            "triggering_context": {
                "emotional_state": self.triggering_context.emotional_state,
                "market_condition": self.triggering_context.market_condition,
                "triggering_event": self.triggering_context.triggering_event,
            },
            "evidence": self.evidence,
            "contradictions": self.contradictions,
            "tags": self.tags,
            "quality_score": self.quality_score,
            "emotional_valence": self.emotional_valence,
            "document_type": self.document_type,
            "confidence": self.confidence,
            "reasoning": self.reasoning,
        }
