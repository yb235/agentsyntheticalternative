"""Synthesis Agent - Stage 3: Synthesis."""

from typing import List, Dict
from .base import BaseAgent
from ..models import (
    AnalyzedDocument, Theme, SynthesisChapter, 
    CorePrinciple, Contradiction, PatternReport
)


class SynthesisAgent(BaseAgent):
    """Generates insights and synthesis for themes."""
    
    def __init__(self, config: Dict = None):
        """Initialize synthesis agent."""
        super().__init__("SynthesisAgent", config)
    
    def process(self, themes: List[Theme], analyzed_docs: List[AnalyzedDocument],
                patterns: PatternReport) -> List[SynthesisChapter]:
        """Synthesize insights for each theme."""
        self.log_info(f"Synthesizing insights for {len(themes)} themes")
        
        chapters = []
        for theme in themes:
            try:
                chapter = self.synthesize_theme(theme, analyzed_docs, patterns)
                chapters.append(chapter)
                self.log_info(f"Synthesized chapter for theme: {theme.name}")
            except Exception as e:
                self.log_error(f"Failed to synthesize theme {theme.theme_id}: {str(e)}")
        
        self.log_info(f"Successfully synthesized {len(chapters)}/{len(themes)} chapters")
        return chapters
    
    def synthesize_theme(self, theme: Theme, analyzed_docs: List[AnalyzedDocument],
                        patterns: PatternReport) -> SynthesisChapter:
        """Synthesize a single theme."""
        # Get documents for this theme
        theme_docs = [doc for doc in analyzed_docs if doc.document_id in theme.document_ids]
        
        # Generate executive summary
        exec_summary = self._generate_executive_summary(theme, theme_docs)
        
        # Extract core principles
        principles = self._extract_principles(theme_docs)
        
        # Generate actionable rules
        rules = self._generate_actionable_rules(theme_docs)
        
        # Identify contradictions
        contradictions = self._identify_contradictions(theme_docs)
        
        # Extract key quotes
        quotes = self._extract_key_quotes(theme_docs)
        
        # Generate implications
        implications = self._generate_implications(principles)
        
        # Identify open questions
        questions = self._identify_open_questions(theme_docs)
        
        return SynthesisChapter(
            theme_id=theme.theme_id,
            theme_name=theme.name,
            executive_summary=exec_summary,
            core_principles=principles,
            actionable_rules=rules,
            contradictions=contradictions,
            key_quotes=quotes,
            second_order_implications=implications,
            open_questions=questions,
        )
    
    def _generate_executive_summary(self, theme: Theme, 
                                   docs: List[AnalyzedDocument]) -> str:
        """Generate executive summary for theme."""
        doc_count = len(docs)
        key_concepts = ", ".join(theme.key_concepts[:3])
        
        return (f"{theme.name} encompasses {doc_count} documents examining {key_concepts}. "
                f"This theme explores key insights and patterns related to these concepts.")
    
    def _extract_principles(self, docs: List[AnalyzedDocument]) -> List[CorePrinciple]:
        """Extract core principles from documents."""
        principles = []
        
        # Aggregate principles from documents
        principle_counts = {}
        for doc in docs:
            if doc.core_principle and len(doc.core_principle) > 20:
                principle = doc.core_principle[:200]
                if principle not in principle_counts:
                    principle_counts[principle] = {
                        "count": 0,
                        "evidence": [],
                        "doc_ids": []
                    }
                principle_counts[principle]["count"] += 1
                principle_counts[principle]["evidence"].extend(doc.evidence[:2])
                principle_counts[principle]["doc_ids"].append(doc.document_id)
        
        # Convert to CorePrinciple objects (top 3)
        sorted_principles = sorted(principle_counts.items(), 
                                  key=lambda x: x[1]["count"], 
                                  reverse=True)
        
        for principle_text, data in sorted_principles[:3]:
            principles.append(CorePrinciple(
                principle=principle_text,
                evidence=data["evidence"][:5],
                implications=[f"Based on {len(data['doc_ids'])} documents"],
                confidence=min(data["count"] / len(docs), 1.0),
            ))
        
        return principles
    
    def _generate_actionable_rules(self, docs: List[AnalyzedDocument]) -> Dict:
        """Generate actionable rules from documents."""
        rules = {
            "do": [],
            "dont": [],
            "when_to": []
        }
        
        # Aggregate rules from all documents
        for doc in docs:
            rules["do"].extend(doc.actionable_rules.do[:2])
            rules["dont"].extend(doc.actionable_rules.dont[:2])
        
        # Deduplicate
        rules["do"] = list(set(rules["do"]))[:5]
        rules["dont"] = list(set(rules["dont"]))[:5]
        
        return rules
    
    def _identify_contradictions(self, docs: List[AnalyzedDocument]) -> List[Contradiction]:
        """Identify contradictions within theme."""
        contradictions = []
        
        # Simple heuristic: look for docs with contradictory info
        for doc in docs:
            if doc.contradictions:
                for contra in doc.contradictions[:2]:
                    contradictions.append(Contradiction(
                        contradiction_id=f"contra_{doc.document_id}",
                        description=str(contra),
                        position_a={"source": doc.document_id},
                        position_b={"source": "other documents"},
                        resolution_status="unresolved",
                    ))
        
        return contradictions[:3]  # Limit to 3
    
    def _extract_key_quotes(self, docs: List[AnalyzedDocument]) -> List[str]:
        """Extract key quotes from documents."""
        quotes = []
        
        for doc in docs:
            if doc.evidence:
                quotes.extend(doc.evidence[:1])
        
        return quotes[:5]  # Top 5 quotes
    
    def _generate_implications(self, principles: List[CorePrinciple]) -> List[str]:
        """Generate second-order implications."""
        implications = []
        
        for principle in principles:
            if principle.implications:
                implications.extend(principle.implications[:1])
        
        if not implications:
            implications.append("Further analysis needed to identify implications")
        
        return implications[:3]
    
    def _identify_open_questions(self, docs: List[AnalyzedDocument]) -> List[str]:
        """Identify open questions."""
        questions = [
            "How can these insights be operationalized?",
            "What additional evidence is needed?",
            "Are there boundary conditions that need exploration?",
        ]
        
        return questions[:3]
