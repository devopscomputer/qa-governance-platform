import pytest
import allure

@allure.feature("API - Usuário")
@allure.story("DELETE /users/{id}")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "delete", "regression")
@pytest.mark.api
@pytest.mark.delete
@pytest.mark.parametrize("user_id", [1, 2])
def test_delete_user(api_client, base_url, user_id):
    url = f"{base_url}/users/{user_id}"

    with allure.step(f"🗑️ Enviando DELETE para {url}"):
        response = api_client("delete", url)
        assert response.status_code in [200, 204], f"Status inesperado: {response.status_code}"

    with allure.step("📉 Validar que o recurso foi removido ou tratado corretamente"):
        assert response.status_code in [200, 204]
        assert response.text.strip() == "" or response.json() == {} or "id" not in response.json()

