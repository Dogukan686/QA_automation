import pytest
from pages.home_page import HomePage
from pages.qa_page import QAPage
import time

def test_insider_qa_flow(driver):
    """
    Insider QA İş Akışı Otomasyon Testi
    - Ana sayfa, QA sayfası ve filtreleme kontrollerini yapar.
    - Berlin gibi filtre dışı ilanların sızmasını engeller.
    """
    home = HomePage(driver)
    qa = QAPage(driver)

    # 1. Ana sayfayı aç ve kontrol et
    home.open()
    assert home.is_opened(), "❌ HATA: Ana sayfa navigasyon barı görünür değil!"

    # 2. QA ilanlarına git ve filtreleri uygula
    # Not: 'qa.filter_jobs' içerisinde JavaScript click ve bekleme (sleep) olmalı.
    qa.open_qa_jobs()
    qa.filter_jobs()
    
    # 3. Liste görünürlüğünü doğrula
    assert qa.verify_jobs_list(), "❌ HATA: Filtreleme sonrası iş listesi yüklenemedi!"

    # 4. Tüm ilan kartlarını al ve tek tek doğrula
    job_cards = qa.get_all_jobs_data()
    assert len(job_cards) > 0, "❌ HATA: Filtreleme kriterlerine uygun hiç ilan bulunamadı!"

    print(f"\n--- {len(job_cards)} İlan Kontrol Ediliyor ---")

    for card in job_cards:
        # İlan verilerini çek
        title = card.find_element(*qa.POSITION_TITLE).text
        location = card.find_element(*qa.LOCATION_TEXT).text
        
        print(f"İnceleme: {title} | Lokasyon: {location}")

        # ✅ Başlık Doğrulaması (QA ile ilgili olmalı)
        qa_keywords = ["Quality Assurance", "Quality Engineering", "QA", "Tester"]
        is_qa_role = any(kw in title for kw in qa_keywords)
        assert is_qa_role, f"❌ HATA: İlan başlığı QA kriterlerine uymuyor: {title}"

        # ✅ Lokasyon Doğrulaması (Berlin sızıntısını burada kesiyoruz)
        # Sadece Istanbul veya Remote içerenleri kabul et, geri kalanında testi patlat.
        is_valid_location = "Istanbul" in location or "Remote" in location
        assert is_valid_location, f"❌ HATA: Filtre dışı lokasyon bulundu: {location} (İlan: {title})"

    # 5. 'View Role' butonuna tıkla ve yönlendirmeyi kontrol et
    qa.click_view_role()
    
    # Yeni sekmeye geçiş yap (Eğer açıldıysa)
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[-1])
    
    # Sayfanın yüklenmesi için kısa bir süre bekle
    time.sleep(3)
    
    # 6. Yönlendirilen sayfanın Lever veya ilgili başvuru platformu olduğunu doğrula
    current_url = driver.current_url
    print(f"Yönlendirilen URL: {current_url}")
    
    valid_urls = ["lever.co", "jobs", "linkedin", "insider"]
    is_url_correct = any(site in current_url.lower() for site in valid_urls)
    assert is_url_correct, f"❌ HATA: Yanlış başvuru sayfasına yönlendirildi: {current_url}"

    print("✅ TEST BAŞARIYLA TAMAMLANDI: Tüm kriterler sağlandı.")