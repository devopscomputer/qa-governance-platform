import pytest
import allure

@allure.feature("API - Usuário")
@allure.story("GET /users/{id}")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "contract", "regression")
@pytest.mark.api
@pytest.mark.contract
@pytest.mark.parametrize("user_id", [1, 2])
def test_get_user_by_id(api_client, base_url, user_id):
    """
    Valida o contrato e conteúdo da resposta do endpoint GET /users/{id}
    """

    url = f"{base_url}/users/{user_id}"

    with allure.step(f"📡 Requisição GET no endpoint {url}"):
        response = api_client("get", url)
        assert response.status_code == 200, f"Status inesperado: {response.status_code}"

    with allure.step("✅ Validar campos principais da resposta JSON"):
        body = response.json()
        assert body["id"] == user_id, "ID do usuário não corresponde"
        assert "name" in body and isinstance(body["name"], str)
        assert "email" in body and "@" in body["email"]
        assert "address" in body and isinstance(body["address"], dict)

    with allure.step("🌍 Validar dados de localização (geo)"):
        geo = body["address"].get("geo", {})
        assert "lat" in geo and "lng" in geo, "Coordenadas ausentes em address.geo"
        assert isinstance(geo["lat"], str) and isinstance(geo["lng"], str)
