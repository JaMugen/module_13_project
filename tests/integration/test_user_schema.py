from click import confirm
import pytest

from app.models.user import User
from app.schemas.user import PasswordUpdate, UserCreate


def test_password_update_mismatch_raises_validation_error():
    """Creating PasswordUpdate with non-matching new/confirm should fail."""
    with pytest.raises(Exception) as excinfo:
        PasswordUpdate(
            current_password="OldPass123!",
            new_password="NewPass123!",
            confirm_new_password="Different123!",
        )

    # The validator raises a ValueError which Pydantic wraps; check message
    msg = str(excinfo.value).lower()
    assert "do not match" in msg or "must be different" in msg

def test_password_update_same_as_current_raises_validation_error():
    """Creating PasswordUpdate with new password same as current should fail."""
    with pytest.raises(Exception) as excinfo:
        PasswordUpdate(
            current_password="SamePass123!",
            new_password="SamePass123!",
            confirm_new_password="SamePass123!",
        )

    # The validator raises a ValueError which Pydantic wraps; check message
    msg = str(excinfo.value).lower()
    assert "must be different" in msg

def test_password_update_valid():
    """Creating PasswordUpdate with valid data should succeed."""
    pwd_update = PasswordUpdate(
        current_password="OldPass123!",
        new_password="NewPass123!",
        confirm_new_password="NewPass123!",
    )
    assert pwd_update.current_password == "OldPass123!"
    assert pwd_update.new_password == "NewPass123!"
    assert pwd_update.confirm_new_password == "NewPass123!"


def test_verify_password_match_invalid():
    """Creating UserCreate with mismatched password/confirm should fail."""
    with pytest.raises(Exception) as excinfo:
        UserCreate(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            username="johndoe",
            password="ValidPass123",
            confirm_password="NotValidPass123",
        )

    msg = str(excinfo.value).lower()
    assert "passwords do not match" in msg or "do not match" in msg

def test_verify_password_match_valid():
    """Creating UserCreate with valid matching password/confirm should succeed."""
    user_create = UserCreate(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        username="johndoe",
        password="!ValidPass123",
        confirm_password="!ValidPass123",
    )
    assert user_create.password == "!ValidPass123"
    assert user_create.confirm_password == "!ValidPass123"

 

