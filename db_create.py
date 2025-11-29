"""
Database Creation Script

Creates the PostgreSQL database specified in .env if it doesn't already exist.
Uses the DataConfig class to read database credentials.
"""

import sys
from dotenv import load_dotenv
import psycopg
from psycopg import sql

from rpd_core.data_cfg import DataConfig


def database_exists(cursor, db_name: str) -> bool:
    """Check if a database exists."""
    cursor.execute(
        "SELECT 1 FROM pg_database WHERE datname = %s",
        (db_name,),
    )
    return cursor.fetchone() is not None


def create_database(db_name: str, config: DataConfig) -> None:
    """Create the database if it doesn't exist."""
    # Connect to the default 'postgres' maintenance database
    maintenance_url = (
        f"postgresql://{config.pg_user}:{config.pg_password}"
        f"@{config.pg_host}:{config.pg_port}/postgres"
    )

    try:
        # Connect to maintenance database
        with psycopg.connect(maintenance_url, autocommit=True) as conn:
            with conn.cursor() as cur:
                if database_exists(cur, db_name):
                    print(f"✓ Database '{db_name}' already exists")
                    return

                # Create the database
                print(f"Creating database '{db_name}'...")
                cur.execute(
                    sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))
                )
                print(f"✓ Database '{db_name}' created successfully")

    except psycopg.OperationalError as e:
        print(f"✗ Connection failed: {e}")
        print("\nPlease ensure:")
        print("  1. PostgreSQL server is running")
        print("  2. .env file exists with correct credentials")
        print("  3. Database user has permission to create databases")
        sys.exit(1)
    except psycopg.Error as e:
        print(f"✗ Database error: {e}")
        sys.exit(1)


def main():
    print("=" * 60)
    print("PostgreSQL Database Creation")
    print("=" * 60)

    # Load environment variables
    load_dotenv()

    # Get database configuration
    config = DataConfig()
    db_name = config.pg_db

    if not db_name:
        print("✗ Error: PG_DB environment variable not set")
        print("Please run env_setup.py to configure your environment")
        sys.exit(1)

    print(f"\nDatabase Configuration:")
    print(f"  Host: {config.pg_host}")
    print(f"  Port: {config.pg_port}")
    print(f"  Database: {db_name}")
    print(f"  User: {config.pg_user}")
    print()

    # Create the database
    create_database(db_name, config)

    print("\n" + "=" * 60)
    print("Database setup complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Run migrations: uv run alembic upgrade head")
    print("  2. Start developing your application")


if __name__ == "__main__":
    main()
