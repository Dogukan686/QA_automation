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

    def open_qa_jobs(self):
        """QA kariyer sayfasını açar ve tüm ilanları listeleme butonuna tıklar."""
        self.driver.get("https://useinsider.com/careers/quality-assurance/")
        wait = WebDriverWait(self.driver, 15)
        btn = wait.until(EC.element_to_be_clickable(self.SEE_ALL_JOBS_BTN))
        btn.click()

    def filter_jobs(self):
        wait = WebDriverWait(self.driver, 20)
        
        # 1. Lokasyon menüsünü bekle
        location_container = wait.until(EC.element_to_be_clickable(self.LOCATION_CONTAINER))
        
        # Elementin üzerine kaydır (Scroll)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", location_container)
        time.sleep(1)
        
        # JavaScript ile tıkla (Engelleri aşar)
        self.driver.execute_script("arguments[0].click();", location_container)

        # 2. 'Istanbul, Turkiye' seçeneğini seç
        istanbul_option = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//li[contains(text(), 'Istanbul, Turkiye')]")
        ))
        self.driver.execute_script("arguments[0].click();", istanbul_option)
        
        time.sleep(5)

    def verify_jobs_list(self):
        """İş listesinin yüklendiğini doğrular."""
        wait = WebDriverWait(self.driver, 15)
        return wait.until(EC.visibility_of_element_located(self.JOBS_LIST)).is_displayed()

    def get_all_jobs_data(self):
        """Tüm ilan kartlarını bir liste olarak döner."""
        return self.driver.find_elements(By.CLASS_NAME, "position-list-item")

    def click_view_role(self):
        wait = WebDriverWait(self.driver, 15)
        # Butonun DOM'da hazır olmasını bekle
        btn = wait.until(EC.presence_of_element_located(self.VIEW_ROLE_BTN))
        
        # Elementi ortala ve JavaScript ile tıkla
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", btn)