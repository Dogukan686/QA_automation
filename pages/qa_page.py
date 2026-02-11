from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

class QAPage:
    def __init__(self, driver):
        self.driver = driver
        self.SEE_ALL_JOBS_BTN = (By.LINK_TEXT, "See all QA jobs")
        # Locator'ı ID yerine daha genel bir Select2 seçicisine çevirdik
        self.LOCATION_CONTAINER = (By.ID, "select2-filter-by-location-container")
        self.JOBS_LIST = (By.ID, "jobs-list")
        self.POSITION_TITLE = (By.CLASS_NAME, "position-title")
        self.LOCATION_TEXT = (By.CLASS_NAME, "position-location")
        self.VIEW_ROLE_BTN = (By.LINK_TEXT, "View Role")
        self.COOKIE_ACCEPT_BTN = (By.ID, "wt-cli-accept-all-btn")

    def open_qa_jobs(self):
        self.driver.get("https://useinsider.com/careers/quality-assurance/")
        wait = WebDriverWait(self.driver, 30)
        
        # Çerezleri temizle
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
        # Sayfa yüklense de JS'nin (Select2) kendine gelmesi için zaman ver
        time.sleep(5)

    def filter_jobs(self):
        """İstanbul'u seçer. GitHub Actions'ın yavaşlığına karşı dirençli yapı."""
        wait = WebDriverWait(self.driver, 40) # Süreyi 40 saniyeye çıkardık
        
        # 1. Sayfanın tamamen yüklendiğinden emin ol
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

        # 2. Lokasyon dropdown'ının varlığını bekle (Görünürlük beklemiyoruz, varlık yeterli)
        loc_container = wait.until(EC.presence_of_element_located(self.LOCATION_CONTAINER))
        
        # 3. Elementi ekranın ortasına getir ve bekle
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", loc_container)
        time.sleep(3)
        
        # 4. İstanbul'u seçmek için 3 deneme yap (Retry Logic)
        istanbul_xpath = "//li[contains(@class, 'select2-results__option') and contains(text(), 'Istanbul')]"
        
        for i in range(3):
            try:
                # Menüyü aç
                self.driver.execute_script("arguments[0].click();", loc_container)
                time.sleep(2)
                
                # Seçeneğin görünmesini bekle ve tıkla
                istanbul_option = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, istanbul_xpath))
                )
                self.driver.execute_script("arguments[0].click();", istanbul_option)
                print(f"✅ Başarılı: Istanbul seçildi (Deneme {i+1})")
                break
            except TimeoutException:
                print(f"⚠️ Deneme {i+1}: Menü açılmadı veya Istanbul bulunamadı, tekrar deneniyor...")
                if i == 2: raise # 3 deneme de başarısızsa testi patlat
        
        # Filtrelemenin listeye yansıması için bekle
        time.sleep(6)

    def verify_jobs_list(self):
        wait = WebDriverWait(self.driver, 30)
        try:
            return wait.until(EC.presence_of_element_located(self.JOBS_LIST)).is_displayed()
        except: return False

    def get_all_jobs_data(self):
        # Liste boş geliyorsa sayfayı biraz aşağı kaydırarak tetikleyelim
        self.driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(2)
        return self.driver.find_elements(By.CLASS_NAME, "position-list-item")

    def click_view_role(self):
        wait = WebDriverWait(self.driver, 20)
        btn = wait.until(EC.presence_of_element_located(self.VIEW_ROLE_BTN))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(2)
        self.driver.execute_script("arguments[0].click();", btn)