#tests/conftest.py
from typing import Dict, Any, Tuple

import pytest

@pytest.fixture
def valid_user_data() -> Dict[str, Any]:
    """Фикстура для корректных данных пользователя. Возвращает словарь с валидными полями пользователя."""
    return {
        "email": "test@example.com",
        "first_name": "bob",
        "second_name": "simpson",
        "age": 21,
        "password": "Password123**"
    }

@pytest.fixture
def valid_admin_user_data(valid_user_data) -> Dict[str, Any]:
    """Фикстура для корректных данных администратора. Расширяет user_data, добавляя поле role."""
    return {
        **valid_user_data,
        "role": "admin"
    }

