import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    
    # --- AKILLI ORTAM YÖNETİMİ ---
    # Eğer kod GitHub Actions (veya herhangi bir CI) üzerinde çalışıyorsa Headless yap
    if os.environ.get("GITHUB_ACTIONS") == "true" or os.environ.get("CI") == "true":
        print("🤖 CI Ortamı algılandı: Headless mod aktif.")
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox") # CI ortamları için kritiktir
        options.add_argument("--disable-dev-shm-usage") # Bellek hatalarını önler
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080") # Headless modda çözünürlük sorunu olmaması için
    else:
        print("💻 Yerel Ortam algılandı: Tarayıcı açılıyor.")
        # Yereldeysen headless kapalı kalır, rahatça izlersin.

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    
    yield driver
    
    driver.quit()