# test_validation.py
import pytest
from validation import (
    validate_station,
    validate_train,
    validate_passenger,
    validate_email,
    validate_schedule,
    validate_booking,
)


# 1. Valid entity and cleaned return values
def test_valid_station_is_cleaned():
    # Arrange & Act
    result = validate_station("  Helsinki Central  ", "  Helsinki  ")
    # Assert
    assert result == ("Helsinki Central", "Helsinki")


def test_valid_train_is_cleaned():
    result = validate_train("  IC-101  ", "  InterCity  ", 200)
    assert result == ("IC-101", "InterCity", 200)


# 2. ValueError for blank string fields
def test_empty_station_name_is_rejected():
    with pytest.raises(ValueError, match="Station name cannot be empty"):
        validate_station("", "Helsinki")


def test_empty_train_code_is_rejected():
    with pytest.raises(ValueError, match="Train code cannot be empty"):
        validate_train("", "InterCity", 200)


# 3. Spaces-only strings and negative / zero quantities
def test_spaces_only_city_is_rejected():
    with pytest.raises(ValueError, match="City cannot be empty"):
        validate_station("Helsinki Central", "   ")


def test_negative_capacity_is_rejected():
    with pytest.raises(ValueError, match="Capacity must be greater than zero"):
        validate_train("IC-101", "InterCity", -5)


def test_zero_tickets_is_rejected():
    with pytest.raises(ValueError, match="Number of tickets must be at least 1"):
        validate_booking(1, 1, 0)


# 4. Additional entity validations
def test_valid_passenger_and_email():
    assert validate_passenger("  Ali  ", "  Rezaei  ", "  +358401234567  ") == (
        "Ali",
        "Rezaei",
        "+358401234567",
    )
    assert validate_email("  ali@example.com  ") == "ali@example.com"


def test_invalid_email_format_is_rejected():
    with pytest.raises(ValueError, match="Invalid email format"):
        validate_email("invalid-email")


def test_schedule_same_stations_is_rejected():
    with pytest.raises(ValueError, match="Departure and arrival stations cannot be the same"):
        validate_schedule("08:00:00", "2026-12-01", "10:00:00", 1, 2, 2)


# 5. Advanced: parametrized test for invalid quantity types
@pytest.mark.parametrize("invalid_capacity", [-1, 0, "abc", None])
def test_invalid_capacity_values_are_rejected(invalid_capacity):
    with pytest.raises(ValueError):
        validate_train("IC-101", "InterCity", invalid_capacity)


@pytest.mark.parametrize("invalid_tickets", [-2, 0, "three", None])
def test_invalid_ticket_values_are_rejected(invalid_tickets):
    with pytest.raises(ValueError):
        validate_booking(1, 1, invalid_tickets)