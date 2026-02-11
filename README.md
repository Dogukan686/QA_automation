# 🚀 Insider QA Automation Challenge

Bu proje, Insider kariyer sayfasının uçtan uca (E2E) test otomasyonunu içeren teknik bir çalışmadır. **Page Object Model (POM)** tasarım deseni kullanılarak, sürdürülebilir ve modüler bir yapıda geliştirilmiştir.

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Selenium](https://img.shields.io/badge/Selenium-WebDriver-43B02A?style=for-the-badge&logo=selenium)
![Pytest](https://img.shields.io/badge/Pytest-Framework-yellow?style=for-the-badge&logo=pytest)

## 🎯 Proje Özellikleri ve Teknik Detaylar

Bu otomasyon projesi, sadece "Happy Path" senaryolarını değil, gerçek dünya problemlerini (senkronizasyon, dinamik elementler) de yönetecek şekilde tasarlanmıştır.

* **Page Object Model (POM):** Sayfa elementleri ve test mantığı birbirinden ayrılarak kodun okunabilirliği ve bakımı kolaylaştırıldı.
* **Akıllı Bekleme (Smart Waits):** `time.sleep` yerine `WebDriverWait` ve `ExpectedConditions` kullanılarak senkronizasyon sorunları minimize edildi.
* **Hibrit Locator Stratejisi:** Dinamik olarak değişen elementler (örn: Select2 filtreleri) için ID, CSS ve XPath kombinasyonları kullanılarak "kırılganlık" önlendi.
* **İş Mantığı İstisnaları (Business Logic Handling):** İstanbul filtresinde listelenen "Berlin - Turkish Speaker" gibi istisnai ilanlar, test hatası olarak değil, iş kuralı olarak ele alındı.
* **Veri Doğrulama (Assertions):** İlanların Pozisyon, Departman ve Lokasyon ("Turkey" vs "Turkiye") bilgileri esnek doğrulama yöntemleriyle kontrol edildi.

## 📂 Proje Yapısı

```text
QA_automation/
├── pages/                  # Sayfa sınıfları (POM)
│   ├── base_page.py        # Ortak metodlar (Click, Scroll, Wait)
│   ├── home_page.py        # Ana sayfa işlemleri
│   └── careers_page.py     # QA Kariyer, Filtreleme ve İlan kontrolleri
├── tests/                  # Test senaryoları
│   └── test_insider_flow.py
├── conftest.py             # Pytest driver konfigürasyonu (Fixture)
├── requirements.txt        # Proje bağımlılıkları
└── README.md               # Proje dokümantasyonu


✅ Test Senaryosu (Workflow)
Test test_insider_flow.py dosyası üzerinden şu adımları izler:

Ana Sayfa: Insider ana sayfasına gidilir ve navbar veya logo kontrolü ile sayfanın yüklendiği doğrulanır.

Kariyer Sayfası: QA kariyer sayfasına gidilir, çerezler (varsa) kapatılır.

İlanları Görüntüleme: "See all QA jobs" butonuna tıklanır.

Fail-Safe: Eğer buton çalışmazsa, URL kontrolü yapılıp manuel yönlendirme devreye girer.

Filtreleme:

Lokasyon filtresi dinamik olarak bulunur.

Listeden veya klavye simülasyonu ile "Istanbul" seçilir.

İlan Kontrolü:

Listelenen ilanların yüklenmesi beklenir.

Her ilanın "Quality Assurance" veya "QA" içerdiği doğrulanır.

Her ilanın "Istanbul, Turkey" veya "Istanbul, Turkiye" lokasyonuna sahip olduğu doğrulanır.

Başvuru Yönlendirmesi: "View Role" butonuna tıklanarak kullanıcının lever.co başvuru formuna yönlendirildiği doğrulanır.

🛠️ Kurulum ve Çalıştırma
Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin:

1. Repoyu Klonlayın

git clone [https://github.com/KULLANICI_ADINIZ/QA_automation.git](https://github.com/KULLANICI_ADINIZ/QA_automation.git)
cd QA_automation

2. Sanal Ortamı Kurun (Önerilen)

# Windows için
python -m venv venv
venv\Scripts\activate

# Mac/Linux için
python3 -m venv venv
source venv/bin/activate
3. Bağımlılıkları Yükleyin

pip install -r requirements.txt

4. Testi Çalıştırın

Test sonuçlarını ve logları konsolda görmek için -s parametresini kullanın:

python -m pytest tests/test_insider_flow.py -s

📊 Raporlama (Allure)
Eğer Allure yüklü ise, detaylı HTML raporu oluşturabilirsiniz:

# Testi raporla çalıştır
python -m pytest tests/test_insider_flow.py --alluredir=allure-results

# Raporu görüntüle
allure serve allure-results

📊 Canlı Test Raporu
Projenin her push işleminden sonra otomatik olarak koşan test sonuçlarına ve ekran görüntülerine aşağıdaki linkten ulaşabilirsiniz:https://Dogukan686.github.io/QA_automation/
