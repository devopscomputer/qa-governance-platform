import pytest
import allure
from selenium.webdriver.common.by import By

@allure.feature("UI - Cadastro")
@allure.story("Cadastro de novo usuário")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.ui
def test_signup_user(browser):
    browser.get("https://the-internet.herokuapp.com/login")

    with allure.step("Preencher formulário de cadastro"):
        browser.find_element(By.NAME, "username").send_keys("Usuário Teste")
        browser.find_element(By.NAME, "email").send_keys("usuario@teste.com")
        browser.find_element(By.NAME, "password").send_keys("123456")
        browser.find_element(By.NAME, "confirm_password").send_keys("123456")

    with allure.step("Submeter cadastro"):
        browser.find_element(By.ID, "btn-register").click()

    with allure.step("Validar mensagem de sucesso"):
        msg = browser.find_element(By.CLASS_NAME, "alert-success").text
        assert "Cadastro realizado" in msg
