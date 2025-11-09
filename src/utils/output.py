"""Output generation utilities."""

import json
from pathlib import Path
from typing import Dict
from datetime import datetime


class MarkdownGenerator:
    """Generates markdown output from synthesis results."""
    
    def __init__(self, output_dir: str = "./output"):
        """Initialize markdown generator."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_report(self, final_report: Dict, filename: str = None) -> Path:
        """Generate complete markdown report."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"synthesis_report_{timestamp}.md"
        
        output_file = self.output_dir / filename
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write header
            f.write("# Thematic Insight Extraction Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Write metadata
            self._write_metadata(f, final_report.get("metadata", {}))
            
            # Write synthesis chapters
            self._write_synthesis(f, final_report.get("synthesis", []))
            
            # Write validation summary
            self._write_validation(f, final_report.get("validation", {}))
            
            # Write patterns
            self._write_patterns(f, final_report.get("patterns", {}))
        
        return output_file
    
    def _write_metadata(self, f, metadata: Dict):
        """Write metadata section."""
        f.write("## Overview\n\n")
        f.write(f"- **Total Documents Analyzed:** {metadata.get('total_documents', 0)}\n")
        f.write(f"- **Themes Identified:** {metadata.get('total_themes', 0)}\n")
        f.write(f"- **Overall Quality Score:** {metadata.get('overall_quality_score', 0):.2f}/10\n")
        f.write(f"- **Processing Stage:** {metadata.get('stage', 'unknown')}\n\n")
        f.write("---\n\n")
    
    def _write_synthesis(self, f, synthesis_chapters: list):
        """Write synthesis chapters."""
        f.write("## Synthesis by Theme\n\n")
        
        for chapter in synthesis_chapters:
            f.write(f"### {chapter.get('theme_name', 'Unknown Theme')}\n\n")
            
            # Executive summary
            if chapter.get('executive_summary'):
                f.write("#### Executive Summary\n\n")
                f.write(f"{chapter['executive_summary']}\n\n")
            
            # Core principles
            if chapter.get('core_principles'):
                f.write("#### Core Principles\n\n")
                for i, principle in enumerate(chapter['core_principles'], 1):
                    f.write(f"**{i}. {principle.get('principle', 'N/A')}**\n\n")
                    
                    if principle.get('evidence'):
                        f.write("*Evidence:*\n")
                        for evidence in principle['evidence'][:3]:
                            f.write(f"- {evidence}\n")
                        f.write("\n")
                    
                    if principle.get('implications'):
                        f.write("*Implications:*\n")
                        for implication in principle['implications']:
                            f.write(f"- {implication}\n")
                        f.write("\n")
                    
                    if principle.get('confidence'):
                        f.write(f"*Confidence:* {principle['confidence']:.2f}\n\n")
            
            # Actionable rules
            if chapter.get('actionable_rules'):
                rules = chapter['actionable_rules']
                
                if rules.get('do'):
                    f.write("#### DO:\n\n")
                    for rule in rules['do']:
                        f.write(f"- {rule}\n")
                    f.write("\n")
                
                if rules.get('dont'):
                    f.write("#### DON'T:\n\n")
                    for rule in rules['dont']:
                        f.write(f"- {rule}\n")
                    f.write("\n")
            
            # Contradictions
            if chapter.get('contradictions'):
                f.write("#### Contradictions Identified\n\n")
                for contradiction in chapter['contradictions']:
                    f.write(f"- **{contradiction.get('description', 'N/A')}**\n")
                    f.write(f"  - Status: {contradiction.get('resolution_status', 'unresolved')}\n")
                    if contradiction.get('attempted_resolution'):
                        f.write(f"  - Resolution: {contradiction['attempted_resolution']}\n")
                    f.write("\n")
            
            # Key quotes
            if chapter.get('key_quotes'):
                f.write("#### Key Quotes\n\n")
                for quote in chapter['key_quotes']:
                    f.write(f"> {quote}\n\n")
            
            # Open questions
            if chapter.get('open_questions'):
                f.write("#### Open Questions\n\n")
                for question in chapter['open_questions']:
                    f.write(f"- {question}\n")
                f.write("\n")
            
            f.write("---\n\n")
    
    def _write_validation(self, f, validation: Dict):
        """Write validation summary."""
        f.write("## Validation Summary\n\n")
        
        f.write(f"**Overall Quality Score:** {validation.get('overall_quality_score', 0):.2f}/10\n\n")
        
        # Internal validation
        if validation.get('internal_validation'):
            internal = validation['internal_validation']
            if internal.get('accuracy_check'):
                acc = internal['accuracy_check']
                f.write(f"- **Accuracy Check:** {acc.get('status', 'unknown')} (score: {acc.get('score', 0):.2f})\n")
        
        # Red flags
        if validation.get('red_flags'):
            f.write("\n### Red Flags\n\n")
            for flag in validation['red_flags']:
                f.write(f"- **{flag.get('flag', 'N/A')}**\n")
                f.write(f"  - Severity: {flag.get('severity', 'unknown')}\n")
                f.write(f"  - Recommendation: {flag.get('recommendation', 'N/A')}\n")
        
        f.write("\n---\n\n")
    
    def _write_patterns(self, f, patterns: Dict):
        """Write pattern analysis."""
        f.write("## Pattern Analysis\n\n")
        
        # Frequency patterns
        if patterns.get('frequency'):
            freq = patterns['frequency']
            if freq.get('high_frequency_concepts'):
                f.write("### High-Frequency Concepts\n\n")
                for concept in freq['high_frequency_concepts'][:10]:
                    f.write(f"- **{concept.get('concept', 'N/A')}**: {concept.get('count', 0)} occurrences\n")
                    f.write(f"  - {concept.get('significance', '')}\n")
                f.write("\n")
        
        # Co-occurrence patterns
        if patterns.get('cooccurrence'):
            cooc = patterns['cooccurrence']
            if cooc.get('strong_cooccurrences'):
                f.write("### Strong Co-occurrences\n\n")
                for pair in cooc['strong_cooccurrences'][:5]:
                    f.write(f"- **{pair.get('concept_a', 'N/A')}** ↔ **{pair.get('concept_b', 'N/A')}**\n")
                    f.write(f"  - {pair.get('interpretation', '')}\n")
                f.write("\n")
        
        f.write("---\n\n")
    
    def save_json(self, final_report: Dict, filename: str = None) -> Path:
        """Save report as JSON."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"synthesis_report_{timestamp}.json"
        
        output_file = self.output_dir / filename
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(final_report, f, indent=2, ensure_ascii=False)
        
        return output_file
