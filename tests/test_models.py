#tests/test_models.py
import datetime
from typing import Dict, Any

import pytest
import logging
from models import User, AdminUser
from pydantic import ValidationError


logger = logging.getLogger(__name__)
logger.info(f"Логирование настроено! Время: {datetime.datetime.now().time()}")


class TestModels:

    def test_invalid_user(self, user_data, invalid_user_data):
        test_data =  user_data.copy()
        for key, value in invalid_user_data.items():
            test_data[key] = value

        with pytest.raises(ValidationError):
            User(**test_data)

    def test_name_capitalization(self, capitalization_data, user_data):
        first_name, second_name, expected_first_name, expected_second_name = capitalization_data
        user_data["name"] = first_name
        user_data["second_name"] = second_name

        user = User(**user_data)
        assert user.first_name == expected_first_name
        assert user.second_name == expected_second_name

    def test_age_validation(self, age_data, user_data):
        age_value, expected_result = age_data
        user_data["age"] = age_value  # Устанавливаем возраст в данные
        logger.info(f" Устанавливаем возраст {age_value} для пользователя с данными: {user_data}")

        if expected_result:
            user = User(**user_data)  # Создаем пользователя с корректными данными
            logger.info(f"Создан пользователь с возрастом: {user.age}")
            assert user.age == age_value, f"Ожидалось {age_value}, но получено {user.age}"
        else:
            with pytest.raises(ValidationError) as excinfo:
                User(**user_data) # здесь проверяем исключение при создании пользователя
            logger.info(f"Ожидалось исключение при создании пользователя с возрастом {age_value}: {excinfo.value}")

    def test_password_validation(self, password_data, user_data):
        password_value, expected_result = password_data
        user_data["password"] = password_value
        logger.info(f" Устанавливаем пароль для пользователя с данными: {user_data}")

        if expected_result:
            user = User(**user_data)
            logger.info(f"Создан пользователь с паролем: {user.password}")
            assert user.password == password_value, f"Ожидалось {password_value}, но получено {user.password}"
        else:
            with pytest.raises(ValidationError) as excinfo:
                User(**user_data)  # здесь проверяем исключение при создании пользователя
            logger.info(f"Ожидалось исключение при создании пользователя с паролем {password_value}: {excinfo.value}")

    def test_role_validation(self, role_data, user_data):
        role_value, expected_result = role_data
        user_data['role'] = role_value  # Устанавливаем роль в данные
        logger.info(f" Устанавливаем роль для пользователя с данными: {user_data}")

        if expected_result:
            user = AdminUser(**user_data)  # Создаем администратора с корректными данными
            logger.info(f"Создан администратор с ролью: {user.role}")
            assert user.role.value == role_value, f"Ожидалось {role_value}, но получено {user.role.value}"
        else:
            with pytest.raises(ValidationError) as excinfo:
                AdminUser(**user_data)  # здесь проверяем исключение при создании администратора
            logger.info(f"Ожидалось исключение при создании администратора с ролью {role_value}: {excinfo.value}")
