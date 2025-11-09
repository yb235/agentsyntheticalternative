"""Document Analyzer Agent - Stage 1: Deconstruction."""

import json
import re
from typing import List, Optional
from .base import BaseAgent
from ..models import Document, AnalyzedDocument, ActionableRules, TriggeringContext


class DocumentAnalyzerAgent(BaseAgent):
    """Analyzes documents and extracts structured data."""
    
    def __init__(self, config: Optional[dict] = None):
        """Initialize document analyzer agent."""
        super().__init__("DocumentAnalyzer", config)
        self.llm_client = None
        self._init_llm()
    
    def _init_llm(self):
        """Initialize LLM client."""
        provider = self.config.get("llm", {}).get("provider", "mock")
        
        if provider == "openai":
            try:
                import openai
                api_key = self.config.get("llm", {}).get("openai_api_key")
                if api_key:
                    self.llm_client = openai.OpenAI(api_key=api_key)
                    self.log_info("Initialized OpenAI client")
            except ImportError:
                self.log_warning("OpenAI not installed, using mock mode")
        elif provider == "anthropic":
            try:
                import anthropic
                api_key = self.config.get("llm", {}).get("anthropic_api_key")
                if api_key:
                    self.llm_client = anthropic.Anthropic(api_key=api_key)
                    self.log_info("Initialized Anthropic client")
            except ImportError:
                self.log_warning("Anthropic not installed, using mock mode")
    
    def process(self, documents: List[Document]) -> List[AnalyzedDocument]:
        """Process documents and return analyzed versions."""
        self.log_info(f"Processing {len(documents)} documents")
        analyzed_docs = []
        
        for doc in documents:
            try:
                analyzed = self.analyze_document(doc)
                analyzed_docs.append(analyzed)
                self.log_info(f"Analyzed document: {doc.document_id}")
            except Exception as e:
                self.log_error(f"Failed to analyze {doc.document_id}: {str(e)}")
        
        self.log_info(f"Successfully analyzed {len(analyzed_docs)}/{len(documents)} documents")
        return analyzed_docs
    
    def analyze_document(self, document: Document) -> AnalyzedDocument:
        """Analyze a single document."""
        # Extract core principle
        core_principle = self._extract_core_principle(document.content)
        
        # Extract actionable rules
        actionable_rules = self._extract_rules(document.content)
        
        # Analyze context
        context = self._analyze_context(document.content)
        
        # Extract evidence
        evidence = self._extract_evidence(document.content)
        
        # Generate tags
        tags = self._generate_tags(document.content)
        
        # Calculate quality score
        quality_score = self._score_quality(document.content, evidence, actionable_rules)
        
        return AnalyzedDocument(
            document_id=document.document_id,
            filename=document.filename,
            original_content=document.content,
            date_created=document.date_created,
            core_principle=core_principle,
            actionable_rules=actionable_rules,
            triggering_context=context,
            evidence=evidence,
            tags=tags,
            quality_score=quality_score,
        )
    
    def _extract_core_principle(self, content: str) -> str:
        """Extract the core principle from document."""
        if self.llm_client:
            return self._extract_principle_llm(content)
        else:
            return self._extract_principle_mock(content)
    
    def _extract_principle_llm(self, content: str) -> str:
        """Extract principle using LLM."""
        prompt = f"""Analyze this document and extract the SINGLE most important timeless lesson.

Document:
{content[:2000]}

Respond with JSON:
{{
    "core_principle": "One sentence capturing the essence",
    "confidence": 0.0-1.0,
    "reasoning": "Why this is the core principle"
}}
"""
        
        try:
            if hasattr(self.llm_client, 'chat'):  # OpenAI
                response = self.llm_client.chat.completions.create(
                    model=self.config.get("llm", {}).get("model", "gpt-4"),
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )
                content_response = response.choices[0].message.content
            else:  # Anthropic
                response = self.llm_client.messages.create(
                    model=self.config.get("llm", {}).get("model", "claude-3-5-sonnet-20241022"),
                    max_tokens=1000,
                    messages=[{"role": "user", "content": prompt}],
                )
                content_response = response.content[0].text
            
            # Parse JSON response
            result = json.loads(content_response)
            return result.get("core_principle", "")
        except Exception as e:
            self.log_error(f"LLM extraction failed: {str(e)}")
            return self._extract_principle_mock(content)
    
    def _extract_principle_mock(self, content: str) -> str:
        """Extract principle using simple heuristics (mock mode)."""
        # Look for key phrases that indicate principles
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if len(line) > 20 and any(keyword in line.lower() for keyword in 
                                      ['lesson', 'principle', 'learned', 'key', 'important', 'realize']):
                return line[:200]
        
        # Fallback: return first substantial line
        for line in lines:
            line = line.strip()
            if len(line) > 30:
                return line[:200]
        
        return "Core principle extracted from document"
    
    def _extract_rules(self, content: str) -> ActionableRules:
        """Extract actionable rules from document."""
        rules = ActionableRules()
        lines = content.lower().split('\n')
        
        # Pattern matching for rules
        for line in lines:
            line = line.strip()
            # DO rules
            if any(keyword in line for keyword in ['should', 'must', 'always', 'do:']):
                if line and len(line) > 10:
                    rules.do.append(line[:150])
            # DON'T rules
            elif any(keyword in line for keyword in ["don't", 'never', 'avoid', 'stop']):
                if line and len(line) > 10:
                    rules.dont.append(line[:150])
        
        return rules
    
    def _analyze_context(self, content: str) -> TriggeringContext:
        """Analyze triggering context."""
        context = TriggeringContext()
        content_lower = content.lower()
        
        # Detect emotional states
        if any(word in content_lower for word in ['calm', 'peaceful', 'clear']):
            context.emotional_state = "calm"
        elif any(word in content_lower for word in ['restless', 'anxious', 'stressed']):
            context.emotional_state = "restless"
        elif any(word in content_lower for word in ['coffee', 'caffeinated']):
            context.emotional_state = "caffeinated"
        
        # Detect market conditions
        if any(word in content_lower for word in ['bull', 'rally', 'uptrend']):
            context.market_condition = "bullish"
        elif any(word in content_lower for word in ['bear', 'crash', 'downtrend']):
            context.market_condition = "bearish"
        
        return context
    
    def _extract_evidence(self, content: str) -> List[str]:
        """Extract evidence and examples."""
        evidence = []
        
        # Look for numbers and statistics
        numbers = re.findall(r'\d+\.?\d*%?', content)
        if numbers:
            evidence.extend([f"Metric: {num}" for num in numbers[:5]])
        
        # Look for explicit examples
        lines = content.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['example', 'instance', 'case', 'trade']):
                if len(line.strip()) > 20:
                    evidence.append(line.strip()[:150])
        
        return evidence[:10]  # Limit to 10 pieces of evidence
    
    def _generate_tags(self, content: str) -> List[str]:
        """Generate tags for document."""
        tags = []
        content_lower = content.lower()
        
        # Predefined taxonomy
        tag_keywords = {
            "psychology": ["psychology", "mental", "emotional", "mind"],
            "risk-management": ["risk", "loss", "drawdown", "position size"],
            "technical-analysis": ["technical", "chart", "indicator", "pattern"],
            "fundamental-analysis": ["fundamental", "valuation", "earnings", "dcf"],
            "post-mortem": ["post-mortem", "review", "reflection", "mistake"],
            "strategy": ["strategy", "approach", "framework", "system"],
            "discipline": ["discipline", "rules", "process", "consistency"],
        }
        
        for tag, keywords in tag_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                tags.append(tag)
        
        return tags
    
    def _score_quality(self, content: str, evidence: List[str], 
                       rules: ActionableRules) -> float:
        """Calculate quality score for document."""
        score = 0.0
        
        # Length check (substantial content)
        if len(content) > 100:
            score += 1.0
        if len(content) > 500:
            score += 1.0
        
        # Evidence density
        if len(evidence) > 0:
            score += 1.0
        if len(evidence) > 3:
            score += 1.0
        
        # Actionable rules
        if len(rules.do) > 0 or len(rules.dont) > 0:
            score += 1.0
        
        return min(score, 5.0)
