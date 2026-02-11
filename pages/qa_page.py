from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

class QAPage:
    def __init__(self, driver):
        self.driver = driver
        self.SEE_ALL_JOBS_BTN = (By.LINK_TEXT, "See all QA jobs")
        self.LOCATION_CONTAINER = (By.ID, "select2-filter-by-location-container")
        self.JOBS_LIST = (By.ID, "jobs-list")
        self.POSITION_TITLE = (By.CLASS_NAME, "position-title")
        self.LOCATION_TEXT = (By.CLASS_NAME, "position-location")
        self.VIEW_ROLE_BTN = (By.LINK_TEXT, "View Role")
        self.COOKIE_ACCEPT_BTN = (By.ID, "wt-cli-accept-all-btn")

    def open_qa_jobs(self):
        self.driver.get("https://useinsider.com/careers/quality-assurance/")
        wait = WebDriverWait(self.driver, 25)
        try:
            cookie_btn = wait.until(EC.element_to_be_clickable(self.COOKIE_ACCEPT_BTN))
            cookie_btn.click()
        except: pass
        btn = wait.until(EC.presence_of_element_located(self.SEE_ALL_JOBS_BTN))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(2)
        self.driver.execute_script("arguments[0].click();", btn)
        wait.until(EC.url_contains("open-positions"))
        time.sleep(3)

    def filter_jobs(self):
        """İstanbul'u seçer. Menü açılmazsa tekrar dener."""
        wait = WebDriverWait(self.driver, 30)
        
        # 1. Lokasyon dropdown'ını bul ve tıkla
        loc_container = wait.until(EC.visibility_of_element_located(self.LOCATION_CONTAINER))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", loc_container)
        time.sleep(2)
        
        # Menü açılana kadar (veya 3 deneme boyunca) tıkla
        istanbul_xpath = "//li[contains(@class, 'select2-results__option') and contains(text(), 'Istanbul')]"
        
        for _ in range(3):
            self.driver.execute_script("arguments[0].click();", loc_container)
            time.sleep(2)
            try:
                # Seçeneğin görünür olmasını bekle
                istanbul_option = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located((By.XPATH, istanbul_xpath))
                )
                self.driver.execute_script("arguments[0].click();", istanbul_option)
                print("✅ Istanbul seçeneği başarıyla tıklandı.")
                break
            except TimeoutException:
                print("⚠️ Menü açılmadı veya seçenek bulunamadı, tekrar deneniyor...")
                continue
        
        # Filtrelemenin listeye yansıması için bekle
        time.sleep(6)

    def verify_jobs_list(self):
        wait = WebDriverWait(self.driver, 25)
        try:
            return wait.until(EC.presence_of_element_located(self.JOBS_LIST)).is_displayed()
        except: return False

    def get_all_jobs_data(self):
        # Liste boş geliyorsa scroll yapıp tetiklemek gerekebilir
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(2)
        return self.driver.find_elements(By.CLASS_NAME, "position-list-item")

    def click_view_role(self):
        wait = WebDriverWait(self.driver, 20)
        btn = wait.until(EC.presence_of_element_located(self.VIEW_ROLE_BTN))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(2)
        self.driver.execute_script("arguments[0].click();", btn)