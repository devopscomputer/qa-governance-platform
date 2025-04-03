import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.feature("🌐 UI - Login do Sistema")
@allure.story("✅ Fluxo de Login com Credenciais Válidas")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("ui", "login", "real", "regression")
@pytest.mark.ui
@pytest.mark.smoke
def test_login_success(browser):
    """
    🎯 Cenário: Login bem-sucedido no site de testes HerokuApp
    📥 Quando ele preenche as credenciais corretas
    🎉 Então ele deve ver uma mensagem de sucesso
    """

    with allure.step("🌐 Acessar página de login pública"):
        browser.get("https://the-internet.herokuapp.com/login")
        assert "Login Page" in browser.title

    with allure.step("🧑‍💼 Inserir credenciais válidas"):
        browser.find_element(By.ID, "username").send_keys("tomsmith")
        browser.find_element(By.ID, "password").send_keys("SuperSecretPassword!" + Keys.RETURN)

    with allure.step("✅ Verificar alerta de sucesso"):
        WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.ID, "flash"))
        )
        alert = browser.find_element(By.ID, "flash")
        allure.attach(alert.text, name="Alerta Login", attachment_type=allure.attachment_type.TEXT)

        assert "You logged into a secure area!" in alert.text, "Mensagem de login não detectada"
