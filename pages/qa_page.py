from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def filter_jobs(self):
    wait = WebDriverWait(self.driver, 20)
    
    # 1. Lokasyon menüsünü bekle ve tıkla
    location_container = wait.until(EC.element_to_be_clickable((By.ID, "select2-filter-by-location-container")))
    self.driver.execute_script("arguments[0].click();", location_container)

    # 2. 'Istanbul, Turkiye' seçeneğini bul ve JavaScript ile tıkla
    istanbul_option = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//li[contains(text(), 'Istanbul, Turkiye')]")
    ))
    self.driver.execute_script("arguments[0].click();", istanbul_option)
    
    # 3. İlanların yenilenmesi için 5 saniye bekle (Berlin sızıntısını önleyen kritik bekleme)
    time.sleep(5)