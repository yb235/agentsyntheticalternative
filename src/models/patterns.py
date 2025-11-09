"""Pattern recognition data models."""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class FrequencyReport:
    """Report of concept frequencies across documents."""
    
    high_frequency_concepts: List[Dict] = field(default_factory=list)
    frequency_distribution: Dict = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "high_frequency_concepts": self.high_frequency_concepts,
            "frequency_distribution": self.frequency_distribution,
        }


@dataclass
class CooccurrenceReport:
    """Report of concept co-occurrences."""
    
    strong_cooccurrences: List[Dict] = field(default_factory=list)
    causal_chains: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "strong_cooccurrences": self.strong_cooccurrences,
            "causal_chains": self.causal_chains,
        }


@dataclass
class PatternReport:
    """Aggregated pattern recognition report."""
    
    frequency: FrequencyReport = field(default_factory=FrequencyReport)
    cooccurrence: CooccurrenceReport = field(default_factory=CooccurrenceReport)
    temporal: Dict = field(default_factory=dict)
    contradictions: List[Dict] = field(default_factory=list)
    emotional: Dict = field(default_factory=dict)
    negative_space: Dict = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "frequency": self.frequency.to_dict(),
            "cooccurrence": self.cooccurrence.to_dict(),
            "temporal": self.temporal,
            "contradictions": self.contradictions,
            "emotional": self.emotional,
            "negative_space": self.negative_space,
        }
