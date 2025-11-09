"""Basic tests for the agent system."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models import Document, AnalyzedDocument, Theme, SynthesisChapter
from src.agents import DocumentAnalyzerAgent, ThematicClusteringAgent
from src.utils import load_config


def test_document_creation():
    """Test document model creation."""
    doc = Document(
        document_id="test_001",
        filename="test.md",
        content="This is a test document."
    )
    assert doc.document_id == "test_001"
    assert doc.filename == "test.md"
    assert doc.content == "This is a test document."
    print("✓ Document creation test passed")


def test_document_analyzer():
    """Test document analyzer agent."""
    config = load_config()
    analyzer = DocumentAnalyzerAgent(config.to_dict())
    
    doc = Document(
        document_id="test_001",
        filename="test.md",
        content="""
        # Test Document
        
        Key lesson learned: Never trade when emotional.
        
        Rules to follow:
        - Always check mental state
        - Never trade after coffee
        - Don't force trades
        
        Evidence shows 85% win rate when calm.
        """
    )
    
    analyzed = analyzer.analyze_document(doc)
    
    assert analyzed.document_id == "test_001"
    assert len(analyzed.core_principle) > 0
    assert len(analyzed.tags) > 0
    assert analyzed.quality_score > 0
    
    print("✓ Document analyzer test passed")


def test_theme_creation():
    """Test theme model creation."""
    theme = Theme(
        theme_id="theme_001",
        name="Test Theme",
        description="A test theme",
        document_ids=["doc_001", "doc_002"],
        key_concepts=["concept1", "concept2"],
    )
    
    assert theme.theme_id == "theme_001"
    assert len(theme.document_ids) == 2
    assert len(theme.key_concepts) == 2
    
    print("✓ Theme creation test passed")


def test_synthesis_chapter():
    """Test synthesis chapter model."""
    chapter = SynthesisChapter(
        theme_id="theme_001",
        theme_name="Test Theme",
        executive_summary="This is a test summary",
    )
    
    assert chapter.theme_id == "theme_001"
    assert chapter.theme_name == "Test Theme"
    assert len(chapter.executive_summary) > 0
    
    # Test serialization
    chapter_dict = chapter.to_dict()
    assert isinstance(chapter_dict, dict)
    assert "theme_id" in chapter_dict
    
    print("✓ Synthesis chapter test passed")


def test_config_loading():
    """Test configuration loading."""
    config = load_config()
    
    assert config is not None
    assert config.get("llm.provider") is not None
    assert config.get("stages.deconstruction.enabled") is True
    
    print("✓ Configuration loading test passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Running Agent System Tests")
    print("=" * 60)
    print()
    
    tests = [
        test_document_creation,
        test_config_loading,
        test_document_analyzer,
        test_theme_creation,
        test_synthesis_chapter,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
            import traceback
            traceback.print_exc()
    
    print()
    print("=" * 60)
    print(f"Tests completed: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
