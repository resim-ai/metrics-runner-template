# Metrics Runner Template

## Overview

This repository contains a metrics runner that can process simulation data and generate metrics for both individual experiences and batch operations.

## Repository Structure

### Source Code (`src/`)

The `src/` directory contains the main application logic:

- **`entrypoint.py`** - Main entry point that handles command-line arguments and routes to appropriate metrics processing functions
- **`experience_metrics.py`** - Processes metrics for individual simulation experiences
- **`batch_metrics.py`** - Handles batch-level metrics processing for multiple jobs
- **`utils.py`** - Shared utility functions for metrics processing and proto file writing

The application supports two main modes:
1. **Experience Metrics**: Processes a test's simulation logs to extract metrics
2. **Batch Metrics**: Processes multiple tests within a batch to generate aggregated metrics

## Development Environment

### Devcontainer Setup

The repository includes a complete development container configuration in `.devcontainer/`:

- **Resim CLI**: Automatically installs the Resim CLI tool for API interactions
- **VS Code Extensions**: Pre-configured with Python and Ruff extensions
- **Settings**: Configured for automatic formatting on save using Ruff

### Pre-commit Configuration

The repository uses pre-commit hooks to maintain code quality:

- **Ruff Check**: Automatically fixes code style issues
- **Ruff Format**: Ensures consistent code formatting

Configuration is in `.pre-commit.yaml` and uses Ruff v0.11.11.
Install the pre-commit hooks with:
```bash
pre-commit install
```

## Building and Deployment

### Dockerfile

The main `Dockerfile` creates a production-ready container:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r --no-cache-dir requirements.txt
COPY src/* /app
ENTRYPOINT ["python3", "/app/metrics.py"]
```

#### Building the Image

```bash
docker build -t metrics-runner .
```

#### Running the Container

```bash
docker run -v /path/to/data:/tmp/resim metrics-runner
```

### Default File Paths

The application expects data in specific locations:
- **Metrics Output**: `/tmp/resim/outputs/metrics.binproto`
- **Log Input**: `/tmp/resim/outputs/output.csv`
- **Batch Config**: `/tmp/resim/inputs/batch_metrics_config.json`

## Usage

### Command Line Interface

The runner has two modes - experience metrics and batch metrics.

#### Experience Metrics

```bash
python src/entrypoint.py \
  --output-path ./metrics.binproto \
  --log-path /path/to/log.mcap
```

#### Batch Metrics

When running batch metrics, update `data/batch_metrics_config.json` with:

- `authToken`: Authentication token for Resim API (retrieve from the [ReSim debug page](https://app.resim.ai/debug) > `auth.bearer`)
- `projectID`: UUID of the project to process
- `batchID`: UUID of the batch to process

Then run:
```bash
python src/entrypoint.py \
  --batch-metrics-config-path ./data/batch_metrics_config.json \
  --output-path ./batch_metrics.binproto
```
