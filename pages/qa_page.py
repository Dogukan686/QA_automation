from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

class QAPage:
    def __init__(self, driver):
        self.driver = driver
        self.SEE_ALL_JOBS_BTN = (By.LINK_TEXT, "See all QA jobs")
        # Locator'ı daha geniş kapsamlı bir CSS seçicisine çevirdik
        self.LOCATION_CONTAINER = (By.CSS_SELECTOR, "span[aria-labelledby*='select2-filter-by-location']")
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
        
        # Sayfanın yüklendiğini doğrula
        wait.until(EC.url_contains("open-positions"))
        time.sleep(5) # Sayfanın JS bileşenleri için nefes payı

    def filter_jobs(self):
        """İstanbul'u seçer. GitHub Actions'ın yavaşlığına karşı dirençli yapı."""
        wait = WebDriverWait(self.driver, 45) # Süreyi biraz daha artırdık
        
        # 1. Filtrelerin olduğu bölüme kadar sayfayı kaydır (Lazy load'u tetikle)
        self.driver.execute_script("window.scrollTo(0, 600);")
        time.sleep(3)

        # 2. Lokasyon dropdown'ının varlığını bekle
        try:
            loc_container = wait.until(EC.presence_of_element_located(self.LOCATION_CONTAINER))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", loc_container)
            time.sleep(2)
        except TimeoutException:
            print("❌ HATA: Lokasyon filtresi bulunamadı. Sayfa tam yüklenmemiş olabilir.")
            # Hata anındaki URL'yi yazdır (Debug için)
            print(f"Mevcut URL: {self.driver.current_url}")
            raise

        # 3. İstanbul'u seçmek için denemeler yap
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
                break
            except TimeoutException:
                print(f"⚠️ Deneme {i+1}: Istanbul seçeneği henüz belirmedi, tekrar deneniyor...")
                if i == 2: raise
        
        time.sleep(6)

    def verify_jobs_list(self):
        wait = WebDriverWait(self.driver, 30)
        try:
            return wait.until(EC.presence_of_element_located(self.JOBS_LIST)).is_displayed()
        except: return False

    def get_all_jobs_data(self):
        # Liste güncellenirken sayfa atlamasını önlemek için hafif scroll
        self.driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(2)
        return self.driver.find_elements(By.CLASS_NAME, "position-list-item")

    def click_view_role(self):
        wait = WebDriverWait(self.driver, 25)
        btn = wait.until(EC.presence_of_element_located(self.VIEW_ROLE_BTN))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(2)
        self.driver.execute_script("arguments[0].click();", btn)