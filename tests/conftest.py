#tests/conftest.py
from typing import Dict, Any, Tuple

import pytest

@pytest.fixture
def user_data() -> Dict[str, Any]:
    """Фикстура для корректных данных пользователя. Возвращает словарь с валидными полями пользователя."""
    return {
        "email": "test@example.com",
        "first_name": "bob",
        "second_name": "simpson",
        "age": 21,
        "password": "Password123**"
    }

@pytest.fixture
def admin_user_data(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Фикстура для корректных данных администратора. Расширяет user_data, добавляя поле role."""
    return {
        **user_data,
        "role": "admin"
    }

"""Некорректные данные пользователя для параметризации"""
invalid_user_test_data = [
    {"email": "invalid_email"},
    {"first_name": "",},
    {"second_name": ""},
]
@pytest.fixture(params=invalid_user_test_data)
def invalid_user_data(request) -> Dict[str, Any]:
    """Параметризованная фикстура, для проверки некорректных данных пользователя."""
    return request.param

"""Данные для проверки капитализации имён"""
capitalization_test_data = [
    ("bob", "simpsoN ", "Bob", "Simpson"),
    (" alicE", "smIth", "Alice", "Smith"),
]
@pytest.fixture(params=capitalization_test_data)
def capitalization_data(request) -> Tuple[str, str, str, str]:
    """Параметризованная фикстура для проверки имен."""
    return request.param

"""Данные для проверки валидации возраста"""
age_test_data = [
    (17, False), # Недопустимо: возраст менее 18
    (18, True), # Допустимо: возраст равен 18
    (60, True), # Допустимо: возраст в пределах диапазона
    (120, True), # Допустимо: возраст равен 120
    (121, False), # Недопустимо: возраст больше 120
]
@pytest.fixture(params=age_test_data)
def age_data(request) -> Tuple[int, bool]:
    """Параметризованная фикстура для проверки возрастных ограничений."""
    return request.param

"""Данные для проверки валидации пароля"""
password_test_data = [
    ("Weak1", False),          # Слишком короткий, нет спецсимвола
    ("StrongPassword", False), # Нет цифр и спецсимволов
    ("Strong1", False),        # Нет спецсимвола
    ("Strong!@#", False),      # Нет цифр
    ("Strong1!", True),        # Корректный пароль
]
@pytest.fixture(params=password_test_data)
def password_data(request) -> Tuple[str, bool]:
    """Параметризованная фикстура для проверки требований к паролю."""
    return request.param

"""Данные для проверки валидации ролей"""
role_test_data = [
    ("admin", True),
    ("superadmin", True),
    ("invalid", False),
]
@pytest.fixture(params=role_test_data)
def role_data(request) -> Tuple[str, bool]:
    """Параметризованная фикстура для проверки валидности ролей."""
    return request.param