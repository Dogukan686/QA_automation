from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class QAPage:
    def __init__(self, driver):
        self.driver = driver
        # Locator Tanımları (Daha esnek CSS seçiciler eklendi)
        self.SEE_ALL_JOBS_BTN = (By.LINK_TEXT, "See all QA jobs")
        self.LOCATION_CONTAINER = (By.CSS_SELECTOR, ".select2-selection--single") # Genel select2 kutusu
        self.JOBS_LIST = (By.ID, "jobs-list")
        self.POSITION_TITLE = (By.CLASS_NAME, "position-title")
        self.LOCATION_TEXT = (By.CLASS_NAME, "position-location")
        self.VIEW_ROLE_BTN = (By.LINK_TEXT, "View Role")
        self.COOKIE_ACCEPT_BTN = (By.ID, "wt-cli-accept-all-btn")

    def open_qa_jobs(self):
        """QA kariyer sayfasını açar ve ilanlar sayfasına geçişi bekler."""
        self.driver.get("https://useinsider.com/careers/quality-assurance/")
        wait = WebDriverWait(self.driver, 25)
        
        # 1. Çerez Banner'ını kapat (Zaman aşımını önlemek için)
        try:
            cookie_btn = wait.until(EC.element_to_be_clickable(self.COOKIE_ACCEPT_BTN))
            cookie_btn.click()
        except:
            pass

        # 2. 'See all QA jobs' butonuna JS ile tıkla
        btn = wait.until(EC.presence_of_element_located(self.SEE_ALL_JOBS_BTN))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(2)
        self.driver.execute_script("arguments[0].click();", btn)

        # 3. İlanlar sayfasına geçtiğimizden emin ol
        wait.until(EC.url_contains("open-positions"))
        # Sayfanın JS bileşenlerinin (Select2) yüklenmesi için 3 saniye ek nefes payı
        time.sleep(3)

    def filter_jobs(self):
        """Filtrelerin hazır olmasını bekler ve İstanbul'u seçer."""
        wait = WebDriverWait(self.driver, 40) # CI ortamı için süreyi artırdık
        
        # 1. Lokasyon dropdown kutusunu bekle
        # filter-utils ID'si bazen geç gelir, doğrudan seçim kutusunu bekliyoruz
        location_box = wait.until(EC.presence_of_all_elements_located(self.LOCATION_CONTAINER))[0]
        
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", location_box)
        time.sleep(2)
        
        # JavaScript ile tıkla (En garantisi)
        self.driver.execute_script("arguments[0].click();", location_box)

        # 2. 'Istanbul, Turkiye' seçeneğini DOM'da bul ve tıkla
        istanbul_option = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//li[contains(text(), 'Istanbul, Turkiye')]")
        ))
        self.driver.execute_script("arguments[0].click();", istanbul_option)
        
        # 3. İlanların filtrelenmesi için bekle
        time.sleep(5)

    def verify_jobs_list(self):
        wait = WebDriverWait(self.driver, 25)
        try:
            return wait.until(EC.visibility_of_element_located(self.JOBS_LIST)).is_displayed()
        except:
            return False

    def get_all_jobs_data(self):
        return self.driver.find_elements(By.CLASS_NAME, "position-list-item")

    def click_view_role(self):
        wait = WebDriverWait(self.driver, 20)
        btn = wait.until(EC.presence_of_element_located(self.VIEW_ROLE_BTN))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(2)
        self.driver.execute_script("arguments[0].click();", btn)