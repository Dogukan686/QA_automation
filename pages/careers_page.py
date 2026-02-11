from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import BasePage
import time

class CareersPage(BasePage):
    QA_URL = "https://useinsider.com/careers/quality-assurance/"
    
    # --- Locators ---
    SEE_ALL_JOBS_BTN = (By.XPATH, "//a[contains(text(), 'See all QA jobs')]")
    
    # Seçenekler
    ISTANBUL_OPTION = (By.XPATH, "//li[contains(@class, 'select2-results__option') and contains(text(), 'Istanbul')]")
    
    # İlan Listesi
    JOB_LIST_SECTION = (By.ID, "jobs-list")
    JOB_CARD = (By.CLASS_NAME, "position-list-item")
    
    # İlan Kartı Detayları
    POSITION_TITLE = (By.CLASS_NAME, "position-title")
    POSITION_DEPT = (By.CLASS_NAME, "position-department")
    POSITION_LOC = (By.CLASS_NAME, "position-location")
    VIEW_ROLE_BTN = (By.XPATH, ".//a[contains(text(), 'View Role')]")

    def load_qa_page(self):
        self.open_url(self.QA_URL)
        try:
            cookie_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "wt-cli-accept-all-btn")))
            cookie_btn.click()
        except:
            pass

    def click_see_all_jobs(self):
        self.js_click(self.SEE_ALL_JOBS_BTN)
        print("   -> 'See all QA jobs' butonuna tıklandı...")
        try:
            self.wait.until(EC.url_contains("open-positions"))
            print("   -> Sayfa geçişi başarılı.")
        except:
            print("   ⚠️ URL değişmedi, manuel yönlendirme yapılıyor.")
            self.open_url("https://useinsider.com/careers/open-positions/?department=qualityassurance")
        
        time.sleep(5)

    def filter_jobs(self):
        print("   -> Filtreleme adımı başlıyor...")
        self.driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(3)
        
        # 1. Lokasyon Filtresini Bul
        try:
            containers = self.find_all((By.CSS_SELECTOR, ".select2-container--default"))
            loc_container = None
            for container in containers:
                if not container.is_displayed(): continue
                loc_container = container
                break 
            
            if not loc_container:
                loc_container = self.wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[contains(@class, 'select2-selection')])[1]")))

            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", loc_container)
            time.sleep(1)
            loc_container.click()
            print("   -> Lokasyon menüsü açıldı.")
            time.sleep(1)

        except Exception as e:
            self.driver.save_screenshot("filter_not_found.png")
            raise Exception(f"❌ Lokasyon filtresi bulunamadı! Hata: {str(e)}")

        # 2. Seçeneği Seç (Klavye Yöntemi)
        try:
            actions = ActionChains(self.driver)
            actions.send_keys("Istanbul")
            time.sleep(1)
            actions.send_keys(Keys.ENTER)
            actions.perform()
            print("   -> Klavye ile 'Istanbul' yazılıp Enter'a basıldı.")
            
        except Exception as k_e:
            try:
                option = self.wait.until(EC.presence_of_element_located(self.ISTANBUL_OPTION))
                self.driver.execute_script("arguments[0].click();", option)
                print("   -> 'Istanbul' seçeneği JS ile tıklandı.")
            except:
                self.driver.save_screenshot("filter_fail.png")
                raise Exception(f"❌ Seçim yapılamadı! Hata: {str(k_e)}")
        
        time.sleep(3)

    def verify_jobs_list_present(self):
        return self.find(self.JOB_LIST_SECTION).is_displayed()

    def get_all_jobs(self):
        print("   -> İlanlar taranıyor...")
        self.driver.execute_script("window.scrollTo(0, 500);")
        time.sleep(2)
        
        end_time = time.time() + 15 
        jobs = []
        
        while time.time() < end_time:
            jobs = self.find_all(self.JOB_CARD)
            if len(jobs) > 0:
                print(f"   -> {len(jobs)} adet ilan tespit edildi.")
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", jobs[0])
                time.sleep(1)
                return jobs
            print("   -> Henüz ilan gelmedi, bekleniyor...")
            time.sleep(2)
            
        print("   ⚠️ UYARI: Süre doldu, ilan listesi boş!")
        self.driver.save_screenshot("no_jobs_found.png")
        return []

    def check_job_details(self, job_element):
        title = job_element.find_element(*self.POSITION_TITLE).text
        dept = job_element.find_element(*self.POSITION_DEPT).text
        loc = job_element.find_element(*self.POSITION_LOC).text
        return {"title": title, "department": dept, "location": loc}

    def click_first_job_view_role(self):
        first_job = self.find_all(self.JOB_CARD)[0]
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_job)
        time.sleep(1)
        btn = first_job.find_element(*self.VIEW_ROLE_BTN)
        self.driver.execute_script("arguments[0].click();", btn)