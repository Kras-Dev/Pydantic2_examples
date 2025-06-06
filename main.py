from pydantic import ValidationError

from models import BaseUser, User, AdminUser

def main():
    us = BaseUser(email="asd@dfa.com", first_name="bo12b", second_name="siEson")
    print(us)
    us_v1 = User(email="asjdk@asdu.vv", first_name="SDam11", second_name="ASDk", age=99, password="*as12JJJ!asd")
    print(us_v1)
    us_v2 = AdminUser(email="Asdas@lo.cv", first_name="vvVir", second_name="OOOO", age=44, password="!0auld*asdA", role="admin")
    print(us_v2)

    print(us_v2.has_permission("read"))

    us_v3_data = us_v1.model_dump(by_alias=True)
    us_v3 = AdminUser(**us_v3_data, role="superadmin")

    print(us_v3.has_permission("manage_users"))
    print(f"schema: {us_v3.model_json_schema()}")

    # Пример данных для проверки
    test_data = [
        {"email": "invalid_email", "first_name": "John", "second_name": "Doe", "age": 22, "password":"psq12!JJasd&"},
        {"email": "john@example.com", "first_name": "", "second_name": "Doe", "age": 22, "password":"psq12!JJasd&"},
        {"email": "john@example.com", "first_name": "John", "second_name": "", "age": 22, "password":"psq12!JJasd&"},
    ]

    for data in test_data:
        try:
            User(**data)
        except ValidationError as e:
            # Перебираем все ошибки и выводим их типы
            for error in e.errors():
                print(f"Field: {error['loc']}, Error Type: {error['type']}, Message: {error['msg']}")

if __name__ == "__main__":
    main()
