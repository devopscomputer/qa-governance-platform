import pytest
import allure
from selenium.webdriver.common.by import By

@allure.feature("UI - Alertas e Feedback")
@allure.story("Mensagens de erro e sucesso")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.ui
def test_alert_display(browser):
    browser.get("https://the-internet.herokuapp.com/login")


    with allure.step("Tentar login sem senha"):
        browser.find_element(By.NAME, "username").send_keys("sem.senha@example.com")
        browser.find_element(By.ID, "btn-login").click()

    with allure.step("Validar alerta de erro"):
        alert = browser.find_element(By.CLASS_NAME, "alert-danger").text
        assert "Senha obrigatória" in alert
