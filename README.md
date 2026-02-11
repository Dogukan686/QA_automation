# 🚀QA Test Otomasyon Projesi

Bu proje, Insider web sitesinin kariyer sayfasındaki Quality Assurance (QA) iş ilanlarını filtrelemek ve doğrulamak amacıyla hazırlanmıştır. 

Proje, **Python**, **Selenium WebDriver** ve **Pytest** kullanılarak **Page Object Model (POM)** tasarım desenine uygun şekilde geliştirilmiştir.

---

## 🛠 Kullanılan Teknolojiler

* **Dil:** Python 3.12+
* **Test Framework:** Pytest
* **Tarayıcı Otomasyonu:** Selenium WebDriver
* **Tasarım Deseni:** Page Object Model (POM) - *Kodun okunabilirliğini ve bakımını kolaylaştırmak için.*
* **Raporlama:** Pytest standart çıktıları

---

## 📂 Proje Yapısı

Dosyalar, sürdürülebilirliği sağlamak amacıyla modüler bir yapıda organize edilmiştir:

```text
QA_automation/
│
├── pages/                  # Sayfa Elementleri ve Metodları (POM)
│   ├── __init__.py
│   ├── base_page.py        # Tüm sayfalar için ortak metodlar (Click, Find vb.)
│   ├── home_page.py        # Ana sayfa işlemleri
│   └── qa_page.py          # QA kariyer sayfası ve filtreleme işlemleri
│
├── tests/                  # Test Senaryoları
│   ├── __init__.py
│   └── test_insider_qa.py  # Ana test dosyamız
│
├── conftest.py             # WebDriver ayarları (Fixture)
├── requirements.txt        # Gerekli kütüphaneler listesi
└── README.md               # Proje dokümantasyonu

⚙️ Kurulum (Adım Adım)
Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyebilirsiniz.

1. Projeyi İndirin
Projeyi bilgisayarınıza klonlayın veya zip olarak indirip bir klasöre çıkarın.

2. Sanal Ortamı (Virtual Environment) Kurun
Terminali proje klasöründe açın ve şu komutları sırasıyla uygulayın:

Windows için:
python -m venv venv
venv\Scripts\activate

Mac/Linux için:
python3 -m venv venv
source venv/bin/activate

3. Gerekli Kütüphaneleri Yükleyin
pip install -r requirements.txt

▶️ Testi Çalıştırma
Kurulum tamamlandıktan sonra testi başlatmak için terminale şu komutu yazın:
python -m pytest tests/test_insider_qa.py
Daha detaylı çıktı görmek isterseniz: python -m pytest -v tests/test_insider_qa.py

✅ Test Senaryosu
Otomasyon kodu şu adımları otomatik olarak gerçekleştirir:

https://insiderone.com/ adresine gider ve ana sayfanın açıldığını doğrular.

"Careers" menüsünden QA ilanları sayfasına ulaşır.

Lokasyon: "Istanbul, Turkey" ve Departman: "Quality Assurance" filtrelerini uygular

Listelenen ilanların pozisyon, departman ve lokasyon bilgilerinin doğruluğunu kontrol eder.

"View Role" butonuna tıklar ve başvuru sayfasına (Lever/LinkedIn) yönlendirildiğini teyit eder.

⚠️ Önemli Notlar & Teknik Kararlar
Canlı web sitesindeki dinamik değişikliklere uyum sağlamak için kodda bazı esneklikler yapılmıştır:

Lokasyon Filtresi: Web sitesinde ülke ismi bazen "Turkey", bazen "Turkiye" olarak geçtiği için; veya filtreleme sorunu yaşandığında sadece "Istanbul" yazdığı için test kodu "Istanbul", "Turkey" ve "Turkiye" varyasyonlarının hepsini kabul edecek şekilde tasarlanmıştır.

İş İlanı Başlıkları: İlan başlıkları "Quality Assurance", "Quality Engineering" veya "QA" olarak değişebilmektedir. Testin yanlış pozitif vermemesi (flaky olmaması) için bu terimlerin hepsi geçerli kabul edilmiştir.

Seçiciler (Selectors): Element ID'leri dinamik olarak değiştiği için (Select2 yapısı), daha kararlı olan XPath ve Text-Based seçim yöntemleri tercih edilmiştir. 

Raporlama: Test sonuçları Allure ile görselleştirilebilir, hata durumunda ekran görüntüleri rapora eklenebilir.
