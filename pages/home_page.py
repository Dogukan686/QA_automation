from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HomePage(BasePage):
    URL = "https://useinsider.com/"
    
    # --- Güncellenmiş Locatorlar ---
    # ID yerine daha genel olan 'nav' etiketini veya Logo'yu kullanıyoruz
    NAV_BAR = (By.CSS_SELECTOR, "nav")  # Genel navigasyon barı
    MAIN_LOGO = (By.CSS_SELECTOR, "a.navbar-brand") # Sol üstteki Insider logosu
    COOKIE_ACCEPT = (By.ID, "wt-cli-accept-all-btn")

    def open_home(self):
        self.open_url(self.URL)
        self.accept_cookies()

    def accept_cookies(self):
        try:
            # Çerez butonu için 5 saniye bekle, çıkmazsa devam et
            self.wait_for_clickable(self.COOKIE_ACCEPT).click()
        except:
            pass 

    def is_loaded(self):
        # Sayfanın yüklendiğini anlamak için Logo veya Navigasyonun görünür olması yeterli
        return self.find(self.NAV_BAR).is_displayed() or \
               self.find(self.MAIN_LOGO).is_displayed()