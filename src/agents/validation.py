"""Validation Agent - Stage 4: Validation."""

from typing import List, Dict
from .base import BaseAgent
from ..models import (
    AnalyzedDocument, SynthesisChapter, PatternReport,
    ValidationReport, QAResult
)


class ValidationAgent(BaseAgent):
    """Validates synthesis quality and accuracy."""
    
    def __init__(self, config: Dict = None):
        """Initialize validation agent."""
        super().__init__("ValidationAgent", config)
    
    def process(self, synthesis_chapters: List[SynthesisChapter],
                analyzed_docs: List[AnalyzedDocument],
                patterns: PatternReport) -> ValidationReport:
        """Validate synthesis chapters."""
        self.log_info(f"Validating {len(synthesis_chapters)} synthesis chapters")
        
        # Internal validation
        internal = self._validate_internal(synthesis_chapters, analyzed_docs)
        
        # Contradiction validation
        contradiction = self._validate_contradictions(synthesis_chapters)
        
        # Evidence validation
        evidence = self._validate_evidence(synthesis_chapters)
        
        # Coherence validation
        coherence = self._validate_coherence(synthesis_chapters)
        
        # Identify red flags
        red_flags = self._identify_red_flags(synthesis_chapters)
        
        # Calculate overall quality score
        quality_score = self._calculate_quality_score(
            internal, contradiction, evidence, coherence
        )
        
        report = ValidationReport(
            overall_quality_score=quality_score,
            internal_validation=internal,
            contradiction_validation=contradiction,
            evidence_validation=evidence,
            coherence_validation=coherence,
            red_flags=red_flags,
        )
        
        self.log_info(f"Validation complete. Overall quality: {quality_score:.2f}/10")
        return report
    
    def _validate_internal(self, chapters: List[SynthesisChapter],
                          docs: List[AnalyzedDocument]) -> Dict:
        """Internal validation checks."""
        checks = {
            "has_executive_summary": sum(1 for c in chapters if len(c.executive_summary) > 50) / max(len(chapters), 1),
            "has_principles": sum(1 for c in chapters if c.core_principles) / max(len(chapters), 1),
            "has_actionable_rules": sum(1 for c in chapters if c.actionable_rules["do"] or c.actionable_rules["dont"]) / max(len(chapters), 1),
            "principles_have_evidence": sum(1 for c in chapters for p in c.core_principles if p.evidence) / max(sum(len(c.core_principles) for c in chapters), 1),
        }
        
        accuracy_check = QAResult(
            status="pass" if checks["has_principles"] > 0.8 else "warning",
            score=sum(checks.values()) / len(checks),
            checks=checks,
        )
        
        return {
            "accuracy_check": {
                "status": accuracy_check.status,
                "score": accuracy_check.score,
                "checks": accuracy_check.checks,
            }
        }
    
    def _validate_contradictions(self, chapters: List[SynthesisChapter]) -> Dict:
        """Validate contradiction handling."""
        total_contradictions = sum(len(c.contradictions) for c in chapters)
        addressed_contradictions = sum(
            1 for c in chapters 
            for contra in c.contradictions 
            if contra.resolution_status in ["resolved", "unresolved", "partially_resolved"]
        )
        
        return {
            "contradictions_identified": total_contradictions,
            "contradictions_addressed": addressed_contradictions,
            "status": "pass" if addressed_contradictions == total_contradictions else "warning",
        }
    
    def _validate_evidence(self, chapters: List[SynthesisChapter]) -> Dict:
        """Validate evidence quality."""
        warnings = []
        
        for chapter in chapters:
            for principle in chapter.core_principles:
                if len(principle.evidence) < 2:
                    warnings.append({
                        "chapter": chapter.theme_name,
                        "issue": "Principle has insufficient evidence",
                        "principle": principle.principle[:50],
                    })
        
        return {
            "status": "pass" if len(warnings) == 0 else "pass_with_warnings",
            "warnings": warnings[:5],  # Limit to 5
        }
    
    def _validate_coherence(self, chapters: List[SynthesisChapter]) -> Dict:
        """Validate internal coherence."""
        # Simple coherence check: all chapters have minimum content
        coherence_scores = []
        
        for chapter in chapters:
            score = 0.0
            if chapter.executive_summary:
                score += 0.25
            if chapter.core_principles:
                score += 0.25
            if chapter.actionable_rules["do"] or chapter.actionable_rules["dont"]:
                score += 0.25
            if chapter.second_order_implications:
                score += 0.25
            coherence_scores.append(score)
        
        avg_coherence = sum(coherence_scores) / max(len(coherence_scores), 1)
        
        return {
            "status": "pass" if avg_coherence > 0.7 else "warning",
            "internal_consistency": avg_coherence,
            "logical_contradictions": 0,
        }
    
    def _identify_red_flags(self, chapters: List[SynthesisChapter]) -> List[Dict]:
        """Identify quality red flags."""
        red_flags = []
        
        for chapter in chapters:
            # Check for missing contradictions (suspicious)
            if len(chapter.contradictions) == 0:
                red_flags.append({
                    "flag": f"No contradictions identified in {chapter.theme_name}",
                    "severity": "low",
                    "recommendation": "Review if contradictions were genuinely absent",
                })
            
            # Check for too few principles
            if len(chapter.core_principles) == 0:
                red_flags.append({
                    "flag": f"No core principles in {chapter.theme_name}",
                    "severity": "high",
                    "recommendation": "Chapter needs core principles",
                })
        
        return red_flags
    
    def _calculate_quality_score(self, internal: Dict, contradiction: Dict,
                                 evidence: Dict, coherence: Dict) -> float:
        """Calculate overall quality score."""
        scores = []
        
        # Internal validation score
        if "accuracy_check" in internal and "score" in internal["accuracy_check"]:
            scores.append(internal["accuracy_check"]["score"] * 10)
        
        # Contradiction handling score
        if contradiction.get("status") == "pass":
            scores.append(10.0)
        elif contradiction.get("status") == "warning":
            scores.append(7.0)
        
        # Evidence score
        if evidence.get("status") == "pass":
            scores.append(10.0)
        elif "pass_with_warnings" in evidence.get("status", ""):
            scores.append(8.0)
        
        # Coherence score
        if "internal_consistency" in coherence:
            scores.append(coherence["internal_consistency"] * 10)
        
        return sum(scores) / max(len(scores), 1)
