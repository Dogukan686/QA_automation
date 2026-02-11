Bu proje, Insider kariyer sayfasındaki Quality Assurance ilanlarını otomatik olarak filtreleyen, doğrulayan ve sonuçları profesyonel bir raporlama sistemiyle sunan bir Selenium Webdriver otomasyon projesidir.

🛠 Kullanılan Teknolojiler
Dil: Python 3.12+

Test Framework: Pytest

Web Otomasyon: Selenium WebDriver

Raporlama: Allure Report

Tasarım Deseni: Page Object Model (POM)

Sürüm Kontrol: Git & GitHub

✨ Öne Çıkan Özellikler
POM Mimarisi: Kodun sürdürülebilirliği ve okunabilirliği için Page Object Model yapısı kullanılmıştır.

Dinamik Filtreleme: Insider sitesindeki karmaşık Select2 dropdown yapıları, JavaScript Executor ve Explicit Wait kombinasyonu ile stabilize edilmiştir.

Hata Anı Ekran Görüntüsü (Screenshot on Failure): Test fail ettiğinde, conftest.py içerisindeki hook sayesinde otomatik olarak o anın ekran görüntüsünü alıp Allure raporuna ekler.

Esnek Locator Stratejisi: Lokasyon ve departman isimlerindeki karakter farklarını (Turkey/Turkiye) tolore eden esnek XPath'ler kullanılmıştır.

📁 Proje Yapısı

QA_automation/

├── pages/                  # Sayfa Nesneleri (POM)

│   ├── base_page.py        # Temel metodlar (wait, click, find)

│   └── qa_page.py          # QA sayfasına özel elementler ve aksiyonlar

├── tests/                  # Test Senaryoları

│   └── test_insider_qa.py  # Ana test akışı

├── allure-results/         # Test sonrası oluşan ham veriler (Git'e gönderilmez)

├── allure-report/          # Görselleştirilmiş HTML raporu

├── conftest.py             # Pytest fixture'ları ve Allure screenshot hook'u

├── requirements.txt        # Gerekli kütüphaneler listesi

└── .gitignore              # Takip edilmeyecek dosyalar (venv, pycache vb.)

🚀 Kurulum ve Çalıştırma

git clone https://github.com/Dogukan686/QA_automation.git

cd QA_automation

2. Sanal Ortamı Kurun ve Aktif Edin

python -m venv venv

venv\Scripts\activate  # Windows

3. Bağımlılıkları Yükleyin

pip install -r requirements.txt

4. Testleri Koşturun

python -m pytest tests/test_insider_qa.py --alluredir=allure-results

5. Raporu Oluşturun ve Açın

allure generate allure-results --clean -o allure-report

allure open allure-report

