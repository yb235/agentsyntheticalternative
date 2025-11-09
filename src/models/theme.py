"""Theme data models."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Theme:
    """A thematic cluster of related documents."""
    
    theme_id: str
    name: str
    description: str
    document_ids: List[str] = field(default_factory=list)
    key_concepts: List[str] = field(default_factory=list)
    importance_score: float = 0.0
    cross_cutting: bool = False
    related_theme_ids: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "theme_id": self.theme_id,
            "name": self.name,
            "description": self.description,
            "document_ids": self.document_ids,
            "key_concepts": self.key_concepts,
            "importance_score": self.importance_score,
            "cross_cutting": self.cross_cutting,
            "related_theme_ids": self.related_theme_ids,
        }


@dataclass
class ThemeStructure:
    """Overall theme structure for a document collection."""
    
    themes: List[Theme] = field(default_factory=list)
    cross_theme_patterns: List[dict] = field(default_factory=list)
    orphan_documents: List[dict] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "themes": [theme.to_dict() for theme in self.themes],
            "cross_theme_patterns": self.cross_theme_patterns,
            "orphan_documents": self.orphan_documents,
        }
