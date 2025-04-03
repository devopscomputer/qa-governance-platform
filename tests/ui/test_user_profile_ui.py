import pytest
import allure
from selenium.webdriver.common.by import By

@allure.feature("UI - Perfil")
@allure.story("Edição de perfil do usuário")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.ui
def test_edit_user_profile(browser):
    browser.get("https://the-internet.herokuapp.com/login")

    with allure.step("Editar nome de usuário"):
        name_field = browser.find_element(By.NAME, "username")
        name_field.clear()
        name_field.send_keys("Nome Atualizado")
        browser.find_element(By.ID, "btn-save-profile").click()

    with allure.step("Validar atualização"):
        success = browser.find_element(By.CLASS_NAME, "alert-success").text
        assert "Perfil atualizado" in success
