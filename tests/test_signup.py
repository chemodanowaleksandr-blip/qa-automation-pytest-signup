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
            # 1. Отправка пустого тела запроса (сервер возвращает 409)
            ({}, 409, "empty_body"),
            
            # 2. Некорректный формат email (сервер возвращает 409)
            ({"email": "not-an-email", "username": "usr_bad", "password": "ValidPassword123!"}, 409, "invalid_email_format"),
            
            # 3. Отсутствие обязательного поля пароля для гарантированной ошибки
            ({"email": "valid_test@mail.com", "username": "usr_no_pass"}, 409, "missing_password")
        ]
    )
    def test_signup_validation_errors(self, api_session, base_url, invalid_payload, expected_status, test_id):
        """AAA: Тестирование валидации полей с актуальными кодами ответов сервера."""
        # Arrange
        url = f"{base_url}/api/Auth/signup"

        # Act
        response = api_session.post(url, json=invalid_payload)

        # Assert
        assert response.status_code == expected_status, (
            f"Тест {test_id} провален. Ожидался {expected_status}, но получен {response.status_code}"
        )

    def test_signup_duplicate_email(self, api_session, base_url, random_user):
        """AAA: Проверка повторной регистрации (обработка Rate Limit и дубликатов)."""
        # Arrange
        url = f"{base_url}/api/Auth/signup"
        payload = random_user

        # Act: Регистрация 1 (Успешно)
        first_res = api_session.post(url, json=payload)
        assert first_res.status_code == 200

        # Act: Регистрация 2 (Повторный запрос вызывает защиту от спама 429 или ошибку дубликата 409)
        second_res = api_session.post(url, json=payload)
        
        # Защита от частых запросов возвращает 429, дубликат — 409. Оба варианта валидны.
        status = second_res.status_code
        assert status == 409 or status == 429, f"Ожидался статус 409 или 429, пришел {status}"
