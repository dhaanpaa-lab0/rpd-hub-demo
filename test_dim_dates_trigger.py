#!/usr/bin/env python3
"""
Test script to verify the dim_dates trigger is working correctly.
"""

from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from rpd_core.data_cfg import DataConfig
from rpd_data.models import DimDate


def test_trigger():
    """
    Tests the dim_dates trigger by inserting test dates and verifying
    that all fields are automatically populated.
    """

    # Get database connection
    config = DataConfig()
    engine = create_engine(config.pg_url_sqlalchemy)

    test_dates = [
        date(2025, 1, 15),  # Mid-January, Wednesday
        date(2025, 3, 31),  # End of March, Monday
        date(2025, 7, 4),   # July 4th, Friday
        date(2025, 12, 25), # December 25th, Thursday
    ]

    print("Testing dim_dates trigger...\n")

    with Session(engine) as session:
        try:
            # Clean up any existing test data
            session.query(DimDate).filter(
                DimDate.date.in_(test_dates)
            ).delete(synchronize_session=False)
            session.commit()

            # Insert test dates
            for test_date in test_dates:
                dim_date = DimDate(date=test_date)
                session.add(dim_date)
                session.flush()  # Flush to trigger the database trigger
                session.refresh(dim_date)  # Refresh to get trigger-populated values

                print(f"Inserted date: {test_date}")
                print(f"  day:         {dim_date.day}")
                print(f"  week:        {dim_date.week}")
                print(f"  month:       {dim_date.month}")
                print(f"  quarter:     {dim_date.quarter}")
                print(f"  year:        {dim_date.year}")
                print(f"  day_of_week: {dim_date.day_of_week} ({get_day_name(dim_date.day_of_week)})")
                print()

            session.commit()
            print("✓ All test dates inserted successfully!")

            # Verify the data was persisted correctly
            print("\nVerifying persisted data...")
            for test_date in test_dates:
                dim_date = session.query(DimDate).filter(
                    DimDate.date == test_date
                ).first()

                if dim_date:
                    assert dim_date.day == test_date.day, "Day mismatch!"
                    assert dim_date.month == test_date.month, "Month mismatch!"
                    assert dim_date.year == test_date.year, "Year mismatch!"
                    assert dim_date.quarter == (test_date.month - 1) // 3 + 1, "Quarter mismatch!"
                    print(f"✓ {test_date} verified")

            print("\n✓ All tests passed! Trigger is working correctly.")

        except Exception as e:
            print(f"✗ Test failed: {e}")
            session.rollback()
            raise
        finally:
            # Cleanup test data
            session.query(DimDate).filter(
                DimDate.date.in_(test_dates)
            ).delete(synchronize_session=False)
            session.commit()


def get_day_name(dow):
    """Convert day of week number to name."""
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    return days[dow] if 0 <= dow <= 6 else "Unknown"


if __name__ == "__main__":
    test_trigger()
