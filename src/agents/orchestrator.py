"""Orchestrator Agent - Coordinates the entire synthesis workflow."""

from typing import List, Optional, Dict
from pathlib import Path
from .base import BaseAgent
from .document_analyzer import DocumentAnalyzerAgent
from .pattern_recognition import FrequencyAnalyzer, CooccurrenceAnalyzer
from .thematic_clustering import ThematicClusteringAgent
from .synthesis import SynthesisAgent
from .validation import ValidationAgent
from ..models import Document, PatternReport
from ..utils import StateManager


class OrchestratorAgent(BaseAgent):
    """Orchestrates the multi-agent synthesis workflow."""
    
    def __init__(self, config: Dict = None):
        """Initialize orchestrator agent."""
        super().__init__("Orchestrator", config)
        
        # Initialize state manager
        checkpoint_dir = self.config.get("checkpoints", {}).get("directory", "./checkpoints")
        self.state_manager = StateManager(checkpoint_dir)
        
        # Initialize sub-agents
        self.document_analyzer = DocumentAnalyzerAgent(config)
        self.frequency_analyzer = FrequencyAnalyzer(config)
        self.cooccurrence_analyzer = CooccurrenceAnalyzer(config)
        self.thematic_clustering = ThematicClusteringAgent(config)
        self.synthesis_agent = SynthesisAgent(config)
        self.validation_agent = ValidationAgent(config)
        
        self.log_info("Orchestrator initialized with all sub-agents")
    
    def process(self, documents: List[Document]) -> Dict:
        """Run the complete synthesis workflow."""
        self.log_info(f"Starting synthesis workflow with {len(documents)} documents")
        
        try:
            # Stage 1: Deconstruction
            analyzed_docs = self._stage_1_deconstruction(documents)
            
            # Pattern Recognition (parallel)
            patterns = self._pattern_recognition(analyzed_docs)
            
            # Stage 2: Categorization
            themes = self._stage_2_categorization(analyzed_docs, patterns)
            
            # Stage 3: Synthesis
            synthesis_chapters = self._stage_3_synthesis(themes, analyzed_docs, patterns)
            
            # Stage 4: Validation
            validation_report = self._stage_4_validation(
                synthesis_chapters, analyzed_docs, patterns
            )
            
            # Compile final report
            final_report = self._compile_final_report(
                analyzed_docs, themes, synthesis_chapters, 
                validation_report, patterns
            )
            
            self.log_info("Synthesis workflow completed successfully")
            return final_report
            
        except Exception as e:
            self.log_error(f"Synthesis workflow failed: {str(e)}")
            raise
    
    def _stage_1_deconstruction(self, documents: List[Document]):
        """Stage 1: Document Analysis."""
        self.log_info("=== STAGE 1: DECONSTRUCTION ===")
        
        analyzed_docs = self.document_analyzer.process(documents)
        
        # Save checkpoint
        if self.config.get("checkpoints", {}).get("enabled", True):
            checkpoint_file = self.state_manager.save_checkpoint(
                "stage1_deconstruction", 
                analyzed_docs
            )
            self.log_info(f"Checkpoint saved: {checkpoint_file}")
        
        self.state_manager.analyzed_documents = analyzed_docs
        self.state_manager.set_stage("stage1_complete")
        
        return analyzed_docs
    
    def _pattern_recognition(self, analyzed_docs):
        """Pattern Recognition (cross-cutting)."""
        self.log_info("=== PATTERN RECOGNITION ===")
        
        # Run pattern analyzers
        frequency_report = self.frequency_analyzer.process(analyzed_docs)
        cooccurrence_report = self.cooccurrence_analyzer.process(analyzed_docs)
        
        # Compile pattern report
        patterns = PatternReport(
            frequency=frequency_report,
            cooccurrence=cooccurrence_report,
        )
        
        # Save checkpoint
        if self.config.get("checkpoints", {}).get("enabled", True):
            checkpoint_file = self.state_manager.save_checkpoint(
                "pattern_recognition",
                patterns
            )
            self.log_info(f"Checkpoint saved: {checkpoint_file}")
        
        self.state_manager.patterns = patterns
        
        return patterns
    
    def _stage_2_categorization(self, analyzed_docs, patterns):
        """Stage 2: Thematic Clustering."""
        self.log_info("=== STAGE 2: CATEGORIZATION ===")
        
        theme_structure = self.thematic_clustering.process(analyzed_docs, patterns)
        
        # Save checkpoint
        if self.config.get("checkpoints", {}).get("enabled", True):
            checkpoint_file = self.state_manager.save_checkpoint(
                "stage2_categorization",
                theme_structure
            )
            self.log_info(f"Checkpoint saved: {checkpoint_file}")
        
        self.state_manager.themes = theme_structure
        self.state_manager.set_stage("stage2_complete")
        
        return theme_structure
    
    def _stage_3_synthesis(self, theme_structure, analyzed_docs, patterns):
        """Stage 3: Synthesis."""
        self.log_info("=== STAGE 3: SYNTHESIS ===")
        
        synthesis_chapters = self.synthesis_agent.process(
            theme_structure.themes,
            analyzed_docs,
            patterns
        )
        
        # Save checkpoint
        if self.config.get("checkpoints", {}).get("enabled", True):
            checkpoint_file = self.state_manager.save_checkpoint(
                "stage3_synthesis",
                synthesis_chapters
            )
            self.log_info(f"Checkpoint saved: {checkpoint_file}")
        
        self.state_manager.synthesis_chapters = synthesis_chapters
        self.state_manager.set_stage("stage3_complete")
        
        return synthesis_chapters
    
    def _stage_4_validation(self, synthesis_chapters, analyzed_docs, patterns):
        """Stage 4: Validation."""
        self.log_info("=== STAGE 4: VALIDATION ===")
        
        validation_report = self.validation_agent.process(
            synthesis_chapters,
            analyzed_docs,
            patterns
        )
        
        # Save checkpoint
        if self.config.get("checkpoints", {}).get("enabled", True):
            checkpoint_file = self.state_manager.save_checkpoint(
                "stage4_validation",
                validation_report
            )
            self.log_info(f"Checkpoint saved: {checkpoint_file}")
        
        self.state_manager.validation_report = validation_report
        self.state_manager.set_stage("stage4_complete")
        
        return validation_report
    
    def _compile_final_report(self, analyzed_docs, theme_structure, 
                             synthesis_chapters, validation_report, patterns):
        """Compile final synthesis report."""
        self.log_info("Compiling final report")
        
        final_report = {
            "metadata": {
                "total_documents": len(analyzed_docs),
                "total_themes": len(theme_structure.themes),
                "overall_quality_score": validation_report.overall_quality_score,
                "stage": self.state_manager.get_stage(),
            },
            "themes": [theme.to_dict() for theme in theme_structure.themes],
            "synthesis": [chapter.to_dict() for chapter in synthesis_chapters],
            "validation": validation_report.to_dict(),
            "patterns": patterns.to_dict(),
        }
        
        return final_report
