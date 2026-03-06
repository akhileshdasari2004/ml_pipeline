# Architecture Overview

The Enterprise ML Training Data Pipeline is designed as a modular, asynchronous system for transforming diverse document sources into high-quality training datasets.

## Core Modules
1. **Loaders**: Unified interface for ingesting Web, PDF, Markdown, CSV, and Docx content.
2. **Processing**: Text cleaning and smart overlapping chunking.
3. **AI Generators**: Task-specific LLM wrappers (QA, Summarization, etc.) with cost tracking.
4. **Quality Lab**: Automated scoring and filtering of generated examples.
5. **Exporters**: Multi-format export (JSON, CSV, Parquet).
6. **Orchestrator**: The `TrainingDataBot` class that wires everything together.

## Data Flow
Source URL/File -> Loader -> Raw Document -> Cleaner -> Chunker -> Text Chunks -> AI Generator -> Training Examples -> Quality Evaluator -> Dataset -> Exporter -> Output File
