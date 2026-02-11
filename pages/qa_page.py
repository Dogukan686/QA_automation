from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

class QAPage:
    def __init__(self, driver):
        self.driver = driver
        self.SEE_ALL_JOBS_BTN = (By.LINK_TEXT, "See all QA jobs")
        # --- EN SAĞLAM LOCATOR: Etiket metni üzerinden bulma ---
        self.LOCATION_DROPDOWN = (By.XPATH, "//label[contains(text(), 'Filter by Location')]/following-sibling::span")
        self.JOBS_LIST = (By.ID, "jobs-list")
        self.POSITION_TITLE = (By.CLASS_NAME, "position-title")
        self.LOCATION_TEXT = (By.CLASS_NAME, "position-location")
        self.VIEW_ROLE_BTN = (By.LINK_TEXT, "View Role")
        self.COOKIE_ACCEPT_BTN = (By.ID, "wt-cli-accept-all-btn")

    def open_qa_jobs(self):
        self.driver.get("https://useinsider.com/careers/quality-assurance/")
        wait = WebDriverWait(self.driver, 30)
        
        try:
            cookie_btn = wait.until(EC.element_to_be_clickable(self.COOKIE_ACCEPT_BTN))
            cookie_btn.click()
        except: pass

        btn = wait.until(EC.presence_of_element_located(self.SEE_ALL_JOBS_BTN))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(2)
        self.driver.execute_script("arguments[0].click();", btn)
        
        # Sayfanın değiştiğinden emin ol
        wait.until(EC.url_contains("open-positions"))
        time.sleep(5) 

    def filter_jobs(self):
        """İstanbul'u seçer. Etiket referanslı ve retry mekanizmalı."""
        wait = WebDriverWait(self.driver, 50) # Süreyi daha da artırdık
        
        # 1. Sayfanın en altına kadar kaydırıp geri çık (Lazy-load tetikleyici)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)

        # 2. Lokasyon dropdown'ının varlığını bekle
        try:
            loc_container = wait.until(EC.presence_of_element_located(self.LOCATION_DROPDOWN))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", loc_container)
            time.sleep(3)
        except TimeoutException:
            print(f"❌ HATA: Lokasyon filtresi bulunamadı. URL: {self.driver.current_url}")
            raise

        # 3. İstanbul'u seçmek için denemeler
        istanbul_xpath = "//li[contains(@class, 'select2-results__option') and contains(text(), 'Istanbul')]"
        
        for i in range(3):
            try:
                # Menüyü JavaScript ile aç
                self.driver.execute_script("arguments[0].click();", loc_container)
                time.sleep(2)
                
                # Seçeneğin görünmesini bekle ve tıkla
                istanbul_option = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, istanbul_xpath))
                )
                self.driver.execute_script("arguments[0].click();", istanbul_option)
                print(f"✅ Başarılı: Istanbul seçildi (Deneme {i+1})")
                return # Başarılıysa çık
            except TimeoutException:
                print(f"⚠️ Deneme {i+1}: Menü açılmadı, tekrar deneniyor...")
        
        raise TimeoutException("3 denemede de Istanbul seçilemedi.")

    def verify_jobs_list(self):
        wait = WebDriverWait(self.driver, 30)
        try:
            # Liste bazen 'is-loading' class'ına sahip olur, onun bitmesini beklemek gerekebilir
            # Şimdilik varlığını kontrol ediyoruz
            return wait.until(EC.presence_of_element_located(self.JOBS_LIST)).is_displayed()
        except: return False

    def get_all_jobs_data(self):
        self.driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(3)
        return self.driver.find_elements(By.CLASS_NAME, "position-list-item")

    def click_view_role(self):
        wait = WebDriverWait(self.driver, 30)
        btn = wait.until(EC.presence_of_element_located(self.VIEW_ROLE_BTN))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(2)
        self.driver.execute_script("arguments[0].click();", btn)