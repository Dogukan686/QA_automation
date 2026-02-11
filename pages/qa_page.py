from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class QAPage:
    def __init__(self, driver):
        self.driver = driver
        # Locator Tanımları
        self.SEE_ALL_JOBS_BTN = (By.LINK_TEXT, "See all QA jobs")
        self.LOCATION_CONTAINER = (By.ID, "select2-filter-by-location-container")
        self.FILTER_SECTION = (By.ID, "filter-utils") # Filtrelerin olduğu ana bölüm
        self.JOBS_LIST = (By.ID, "jobs-list")
        self.POSITION_TITLE = (By.CLASS_NAME, "position-title")
        self.LOCATION_TEXT = (By.CLASS_NAME, "position-location")
        self.VIEW_ROLE_BTN = (By.LINK_TEXT, "View Role")
        self.COOKIE_ACCEPT_BTN = (By.ID, "wt-cli-accept-all-btn")

    def open_qa_jobs(self):
        """QA kariyer sayfasını açar ve ilanlar sayfasına geçişi bekler."""
        self.driver.get("https://useinsider.com/careers/quality-assurance/")
        wait = WebDriverWait(self.driver, 20)
        
        # 1. Çerez Banner'ını kapat
        try:
            cookie_btn = wait.until(EC.element_to_be_clickable(self.COOKIE_ACCEPT_BTN))
            cookie_btn.click()
        except:
            pass

        # 2. 'See all QA jobs' butonuna JS ile tıkla
        btn = wait.until(EC.presence_of_element_located(self.SEE_ALL_JOBS_BTN))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn)

        # 3. KRİTİK: İlanlar sayfasının yüklendiğini doğrula (URL kontrolü)
        wait.until(EC.url_contains("open-positions"))

    def filter_jobs(self):
        """Filtre bölümünün hazır olmasını bekler ve İstanbul'u seçer."""
        wait = WebDriverWait(self.driver, 30) # Süreyi biraz daha artırdık
        
        # 1. Filtreleme bölümünün (Dropdown'ların olduğu alan) görünür olmasını bekle
        wait.until(EC.visibility_of_element_located(self.FILTER_SECTION))
        
        # 2. Lokasyon menüsünü bekle ve tıkla
        location_container = wait.until(EC.element_to_be_clickable(self.LOCATION_CONTAINER))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", location_container)
        time.sleep(2) # Select2 bileşeninin kendine gelmesi için kısa bir es
        self.driver.execute_script("arguments[0].click();", location_container)

        # 3. 'Istanbul, Turkiye' seçeneğini bul ve tıkla
        istanbul_option = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//li[contains(text(), 'Istanbul, Turkiye')]")
        ))
        self.driver.execute_script("arguments[0].click();", istanbul_option)
        
        # 4. İlanların yenilenmesi için bekle
        time.sleep(5)

    def verify_jobs_list(self):
        wait = WebDriverWait(self.driver, 20)
        try:
            # İlan listesinin görünür olmasını bekle
            return wait.until(EC.visibility_of_element_located(self.JOBS_LIST)).is_displayed()
        except:
            return False

    def get_all_jobs_data(self):
        return self.driver.find_elements(By.CLASS_NAME, "position-list-item")

    def click_view_role(self):
        wait = WebDriverWait(self.driver, 20)
        btn = wait.until(EC.presence_of_element_located(self.VIEW_ROLE_BTN))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn)