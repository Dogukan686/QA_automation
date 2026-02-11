import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="function")
def driver():
    options = Options()
    
    # --- CI/CD ve GitHub Actions için Kritik Ayarlar ---
    options.add_argument("--headless") # Tarayıcıyı görünmez modda açar
    options.add_argument("--no-sandbox") # Güvenlik duvarını Linux için esnetir
    options.add_argument("--disable-dev-shm-usage") # Bellek sorunlarını önler
    options.add_argument("--window-size=1920,1080") # Ekran boyutu tanımlar
    
    # Driver başlatma
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.maximize_window()
    yield driver
    driver.quit()