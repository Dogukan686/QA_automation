import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="function")
def driver():
    options = Options()
    
    # --- GitHub Actions (Linux) İçin Kritik Parametreler ---
    options.add_argument("--headless=new") # Tarayıcıyı görünmez yapar
    options.add_argument("--no-sandbox")   # Güvenlik katmanını aşar (Linux için şart)
    options.add_argument("--disable-dev-shm-usage") # Bellek sorunlarını önler
    options.add_argument("--window-size=1920,1080") # Ekran boyutu tanımlar
    
    # WebDriver kurulumu
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.maximize_window()
    yield driver
    driver.quit()