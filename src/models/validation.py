"""Validation data models."""

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class QAResult:
    """Quality assurance result for a component."""
    
    status: str  # "pass", "fail", "warning", "critical_fail"
    score: float = 0.0
    checks: Dict = field(default_factory=dict)
    message: Optional[str] = None


@dataclass
class ValidationReport:
    """Validation report for synthesis."""
    
    overall_quality_score: float = 0.0
    
    # Validation results
    internal_validation: Dict = field(default_factory=dict)
    contradiction_validation: Dict = field(default_factory=dict)
    evolution_validation: Dict = field(default_factory=dict)
    evidence_validation: Dict = field(default_factory=dict)
    coherence_validation: Dict = field(default_factory=dict)
    
    # Issues and corrections
    red_flags: List[Dict] = field(default_factory=list)
    corrections_required: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "overall_quality_score": self.overall_quality_score,
            "internal_validation": self.internal_validation,
            "contradiction_validation": self.contradiction_validation,
            "evolution_validation": self.evolution_validation,
            "evidence_validation": self.evidence_validation,
            "coherence_validation": self.coherence_validation,
            "red_flags": self.red_flags,
            "corrections_required": self.corrections_required,
        }
