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
        self.JOBS_LIST = (By.ID, "jobs-list")
        self.POSITION_TITLE = (By.CLASS_NAME, "position-title")
        self.LOCATION_TEXT = (By.CLASS_NAME, "position-location")
        self.VIEW_ROLE_BTN = (By.LINK_TEXT, "View Role")
        self.COOKIE_ACCEPT_BTN = (By.ID, "wt-cli-accept-all-btn")

    def open_qa_jobs(self):
        """QA kariyer sayfasını açar, çerezleri kabul eder ve ilanlara tıklar."""
        self.driver.get("https://useinsider.com/careers/quality-assurance/")
        wait = WebDriverWait(self.driver, 20)
        
        # 1. Çerez Banner'ını Kapat (Tıklamayı engelleyen en büyük sebep)
        try:
            cookie_btn = wait.until(EC.element_to_be_clickable(self.COOKIE_ACCEPT_BTN))
            cookie_btn.click()
        except:
            pass # Görünmüyorsa devam et

        # 2. 'See all QA jobs' butonunu bekle ve JS ile tıkla
        btn = wait.until(EC.presence_of_element_located(self.SEE_ALL_JOBS_BTN))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn)

    def filter_jobs(self):
        """İstanbul lokasyonunu seçer ve filtrenin oturması için bekler."""
        wait = WebDriverWait(self.driver, 20)
        
        # 1. Lokasyon menüsünü bekle ve JS ile tıkla
        location_container = wait.until(EC.presence_of_element_located(self.LOCATION_CONTAINER))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", location_container)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", location_container)

        # 2. 'Istanbul, Turkiye' seçeneğini bul ve JS ile tıkla
        istanbul_option = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//li[contains(text(), 'Istanbul, Turkiye')]")
        ))
        self.driver.execute_script("arguments[0].click();", istanbul_option)
        
        # 3. İlanların yenilenmesi için 5 saniye bekle (Berlin sızıntısını önler)
        time.sleep(5)

    def verify_jobs_list(self):
        """İş listesinin (ilanların) sayfada göründüğünü doğrular."""
        wait = WebDriverWait(self.driver, 20)
        try:
            jobs_list = wait.until(EC.visibility_of_element_located(self.JOBS_LIST))
            return jobs_list.is_displayed()
        except:
            return False

    def get_all_jobs_data(self):
        """Tüm ilan kartlarını bir liste olarak döner."""
        return self.driver.find_elements(By.CLASS_NAME, "position-list-item")

    def click_view_role(self):
        """İlk ilanın 'View Role' butonuna JavaScript ile tıkla."""
        wait = WebDriverWait(self.driver, 20)
        # Butonun DOM'da hazır olmasını bekle
        btn = wait.until(EC.presence_of_element_located(self.VIEW_ROLE_BTN))
        
        # Elementi ortala ve JS ile tıkla (Interception hatasını önler)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn)