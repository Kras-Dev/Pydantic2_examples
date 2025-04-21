#tests/test_models.py

from typing import Dict, Any
import pytest
from models import User, AdminUser
from pydantic import ValidationError

def validate_user_data(user_data: Dict[str, Any], expected_result: bool, user_class):
    """Функция для проверки валидации данных пользователя.
    Args:
        user_data (Dict[str, Any]): Данные пользователя для валидации.
        expected_result (bool): True, если ожидается успешное создание объекта,
                                False — если ожидается ошибка валидации.
        user_class: Класс модели пользователя (User или AdminUser).
    Returns:
        user_class instance при успешной валидации.
    Raises:
        pytest.raises(ValidationError) если данные невалидны."""
    if expected_result:
        return user_class(**user_data)
    else:
        with pytest.raises(ValidationError):
            user_class(**user_data)

class TestModels:
    def test_invalid_user(self, user_data, invalid_user_data):
        """Проверяет, что при передаче некорректных данных пользователя возникает ValidationError."""
        test_data = {**user_data, **invalid_user_data}
        validate_user_data(test_data, False, User)

    def test_name_capitalization(self, capitalization_data, user_data):
        """Проверяет, что имена пользователя автоматически капитализируются в соответствии с ожидаемым результатом."""
        first_name, second_name, expected_first_name, expected_second_name = capitalization_data
        test_data = {**user_data, "first_name": first_name, "second_name": second_name}

        user = validate_user_data(test_data, True, User)
        assert user.first_name == expected_first_name
        assert user.second_name == expected_second_name

    def test_age_validation(self, age_data, user_data):
        """Проверяет корректность валидации возраста пользователя. Допускает возраст от 18 до 120 включительно."""
        age_value, expected_result = age_data
        test_data = {**user_data, "age": age_value}

        if expected_result:
            user = validate_user_data(test_data, True, User)
            assert user.age == age_value
        else:
            validate_user_data(test_data, False, User)

    def test_password_validation(self, password_data, user_data):
        """Проверяет требования к паролю пользователя"""
        password_value, expected_result = password_data
        test_data = {**user_data, "password": password_value}

        if expected_result:
            user = validate_user_data(test_data, True, User)
            assert user.password == password_value
        else:
            validate_user_data(test_data, False, User)

    def test_role_validation(self, role_data, user_data):
        """Проверяет корректность валидации ролей для администратора."""
        role_value, expected_result = role_data
        test_data = {**user_data, "role": role_value}

        if expected_result:
            user = validate_user_data(test_data, True, AdminUser)
            assert user.role.value == role_value
        else:
            validate_user_data(test_data, False, AdminUser)