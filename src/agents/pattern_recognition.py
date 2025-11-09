"""Pattern Recognition Agents."""

from collections import Counter, defaultdict
from typing import List, Dict
from .base import BaseAgent
from ..models import AnalyzedDocument, FrequencyReport, CooccurrenceReport


class FrequencyAnalyzer(BaseAgent):
    """Analyzes concept frequencies across documents."""
    
    def __init__(self, config: Dict = None):
        """Initialize frequency analyzer."""
        super().__init__("FrequencyAnalyzer", config)
    
    def process(self, analyzed_docs: List[AnalyzedDocument]) -> FrequencyReport:
        """Analyze frequency patterns."""
        self.log_info(f"Analyzing frequency patterns across {len(analyzed_docs)} documents")
        
        concept_counter = Counter()
        concept_docs = defaultdict(list)
        
        for doc in analyzed_docs:
            concepts = self._extract_concepts(doc)
            for concept in concepts:
                concept_counter[concept] += 1
                concept_docs[concept].append(doc.document_id)
        
        # Identify high-frequency concepts
        high_frequency = []
        significance_threshold = max(3, len(analyzed_docs) * 0.1)  # At least 10% or 3 docs
        
        for concept, count in concept_counter.most_common(20):
            if count >= significance_threshold:
                high_frequency.append({
                    "concept": concept,
                    "count": count,
                    "documents": concept_docs[concept],
                    "significance": f"Appears in {count} documents ({count/len(analyzed_docs)*100:.1f}%)",
                })
        
        # Create frequency distribution
        frequency_distribution = {
            "1-5 mentions": [],
            "6-10 mentions": [],
            "11-20 mentions": [],
            "20+ mentions": [],
        }
        
        for concept, count in concept_counter.items():
            if count <= 5:
                frequency_distribution["1-5 mentions"].append(concept)
            elif count <= 10:
                frequency_distribution["6-10 mentions"].append(concept)
            elif count <= 20:
                frequency_distribution["11-20 mentions"].append(concept)
            else:
                frequency_distribution["20+ mentions"].append(concept)
        
        report = FrequencyReport(
            high_frequency_concepts=high_frequency,
            frequency_distribution=frequency_distribution
        )
        
        self.log_info(f"Found {len(high_frequency)} high-frequency concepts")
        return report
    
    def _extract_concepts(self, doc: AnalyzedDocument) -> List[str]:
        """Extract concepts from document."""
        concepts = []
        
        # Add tags as concepts
        concepts.extend(doc.tags)
        
        # Extract key terms from core principle
        if doc.core_principle:
            # Simple keyword extraction
            words = doc.core_principle.lower().split()
            # Filter meaningful words (length > 4)
            concepts.extend([w for w in words if len(w) > 4])
        
        return concepts


class CooccurrenceAnalyzer(BaseAgent):
    """Analyzes concept co-occurrences."""
    
    def __init__(self, config: Dict = None):
        """Initialize co-occurrence analyzer."""
        super().__init__("CooccurrenceAnalyzer", config)
    
    def process(self, analyzed_docs: List[AnalyzedDocument]) -> CooccurrenceReport:
        """Analyze co-occurrence patterns."""
        self.log_info(f"Analyzing co-occurrence patterns across {len(analyzed_docs)} documents")
        
        # Build co-occurrence matrix
        concept_pairs = defaultdict(int)
        concept_counts = Counter()
        
        for doc in analyzed_docs:
            concepts = list(set(doc.tags))  # Unique concepts per document
            
            # Count individual concepts
            for concept in concepts:
                concept_counts[concept] += 1
            
            # Count pairs
            for i, concept_a in enumerate(concepts):
                for concept_b in concepts[i+1:]:
                    pair = tuple(sorted([concept_a, concept_b]))
                    concept_pairs[pair] += 1
        
        # Identify strong co-occurrences
        strong_cooccurrences = []
        for (concept_a, concept_b), cooccur_count in concept_pairs.items():
            if cooccur_count >= 2:  # Appear together at least twice
                total_a = concept_counts[concept_a]
                total_b = concept_counts[concept_b]
                cooccur_rate = cooccur_count / min(total_a, total_b)
                
                if cooccur_rate >= 0.5:  # At least 50% co-occurrence rate
                    strong_cooccurrences.append({
                        "concept_a": concept_a,
                        "concept_b": concept_b,
                        "cooccurrence_count": cooccur_count,
                        "total_a_mentions": total_a,
                        "total_b_mentions": total_b,
                        "cooccurrence_rate": cooccur_rate,
                        "interpretation": f"{cooccur_rate*100:.0f}% of '{concept_a}' mentions include '{concept_b}'",
                    })
        
        # Sort by co-occurrence count
        strong_cooccurrences.sort(key=lambda x: x["cooccurrence_count"], reverse=True)
        
        report = CooccurrenceReport(
            strong_cooccurrences=strong_cooccurrences[:10],  # Top 10
            causal_chains=[]  # Placeholder for MVP
        )
        
        self.log_info(f"Found {len(strong_cooccurrences)} strong co-occurrences")
        return report
