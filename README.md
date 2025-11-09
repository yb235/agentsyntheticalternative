# Thematic Insight Extraction Agent System

A multi-agent system for extracting meaningful patterns and insights from large document collections. This system implements a rigorous 4-stage framework: Deconstruction → Categorization → Synthesis → Validation.

## Overview

This agent system automates the process of synthesizing insights from document collections, transforming disconnected notes into coherent understanding. It's designed based on academically grounded methodology (CIHR, RTARG 2024 guidelines) and implements human-in-the-loop quality control.

### Key Features

- **4-Stage Processing Pipeline**: Systematic approach to document analysis and synthesis
- **Multi-Agent Architecture**: Specialized agents for different aspects of analysis
- **Pattern Recognition**: Automatically identifies frequency patterns, co-occurrences, and contradictions
- **Quality Validation**: Built-in validation checks to ensure synthesis accuracy
- **Checkpointing**: Save and resume workflow at any stage
- **Multiple Output Formats**: Markdown and JSON reports

## Architecture

The system consists of several specialized agents:

1. **Orchestrator Agent**: Coordinates the entire workflow
2. **Document Analyzer Agent** (Stage 1): Extracts structured data from raw documents
3. **Pattern Recognition Agents**: Identify patterns across documents
   - Frequency Analyzer
   - Co-occurrence Analyzer
4. **Thematic Clustering Agent** (Stage 2): Groups documents into themes
5. **Synthesis Agent** (Stage 3): Generates insights and principles
6. **Validation Agent** (Stage 4): Ensures quality and accuracy

### Processing Stages

```
Stage 1: DECONSTRUCTION
├─ Extract core principles
├─ Identify actionable rules  
├─ Tag and categorize
└─ Detect contradictions

Stage 2: CATEGORIZATION
├─ Cluster related documents
├─ Generate themes
└─ Identify cross-cutting patterns

Stage 3: SYNTHESIS
├─ Generate insights per theme
├─ Extract core principles
├─ Create actionable frameworks
└─ Resolve contradictions

Stage 4: VALIDATION
├─ Internal accuracy checks
├─ Evidence validation
├─ Coherence testing
└─ Quality scoring
```

## Installation

### Prerequisites

- Python 3.11 or higher
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yb235/agentsyntheticalternative.git
cd agentsyntheticalternative
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up API keys for LLM providers:
```bash
# For OpenAI
export OPENAI_API_KEY="your-api-key"

# For Anthropic
export ANTHROPIC_API_KEY="your-api-key"
```

> **Note**: The system works in "mock mode" without API keys, using rule-based extraction. For best results, configure an LLM provider.

## Usage

### Quick Start with Example

Run the included example to see the system in action:

```bash
python examples/basic_example.py
```

This will:
- Create sample documents
- Run the complete synthesis workflow
- Generate output reports in `./output/`

### Processing Your Own Documents

1. **Prepare your documents**: Place markdown files in a directory (e.g., `./data/`)

2. **Run the synthesis**:
```bash
python src/main.py --documents ./data --output ./output
```

3. **Check the output**: Find generated reports in the output directory:
   - `synthesis_report_TIMESTAMP.md` - Human-readable markdown report
   - `synthesis_report_TIMESTAMP.json` - Machine-readable JSON data
   - Checkpoints saved in `./checkpoints/`

### Command Line Options

```bash
python src/main.py [OPTIONS]

Options:
  --documents PATH    Directory containing markdown documents (default: ./data)
  --config PATH       Configuration file path (optional)
  --output PATH       Output directory for reports (default: ./output)
```

### Configuration

Create a JSON configuration file to customize behavior:

```json
{
  "llm": {
    "provider": "openai",
    "model": "gpt-4",
    "temperature": 0.7,
    "openai_api_key": "your-key-here"
  },
  "processing": {
    "parallel_workers": 4,
    "batch_size": 10
  },
  "stages": {
    "deconstruction": {"enabled": true},
    "pattern_recognition": {"enabled": true},
    "categorization": {"enabled": true},
    "synthesis": {"enabled": true, "depth": "standard"},
    "validation": {"enabled": true}
  },
  "output": {
    "format": "markdown",
    "destination": "./output"
  },
  "checkpoints": {
    "enabled": true,
    "directory": "./checkpoints"
  }
}
```

Use with:
```bash
python src/main.py --config config.json
```

## Project Structure

```
.
├── src/
│   ├── agents/              # Agent implementations
│   │   ├── base.py          # Base agent class
│   │   ├── orchestrator.py  # Main orchestrator
│   │   ├── document_analyzer.py
│   │   ├── pattern_recognition.py
│   │   ├── thematic_clustering.py
│   │   ├── synthesis.py
│   │   └── validation.py
│   ├── models/              # Data models
│   │   ├── document.py
│   │   ├── theme.py
│   │   ├── synthesis.py
│   │   ├── patterns.py
│   │   └── validation.py
│   ├── utils/               # Utilities
│   │   ├── config.py        # Configuration management
│   │   ├── logging.py       # Logging setup
│   │   ├── state.py         # State management
│   │   └── output.py        # Output generation
│   └── main.py              # Main entry point
├── examples/
│   └── basic_example.py     # Example usage
├── data/                    # Input documents (user-provided)
├── output/                  # Generated reports
├── checkpoints/             # Workflow checkpoints
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Output Format

The system generates two types of output:

### Markdown Report

Human-readable synthesis report containing:
- Overview and metadata
- Synthesis chapters by theme
  - Executive summary
  - Core principles with evidence
  - Actionable rules (DO/DON'T)
  - Contradictions and resolutions
  - Key quotes
  - Open questions
- Validation summary
- Pattern analysis

### JSON Report

Machine-readable data structure containing:
- Complete metadata
- All themes with document mappings
- Detailed synthesis for each theme
- Validation results
- Pattern analysis data

## Design Philosophy

This system is built on several key principles:

1. **Methodology Fidelity**: Faithfully implements the 4-stage synthesis framework
2. **Transparency**: All agent decisions are logged and auditable
3. **Human-in-the-Loop**: AI accelerates, humans validate
4. **Fail Gracefully**: System degrades gracefully and escalates when uncertain
5. **Extensibility**: Easy to add new agents and capabilities

For detailed design rationale, see:
- `Agent-System-Design-Thinking.md` - Design philosophy and decisions
- `Thematic-Insight-Extraction-Agent-System-Architecture.md` - Complete architecture

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Adding New Agents

1. Create a new agent class inheriting from `BaseAgent`
2. Implement the `process()` method
3. Register in `src/agents/__init__.py`
4. Integrate into orchestrator workflow if needed

Example:
```python
from src.agents.base import BaseAgent

class MyCustomAgent(BaseAgent):
    def __init__(self, config=None):
        super().__init__("MyAgent", config)
    
    def process(self, input_data):
        self.log_info("Processing data...")
        # Your logic here
        return result
```

## Limitations (MVP)

This is an MVP (Minimum Viable Product) implementation with some limitations:

- **Pattern Recognition**: Basic frequency and co-occurrence analysis only
- **LLM Integration**: Simplified prompts; production would use more sophisticated prompt engineering
- **Clustering**: Simple tag-based clustering; advanced version would use embeddings and hierarchical clustering
- **Validation**: Rule-based validation; could be enhanced with ML-based quality prediction
- **Parallelization**: Sequential processing; could be parallelized for speed

See the architecture document for planned enhancements in Phase 2 and Phase 3.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is provided as-is for educational and research purposes.

## References

- CIHR Guidelines for Thematic Analysis
- RTARG 2024 Framework for Qualitative Synthesis
- Agent-System-Design-Thinking.md (in this repository)
- Thematic-Insight-Extraction-Agent-System-Architecture.md (in this repository)

## Support

For questions or issues:
- Open an issue on GitHub
- Review the design documents for detailed information
- Check the examples directory for usage patterns

---

**Version**: 1.0 (MVP)  
**Last Updated**: 2025-11-09
