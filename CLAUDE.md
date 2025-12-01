# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based reporting/data hub demo application that uses PostgreSQL for data storage. The project is managed with `uv` (modern Python package manager) and follows a workspace-based directory structure for data processing.

## Development Commands

### Environment Setup
```bash
# Install dependencies using uv
uv sync

# Activate virtual environment (if needed)
source .venv/bin/activate

# Create .env file interactively with database credentials
uv run python env_setup.py

# Create the PostgreSQL database if it doesn't exist
uv run python db_create.py
```

### Code Formatting
```bash
# Format code with black
uv run black .

# Format specific files
uv run black rpd_core/
```

### Running the Application
```bash
# Run main entry point
uv run python main.py

# Run workspace setup demo
uv run python workspace_setup.py
```

### Database Operations
The project uses Alembic for database migrations with SQLAlchemy and psycopg (PostgreSQL driver). Alembic is configured to use the `DataConfig` class for database connection URLs.

Database configuration is managed through environment variables (see DataConfig class):
- `PG_DB` - Database name
- `PG_HOST` - PostgreSQL host
- `PG_PORT` - PostgreSQL port
- `PG_USER` - Database user
- `PG_PASS` - Database password (URL-encoded automatically)

```bash
# Create the database (safe to run multiple times)
uv run python db_create.py

# Create a new migration
uv run alembic revision --autogenerate -m "description of changes"

# Apply migrations to database
uv run alembic upgrade head

# Downgrade one revision
uv run alembic downgrade -1

# Show current migration status
uv run alembic current

# Show migration history
uv run alembic history
```

## Architecture

### Core Package: `rpd_core/`

The main application logic resides in the `rpd_core` package with two key components:

1. **PlatformServices** (`rpd_core/platform.py`)
   - Provides standardized workspace directory management
   - Automatically creates directories if they don't exist
   - Key directories under `_workspace/`:
     - `in/` - Inbox for incoming files (via `fldr_inbox()`)
     - `out/` - Outbox for output files (via `fldr_outbox()`)
     - `tmp/` - Temporary files (via `fldr_temp()`)
     - `logs/` - Log files (via `fldr_logs()`)
     - `dat/` - Data files (via `fldr_data()`)
   - All folder methods accept optional `file_name` parameter to construct full paths

2. **DataConfig** (`rpd_core/data_cfg.py`)
   - Centralizes database connection configuration
   - Reads PostgreSQL credentials from environment variables
   - Provides connection URLs in two formats:
     - `pg_url_sqlalchemy` - For SQLAlchemy connections (uses `postgresql+psycopg://`)
     - `pg_url` - Standard PostgreSQL URL format
   - Automatically URL-encodes passwords to handle special characters
   - Used by Alembic migrations (`migrations/env.py`) for database connections

### Environment Configuration

The project uses `.env` file for configuration (gitignored). Required environment variables are accessed through the `DataConfig` class.

Use `env_setup.py` to interactively create the `.env` file with proper PostgreSQL credentials. The script provides sensible defaults and validates required fields.

### Workspace Directory Pattern

The `_workspace/` directory is gitignored and serves as the runtime workspace for all file I/O operations. The `PlatformServices` class ensures consistent path handling and automatic directory creation across the application.

## Dependencies

Key dependencies (Python 3.12+):
- `sqlalchemy` - ORM and database toolkit
- `alembic` - Database migration tool
- `psycopg` - PostgreSQL adapter (version 3.x)
- `pandas` - Data manipulation
- `python-dotenv` - Environment variable management
- `black` - Code formatting
