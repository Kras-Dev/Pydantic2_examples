#tests/test_models.py

from typing import Dict, Any
import pytest
from models import User, AdminUser
from pydantic import ValidationError

def validate_user_data(user_data: Dict[str, Any] | tuple, expected_result: bool, user_class):
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
    @pytest.mark.parametrize("invalid_user_data",[
        {"email": "invalid_email"},
        {"first_name": ""},
        {"second_name": ""},
    ])
    def test_invalid_user(self, valid_user_data, invalid_user_data):
        """Проверяет, что при передаче некорректных данных пользователя возникает ValidationError."""
        test_data = {**valid_user_data, **invalid_user_data}
        validate_user_data(test_data, False, User)

    @pytest.mark.parametrize("user_data, expected_result", [
        ({"first_name": "bob", "second_name": "simpsoN "}, {"first_name": "Bob", "second_name": "Simpson"}),
        ({"first_name": " alicE", "second_name": "smIth"}, {"first_name": "Alice", "second_name": "Smith"}),
    ])
    def test_name_capitalization(self, user_data, expected_result, valid_user_data):
        """Проверяет, что имена пользователя автоматически капитализируются в соответствии с ожидаемым результатом."""
        test_data = {**valid_user_data, **user_data}

        user = validate_user_data(test_data, True, User)
        assert user.first_name == expected_result["first_name"]
        assert user.second_name == expected_result["second_name"]

    @pytest.mark.parametrize("age_value, expected_result",[
        (17, False),   # Недопустимо: возраст менее 18
        (18, True),    # Допустимо: возраст равен 18
        (60, True),    # Допустимо: возраст в пределах диапазона
        (120, True),   # Допустимо: возраст равен 120
        (121, False),  # Недопустимо: возраст больше 120
    ])
    def test_age_validation(self, age_value, expected_result, valid_user_data):
        """Проверяет корректность валидации возраста пользователя. Допускает возраст от 18 до 120 включительно."""
        test_data = {**valid_user_data, "age": age_value}

        if expected_result:
            user = validate_user_data(test_data, expected_result, User)
            assert user.age == age_value
        else:
            validate_user_data(test_data, expected_result, User)

    @pytest.mark.parametrize("password_value, expected_result",[
        ("Weak1", False),           # Слишком короткий, нет спецсимвола
        ("StrongPassword", False),  # Нет цифр и спецсимволов
        ("Strong1", False),         # Нет спецсимвола
        ("Strong!@#", False),       # Нет цифр
        ("Strong1!", True),         # Корректный пароль
    ])
    def test_password_validation(self, password_value, expected_result, valid_user_data):
        """Проверяет требования к паролю пользователя"""
        test_data = {**valid_user_data, "password": password_value}

        if expected_result:
            user = validate_user_data(test_data, expected_result, User)
            assert user.password == password_value
        else:
            validate_user_data(test_data, expected_result, User)

    @pytest.mark.parametrize("role_value, expected_result",[
        ("admin", True),
        ("superadmin", True),
        ("invalid", False),
    ])
    def test_role_validation(self, role_value, expected_result,  valid_user_data):
        """Проверяет корректность валидации ролей для администратора."""
        test_data = {**valid_user_data, "role": role_value}

        if expected_result:
            user = validate_user_data(test_data, expected_result, AdminUser)
            assert user.role.value == role_value
        else:
            validate_user_data(test_data, expected_result, AdminUser)
