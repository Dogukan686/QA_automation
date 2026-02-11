from selenium.webdriver.common.by import By
from .base_page import BasePage

class HomePage(BasePage):
    URL = "https://insiderone.com/"
    # Optimize edilmiş CSS/Xpath seçiciler
    NAVBAR = (By.ID, "navigation")
    SLIDER = (By.CSS_SELECTOR, ".home-hero-slider")

    def open(self):
        self.driver.get(self.URL)

    def is_opened(self):
        # Ana blokların yüklendiğini kontrol eder.
        return self.find_element(self.NAVBAR).is_displayed() 