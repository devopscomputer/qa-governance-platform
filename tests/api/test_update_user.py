import pytest
import allure
import requests


@allure.feature("🧩 API - Usuário")
@allure.story("🔄 PUT /users/{id}")
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
    timeout_seconds = 60

    try:
        with allure.step(f"🔄 Enviando requisição PUT para: {url}"):
            response = api_client("put", url, json=updated_data, timeout=timeout_seconds)
            allure.attach(str(response.status_code), name="🔢 Código de Status", attachment_type=allure.attachment_type.TEXT)
            allure.attach(response.text, name="📨 Corpo da Resposta", attachment_type=allure.attachment_type.JSON)
            assert response.status_code in [200, 204], f"❌ Status inesperado: {response.status_code}"
            print(f"✅ PUT executado com sucesso para user_id={user_id}")

        with allure.step("🧾 Validação da resposta após atualização"):
            try:
                body = response.json()
            except ValueError:
                pytest.fail("❌ Erro ao converter JSON da resposta.")

            assert body.get("name") == updated_data["name"], f"❌ Nome incorreto: {body.get('name')}"
            assert body.get("email") == updated_data["email"], f"❌ Email incorreto: {body.get('email')}"
            print("✅ Dados atualizados corretamente.")

        with allure.step("📎 Log final da operação"):
            log_text = (
                f"Request: PUT {url}\n"
                f"Payload: {updated_data}\n"
                f"Status: {response.status_code}\n"
                f"Response JSON: {body}"
            )
            allure.attach(log_text, name="🧩 Log Completo", attachment_type=allure.attachment_type.TEXT)

    except requests.exceptions.Timeout:
        pytest.fail(f"⏱️ Timeout: A solicitação excedeu o tempo limite de {timeout_seconds}s.")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"❌ Erro de requisição: {e}")
