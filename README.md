# 🎓 Veritabanı Yönetim Sistemleri (VTYS) Final Hazırlık Simülatörü

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/database-SQLite-green.svg)](https://www.sqlite.org/)
[![CLI](https://img.shields.io/badge/interface-Rich--CLI-magenta.svg)](https://github.com/Textualize/rich)
[![License](https://img.shields.io/badge/license-emirberasoguk-yellow.svg)](#-lisanslama-ve-doğrulama)

Bu proje, üniversitelerin Bilgisayar Mühendisliği bölümlerinde okutulan **Veritabanı Yönetim Sistemleri (VTYS)** dersinin final sınavlarına interaktif ve uygulamalı bir şekilde hazırlanmak için geliştirilmiş eğlenceli bir konsol (CLI) uygulamasıdır.

Uygulama, geçmiş yıllarda çıkmış sınav soruları ve ders müfredatı (ER Modeli, İlişkisel Cebir, SQL, Normalizasyon, İndeksleme ve Transactions) temel alınarak geliştirilmiştir.

---

## 🚀 Özellikler

Uygulama şu anda 6 ana bölümden oluşmaktadır:

1. **💻 Canlı SQL Prompt:** Serbest denemeler yapabileceğiniz, çok satırlı SQL sorgularını destekleyen ve sonuçları tablo halinde basan SQLite terminali.
2. **📊 Tabloları ve Şemaları İnceleme:** Sınav senaryolarında kullanılan veritabanı şemalarını (Sailors/Boats, Student/Enrolled) ve örnek kayıtları canlı inceleme alanı.
3. **🔬 Uygulamalı VTYS Laboratuvarları (9 Adet):**
   * ER modelden zayıf varlık şeması oluşturma (DDL).
   * Kapanış kümesi ($X^+$) hesaplama simülasyonu.
   * Çakışma grafiği (Precedence Graph) üzerinden eşzamanlılık analizi.
   * Canlı indeks performansı ve hız karşılaştırma testi (Table Scan vs. Index Lookup).
   * İlişkisel cebir ifadelerini SQL'e dönüştürme.
   * ALTER TABLE ve CREATE INDEX DDL testleri.
   * **BCNF Ayrıştırma (Decomposition) İzleme Labı.**
   * **Dış Bellek Sıralama (External Merge Sort) Maliyeti Hesaplama Labı.**
4. **✍️ Teorik Test Simülatörü:** Sınavda çıkmış veya çıkabilecek konulardan derlenmiş **20 soruluk** çoktan seçmeli interaktif test.
5. **📝 SQL Sınav Soruları Simülatörü:** Geçmiş sınavlarda sorulan 10 zorlu SQL sorgusunu çözüp doğruluğunu otomatik kontrol edebileceğiniz test alanı.
6. **📚 VTYS Ders Özetleri:** Sınav öncesi hızlıca göz atabileceğiniz formüllerle desteklenmiş konu özetleri.

---

## 🛠️ Kurulum ve Çalıştırma

### Gereksinimler
Uygulamanın zengin terminal grafiklerini (Rich) düzgün gösterebilmesi için sisteminizde Python ve `rich` kütüphanesinin kurulu olması gerekmektedir.

```bash
pip install rich
```

### Çalıştırma
Projeyi klonladıktan veya indirdikten sonra terminal üzerinden şu komutla çalıştırabilirsiniz:

```bash
python sql_pratik.py
```

---

## 🔒 Lisanslama ve Doğrulama

Bu yazılım **emirberasoguk** lisans koruması altındadır. Yazılımın çalışabilmesi için başlangıçta karşınıza çıkan esprili doğrulama panelini onaylamanız veya geliştiriciye bir bardak çay ısmarlamanız gerekmektedir. 😉

---

## 👨‍💻 Geliştirici
Geliştiren: **[emirberasoguk](https://github.com/emirberasoguk)**

*Sınavlarınızda başarılar dilerim!*
