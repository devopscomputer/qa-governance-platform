import pytest
import allure

@allure.feature("API - Usuário")
@allure.story("POST /users")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "create", "regression")
@pytest.mark.api
@pytest.mark.create
@pytest.mark.parametrize("payload", [
    {
        "name": "Ana Testadora",
        "email": "ana.testadora@example.com"
    },
    {
        "name": "Bruno QA",
        "email": "bruno.qa@example.com"
    }
])
def test_create_user(api_client, base_url, payload):
    """
    Testa o endpoint de criação de usuário (POST /users)
    """

    url = f"{base_url}/users"

    with allure.step(f"📤 Enviando POST para {url} com payload: {payload}"):
        response = api_client("post", url, json=payload)
        assert response.status_code in [200, 201], f"Status inválido: {response.status_code}"

    with allure.step("✅ Validar corpo da resposta"):
        body = response.json()
        assert "id" in body, "ID ausente na resposta"
        assert body["name"] == payload["name"]
        assert body["email"] == payload["email"]
