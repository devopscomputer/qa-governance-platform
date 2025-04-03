import pytest
import allure


@allure.feature("🧩 API - Usuário")
@allure.story("🗑️ DELETE /users/{id}")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "delete", "regression")
@pytest.mark.api
@pytest.mark.delete
@pytest.mark.parametrize("user_id", [1, 2])
def test_delete_user(api_client, base_url, user_id):
    url = f"{base_url}/users/{user_id}"

    with allure.step(f"📤 Enviando requisição DELETE para: {url}"):
        response = api_client("delete", url)
        allure.attach(str(response.status_code), name="Código de Status", attachment_type=allure.attachment_type.TEXT)
        allure.attach(response.text, name="Resposta (Raw)", attachment_type=allure.attachment_type.TEXT)

        assert response.status_code in [200, 204], f"❌ Status inesperado: {response.status_code}"
        print(f"✅ DELETE executado com sucesso para user_id={user_id}")

    with allure.step("🧪 Validação da exclusão do recurso (assertivas avançadas)"):
        try:
            body = response.json()
        except ValueError:
            body = {}

        assert response.text.strip() == "" or body == {} or "id" not in body, (
            f"❌ Requisição retornou corpo inválido para exclusão: {body}"
        )
        print("✅ Validação da resposta concluída com sucesso.")

    with allure.step("📎 Log completo do fluxo"):
        allure.attach(
            f"Request: DELETE {url}\nStatus: {response.status_code}\nBody: {body}",
            name="Log Final",
            attachment_type=allure.attachment_type.TEXT
        )
