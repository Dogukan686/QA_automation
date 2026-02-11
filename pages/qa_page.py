from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import time

class QAPage(BasePage):
    QA_URL = "https://useinsider.com/careers/quality-assurance/"
    
    # --- LOCATORS ---
    COOKIE_ACCEPT = (By.ID, "wt-cli-accept-all-btn")
    SEE_JOBS_BTN = (By.XPATH, "//a[contains(text(), 'See all QA jobs')]")
    JOB_LIST = (By.ID, "jobs-list")
    JOB_CARDS = (By.CSS_SELECTOR, ".position-list-item")
    
    # Test dosyasının (tests/test_insider_qa.py) beklediği tam isimler
    POSITION_TITLE = (By.CSS_SELECTOR, ".position-title")
    LOCATION_TEXT = (By.CSS_SELECTOR, ".position-location")
    DEPARTMENT_TEXT = (By.CSS_SELECTOR, ".position-department")
    VIEW_ROLE_BTN = (By.XPATH, ".//a[contains(text(), 'View Role')]")
    
    # Filtreleme Elementleri
    FILTER_CONTAINERS = (By.CSS_SELECTOR, ".select2-selection--single")
    ISTANBUL_OPTION = (By.XPATH, "//li[contains(@class, 'select2-results__option') and contains(text(), 'Istanbul')]")

    def open_qa_jobs(self):
        self.driver.get(self.QA_URL)
        try:
            self.wait.until(EC.element_to_be_clickable(self.COOKIE_ACCEPT)).click()
        except: pass
        
        btn = self.wait.until(EC.element_to_be_clickable(self.SEE_JOBS_BTN))
        self.driver.execute_script("arguments[0].click();", btn)

    def filter_jobs(self):
        """Filtreleme işlemini JS click ve ekstra bekleme ile yapar."""
        time.sleep(8) # Sayfanın ve Select2 kütüphanesinin tam yüklenmesi için
        self.driver.execute_script("window.scrollBy(0, 500);")
        
        try:
            # 1. Lokasyon Dropdown'ını aç
            dropdowns = self.wait.until(EC.presence_of_all_elements_located(self.FILTER_CONTAINERS))
            self.driver.execute_script("arguments[0].click();", dropdowns[0])
            
            # 2. İstanbul seçeneğinin görünmesini bekle ve tıkla
            ist_opt = self.wait.until(EC.visibility_of_element_located(self.ISTANBUL_OPTION))
            self.driver.execute_script("arguments[0].click();", ist_opt)
            print(">>> Lokasyon filtresi: Istanbul başarıyla seçildi.")
            
            # Listenin yenilenmesi için Insider'ın API'sine zaman tanı
            time.sleep(5) 

        except Exception as e:
            print(f"!!! Filtreleme hatası: {str(e)}")

    def verify_jobs_list(self):
        return self.wait.until(EC.visibility_of_element_located(self.JOB_LIST)).is_displayed()

    def get_all_jobs_data(self):
        return self.driver.find_elements(*self.JOB_CARDS)

    def click_view_role(self):
        """İlandaki 'View Role' butonuna tıklar ve yeni sekmeye odaklanır."""
        time.sleep(2)
        buttons = self.driver.find_elements(*self.VIEW_ROLE_BTN)