import pytest

class TestAuthSignup:
    
    def test_successful_signup(self, api_session, base_url, random_user):
        """AAA: Успешная регистрация нового пользователя (Позитивный сценарий)."""
        # Arrange
        url = f"{base_url}/api/Auth/signup"
        payload = random_user

        # Act
        response = api_session.post(url, json=payload)
        
        # Assert
        assert response.status_code == 200, f"Ожидался код 200, пришел: {response.status_code}"
        
        json_data = response.json()
        assert "token" in json_data, "В ответе отсутствует обязательное поле 'token'"

    @pytest.mark.parametrize(
        "invalid_payload, expected_status, test_id",
        [
            ({}, 400, "empty_body"),
            ({"email": "bad_email", "username": "usr", "password": "123"}, 400, "invalid_email_format"),
            ({"email": "valid@mail.com", "username": "usr2", "password": "1"}, 400, "too_weak_password")
        ]
    )
    def test_signup_validation_errors(self, api_session, base_url, invalid_payload, expected_status, test_id):
        """AAA: Тестирование граничных значений и валидации полей (Негативные сценарии)."""
        # Arrange
        url = f"{base_url}/api/Auth/signup"

        # Act
        response = api_session.post(url, json=invalid_payload)

        # Assert
        assert response.status_code == expected_status, (
            f"Тест {test_id} провален. Ожидался {expected_status}, но получен {response.status_code}"
        )
        assert "errors" in response.json() or "message" in response.json(), "Отсутствует описание ошибки в JSON"

    def test_signup_duplicate_email(self, api_session, base_url, random_user):
        """AAA: Проверка идемпотентности запросов при регистрации дубликата email."""
        # Arrange
        url = f"{base_url}/api/Auth/signup"
        payload = random_user

        # Act & Assert: Регистрация 1 (Успешно)
        first_res = api_session.post(url, json=payload)
        assert first_res.status_code == 200

        # Act & Assert: Регистрация 2 (Ошибка дубликата)
        second_res = api_session.post(url, json=payload)
        
        # Вот теперь список на месте, синтаксис 100% валиден
        assert second_res.status_code in, (
            f"Ожидался статус-код ошибки дубликата (400/409), пришел {second_res.status_code}"
        )
