import pytest
import allure

@allure.feature("API - Usuário")
@allure.story("PUT /users/{id}")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "update", "regression")
@pytest.mark.api
@pytest.mark.update
@pytest.mark.parametrize("user_id, updated_data", [
    (1, {"name": "João Atualizado", "email": "joao.atualizado@example.com"}),
    (2, {"name": "Maria Editada", "email": "maria.editada@example.com"})
])
def test_update_user(api_client, base_url, user_id, updated_data):
    url = f"{base_url}/users/{user_id}"

    with allure.step(f"🔄 Enviando PUT para {url} com dados atualizados"):
        response = api_client("put", url, json=updated_data)
        assert response.status_code in [200, 204], f"Status inesperado: {response.status_code}"

    with allure.step("🧾 Validar resposta da atualização"):
        body = response.json()
        assert body["name"] == updated_data["name"]
        assert body["email"] == updated_data["email"]
