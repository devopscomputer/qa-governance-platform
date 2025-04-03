import pytest
import allure
from selenium.webdriver.common.by import By

@allure.feature("UI - Visual")
@allure.story("Captura de tela da Home")
@allure.severity(allure.severity_level.TRIVIAL)
@pytest.mark.ui
def test_capture_home(browser):
    browser.get("https://exemplo.com")

    with allure.step("Capturar screenshot da homepage"):
        browser.save_screenshot("reports/screenshots/home.png")
        allure.attach.file("reports/screenshots/home.png", name="Home Screenshot", attachment_type=allure.attachment_type.PNG)

    assert "Bem-vindo" in browser.page_source
