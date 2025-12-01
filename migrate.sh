#!/bin/bash

# migrate.sh - Autogenerate and apply Alembic migrations
# Usage: ./migrate.sh "migration description"

set -e  # Exit on error

# Check if migration message is provided
if [ -z "$1" ]; then
    echo "Error: Migration message is required"
    echo "Usage: ./migrate.sh \"description of changes\""
    exit 1
fi

MIGRATION_MSG="$1"

echo "===================================="
echo "Creating migration: $MIGRATION_MSG"
echo "===================================="

# Generate migration
uv run alembic revision --autogenerate -m "$MIGRATION_MSG"

if [ $? -ne 0 ]; then
    echo "Error: Failed to generate migration"
    exit 1
fi

echo ""
echo "===================================="
echo "Applying migration to database"
echo "===================================="

# Apply migration
uv run alembic upgrade head

if [ $? -ne 0 ]; then
    echo "Error: Failed to apply migration"
    exit 1
fi

echo ""
echo "===================================="
echo "Migration complete!"
echo "===================================="

# Show current migration status
echo ""
echo "Current migration status:"
uv run alembic current
