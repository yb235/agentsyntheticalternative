"""Example usage of the agent system."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents import OrchestratorAgent
from src.models import Document
from src.utils import setup_logging, load_config
from src.utils.output import MarkdownGenerator


def create_sample_documents():
    """Create sample documents for demonstration."""
    documents = [
        Document(
            document_id="doc_001",
            filename="trading_psychology.md",
            content="""# Trading Psychology Reflection

Key lesson learned: Emotional state directly impacts trading decisions.

When I'm calm and well-rested, my win rate is around 85%. But after drinking coffee, 
I become restless and make impulsive trades. This has led to losses in 6 out of 7 cases.

**Rules I need to follow:**
- Always check my mental state before trading
- Never trade after drinking coffee
- Wait for genuine opportunity clusters
- Don't force trades when there's nothing to do

The biggest realization is that psychology matters more than analytical skills.
Calm mind is a prerequisite for good research and patient execution.
""",
        ),
        Document(
            document_id="doc_002",
            filename="position_management.md",
            content="""# Position Management Strategy

Core principle: Sit tight and be patient. Big money is made in waiting, not trading.

My position sizing framework:
- 50% in high conviction ideas
- 30% in medium conviction
- 20% cash for opportunities

Key mistakes to avoid:
- Don't exit positions too early due to impatience
- Never add to losing positions hoping for recovery
- Stop macro directional trades - my win rate is 0%

Evidence from my trades:
- Best returns came from holding NVDA for 18 months
- Worst losses from intraday trading decisions
- Patient waiting beats active trading
""",
        ),
        Document(
            document_id="doc_003",
            filename="analysis_approach.md",
            content="""# Analysis Approach Evolution

I've evolved from being a technical analysis believer to focusing on fundamentals.

Early period (2017-2019): Studied Minervini, used MACD, believed in charts.
Middle period (2020-2022): Started questioning TA after repeated failures.
Current position (2023-present): TA is mostly noise, fundamentals are what matter.

However, I acknowledge the tension: I still sometimes look at weekly/monthly charts.
Maybe there's a place for TA at longer timeframes, but daily charts are just noise.

The key realization: Deep fundamental research requires calm mental state.
Can't do quality research when restless or caffeinated.
""",
        ),
        Document(
            document_id="doc_004",
            filename="risk_management.md",
            content="""# Risk Management Rules

Never risk more than 2% on a single position.

Position sizing must match psychological capacity - if a position keeps you up at night,
it's too large regardless of the math.

Key lessons from losses:
- All major losses came from oversized positions
- Emotional attachment to positions prevents rational decisions
- Need written thesis before entry to prevent impulsive trades

Risk management is really psychology management.
The math is easy, the discipline is hard.
""",
        ),
    ]
    return documents


def main():
    """Run example synthesis."""
    # Setup logging
    setup_logging(level="INFO")
    
    print("=" * 60)
    print("Agent System Example")
    print("=" * 60)
    print()
    
    # Create sample documents
    print("Creating sample documents...")
    documents = create_sample_documents()
    print(f"✓ Created {len(documents)} sample documents")
    print()
    
    # Load configuration
    config = load_config()
    
    # Initialize orchestrator
    print("Initializing agent system...")
    orchestrator = OrchestratorAgent(config.to_dict())
    print("✓ Agent system initialized")
    print()
    
    # Run synthesis
    print("Running synthesis workflow...")
    print("-" * 60)
    final_report = orchestrator.process(documents)
    print("-" * 60)
    print("✓ Synthesis completed")
    print()
    
    # Generate output
    print("Generating reports...")
    generator = MarkdownGenerator("./output")
    
    md_file = generator.generate_report(final_report, "example_report.md")
    json_file = generator.save_json(final_report, "example_report.json")
    
    print(f"✓ Markdown report: {md_file}")
    print(f"✓ JSON report: {json_file}")
    print()
    
    # Print summary
    print("=" * 60)
    print("Summary:")
    print(f"  Documents: {final_report['metadata']['total_documents']}")
    print(f"  Themes: {final_report['metadata']['total_themes']}")
    print(f"  Quality: {final_report['metadata']['overall_quality_score']:.2f}/10")
    print()
    
    # Print theme names
    print("Themes identified:")
    for theme in final_report['themes']:
        print(f"  - {theme['name']} ({len(theme['document_ids'])} documents)")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
