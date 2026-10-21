import pytest
import requests
from faker import Faker

@pytest.fixture(scope="class")
def base_url():
    """Фикстура для хранения базового URL API."""
    return "https://automation.tivaliclub.com/fcle"

@pytest.fixture(scope="class")
def api_session():
    """Фикстура для управления HTTP-сессией requests."""
    session = requests.Session()
    yield session
    session.close()

@pytest.fixture
def random_user():
    """Фикстура для генерации уникальных тестовых данных пользователя."""
    fake = Faker()
    return {
        "email": fake.email(),
        "username": fake.user_name(),
        "password": f"SecureP@ss{fake.random_int(1000, 9999)}"
    }
