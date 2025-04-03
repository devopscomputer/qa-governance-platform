import pytest
import requests
import allure
import os
from typing import Callable

# -------------------------------
# CLI: Parametrização por Ambiente
# -------------------------------

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Ambiente de execução: dev, staging ou prod"
    )

@pytest.fixture(scope="session")
def env(request) -> str:
    return request.config.getoption("--env")

@pytest.fixture(scope="session")
def base_url(env: str) -> str:
    urls = {
        "dev": "https://jsonplaceholder.typicode.com",
        "staging": "https://staging.api.exemplo.com",
        "prod": "https://api.exemplo.com"
    }
    return urls.get(env, urls["dev"])

# -------------------------------
# Fixture API Client com Log Allure
# -------------------------------

@pytest.fixture
def api_client() -> Callable:
    session = requests.Session()

    def _log_request(method: str, url: str, **kwargs):
        with allure.step(f"🔗 {method.upper()} {url}"):
            if "headers" in kwargs:
                allure.attach(str(kwargs["headers"]), name="Headers", attachment_type=allure.attachment_type.JSON)
            if "json" in kwargs:
                allure.attach(str(kwargs["json"]), name="Payload", attachment_type=allure.attachment_type.JSON)

            response = session.request(method, url, **kwargs)

            try:
                body = response.json()
                allure.attach(str(body), name="Resposta JSON", attachment_type=allure.attachment_type.JSON)
            except Exception:
                allure.attach(response.text, name="Resposta Raw", attachment_type=allure.attachment_type.TEXT)

            allure.attach(str(response.status_code), name="Status Code", attachment_type=allure.attachment_type.TEXT)
            return response

    return _log_request

# -------------------------------
# Fixture: Navegador Headless para UI Tests
# -------------------------------

@pytest.fixture(scope="function")
def browser():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1280,1024")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

# -------------------------------
# Fixture: Payload padrão de criação de usuário
# -------------------------------

@pytest.fixture
def user_payload():
    return {
        "name": "Usuário Teste",
        "email": "usuario.teste@example.com"
    }
