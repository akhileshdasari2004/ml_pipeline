# 🤖 Enterprise ML Training Data Pipeline

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-412991?style=for-the-badge&logo=openai&logoColor=white)
![Anthropic](https://img.shields.io/badge/Anthropic-Claude-CC785C?style=for-the-badge)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)

**A production-grade, async-first pipeline for automating the creation of high-quality ML training datasets from any document source.**

[Quick Start](#-quick-start) · [Architecture](#-architecture) · [Features](#-features) · [Configuration](#-configuration) · [Contributing](#-contributing)

</div>

---

## 📌 What Is This?

Building high-quality training datasets is one of the most time-consuming bottlenecks in ML development. This project automates the entire pipeline — from ingesting raw documents (web pages, PDFs, CSVs, Word files) to generating structured instruction datasets ready for fine-tuning LLMs.

It is designed as a **modular factory system** where a central manager coordinates specialized workers for scraping, cleaning, chunking, AI-driven generation, quality evaluation, and multi-format export. Think of it as an MLOps assembly line — not a notebook.

**Use it to generate:**
- Question-Answer pairs from documentation
- Summarization training data from long-form content
- Classification datasets from labeled corpora
- Instruction-following datasets for chatbot fine-tuning

---

## ✨ Features

| Layer | Capability |
|---|---|
| 📥 **Ingestion** | Web scraping (bot-bypass), PDF, CSV, Markdown, Word docs |
| 🧹 **Processing** | Noise removal, smart overlapping text chunking |
| 🧠 **Generation** | Q&A, summarization, classification, instruction datasets |
| ⚡ **AI Support** | OpenAI GPT-4 + Anthropic Claude, with simulation fallback |
| 🔬 **Quality Control** | Toxicity, bias, relevance & coherence scoring per example |
| 📦 **Export** | JSON, CSV, Parquet (ML-ready columnar format) |
| 📊 **Dashboard** | Real-time Streamlit UI for monitoring jobs and analytics |
| 💰 **Cost Tracking** | Token usage monitoring and budget alerts |
| 🔁 **Async** | Concurrent document loading and processing via `asyncio` |

---

## 🏗️ Architecture

The system is modeled as a **factory pipeline** with a central manager coordinating all stages:

```
┌─────────────────────────────────────────────────────────┐
│                    USER INTERFACES                       │
│              CLI (click)  │  Streamlit Dashboard         │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│              FACTORY MANAGER  (bot.py)                   │
│   Orchestrates all stages · State · Cost · Error mgmt    │
└──┬──────────┬──────────┬──────────┬──────────┬──────────┘
   │          │          │          │          │
   ▼          ▼          ▼          ▼          ▼
LOADERS  PROCESSING  GENERATORS  QUALITY   EXPORTERS
Web/PDF  Clean+Chunk  QA/Summ/   Eval+     JSON/CSV/
CSV/DOCX  Pipeline   Classify   Reports   Parquet
```

### Module Breakdown

```
src/training_bot/
├── __init__.py          # Public API & versioning
├── bot.py               # 🧠 Factory Manager (main orchestrator)
├── models/              # Pydantic data blueprints
│   ├── document.py      # SourceDocument
│   ├── chunk.py         # TextChunk
│   ├── task.py          # TaskTemplate
│   ├── example.py       # TrainingExample
│   ├── dataset.py       # Dataset
│   └── job.py           # Job (async state tracking)
├── loaders/             # 📥 Document Highway
│   ├── unified.py       # Auto-routing supervisor
│   ├── web.py           # Enterprise web scraper
│   ├── pdf.py           # PDF parser
│   ├── csv_loader.py    # Tabular ingestion
│   ├── markdown.py      # Markdown parser
│   └── docx_loader.py   # Word document reader
├── processing/          # 🧹 Text Kitchen
│   ├── cleaner.py       # Noise & whitespace removal
│   ├── chunker.py       # Overlapping smart chunker
│   └── pipeline.py      # Clean → Chunk orchestration
├── generators/          # ⚡ AI Brain
│   ├── manager.py       # Task routing
│   ├── client.py        # OpenAI + Anthropic client
│   ├── qa_generator.py
│   ├── summarization.py
│   ├── classification.py
│   ├── instruction.py
│   └── simulation.py    # Mock client (dev/no-cost mode)
├── quality/             # 🔬 Quality Lab
│   ├── evaluator.py     # Toxicity, bias, coherence scoring
│   ├── filters.py       # Pass/fail thresholds
│   └── reports.py       # Per-dataset audit reports
├── exporters/           # 📦 Shipping
│   ├── json_exporter.py
│   ├── csv_exporter.py
│   └── parquet_exporter.py
├── interfaces/          # 🖥️ User Interfaces
│   ├── cli.py
│   └── dashboard.py
├── config/
│   ├── settings.py      # Central config
│   └── constants.py     # Enums (TaskType, ExportFormat...)
└── utils/
    ├── logging.py
    ├── errors.py
    ├── cost_monitor.py  # Token usage & budget tracking
    └── retry.py         # Exponential backoff for API calls
```

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/akhileshdasari2004/ml_pipeline.git
cd ml_pipeline
pip install -e .
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your API keys:

```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Optional tuning
CHUNK_SIZE=512
CHUNK_OVERLAP=64
QUALITY_THRESHOLD=0.7
SIMULATION_MODE=false        # Set true to run without API calls (dev mode)
MAX_MONTHLY_COST_USD=50.0
```

### 3. Run via CLI

```bash
# Load a web page
training-bot load --url https://docs.example.com/guide

# Load a local PDF
training-bot load --file ./data/raw/manual.pdf

# Process all loaded documents (clean + chunk)
training-bot process

# Generate Q&A training pairs
training-bot generate --type qa

# Generate summarization pairs
training-bot generate --type summarization

# Export the final dataset
training-bot export --format json --output ./data/outputs/
training-bot export --format parquet --output ./data/outputs/
```

### 4. Launch the Dashboard

```bash
streamlit run src/training_bot/interfaces/dashboard.py
```

Open `http://localhost:8501` to monitor jobs, view quality analytics, and manage settings.

---

## 🐍 Python API

You can also drive the pipeline programmatically:

```python
import asyncio
from training_bot import TrainingDataBot

async def main():
    bot = TrainingDataBot()

    # Load documents from multiple sources
    await bot.load_documents([
        "https://docs.yoursite.com/overview",
        "./data/raw/product_manual.pdf",
        "./data/raw/faq.csv",
    ])

    # Clean and chunk
    await bot.process_documents()

    # Generate Q&A pairs using GPT-4
    await bot.generate_training_data(task_type="qa")

    # Evaluate quality (toxicity, bias, relevance, coherence)
    report = await bot.evaluate_quality()
    print(f"Dataset quality score: {report.average_score:.2f}")
    print(f"Examples passed: {report.passed}/{report.total}")

    # Export
    await bot.export(format="parquet", path="./data/outputs/")
    await bot.export(format="json", path="./data/outputs/")

    # Check cost
    print(f"Total cost: ${bot.estimated_cost:.4f}")
    print(f"Tokens used: {bot.total_tokens_used:,}")

asyncio.run(main())
```

---

## 🔧 Configuration Reference

| Variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | — | OpenAI API key |
| `ANTHROPIC_API_KEY` | — | Anthropic API key |
| `DEFAULT_MODEL` | `gpt-4` | Primary AI model |
| `FALLBACK_MODEL` | `claude-3-sonnet` | Fallback AI model |
| `SIMULATION_MODE` | `false` | Skip real API calls (dev mode) |
| `CHUNK_SIZE` | `512` | Max tokens per text chunk |
| `CHUNK_OVERLAP` | `64` | Overlap tokens between chunks |
| `QUALITY_THRESHOLD` | `0.7` | Minimum quality score (0–1) |
| `MAX_MONTHLY_COST_USD` | `50.0` | Budget cap with alerts |
| `LOG_LEVEL` | `INFO` | Logging verbosity |
| `EXPORT_DIR` | `./data/outputs` | Default export directory |

---

## 🧪 Testing

```bash
# Run all tests
make test

# Run with coverage report
make test-coverage

# Run a specific module
pytest tests/test_generators/ -v

# Run without API calls (simulation mode)
SIMULATION_MODE=true pytest tests/ -v
```

### Test Structure

```
tests/
├── conftest.py              # Shared fixtures
├── test_models.py
├── test_loaders/
├── test_processing/
├── test_generators/
├── test_quality/
├── test_exporters/
└── test_bot.py              # Full integration tests
```

---

## 🛠️ Development

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Lint & format
make lint      # runs black + isort + mypy

# Type check only
mypy src/

# Format only
black src/ tests/

# Build Docker environment
docker-compose up --build
```

---

## 📊 Supported Task Types

| Task | CLI Flag | Description | Output Format |
|---|---|---|---|
| Q&A Generation | `--type qa` | Generates question-answer pairs from chunks | `{"question": ..., "answer": ...}` |
| Summarization | `--type summarization` | Generates long → short summary pairs | `{"document": ..., "summary": ...}` |
| Classification | `--type classification` | Assigns labels to text passages | `{"text": ..., "label": ...}` |
| Instruction | `--type instruction` | Creates instruction-following examples | `{"instruction": ..., "response": ...}` |

---

## 📤 Export Formats

| Format | Use Case | Notes |
|---|---|---|
| **JSON** | General use, API ingestion | Pretty-printed or JSONL |
| **CSV** | Spreadsheet review, labeling tools | Flat with metadata columns |
| **Parquet** | Large-scale ML training | Columnar, compressed, fast I/O |

---

## 🗺️ Roadmap

- [ ] Support for YouTube transcript ingestion
- [ ] Multi-language dataset generation
- [ ] Fine-tuning integration (Hugging Face Trainer, Axolotl)
- [ ] Dataset versioning and diff tracking
- [ ] Vector similarity deduplication
- [ ] REST API server mode
- [ ] Weights & Biases logging integration

---

**Akhilesh Dasari**
- GitHub: [@akhileshdasari2004](https://github.com/akhileshdasari2004)

---

<div align="center">

If this project helped you, consider giving it a ⭐ on GitHub!

</div>
