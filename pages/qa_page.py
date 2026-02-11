from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import time

class QAPage(BasePage):
    QA_URL = "https://insiderone.com/careers/quality-assurance/"
    COOKIE_ACCEPT = (By.ID, "wt-cli-accept-all-btn")
    SEE_JOBS_BTN = (By.XPATH, "//a[contains(text(), 'See all QA jobs')]")
    
    # --- LOCATORS ---
    JOB_LIST = (By.ID, "jobs-list")
    JOB_CARDS = (By.CSS_SELECTOR, ".position-list-item")
    POSITION_TITLE = (By.CSS_SELECTOR, ".position-title")
    LOCATION_TEXT = (By.CSS_SELECTOR, ".position-location")
    VIEW_ROLE_BTN = (By.XPATH, ".//a[contains(text(), 'View Role')]")

    # Lokasyon ve Departman Seçenekleri (Daha geniş kapsamlı XPath)
    ISTANBUL_OPTION = (By.XPATH, "//li[contains(@class, 'select2-results__option') and (contains(text(), 'Istanbul') or contains(text(), 'İstanbul'))]")
    QA_OPTION = (By.XPATH, "//li[contains(@class, 'select2-results__option') and contains(text(), 'Quality Assurance')]")

    def open_qa_jobs(self):
        self.driver.get(self.QA_URL)
        time.sleep(2)
        try:
            self.wait.until(EC.element_to_be_clickable(self.COOKIE_ACCEPT)).click()
        except:
            pass
        
        btn = self.wait.until(EC.element_to_be_clickable(self.SEE_JOBS_BTN))
        self.driver.execute_script("arguments[0].click();", btn)

    def filter_jobs(self):
        time.sleep(5) # Sayfa elementlerinin oturması için
        self.driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(2)

        # --- LOKASYON SEÇİMİ ---
        try:
            containers = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".select2-container")))
            location_dropdown = containers[0]
            self.driver.execute_script("arguments[0].click();", location_dropdown)
            
            # Seçeneğin tıklanabilir olmasını bekle
            ist_opt = self.wait.until(EC.element_to_be_clickable(self.ISTANBUL_OPTION))
            self.driver.execute_script("arguments[0].click();", ist_opt)
            print(">>> İstanbul başarıyla seçildi.")
        except Exception as e:
            print(f"!!! Lokasyon seçimi başarısız: {str(e)}")

        # --- DEPARTMAN SEÇİMİ ---
        time.sleep(2)
        try:
            containers = self.driver.find_elements(By.CSS_SELECTOR, ".select2-container")
            if len(containers) > 1:
                self.driver.execute_script("arguments[0].click();", containers[1])
                time.sleep(1)
                qa_opt = self.wait.until(EC.element_to_be_clickable(self.QA_OPTION))
                self.driver.execute_script("arguments[0].click();", qa_opt)
        except:
            pass

        time.sleep(3)

    def verify_jobs_list(self):
        # İş listesinin DOM'da varlığını ve görünürlüğünü kontrol eder
        try:
            return self.wait.until(EC.visibility_of_element_located(self.JOB_LIST)).is_displayed()
        except:
            return False

    def get_all_jobs_data(self):
        # Mevcut iş kartlarını listeler
        return self.driver.find_elements(*self.JOB_CARDS)

    def click_view_role(self):
        # İlk ilanın 'View Role' butonuna tıklar
        time.sleep(2)
        buttons = self.driver.find_elements(*self.VIEW_ROLE_BTN)
        if len(buttons) > 0:
            btn = buttons[0]
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            self.driver.execute_script("arguments[0].setAttribute('target', '_blank');", btn)
            self.driver.execute_script("arguments[0].click();", btn)
        else:
            raise Exception("View Role butonu bulunamadı!")