<a href="README.md">
  <img src="https://img.shields.io/badge/Language-English-blue?style=flat-square&logo=google-translate&logoColor=white" alt="English">
</a>
<a href="README-TR.md">
  <img src="https://img.shields.io/badge/Dil-Türkçe-red?style=flat-square&logo=google-translate&logoColor=white" alt="Türkçe">
</a>

  <br />
  <br />

<div align="center">
  <img src="logo.png" width="120" height="120">
  <br />
  <br />

  <p>
    Windows için şık, hafif ve basit bir klasör koruma aracı.
  </p>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

  <p>
    <a href="#features">Özellikler</a> •
    <a href="#installation">Kurulum</a> •
    <a href="#usage">Kullanım</a> •
    <a href="#configuration">Yapılandırma</a> •
    <a href="#license">Lisans</a> 
  </p>

  <br />
  <br />
</div>

## 📋 Hakkında

**Aether Guard**, Windows için şık, modern ve hafif bir klasör koruma aracıdır. Aktif Windows Gezgini (Windows Explorer) pencerelerini izleyerek ve bunlara erişmek için şifre doğrulaması gerektirerek ek bir güvenlik katmanı sağlar.

<img src="md/20260312140807256.jpg" width="auto" />

## ✨ Özellikler <a id="features"></a>

- **Gerçek Zamanlı Koruma**: Windows Gezgini'ni (Windows Explorer) aktif olarak izler ve yetkisiz pencereleri anında kapatır.
- **Kaba Kuvvet Koruması**: Başarısız denemelerden sonra üstel bekleme süresi (exponential backoff) uygulayan gelişmiş bir oran sınırlama sistemi.
- **Oturum İzin Süresi**: Erişim anahtarınızı tekrar girmek zorunda kalmadan yapılandırılabilir bir süre boyunca (varsayılan: 5 dakika) doğrulanmış kalmanızı sağlar.
- **Tekil Örnek Zorunluluğu**: Gereksiz süreçleri önlemek için uygulamanın halihazırda çalışıp çalışmadığını otomatik olarak algılar.
- **Gizli Çalışma**: Görünür bir konsol penceresi olmadan çalışması için VBS başlangıç desteği sağlar.

## 🚀 Kurulum <a id="installation"></a>

### Gereksinimler

- **OS**: Windows 10/11 (Windows API entegrasyonu için gereklidir)
- **Python**: Sürüm 3.8 veya üzeri

### Kurulum

1.  **Depoyu Klonlayın**:

    ```bash
    git clone https://github.com/xkintaro/aether-guard.git
    cd aether-guard
    ```

2. **Bağımlılıkları yükleyin:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Uygulamayı çalıştırın:**

   ```bash
   python app.py
   ```

## ⚒️ Kullanım <a id="usage"></a>

1.  **Uygulamayı Başlatın**:
    - Konsola bağlı bir oturum için `run.bat` dosyasını çalıştırın.
    - Arka planda başlatmak için `run-aether-guard.vbs` dosyasını çalıştırın.
2.  **Kimlik Doğrulama**:
    - **Varsayılan Şifre**: `1234`
    - Bir klasörü açmaya çalıştığınızda, modern bir arayüz (UI) erişim anahtarınızı isteyecektir.
3.  **Kapatmak İçin**:
    - Konsolda çalışıyorsa `Ctrl+C` tuşlarına basın.
    - Aksi takdirde, Görev Yöneticisi (Task Manager) aracılığıyla işlemi sonlandırın.

## ⚙️ Yapılandırma <a id="configuration"></a>

`Config` sınıfı ayarlarını değiştirmek için `app.py` dosyasını açın:

```python
class Config:
    DEFAULT_PASSWORD = "1234"    # Ana erişim şifreniz (master access key)
    MAX_ATTEMPTS = 5             # Kilitlenmeden önce izin verilen deneme sayısı
    LOCKOUT_TIME = 60            # Saniye cinsinden ilk kilitlenme süresi
    GRACE_PERIOD = 300           # Yetkilendirilmiş oturum süresi (5 dakika)
```

## 📄 Lisans <a id="license"></a>

Bu proje MIT Lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasını kontrol edebilirsiniz.

#

<p align="center">
  <sub>❤️ Developed by "Mustafa TAŞAL" (kintaro)</sub>
</p>