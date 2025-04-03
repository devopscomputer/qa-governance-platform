import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

@allure.feature("UI - Login")
@allure.story("Login bem-sucedido")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("ui", "smoke", "regression")
@pytest.mark.ui
@pytest.mark.smoke
def test_login_success(browser):
    with allure.step("Abrir página de login"):
        browser.get("https://exemplo.com/login")
        assert "Login" in browser.title

    with allure.step("Preencher credenciais válidas"):
        browser.find_element(By.ID, "email").send_keys("usuario@teste.com")
        browser.find_element(By.ID, "password").send_keys("SenhaForte123" + Keys.RETURN)

    with allure.step("Verificar redirecionamento para dashboard"):
        assert "Dashboard" in browser.title
