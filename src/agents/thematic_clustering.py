"""Thematic Clustering Agent - Stage 2: Categorization."""

from typing import List, Dict
from collections import defaultdict
from .base import BaseAgent
from ..models import AnalyzedDocument, Theme, ThemeStructure, PatternReport


class ThematicClusteringAgent(BaseAgent):
    """Groups related documents into coherent themes."""
    
    def __init__(self, config: Dict = None):
        """Initialize thematic clustering agent."""
        super().__init__("ThematicClustering", config)
    
    def process(self, analyzed_docs: List[AnalyzedDocument], 
                patterns: PatternReport) -> ThemeStructure:
        """Cluster documents into themes."""
        self.log_info(f"Clustering {len(analyzed_docs)} documents into themes")
        
        # For MVP, use simple tag-based clustering
        themes = self._cluster_by_tags(analyzed_docs, patterns)
        
        # Identify cross-theme patterns
        cross_theme_patterns = self._identify_cross_patterns(themes, patterns)
        
        # Identify orphan documents
        orphans = self._identify_orphans(analyzed_docs, themes)
        
        structure = ThemeStructure(
            themes=themes,
            cross_theme_patterns=cross_theme_patterns,
            orphan_documents=orphans
        )
        
        self.log_info(f"Created {len(themes)} themes")
        return structure
    
    def _cluster_by_tags(self, analyzed_docs: List[AnalyzedDocument], 
                         patterns: PatternReport) -> List[Theme]:
        """Cluster documents by tags."""
        # Group documents by primary tag
        tag_groups = defaultdict(list)
        
        for doc in analyzed_docs:
            if doc.tags:
                primary_tag = doc.tags[0]  # Use first tag as primary
                tag_groups[primary_tag].append(doc.document_id)
        
        # Create themes from tag groups
        themes = []
        for idx, (tag, doc_ids) in enumerate(tag_groups.items()):
            if len(doc_ids) >= 2:  # At least 2 documents to form a theme
                theme = Theme(
                    theme_id=f"theme_{idx:03d}",
                    name=self._generate_theme_name(tag),
                    description=self._generate_theme_description(tag, doc_ids),
                    document_ids=doc_ids,
                    key_concepts=[tag],
                    importance_score=self._calculate_importance(len(doc_ids), len(analyzed_docs)),
                )
                themes.append(theme)
        
        return themes
    
    def _generate_theme_name(self, tag: str) -> str:
        """Generate theme name from tag."""
        # Convert tag to title case
        name_map = {
            "psychology": "Investment Psychology & Mental States",
            "risk-management": "Risk Management & Position Sizing",
            "technical-analysis": "Technical Analysis Approach",
            "fundamental-analysis": "Fundamental Analysis Framework",
            "post-mortem": "Learning from Mistakes",
            "strategy": "Investment Strategy & Philosophy",
            "discipline": "Discipline & Process",
        }
        return name_map.get(tag, tag.replace("-", " ").title())
    
    def _generate_theme_description(self, tag: str, doc_ids: List[str]) -> str:
        """Generate theme description."""
        return f"Theme covering {len(doc_ids)} documents related to {tag}"
    
    def _calculate_importance(self, doc_count: int, total_docs: int) -> float:
        """Calculate theme importance score."""
        # Simple heuristic: percentage of total documents, scaled to 0-10
        return min((doc_count / total_docs) * 30, 10.0)
    
    def _identify_cross_patterns(self, themes: List[Theme], 
                                 patterns: PatternReport) -> List[Dict]:
        """Identify patterns that cut across themes."""
        cross_patterns = []
        
        # Check if any concept appears in multiple themes
        concept_themes = defaultdict(list)
        for theme in themes:
            for concept in theme.key_concepts:
                concept_themes[concept].append(theme.theme_id)
        
        for concept, theme_ids in concept_themes.items():
            if len(theme_ids) > 1:
                cross_patterns.append({
                    "pattern": f"{concept} appears across {len(theme_ids)} themes",
                    "themes": theme_ids,
                    "significance": "Cross-cutting concept",
                })
        
        return cross_patterns
    
    def _identify_orphans(self, analyzed_docs: List[AnalyzedDocument], 
                         themes: List[Theme]) -> List[Dict]:
        """Identify documents not assigned to any theme."""
        assigned_doc_ids = set()
        for theme in themes:
            assigned_doc_ids.update(theme.document_ids)
        
        orphans = []
        for doc in analyzed_docs:
            if doc.document_id not in assigned_doc_ids:
                orphans.append({
                    "doc_id": doc.document_id,
                    "reason": "No matching theme found",
                    "recommendation": "Create new theme or manual assignment",
                })
        
        return orphans
