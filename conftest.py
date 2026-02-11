import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    # CI/CD için: options.add_argument("--headless")
    
    # Yeni Nesil Kullanım: Service ve DriverManager'a gerek kalmadan direkt başlatın
    # Selenium Manager arka planda doğru sürümü otomatik bulacaktır.
    driver = webdriver.Chrome(options=options)
    
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        try:
            driver_fixture = item.funcargs.get('driver')
            if driver_fixture:
                allure.attach(
                    driver_fixture.get_screenshot_as_png(),
                    name="Hata_Anı_Ekran_Görüntüsü",
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as e:
            print(f"Ekran görüntüsü hatası: {e}")