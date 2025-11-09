"""Main entry point for the agent system."""

import sys
from pathlib import Path
from typing import List, Optional
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents import OrchestratorAgent
from src.models import Document
from src.utils import setup_logging, load_config, get_config
from src.utils.output import MarkdownGenerator


def load_documents(document_dir: str) -> List[Document]:
    """Load documents from directory."""
    doc_path = Path(document_dir)
    if not doc_path.exists():
        raise FileNotFoundError(f"Document directory not found: {document_dir}")
    
    documents = []
    for file in doc_path.glob("*.md"):
        if file.name not in ["Agent-System-Design-Thinking.md", 
                             "Thematic-Insight-Extraction-Agent-System-Architecture.md"]:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                documents.append(Document(
                    document_id=f"doc_{len(documents):03d}",
                    filename=file.name,
                    content=content,
                ))
    
    return documents


def main(document_dir: str = "./data", 
         config_file: Optional[str] = None,
         output_dir: str = "./output"):
    """Main execution function."""
    # Setup logging
    setup_logging(level="INFO")
    
    # Load configuration
    if config_file and Path(config_file).exists():
        config = load_config(config_file)
    else:
        config = load_config()
    
    config.set("output.destination", output_dir)
    
    print("=" * 60)
    print("Thematic Insight Extraction Agent System")
    print("=" * 60)
    print()
    
    # Load documents
    print(f"Loading documents from: {document_dir}")
    try:
        documents = load_documents(document_dir)
        print(f"✓ Loaded {len(documents)} documents")
    except Exception as e:
        print(f"✗ Failed to load documents: {e}")
        return 1
    
    if len(documents) == 0:
        print("No documents found. Please add markdown files to the data directory.")
        return 1
    
    print()
    
    # Initialize orchestrator
    print("Initializing agent system...")
    orchestrator = OrchestratorAgent(config.to_dict())
    print("✓ Agent system initialized")
    print()
    
    # Run synthesis workflow
    print("Starting synthesis workflow...")
    print("-" * 60)
    try:
        final_report = orchestrator.process(documents)
        print("-" * 60)
        print("✓ Synthesis workflow completed successfully")
    except Exception as e:
        print(f"✗ Synthesis workflow failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print()
    
    # Generate output
    print("Generating output files...")
    generator = MarkdownGenerator(output_dir)
    
    try:
        # Save markdown report
        md_file = generator.generate_report(final_report)
        print(f"✓ Markdown report: {md_file}")
        
        # Save JSON report
        json_file = generator.save_json(final_report)
        print(f"✓ JSON report: {json_file}")
    except Exception as e:
        print(f"✗ Failed to generate output: {e}")
        return 1
    
    print()
    print("=" * 60)
    print("Summary:")
    print(f"  Documents processed: {final_report['metadata']['total_documents']}")
    print(f"  Themes identified: {final_report['metadata']['total_themes']}")
    print(f"  Quality score: {final_report['metadata']['overall_quality_score']:.2f}/10")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Thematic Insight Extraction Agent System"
    )
    parser.add_argument(
        "--documents",
        default="./data",
        help="Directory containing markdown documents (default: ./data)"
    )
    parser.add_argument(
        "--config",
        default=None,
        help="Configuration file path (optional)"
    )
    parser.add_argument(
        "--output",
        default="./output",
        help="Output directory for reports (default: ./output)"
    )
    
    args = parser.parse_args()
    
    sys.exit(main(args.documents, args.config, args.output))
