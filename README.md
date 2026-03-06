# Enterprise ML Training Data Pipeline

A comprehensive tool for building high-quality, AI-generated training datasets from diverse document sources.

## Features
- **Unified Loader**: Ingest data from Web, PDF, CSV, Word, and Markdown.
- **Smart Processing**: Noise removal and token-aware text chunking.
- **AI Brain**: Multi-model support (OpenAI, Anthropic) for QA, Summarization, and more.
- **Quality Lab**: Automated evaluation of toxicity, bias, and relevance.
- **Modular Exporters**: Export to JSON, CSV, or Parquet.

## Quick Start
1. `pip install -e .`
2. `cp .env.example .env` (Add your API keys)
3. `training-bot load --url https://example.com`
4. `training-bot process`
5. `training-bot generate --type qa`
6. `training-bot export --format json`

## Development
- Run tests: `make test`
- Lint code: `make lint`
