#tests/conftest.py
from typing import Dict, Any

import pytest

@pytest.fixture
def user_data() -> Dict[str, Any]:
    """Фикстура для корректных данных пользователя."""
    return {
        "email": "test@example.com",
        "name": "bob",
        "second_name": "simpson",
        "age": 21,
        "password": "Password123**"
    }

@pytest.fixture
def admin_user_data(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Фикстура для корректных данных администратора."""
    return {
        **user_data,
        "role": "admin"
    }

"""Тестовые данные некорректного пользователя"""
invalid_user_test_data = [
    {"email": "invalid_email"},
    {"name": "",},
    {"second_name": ""},
]
@pytest.fixture(params=invalid_user_test_data)
def invalid_user_data(request) -> Dict[str, Any]:
    """Фикстура для проверки данных пользователя."""
    return request.param

capitalization_test_data = [
    ("bob", "simpsoN", "Bob", "Simpson"),
    ("alicE", "smIth", "Alice", "Smith"),
]
@pytest.fixture(params=capitalization_test_data)
def capitalization_data(request) -> tuple:
    """Фикстура для проверки имен."""
    return request.param

"""Тестовые данные для возраста"""
age_test_data = [
    (17, False), # Недопустимо: возраст менее 18
    (18, True), # Допустимо: возраст равен 18
    (60, True), # Допустимо: возраст в пределах диапазона
    (120, True), # Допустимо: возраст равен 120
    (121, False), # Недопустимо: возраст больше 120
]
@pytest.fixture(params=age_test_data)
def age_data(request) -> tuple:
    """Фикстура для проверки возраста."""
    return request.param

"""Тестовые данные для пароля"""
password_test_data = [
    ("Weak1", False), # Недопустимо: слишком коротко, отсутствует спецсимвол
    ("StrongPassword", False), # Недопустимо: отсутствует число и спецсимвол
    ("Strong1", False), # Недопустимо: отсутствует спецсимвол
    ("Strong!@#", False), # Недопустимо: отсутствует число
    ("Strong1!", True), # Допустимо
]
@pytest.fixture(params=password_test_data)
def password_data(request) -> tuple:
    """Фикстура для проверки пароля."""
    return request.param

"""Тестовые данные для роли"""
role_test_data = [
    ("admin", True), # Допустимо: string "admin"
    ("superadmin", True), # Допустимо: string "superadmin"
    ("invalid", False), # Недопустимо: неправильная роль
]
@pytest.fixture(params=role_test_data)
def role_data(request) -> tuple:
    """Фикстура для проверки роли."""
    return request.param