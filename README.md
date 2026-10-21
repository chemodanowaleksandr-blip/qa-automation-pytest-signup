# Тестовое задание для автоматизатора тестов на Python с pytest

Реализация автотестов для проверки операции создания нового аккаунта (POST) на эндпоинте `/api/Auth/signup`.

## Структура проекта
```text
project/
├── .github/workflows/
│   └── run_tests.yml     # Настройка GitHub Actions (CI)
├── tests/
│   ├── __init__.py
│   ├── test_signup.py    # Класс тестов с параметризацией
│   └── conftest.py       # Фикстуры сессии, URL и Faker
├── requirements.txt      # Зависимости проекта
├── .gitignore            # Игнорируемые файлы
└── README.md             # Документация проекта
```

## Локальный запуск (опционально)
1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. Запустите тесты:
   ```bash
   pytest tests/ -v
   ```

## Пример ожидаемого вывода тестов (GitHub Actions)
```text
============================= test session starts ==============================
platform linux -- Python 3.10.x, pytest-8.3.3, pluggy-1.x.x
cachedir: .pytest_cache
collected 5 items

tests/test_signup.py::TestAuthSignup::test_successful_signup PASSED       [ 200%]
tests/test_signup.py::TestAuthSignup::test_signup_validation_errors[empty_body] PASSED [ 40%]
tests/test_signup.py::TestAuthSignup::test_signup_validation_errors[invalid_email_format] PASSED [ 60%]
tests/test_signup.py::TestAuthSignup::test_signup_validation_errors[too_weak_password] PASSED [ 80%]
tests/test_signup.py::TestAuthSignup::test_signup_duplicate_email PASSED [100%]

============================== 5 passed in 1.42s ===============================
```
