from pydantic import ValidationError

from models import BaseUser, User, AdminUser

def main():
    us = BaseUser(email="asd@dfa.com", name="bo12b", second_name="siEson")
    print(us)
    us_v1 = User(email="asjdk@asdu.vv", name="SDam11", second_name="ASDk", age=99, password="*as12JJJ!asd")
    print(us_v1)
    us_v2 = AdminUser(email="Asdas@lo.cv", name="vvVir", second_name="OOOO", age=44, password="!0auld*asdA", role="admin")
    print(us_v2)


    print(us_v2.has_permission("read"))

    us_v3_data = us_v1.model_dump(by_alias=True)
    us_v3 = AdminUser(**us_v3_data, role="superadmin")

    print(us_v3.has_permission("manage_users"))

    # Пример данных для проверки
    test_data = [
        {"email": "invalid_email", "name": "John", "second_name": "Doe", "age": 22, "password":"psq12!JJasd&"},
        {"email": "john@example.com", "name": "", "second_name": "Doe", "age": 22, "password":"psq12!JJasd&"},
        {"email": "john@example.com", "name": "John", "second_name": "", "age": 22, "password":"psq12!JJasd&"},
    ]

    for data in test_data:
        try:
            user = User(**data)
        except ValidationError as e:
            # Перебираем все ошибки и выводим их типы
            for error in e.errors():
                print(f"Field: {error['loc']}, Error Type: {error['type']}, Message: {error['msg']}")

if __name__ == "__main__":
    main()


    # def test_invalid_user(self, invalid_user_data):
    #     with pytest.raises(ValueError) as exc_info:
    #         user = User(**invalid_user_data)
    #     assert invalid_user_data['error'] in str(exc_info.value)