#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import sqlite3
import random
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm

console = Console()

DB_PATH = "kiralama.db"

def check_license():
    """emirberasoguk lisans kontrolü geyiği."""
    os.system("clear")
    console.print(Panel(
        "[bold red]⚠️ LİSANS UYARISI / LICENSE VERIFICATION[/bold red]\n\n"
        "Bu yazılım [bold yellow]emirberasoguk[/bold yellow] lisanslama sistemi altındadır.\n"
        "Uygulamayı kullanabilmek için lütfen aşağıdaki IBAN adresine en az 5 TL (veya bir çay bedeli) gönderin:\n\n"
        "[bold green]IBAN: TR00 0000 0000 0000 0000 0000 00[/bold green] (emirberasoguk)\n\n"
        "[dim]Not: Arkadaş ortamında çay ısmarlanarak da lisans aktif edilebilir.[/dim]",
        border_style="red"
    ))
    
    while True:
        cevap = Prompt.ask("\nÖdemeyi yaptınız mı veya çay ısmarladınız mı? (Evet: E / Hayır: H / Zaten Ödedim: Z)", choices=["E", "H", "Z"], default="H").upper()
        if cevap in ["E", "Z"]:
            with console.status("[bold yellow]Lisans sorgulanıyor...[/bold yellow]"):
                time.sleep(1.5)
            console.print("[bold green]✓ Ödeme onaylandı! emirberasoguk lisansı başarıyla aktifleştirildi.[/bold green]")
            time.sleep(1)
            break
        else:
            console.print("[bold red]❌ Ödeme bulunamadı! emirberasoguk yazılımlarını bedavaya kullanamazsınız.[/bold red]")
            time.sleep(1.5)
            sys.exit(0)

def init_db():
    """Veritabanını oluşturur ve örnek verileri yükler."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Yabancı anahtar desteğini aktif et
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # 1. Denizci Tablosu
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS denizci (
        did INTEGER PRIMARY KEY,
        isim TEXT NOT NULL,
        yas INTEGER NOT NULL
    );
    """)
    
    # 2. Bot Tablosu
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bot (
        bid INTEGER PRIMARY KEY,
        renk TEXT NOT NULL,
        kapasite INTEGER NOT NULL
    );
    """)
    
    # 3. Rezervasyon Tablosu
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rezervasyon (
        did INTEGER,
        bid INTEGER,
        tarih TEXT,
        PRIMARY KEY (did, bid, tarih),
        FOREIGN KEY (did) REFERENCES denizci(did) ON DELETE CASCADE,
        FOREIGN KEY (bid) REFERENCES bot(bid) ON DELETE CASCADE
    );
    """)
    
    # 4. Student Tablosu
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student (
        sid INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        login TEXT NOT NULL,
        age INTEGER NOT NULL,
        gpa REAL NOT NULL
    );
    """)
    
    # 5. Enrolled Tablosu
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS enrolled (
        sid INTEGER,
        cid TEXT,
        grade TEXT,
        PRIMARY KEY (sid, cid, grade),
        FOREIGN KEY (sid) REFERENCES student(sid) ON DELETE CASCADE
    );
    """)
    
    # Verileri dolduralım (Sadece tablolar boşsa ekle)
    cursor.execute("SELECT COUNT(*) FROM denizci")
    if cursor.fetchone()[0] == 0:
        denizciler = [
            (22, 'Dustin', 45),
            (29, 'Brutus', 33),
            (31, 'Lubber', 55),
            (32, 'Andy', 25),
            (58, 'Rusty', 35),
            (64, 'Horatio', 35),
            (71, 'Zorba', 16),
            (74, 'Horatio', 35),
            (85, 'Art', 25),
            (95, 'Bob', 63)
        ]
        cursor.executemany("INSERT INTO denizci VALUES (?, ?, ?)", denizciler)

    cursor.execute("SELECT COUNT(*) FROM bot")
    if cursor.fetchone()[0] == 0:
        botlar = [
            (101, 'mavi', 8),
            (102, 'kırmızı', 10),
            (103, 'yeşil', 12),
            (104, 'mavi', 6),
            (105, 'sarı', 15)
        ]
        cursor.executemany("INSERT INTO bot VALUES (?, ?, ?)", botlar)

    cursor.execute("SELECT COUNT(*) FROM rezervasyon")
    if cursor.fetchone()[0] == 0:
        rezervasyonlar = [
            (22, 101, '2026-05-01'),
            (22, 102, '2026-05-02'),
            (22, 103, '2026-05-03'),
            (22, 104, '2026-05-04'),
            (31, 102, '2026-05-05'),
            (31, 104, '2026-05-06'),
            (64, 101, '2026-05-07'),
            (64, 102, '2026-05-08'),
            (74, 103, '2026-05-09'),
            (58, 101, '2026-05-10'),
            (58, 104, '2026-05-11'),
            (71, 105, '2026-05-12')
        ]
        cursor.executemany("INSERT INTO rezervasyon VALUES (?, ?, ?)", rezervasyonlar)

    cursor.execute("SELECT COUNT(*) FROM student")
    if cursor.fetchone()[0] == 0:
        students = [
            (53666, 'Kayne', 'A@cs', 28, 4.0),
            (53655, 'Tupac', 'B@cs', 26, 3.5),
            (53688, 'Bieber', 'C@cs', 22, 3.9)
        ]
        cursor.executemany("INSERT INTO student VALUES (?, ?, ?, ?, ?)", students)

    cursor.execute("SELECT COUNT(*) FROM enrolled")
    if cursor.fetchone()[0] == 0:
        enrolleds = [
            (53666, '15-415', 'C'),
            (53688, '15-721', 'A'),
            (53688, '15-826', 'B'),
            (53655, '15-415', 'C'),
            (53666, '15-721', 'C')
        ]
        cursor.executemany("INSERT INTO enrolled VALUES (?, ?, ?)", enrolleds)

    conn.commit()
    conn.close()

# SQL Soru Bankası (10 Soru - Genişletilmiş Kapsam)
SORULAR = [
    {
        "id": 1,
        "baslik": "Hiç bot kiralamamış denizciler",
        "aciklama": "Rezervasyon tablosunda kaydı bulunmayan (hiç bot kiralamamış) denizcilerin 'isim' bilgilerini getiren sorguyu yazınız.",
        "ipucu": "NOT EXISTS veya NOT IN kullanarak çözebilirsiniz.",
        "dogru_sorgu": "SELECT isim FROM denizci d WHERE NOT EXISTS(SELECT * FROM rezervasyon r WHERE r.did = d.did);"
    },
    {
        "id": 2,
        "baslik": "Tüm mavi botları kiralayan denizciler (Division)",
        "aciklama": "Rengi 'mavi' olan tüm botları kiralamış olan denizcilerin 'isim' bilgilerini bulunuz.",
        "ipucu": "Çift NOT EXISTS (Division mantığı) kullanmalısınız: 'Öyle bir denizci d bul ki, mavi olup da d tarafından kiralanmamış hiçbir bot olmasın.'",
        "dogru_sorgu": "SELECT isim FROM denizci d WHERE NOT EXISTS(SELECT bid FROM bot WHERE renk = 'mavi' and bid NOT IN (SELECT bid FROM rezervasyon r WHERE r.did = d.did));"
    },
    {
        "id": 3,
        "baslik": "Hiç mavi bot kiralamamış denizciler",
        "aciklama": "Mavi renkteki botlardan hiçbirini kiralamamış olan denizcilerin 'isim' bilgilerini listeleyen sorguyu yazınız. (Hiç kiralama yapmamış olanlar da dahildir!)",
        "ipucu": "Alt sorguda mavi botları kiralayan did'leri bulup ana sorguda NOT IN ile eleyebilir veya NOT EXISTS kullanabilirsiniz.",
        "dogru_sorgu": "SELECT isim FROM denizci d WHERE NOT EXISTS(SELECT r.bid FROM rezervasyon r WHERE r.did = d.did and r.bid IN (SELECT bid FROM bot WHERE renk = 'mavi'));"
    },
    {
        "id": 4,
        "baslik": "Sadece mavi bot kiralayan denizciler",
        "aciklama": "Kiraladığı tüm botlar mavi olan ve en az bir kiralama yapmış olan denizcilerin 'isim' bilgilerini bulunuz.",
        "ipucu": "Denizcinin kiraladığı botlar arasında mavi olmayan bir bot bulunmamalıdır ve denizci rezervasyon tablosunda yer almalıdır.",
        "dogru_sorgu": "SELECT isim FROM denizci d WHERE NOT EXISTS(SELECT bid FROM rezervasyon r WHERE d.did = r.did and r.bid NOT IN (SELECT bid FROM bot WHERE renk = 'mavi')) and d.did IN (SELECT did FROM rezervasyon);"
    },
    {
        "id": 5,
        "baslik": "Birden fazla ders alan benzersiz öğrenciler",
        "aciklama": "enrolled tablosundan birden fazla ders (cid) almış olan öğrencilerin benzersiz 'sid' (Öğrenci No) bilgilerini getiren sorguyu yazınız.",
        "ipucu": "Aynı sid'e sahip fakat cid'leri farklı olan iki enrolled satırını eşlemek için self-join yapabilir veya GROUP BY ... HAVING COUNT(...) > 1 kullanabilirsiniz.",
        "dogru_sorgu": "SELECT DISTINCT e1.sid FROM enrolled AS e1, enrolled AS e2 WHERE e1.sid = e2.sid AND e1.cid != e2.cid;"
    },
    {
        "id": 6,
        "baslik": "Ders Bazlı Kayıt Sayısı ve Başarı Ortalaması (GROUP BY & HAVING)",
        "aciklama": "Her derse (cid) kayıtlı olan öğrencilerin sayısını (COUNT) ve bu öğrencilerin genel GPA ortalamalarını (AVG) listeleyiniz. Yalnızca kayıtlı öğrenci sayısı 1'den büyük olan dersleri raporlayınız.",
        "ipucu": "enrolled ile student tablolarını JOIN edip cid'ye göre gruplamanız ve HAVING kısıtı eklemeniz gerekir.",
        "dogru_sorgu": "SELECT e.cid, COUNT(DISTINCT e.sid), AVG(s.gpa) FROM enrolled e JOIN student s ON e.sid = s.sid GROUP BY e.cid HAVING COUNT(DISTINCT e.sid) > 1;"
    },
    {
        "id": 7,
        "baslik": "Öğrenciler ve Dersleri (LEFT OUTER JOIN)",
        "aciklama": "Sistemdeki TÜM öğrencilerin isimlerini (name) ve kayıtlı oldukları derslerin kodlarını (cid) listeleyen sorguyu yazınız. Herhangi bir derse kaydolmamış öğrenciler de listede çıkmalı, ders kodları boş (NULL) görünmelidir.",
        "ipucu": "student tablosu sol taraf olacak şekilde enrolled tablosuna LEFT JOIN atmalısınız.",
        "dogru_sorgu": "SELECT s.name, e.cid FROM student s LEFT JOIN enrolled e ON s.sid = e.sid;"
    },
    {
        "id": 8,
        "baslik": "En Başarılı İlk İki Öğrenci (ORDER BY & LIMIT)",
        "aciklama": "Ortalaması (gpa) en yüksek olan ilk iki öğrencinin adını (name) ve gpa değerlerini, gpa değerlerine göre azalan (büyükten küçüğe) sırada listeleyiniz.",
        "ipucu": "Sorgunun sonuna ORDER BY ... DESC LIMIT ... eklemelisiniz.",
        "dogru_sorgu": "SELECT name, gpa FROM student ORDER BY gpa DESC LIMIT 2;"
    },
    {
        "id": 9,
        "baslik": "Ortalamanın Üzerindeki Öğrenciler (Alt Sorgu)",
        "aciklama": "Tüm öğrencilerin genel GPA ortalamasından daha yüksek GPA'e sahip öğrencilerin adını (name) ve gpa değerini listeleyiniz.",
        "ipucu": "WHERE gpa > (SELECT AVG(gpa) FROM student) alt sorgusunu kullanmalısınız.",
        "dogru_sorgu": "SELECT name, gpa FROM student WHERE gpa > (SELECT AVG(gpa) FROM student);"
    },
    {
        "id": 10,
        "baslik": "C Alan Öğrencilerin İsimleri (INNER JOIN)",
        "aciklama": "Derslerden 'C' notu (grade) alan öğrencilerin isimlerini (name), ders kodlarını (cid) ve notlarını (grade) listeleyen sorguyu yazınız.",
        "ipucu": "student ve enrolled tablolarını JOINleyip, grade = 'C' filtresini uygulamalısınız.",
        "dogru_sorgu": "SELECT s.name, e.cid, e.grade FROM student s JOIN enrolled e ON s.sid = e.sid WHERE e.grade = 'C';"
    }
]

# Teorik Çoktan Seçmeli Sorular (Genişletilmiş 20 Soru)
THEORY_QUESTIONS = [
    {
        "id": 1,
        "soru": "Bir ilişkisel cebir ifadesinde operatörün koşulları/alan isimleri ve işleme giren tablo isimleri sırasıyla nasıl yazılır?",
        "secenekler": [
            "a) alan isimleri parantez içinde, tablo isimleri alt simge olarak",
            "b) operatörler alt simge olarak, tablo isimleri üst simge olarak",
            "c) alan isimleri alt simge olarak, tablo isimleri parantez içinde",
            "d) tablo isimleri tırnak içinde, alan isimleri parantez içinde"
        ],
        "cevap": "c",
        "aciklama": "İlişkisel cebir gösteriminde seçim (σ) ve izdüşüm (π) gibi operatörlerin kriterleri/koşulları alt simge (subscript) olarak yazılırken, işleme giren ilişkiler/tablolar parantez içine yazılır. Örnek: σ_{yas > 20}(Student)"
    },
    {
        "id": 2,
        "soru": "Aşağıdaki SQL komutlarından hangisi ilişkisel cebirdeki izdüşüm (PROJECTION - π) operatörüne denk gelir?",
        "secenekler": [
            "a) WHERE",
            "b) SELECT",
            "c) FROM",
            "d) EXISTS"
        ],
        "cevap": "b",
        "aciklama": "İlişkisel cebirde İzdüşüm (Projection - π), bir tablodan sadece istenen sütunları (kolonları) almaya yarar. SQL dilindeki karşılığı SELECT ifadesidir."
    },
    {
        "id": 3,
        "soru": "Veritabanı tasarımında, hiçbir aday anahtarın (candidate key) parçası olmayan niteliklere (attributes) ne ad verilir?",
        "secenekler": [
            "a) non-key",
            "b) non-prime",
            "c) non-candidate",
            "d) non-super"
        ],
        "cevap": "b",
        "aciklama": "Aday anahtarlardan herhangi birinin parçası olan özniteliklere 'prime' (birincil) öznitelik, hiçbir aday anahtarın parçası olmayan özniteliklere ise 'non-prime' öznitelik denir."
    },
    {
        "id": 4,
        "soru": "Primary Key (Birincil Anahtar) ile ilgili aşağıda verilen ifadelerden hangisi doğrudur?",
        "secenekler": [
            "a) Null olamaz.",
            "b) Null olabilir.",
            "c) Aynı değeri birden fazla kayıt alabilir.",
            "d) Sadece sayısal değerler (integer, numeric) alabilir."
        ],
        "cevap": "a",
        "aciklama": "Birincil anahtar (Primary Key), bir tablodaki satırları benzersiz şekilde tanımlamalıdır. Bu yüzden benzersiz (unique) olmak zorundadır ve asla boş (NULL) değer alamaz."
    },
    {
        "id": 5,
        "soru": "R(a,b,c) ilişkisi üzerinde 'SELECT b FROM R WHERE c = 8' sorgusunun en hızlı şekilde çalıştırılması için hangi indeksleme yöntemi tercih edilmelidir?",
        "secenekler": [
            "a) b alanı üzerinde B+ tree indeks",
            "b) b alanı üzerinde hash indeks",
            "c) c alanı üzerinde hash indeks",
            "d) c alanı üzerinde B+ tree indeks"
        ],
        "cevap": "c",
        "aciklama": "Sorgu c alanında bir eşitlik araması ('c = 8') yapmaktadır. Eşitlik aramalarında Hash indeks en hızlısıdır ($O(1)$ maliyet). Arama c üzerinde yapıldığından indeks c kolonunda olmalıdır."
    },
    {
        "id": 6,
        "soru": "R(a,b,c) ilişkisi üzerinde 'SELECT b FROM R WHERE c > 8' aralık sorgusunun en hızlı çalıştırılması için hangi indeksleme yöntemi tercih edilmelidir?",
        "secenekler": [
            "a) b alanı üzerinde B+ tree indeks",
            "b) c alanı üzerinde hash indeks",
            "c) c alanı üzerinde B+ tree indeks",
            "d) Dosya araması (Table scan)"
        ],
        "cevap": "c",
        "aciklama": "Sorgu c alanında aralık araması ('c > 8') yapmaktadır. Hash indeks sıralama tutmadığı için aralık sorgularını desteklemez. B+ Tree indeks sıralı yaprakları sayesinde aralık sorgularında en hızlıdır."
    },
    {
        "id": 7,
        "soru": "Eşzamanlılık kontrolünde (Concurrency Control), farklı transaction'lara ait iki işlemin çakışması (conflict) için gereken koşullar nelerdir?",
        "secenekler": [
            "a) Aynı transaction'da olmalı, farklı verilere erişmeli, en az biri Write olmalı",
            "b) Farklı transaction'da olmalı, aynı veriye erişmeli, ikisi de Read olmalı",
            "c) Farklı transaction'da olmalı, aynı veriye erişmeli, en az biri Write olmalı",
            "d) Aynı transaction'da olmalı, aynı veriye erişmeli, ikisi de Write olmalı"
        ],
        "cevap": "c",
        "aciklama": "İki işlemin çakışması için: 1) Farklı transaction'lara ait olmalılar. 2) Aynı veri nesnesi (Örn: A değişkeni) üzerinde çalışmalılar. 3) En az biri yazma (Write) işlemi olmalıdır."
    },
    {
        "id": 8,
        "soru": "Aşağıda verilen işlemlerden hangileri ÇAKIŞMAZ (non-conflicting)?",
        "secenekler": [
            "a) R1(B) ve W2(B)",
            "b) W1(A) ve R2(A)",
            "c) R1(A) ve R2(B)",
            "d) W1(A) ve W2(A)"
        ],
        "cevap": "c",
        "aciklama": "R1(A) ve R2(B) işlemleri farklı veri nesnelerine (A ve B) eriştiğinden ve her ikisi de okuma (Read) işlemi olduğundan asla çakışmaz."
    },
    {
        "id": 9,
        "soru": "R(A,B,C) tablosunda (1,2,3), (4,2,3), (5,3,3) ve (2,4,4) kayıtları bulunmaktadır. Bu verilere göre hangi fonksiyonel bağımlılık GEÇERSİZDİR?",
        "secenekler": [
            "a) C -> B",
            "b) B -> C",
            "c) A -> B",
            "d) AC -> B"
        ],
        "cevap": "a",
        "aciklama": "C -> B bağımlılığında, aynı C değerine karşılık her zaman aynı B değeri gelmelidir. Verilere baktığımızda (1,2,3) ve (5,3,3) satırlarında C=3 olmasına rağmen B değerleri sırasıyla 2 ve 3'tür. Bu durum C -> B kuralını ihlal eder."
    },
    {
        "id": 10,
        "soru": "R(A,B,C,D) ilişkisinde F = {AB->C, AB->D, C->A, D->B} bağımlılıkları verilmiştir. Bu ilişkinin sağladığı en yüksek normal form nedir?",
        "secenekler": [
            "a) 1NF",
            "b) 2NF",
            "c) 3NF",
            "d) BCNF"
        ],
        "cevap": "c",
        "aciklama": "Aday anahtarlar AB, BC, AD, CD'dir. Bütün nitelikler (A,B,C,D) bir aday anahtarın parçası olduğundan hepsi 'prime' (birincil) niteliktir. BCNF kuralı C->A ve D->B için ihlal edilir (çünkü sol taraflar anahtar değildir). Ancak 3NF kuralı ('Y prime niteliktir') sağlandığı için en yüksek normal form 3NF'dir."
    },
    {
        "id": 11,
        "soru": "R(PQRS) ilişkisi F = {QR->S, R->P, S->Q} bağımlılıkları ile R1(PR) ve R2(QRS) şeklinde parçalanmıştır. Hangisi doğrudur?\n1) R1 ve R2 BCNF'dedir.\n2) Parçalanma kayıpsızdır (Lossless Join).",
        "secenekler": [
            "a) 1. Doğru, 2. Yanlış",
            "b) 1. Yanlış, 2. Doğru",
            "c) 1. Doğru, 2. Doğru",
            "d) 1. Yanlış, 2. Yanlış"
        ],
        "cevap": "b",
        "aciklama": "R1(PR) bağıntısı R->P içerir ve BCNF'dedir. Ancak R2(QRS) bağıntısı S->Q içerir ve S bir anahtar olmadığından R2 BCNF'de değildir. Bu yüzden 1. ifade yanlıştır. İki tablonun kesişimi {R} olup, R->P (yani R->R1) kuralı geçerli olduğundan birleşme kayıpsızdır. 2. ifade doğrudur."
    },
    {
        "id": 12,
        "soru": "R(ABCDE) ilişkisinde F = {AB->C, C->DE} bağımlılıkları geçerlidir. Aday anahtarlar DIŞINDA bu ilişkinin kaç süper anahtarı vardır?",
        "secenekler": [
            "a) 3",
            "b) 5",
            "c) 7",
            "d) 8"
        ],
        "cevap": "c",
        "aciklama": "Aday anahtar sadece AB'dir. Süper anahtarlar AB'yi içeren tüm nitelik kümeleridir. Bunlar {AB} birleşimiyle {C, D, E}'nin alt kümeleridir ($2^3 = 8$ adet). Aday anahtarlar çıkarıldığında ($8 - 1 = 7$) adet kalır."
    },
    {
        "id": 13,
        "soru": "R2(B),W2(B),R3(C),W3(C),R1(A),R1(B),W1(A),W1(B),R2(C),W2(C),R3(A),W3(A) işlemleri içeren plan için hangisi doğrudur?",
        "secenekler": [
            "a) Bu plan Conflict Serializable'dır.",
            "b) Bu plan Conflict Serializable DEĞİLDİR (Döngü içerir).",
            "c) Bu planda hiçbir çakışma (conflict) yoktur.",
            "d) Bu plan seri (serial) bir plandır."
        ],
        "cevap": "b",
        "aciklama": "Çakışma grafiği (Precedence Graph) çizildiğinde; A'dan T1 -> T3, B'den T2 -> T1 ve C'den T3 -> T2 kenarları oluşur. Grafikte T1 -> T3 -> T2 -> T1 şeklinde bir döngü (cycle) oluştuğundan plan Conflict Serializable değildir."
    },
    {
        "id": 14,
        "soru": "16, 4, 6, 22, 24, 10, 31, 7, 9, 20, 26 anahtarları kova boyutu (bucket capacity) 3 olan bir Extendible Hashing tablosuna LSB (en önemsiz bitler) sırasına göre eklendiğinde, son durumda global derinlik (g) ve '3' anahtarının yerleşeceği kovanın lokal derinliği (l) ne olur?",
        "secenekler": [
            "a) g = 2, l = 2",
            "b) g = 3, l = 2",
            "c) g = 3, l = 1",
            "d) g = 2, l = 1"
        ],
        "cevap": "c",
        "aciklama": "Trace edildiğinde global derinlik g=3 olur. '3' anahtarı ikilik tabanda ...011 olup, sonu 1 ile bitenlerin toplandığı kovaya gider. Tek sayılı kova hiç bölünmediğinden lokal derinliği l=1 olarak kalır."
    },
    {
        "id": 15,
        "soru": "SQL'de üç değerli mantıkta (Three-Valued Logic) aşağıdaki ifadelerden hangisi 'UNKNOWN' değerini döndürür?\n1) TRUE OR UNKNOWN\n2) FALSE AND UNKNOWN\n3) TRUE AND UNKNOWN\n4) NOT UNKNOWN",
        "secenekler": [
            "a) 1 ve 3",
            "b) 2 ve 4",
            "c) 3 ve 4",
            "d) Yalnızca 4"
        ],
        "cevap": "c",
        "aciklama": "SQL'de: 1) TRUE OR UNKNOWN = TRUE. 2) FALSE AND UNKNOWN = FALSE. 3) TRUE AND UNKNOWN = UNKNOWN. 4) NOT UNKNOWN = UNKNOWN. Dolayısıyla 3 ve 4 ifadeleri UNKNOWN döndürür."
    },
    {
        "id": 16,
        "soru": "Kördüğüm (Deadlock) önlemede kullanılan 'Wait-Die' ve 'Wound-Wait' politikalarıyla ilgili hangisi DOĞRUDUR?\nVarsayım: Ti transaction'ı Tj'nin kilitlediği bir veriyi istiyor. Ti, Tj'den daha eski (yüksek öncelikli).",
        "secenekler": [
            "a) Wait-Die'da Ti bekler; Wound-Wait'te Ti, Tj'yi iptal eder (wound).",
            "b) Wait-Die'da Ti iptal olur (die); Wound-Wait'te Ti bekler.",
            "c) Her iki yöntemde de Ti (eski olan) daima bekletilir.",
            "d) Wound-Wait'te Tj (yeni olan) Ti'yi yaralayarak abort ettirir."
        ],
        "cevap": "a",
        "aciklama": "Wait-Die (bekle veya öl): Eski işlem (Ti) yeni işlemi (Tj) bekler; yeni işlem eskiyi isterse ölür (iptal olur). Wound-Wait (yarala veya bekle): Eski işlem (Ti) kilidi isterse yeniyi (Tj) yaralar/iptal eder; yeni işlem eskiyi isterse bekler."
    },
    {
        "id": 17,
        "soru": "Sıralanacak dosya N = 10.000 sayfa ve kullanılabilir RAM tampon bellek boyutu B = 101 sayfa ise, Dış Bellek Sıralama (External Merge Sort) için Pass 0 sonrasında kaç run (sıralı parça) oluşur ve toplam kaç merge pass (birleştirme adımı) gerekir?",
        "secenekler": [
            "a) 100 run, 1 merge pass",
            "b) 100 run, 2 merge pass",
            "c) 99 run, 1 merge pass",
            "d) 101 run, 2 merge pass"
        ],
        "cevap": "a",
        "aciklama": "Pass 0'da run sayısı = ceil(N / B) = ceil(10000 / 101) = 100 run oluşur. Merge adımlarında B-1 = 100 run tek seferde birleştirilebilir. Merge pass sayısı = ceil(log_{B-1}(100)) = ceil(log_100(100)) = 1 merge pass sürer."
    },
    {
        "id": 18,
        "soru": "ER diyagramındaki bir ISA (Inheritance) yapısını ilişkisel şemaya dönüştürürken 'Single Table / Null Value Style' (Tek Tablo) yaklaşımıyla ilgili hangisi YANLIŞTIR?",
        "secenekler": [
            "a) Sadece alt sınıflara ait nitelikler tablolarda ayrı ayrı saklanır, üst sınıf tablosu oluşturulmaz.",
            "b) Tüm sınıflar tek bir tabloda birleştirilir ve alt sınıflara özel kolonlar NULL değer alabilir.",
            "c) Satırın hangi sınıfa ait olduğunu belirten bir ayırt edici (type discriminator) alan kullanılır.",
            "d) Bu yöntem boş alanlar nedeniyle diskte gereksiz yer kaplayabilir (NULL overhead)."
        ],
        "cevap": "a",
        "aciklama": "a seçeneği 'OO Style' (Nesne Yönelimli) şema dönüştürmeyi tanımlar. Tek Tablo (Single Table) modelinde üst sınıf ve tüm alt sınıflar tek bir tabloda tutulur, alt sınıfların kolonları NULL olabilir."
    },
    {
        "id": 19,
        "soru": "R(A,B,C,D,E) şemasında F = {A -> BC, CD -> E, B -> D} bağımlılıkları verilmiştir. Bu şemayı BCNF Decomposition algoritmasıyla ayrıştırmak istediğimizde, ilk adımda B -> D ihlali üzerinden ayrıştırırsak hangi iki alt şema elde edilir?",
        "secenekler": [
            "a) R1(B,D) ve R2(A,B,C,E)",
            "b) R1(A,B,C) ve R2(B,D,E)",
            "c) R1(B,D) ve R2(A,C,D,E)",
            "d) R1(A,B,D) ve R2(C,D,E)"
        ],
        "cevap": "a",
        "aciklama": "BCNF ihlal eden B -> D bağımlılığı için B+ = {B, D}'dir. Algoritma gereği R1 = B+ = {B, D} olur. R2 = R - (B+ - B) = R - {D} = {A, B, C, E} olur. Bu yüzden R1(B,D) ve R2(A,B,C,E) elde edilir."
    },
    {
        "id": 20,
        "soru": "SQL'de NULL değerlerin aggregate (kümeleme) fonksiyonlarındaki davranışı için hangisi DOĞRUDUR?",
        "secenekler": [
            "a) COUNT(*) sorgusu NULL içeren satırları yok sayar.",
            "b) COUNT(kolon_adi) sorgusu NULL içeren satırları da sayar.",
            "c) AVG(kolon_adi) NULL değerleri tamamen yok sayar; tüm satırlar NULL ise NULL döndürür.",
            "d) SUM(kolon_adi) NULL değerleri 0 kabul ederek toplama dahil eder."
        ],
        "cevap": "c",
        "aciklama": "SQL aggregate fonksiyonlarında; COUNT(*) NULL içeren satırları da sayar (satır sayısını verir). COUNT(kolon_adi), AVG, SUM fonksiyonları NULL değerleri yok sayar (görmezden gelir). Tüm satırlar NULL ise AVG ve SUM NULL döner."
    }
]

def read_multiline_sql(prompt_label="SQL"):
    """Kullanıcıdan noktalı virgül (;) görene kadar çok satırlı girdi alır. 
    İptal veya boş girdiyi yönetir."""
    console.print(f"\n[cyan]{prompt_label} sorgunuzu yazın (Satırı bitirmek için ';' koyup Enter'a basın, iptal için 'iptal' yazın):[/cyan]")
    lines = []
    while True:
        try:
            prompt_symbol = "[cyan]SQL>[/cyan] " if not lines else "   [dim]...[/dim] "
            console.print(prompt_symbol, end="")
            line = input().strip()
            
            if not line:
                continue
            
            if line.lower() == "iptal":
                return "iptal"
                
            lines.append(line)
            
            if line.endswith(";"):
                break
        except (KeyboardInterrupt, EOFError):
            console.print("\nGirdi iptal edildi.")
            return "iptal"
            
    return " ".join(lines)

def print_banner():
    banner = Text()
    banner.append("⚡ EMİRBERASOGUK SQL & VERİTABANI SINAV PRATİK ALANI ⚡\n", style="bold yellow")
    banner.append("Ders notlarındaki şemaları inceleyin, laboratuvarları çözün ve sınava hazırlanın.\n", style="italic cyan")
    banner.append("Lisans Sahibi: emirberasoguk | Sürüm: 2.0-Sade", style="dim white")
    console.print(Panel(banner, border_style="bold magenta", expand=False))

def exec_query(query, show_output=True):
    """Sorguyu çalıştırır ve Rich tablosu olarak basar. Hata durumunda [] ve False döner."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        if cursor.description is None:
            conn.commit()
            rowcount = cursor.rowcount
            if show_output:
                console.print(f"[bold green]✓ Sorgu başarıyla çalıştırıldı. Etkilenen satır sayısı: {rowcount}[/bold green]")
            return [], True
        
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        
        if show_output:
            if not rows:
                console.print("[yellow]Sorgu başarıyla çalıştı ancak hiçbir sonuç dönmedi (Boş Küme).[/yellow]")
            else:
                table = Table(show_header=True, header_style="bold cyan", border_style="dim")
                for col in columns:
                    table.add_column(col)
                for row in rows:
                    table.add_row(*[str(val) if val is not None else "[dim]NULL[/dim]" for val in row])
                console.print(table)
                console.print(f"[dim]Toplam satır sayısı: {len(rows)}[/dim]\n")
                
        return rows, True
    except sqlite3.Error as e:
        console.print(f"[bold red]❌ SQL Hatası:[/bold red] [yellow]{e}[/yellow]\n")
        return [], False
    finally:
        conn.close()

def inspect_schemas():
    """Tabloları ve şemaları gösterir."""
    console.print("\n[bold magenta]📊 VERİTABANI ŞEMALARI VE MEVCUT VERİLER[/bold magenta]\n")
    
    tablolar = ["denizci", "bot", "rezervasyon", "student", "enrolled"]
    
    for tablo in tablolar:
        console.print(Panel(f"[bold yellow]Tablo: {tablo}[/bold yellow]", border_style="cyan"))
        # Şemayı göster
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{tablo}'")
        schema = c.fetchone()[0]
        console.print(f"[bold green]SQL Şeması:[/bold green]\n[dim]{schema}[/dim]\n")
        conn.close()
        
        # İlk 10 veriyi göster
        console.print("[bold green]Mevcut Veriler:[/bold green]")
        exec_query(f"SELECT * FROM {tablo} LIMIT 10")

def show_theory():
    """Teorik özet kartlarını gösterir."""
    while True:
        console.print(Panel("[bold cyan]📚 SQL ve Veritabanı Yönetimi Konu Özetleri[/bold cyan]\n"
                            "1. Ders 4: ER Modeli, Şema Eşleme & Alt Sınıflar (ISA)\n"
                            "2. Ders 16 & SQL: Yazım, Çalışma Sırası, İlişkisel Cebir & NULL Mantığı\n"
                            "3. Ders 5-6-7: FD, Kapanış, Aday Anahtarlar, BCNF Ayrıştırma\n"
                            "4. Lecture 12: Disk Depolama, Buffer Pool, İndeks Seçimi & External Sort\n"
                            "5. Ders 8-9: Transactions, Concurrency (ACID, 2PL, Deadlock Wait-Die/Wound-Wait)\n"
                            "0. Ana Menüye Dön", border_style="magenta"))
        
        secim = Prompt.ask("Seçiminiz", choices=["0", "1", "2", "3", "4", "5"], default="0")
        
        if secim == "0":
            break
        elif secim == "1":
            text = ("[bold yellow]1. ER Bileşenleri:[/bold yellow]\n"
                    " Dikdörtgen: Varlık Seti, Elips: Öznitelik (Altı çizili: PK)\n"
                    " Çift Elips: Çok Değerli (Multivalued), Çift Çizgili Dikdörtgen: Zayıf Varlık\n"
                    " Eşkenar Dörtgen: İlişki Seti, Çift Çizgili Bağlantı: Tam Katılım (Total Participation)\n\n"
                    "[bold green]2. İlişkisel Şemaya Dönüşüm Kuralları:[/bold green]\n"
                    " * Zayıf Varlıklar sahibinin PK'si ile birleşip Composite PK oluşturur.\n"
                    " * M:N İlişkiler, her iki tarafın PK'lerini içeren ayrı bir tabloya dönüşür.\n"
                    " * Çok Değerli Öznitelikler kendi adlarına yeni bir tablo oluşturur (Örn: Ogrenci_Telefon).\n\n"
                    "[bold green]3. Alt Sınıflar (ISA):[/bold green]\n"
                    " * ER Tarzı: Üst ve alt sınıflar için ayrı tablolar. Alt sınıf PK'sı üst sınıfa FK'dir.\n"
                    " * OO Tarzı: Sadece yaprak alt sınıflar için tablolar oluşturulur. Üst sınıf kolonları miras alınır.\n"
                    " * Tek Tablo Tarzı: Tek bir büyük tablo. Alt sınıflara özel alanlar NULL olabilir. Tip kolonu eklenir.")
            console.print(Panel(text, title="Ders 4: ER Tasarımı, Şema Eşleme & Alt Sınıflar", border_style="yellow"))
        elif secim == "2":
            text = ("[bold yellow]SQL Çalışma Sırası:[/bold yellow]\n"
                    " FROM ➔ WHERE ➔ GROUP BY ➔ HAVING ➔ SELECT ➔ ORDER BY\n\n"
                    "[bold green]İlişkisel Cebir Operatörleri:[/bold green]\n"
                    " * Seçim (Selection - σ): Satır filtreleme (WHERE)\n"
                    " * İzdüşüm (Projection - π): Kolon seçme (SELECT)\n"
                    " * Kartezyen Çarpım (×): FROM T1, T2\n"
                    " * Birleştirme (Join - ⋈): JOIN ON / NATURAL JOIN\n"
                    " * Bölme (Division - /): Çift NOT EXISTS içeren sorgular ('tümünü gerçekleştirenler')\n\n"
                    "[bold yellow]💡 Üç Değerli Mantık (NULL):[/bold yellow]\n"
                    " * NULL = NULL ➔ UNKNOWN döndürür. Kontroller `IS NULL` ile yapılmalıdır.\n"
                    " * TRUE AND UNKNOWN = UNKNOWN, FALSE AND UNKNOWN = FALSE.\n"
                    " * TRUE OR UNKNOWN = TRUE, FALSE OR UNKNOWN = UNKNOWN.\n"
                    " * Aggregate'ler NULL değerleri yoksayar (COUNT(*) hariç, o NULL satırları da sayar).")
            console.print(Panel(text, title="SQL, İlişkisel Cebir & NULL Mantığı", border_style="yellow"))
        elif secim == "3":
            text = ("[bold yellow]Kapanış Hesaplama (X+):[/bold yellow]\n"
                    " Verilen FD'leri kullanarak X'in belirleyebileceği tüm kolonları bulma. "
                    "Eğer X+ tüm kolonları içeriyorsa X bir [bold green]Süper Anahtardır[/bold green]. En küçük süper anahtara [bold green]Aday Anahtar[/bold green] denir.\n\n"
                    "[bold yellow]Normal Formlar:[/bold yellow]\n"
                    " * 1NF: Değerler atomik olmalı.\n"
                    " * 2NF: Kısmi bağımlılık (aday anahtar alt kümesine bağımlılık) olmamalı.\n"
                    " * 3NF: X ➔ Y için X süper anahtar veya Y prime (anahtarın parçası) olmalı.\n"
                    " * BCNF: X ➔ Y için X mutlaka bir süper anahtar olmalı.\n\n"
                    "[bold green]📐 BCNF Ayrıştırma (Decomposition) Algoritması:[/bold green]\n"
                    " * BCNF ihlali yapan X ➔ Y bağımlılığı için tabloyu R1(X U Y) ve R2(R - Y) olarak ikiye böleriz.\n"
                    " * Parçalanma her zaman kayıpsızdır (lossless) fakat bağımlılıkları korumayabilir.")
            console.print(Panel(text, title="Ders 5-6-7: FD, Normalizasyon & BCNF Algoritması", border_style="yellow"))
        elif secim == "4":
            text = ("[bold yellow]Buffer Manager Görevleri:[/bold yellow]\n"
                    " * Disk I/O maliyetini azaltmak için sayfaları RAM'de tutar.\n"
                    " * [bold green]Pin Count[/bold green]: Sayfayı kullanan aktif işlem sayısı. Sıfır olmadan diskten atılamaz.\n"
                    " * [bold green]Dirty Bit[/bold green]: Sayfa RAM'de değiştirildiyse 1 olur. Diskten atılmadan önce güncellenmelidir.\n\n"
                    "[bold yellow]İndeks Seçimi (B+ Tree vs. Hash):[/bold yellow]\n"
                    " * [bold cyan]Hash İndeks[/bold cyan]: Eşitlik sorgularında ($c = 8$) çok hızlıdır ($O(1)$). Aralık sorgularını desteklemez.\n"
                    " * [bold cyan]B+ Tree İndeks[/bold cyan]: Aralık sorgularında ($c > 8$) ve sıralı erişimde mükemmeldir ($O(\\log N)$).\n\n"
                    "[bold green]⚙️ Dış Bellek Sıralama (External Merge Sort) Maliyeti:[/bold green]\n"
                    " * N sayfa, B buffer sayısı olmak üzere:\n"
                    " * Pass 0 run sayısı: ceil(N / B)\n"
                    " * Merge pass sayısı: ceil(log_{B-1}(Run Sayısı))\n"
                    " * Toplam I/O maliyeti: 2 * N * (1 + Merge Passes)")
            console.print(Panel(text, title="Lecture 12: Depolama, İndeksleme & Dış Sıralama", border_style="yellow"))
        elif secim == "5":
            text = ("[bold yellow]1. ACID Özellikleri:[/bold yellow]\n"
                    " Atomicity (Hep ya da hiç), Consistency (Tutarlılık), Isolation (Yalıtım), Durability (Kalıcılık)\n\n"
                    "[bold yellow]2. Eşzamanlılık Anomalileri:[/bold yellow]\n"
                    " * Dirty Read (WR): Commit edilmemiş veriyi okuma.\n"
                    " * Unrepeatable Read (RW): Okunan verinin başka işlemce değiştirilmesi.\n"
                    " * Lost Update (WW): Yazılan verinin üzerine başka bir işlemin yazması.\n\n"
                    "[bold yellow]3. İki Fazlı Kilitleme (2PL):[/bold yellow]\n"
                    " * Büyüme Fazı (yalnızca kilit alma) ve Küçülme Fazı (yalnızca kilit bırakma).\n"
                    " * [bold green]Strict 2PL[/bold green]: Tüm özel (X) kilitleri commit/abort anına kadar tutarak zincirleme geri almaları önler.\n\n"
                    "[bold red]🛑 Kördüğüm (Deadlock) Yönetimi:[/bold red]\n"
                    " * [bold green]Tespit:[/bold green] Waits-For Graph (Bekleme grafiğinde döngü arama).\n"
                    " * [bold green]Wait-Die (Önleme):[/bold green] Eski işlem bekler, yeni işlem kilit isterse ölür (iptal olur).\n"
                    " * [bold green]Wound-Wait (Önleme):[/bold green] Eski işlem yeniyi yaralar (iptal eder), yeni işlem bekler.")
            console.print(Panel(text, title="Ders 8-9: Transactions, Concurrency & Deadlocks", border_style="yellow"))
            
        Prompt.ask("\nDevam etmek için [Enter]'a basın")

def run_theory_quiz():
    """Etkileşimli çoktan seçmeli teorik test simülatörü."""
    correct_answers = 0
    total_questions = len(THEORY_QUESTIONS)
    
    console.print("\n[bold magenta]✍️ TEORİK TEST SİMÜLATÖRÜ (ÇIKMIŞ SORULAR)[/bold magenta]")
    console.print("[dim]Sınavda çıkan ER, Normalizasyon, Depolama ve Transactions sorularından derlenmiştir. (Çıkmak için 'q' yazabilirsiniz)[/dim]\n")
    
    for idx, q in enumerate(THEORY_QUESTIONS, 1):
        console.print(Panel(f"[bold yellow]Soru {idx}/{total_questions}:[/bold yellow]\n\n{q['soru']}", border_style="cyan"))
        for secenek in q['secenekler']:
            console.print(f"  {secenek}")
        
        user_ans = Prompt.ask("\nCevabınız (a, b, c, d, çıkmak için q)", choices=["a", "b", "c", "d", "q"], default="q")
        
        if user_ans == "q":
            console.print("[yellow]Test kullanıcı tarafından yarıda kesildi.[/yellow]")
            Prompt.ask("\nAna menüye dönmek için [Enter]'a basın")
            return
            
        if user_ans == q['cevap']:
            console.print("[bold green]✓ DOĞRU CEVAP! Tebrikler.[/bold green]")
            correct_answers += 1
        else:
            console.print(f"[bold red]❌ YANLIŞ CEVAP![/bold red] Doğru Seçenek: [bold green]{q['cevap']}[/bold green]")
            
        console.print(f"[dim]Açıklama: {q['aciklama']}[/dim]\n")
        Prompt.ask("Sonraki soruya geçmek için [Enter]'a basın")
        
    score_percentage = (correct_answers / total_questions) * 100
    color = "green" if score_percentage >= 70 else "yellow" if score_percentage >= 50 else "red"
    
    summary_text = (f"Testi tamamladınız!\n"
                    f"Toplam Soru: {total_questions}\n"
                    f"Doğru Cevap: {correct_answers}\n"
                    f"Başarı Oranı: [bold]{score_percentage:.1f}%[/bold]")
    
    console.print(Panel(summary_text, title="Test Sonucu", border_style=color))
    Prompt.ask("\nAna menüye dönmek için [Enter]'a basın")

def run_hands_on_labs():
    """Uygulamalı İnteraktif Laboratuvarlar (Genişletilmiş Kapsam)."""
    while True:
        console.print("\n[bold magenta]🔬 UYGULAMALI LABORATUVAR ALANI[/bold magenta]")
        console.print("Bu alanda teorik konuları terminalde kod yazarak uygulayacaksınız.\n")
        console.print("[bold yellow]1.[/bold yellow] Ders 4: ER Tasarımından SQL DDL Şeması Oluşturma Labı")
        console.print("[bold yellow]2.[/bold yellow] Ders 5-6-7: Kapanış Hesaplama (Attribute Closure) Labı")
        console.print("[bold yellow]3.[/bold yellow] Ders 8-9: Çakışma Grafiği (Precedence Graph) Analiz Labı")
        console.print("[bold yellow]4.[/bold yellow] Lecture 12: Canlı İndeks Performansı & Hız Testi Laboratuvarı")
        console.print("[bold yellow]5.[/bold yellow] Lecture 16: İlişkisel Cebirden SQL Sorgusuna Çeviri Labı")
        console.print("[bold yellow]6.[/bold yellow] Ders 4/5/7: Tablo Yapısını Güncelleme (ALTER TABLE DDL) Labı")
        console.print("[bold yellow]7.[/bold yellow] Lecture 12: Performans İndeksi Tanımlama (CREATE INDEX DDL) Labı")
        console.print("[bold yellow]8.[/bold yellow] Ders 5-6-7: BCNF Ayrıştırma (Decomposition) İzleme Labı")
        console.print("[bold yellow]9.[/bold yellow] Lecture 12: Dış Bellek Sıralama (External Merge Sort) Maliyeti Hesaplama Labı")
        console.print("[bold yellow]0.[/bold yellow] Ana Menüye Dön\n")
        
        secim = Prompt.ask("Çalışmak istediğiniz lab numarası", choices=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], default="0")
        
        if secim == "0":
            break
            
        if secim == "1":
            # Lab 1: ER to SQL DDL
            console.print(Panel("[bold green]LAB 1: ER Tasarımından Tablo Şeması Oluşturma (DDL)[/bold green]\n\n"
                                "Senaryo: Bir 'departman' (dep_id, ad) güçlü varlığı ile bir 'calisan' (calisan_id, isim) zayıf varlığı vardır. "
                                "Her çalışan mutlaka bir departmana aittir. Zayıf varlığın tablosunu oluşturacak CREATE TABLE komutunu yazınız.\n\n"
                                "Gereksinimler:\n"
                                "1) calisan_id ve dep_id birlikte Composite Primary Key olmalıdır.\n"
                                "2) dep_id kolonu departman(dep_id) tablosuna Foreign Key olarak referans vermelidir.\n"
                                "3) Yabancı anahtar tanımlaması olmalıdır.", border_style="yellow"))
            
            while True:
                user_ddl = read_multiline_sql("calisan tablosu oluşturma DDL")
                if user_ddl.lower() == "iptal":
                    break
                
                # Bellekte geçici veritabanı açıp test edelim
                test_conn = sqlite3.connect(":memory:")
                test_cursor = test_conn.cursor()
                test_cursor.execute("PRAGMA foreign_keys = ON;")
                
                # Önce güçlü departman tablosunu biz ekleyelim
                test_cursor.execute("CREATE TABLE departman(dep_id INTEGER PRIMARY KEY, ad TEXT);")
                
                try:
                    test_cursor.execute(user_ddl)
                    test_cursor.execute("PRAGMA table_info(calisan);")
                    cols = test_cursor.fetchall()
                    
                    test_cursor.execute("PRAGMA foreign_key_list(calisan);")
                    fks = test_cursor.fetchall()
                    
                    has_dep_id = any(c[1] == "dep_id" for c in cols)
                    has_calisan_id = any(c[1] == "calisan_id" for c in cols)
                    
                    pk_cols = [c[1] for c in cols if c[5] > 0]
                    is_composite_pk = set(pk_cols) == {"dep_id", "calisan_id"}
                    
                    has_fk = False
                    for fk in fks:
                        if fk[2] == "departman" and fk[3] == "dep_id" and fk[4] == "dep_id":
                            has_fk = True
                            
                    if has_dep_id and has_calisan_id and is_composite_pk and has_fk:
                        console.print(Panel("🎉 MÜKEMMEL! Zayıf varlık dönüşümünü başarıyla gerçekleştirdiniz.\n"
                                             "Bileşik anahtar ve yabancı anahtar kısıtları 100% doğrudur.", border_style="bold green"))
                        test_conn.close()
                        break
                    else:
                        hata_msg = "Sorgunuz çalıştı ancak kısıtlar eksik:\n"
                        if not is_composite_pk:
                            hata_msg += " - Birincil anahtar (Primary Key) hem calisan_id hem de dep_id içermelidir (Composite PK).\n"
                        if not has_fk:
                            hata_msg += " - dep_id alanı departman(dep_id) tablosuna referans veren bir Foreign Key olmalıdır.\n"
                        console.print(Panel(hata_msg, border_style="bold red"))
                except sqlite3.Error as e:
                    console.print(f"[bold red]❌ SQL Sözdizimi Hatası:[/bold red] {e}\nTekrar deneyin.")
                finally:
                    test_conn.close()
                    
        elif secim == "2":
            # Lab 2: Attribute Closure
            console.print(Panel("[bold green]LAB 2: Kapanış Hesaplama (Attribute Closure)[/bold green]\n\n"
                                "İlişki Şeması: R(A, B, C, D, E)\n"
                                "Fonksiyonel Bağımlılıklar (F):\n"
                                "  1) AB -> C\n"
                                "  2) C -> D\n"
                                "  3) D -> E\n\n"
                                "Soru: {A, B} kümesinin kapanışını (AB+) hesaplayıp cevabı birleşik harfler halinde yazınız (Örn: ABC).", border_style="yellow"))
            
            while True:
                user_ans = Prompt.ask("AB+ Kapanışı").strip().upper()
                if user_ans.lower() == "iptal":
                    break
                user_set = set(user_ans)
                correct_set = {"A", "B", "C", "D", "E"}
                
                if user_set == correct_set:
                    console.print(Panel("🎉 TEBRİKLER! Doğru hesapladınız.\n"
                                        "Hesaplama adımları:\n"
                                        "1) {A, B}+ = {A, B} başlar.\n"
                                        "2) AB -> C kuralıyla {A, B, C} olur.\n"
                                        "3) C -> D kuralıyla {A, B, C, D} olur.\n"
                                        "4) D -> E kuralıyla {A, B, C, D, E} olur.", border_style="bold green"))
                    break
                else:
                    console.print("[bold red]❌ Hatalı veya Eksik Kapanış![/bold red] Lütfen bağımlılık zincirini takip ederek tekrar hesaplayın.")
                    
        elif secim == "3":
            # Lab 3: Conflict Graph Edges
            console.print(Panel("[bold green]LAB 3: Çakışma Grafiği (Precedence Graph) Analiz Labı[/bold green]\n\n"
                                "Aşağıdaki eşzamanlı planı (schedule) inceleyin:\n"
                                "S = R1(A), W2(A), R3(B), W1(B)\n\n"
                                "Soru: Bu planın çakışma grafiğindeki yönlü kenarları (dependencies) yazın.\n"
                                "Format: T1'den T2'ye kenar için `1->2` yazın. Birden fazla kenar varsa virgülle ayırın. (Örn: `1->2, 3->1`).", border_style="yellow"))
            
            while True:
                user_ans = Prompt.ask("Eşzamanlılık Çakışma Kenarları").replace(" ", "")
                if user_ans.lower() == "iptal":
                    break
                user_edges = set(user_ans.split(","))
                correct_edges = {"1->2", "3->1"}
                
                if user_edges == correct_edges:
                    console.print(Panel("🎉 HARİKA! Çakışmaları doğru tespit ettiniz.\n\n"
                                        "Açıklaması:\n"
                                        " * R1(A) ile W2(A) çakışır ➔ T1 -> T2 kenarı çizilir.\n"
                                        " * R3(B) ile W1(B) çakışır ➔ T3 -> T1 kenarı çizilir.\n"
                                        "Döngü (cycle) olmadığı için bu plan Conflict Serializable'dır.", border_style="bold green"))
                    break
                else:
                    console.print("[bold red]❌ Hatalı Kenarlar![/bold red] Lütfen işlemleri veri bazlı (A ve B) ve zaman sırasına göre tekrar inceleyin.")
                    
        elif secim == "4":
            # Lab 4: Index Performance & Speed Test
            console.print(Panel("[bold green]LAB 4: Canlı İndeks Performansı & Hız Testi[/bold green]\n\n"
                                "Bu labda, indekslerin sorgu hızını nasıl etkilediğini canlı verilerle deneyimleyeceksiniz.\n"
                                "Şu adımları izleyeceğiz:\n"
                                "1. Geçici bir tabloda 50.000 satırlık rastgele veri oluşturacağız.\n"
                                "2. İndekssiz arama hızını (Table Scan) ölçeceğiz.\n"
                                "3. İndeks oluşturup sorguyu tekrar çalıştırıp hız farkını göreceğiz.", border_style="yellow"))
            
            if not Confirm.ask("Canlı veri oluşturup hız testine başlamak istiyor musunuz?"):
                continue
                
            conn = sqlite3.connect(":memory:")
            c = conn.cursor()
            
            with console.status("[bold green]50.000 adet veri üretiliyor...[/bold green]"):
                c.execute("CREATE TABLE buyuk_tablo (id INTEGER PRIMARY KEY, veri TEXT, deger INTEGER);")
                veriler = [(i, f"Veri_Kutusu_{i}", random.randint(1, 1000000)) for i in range(50000)]
                veriler[25000] = (25000, "Ozel_Hedef_Verisi", 999999)
                c.executemany("INSERT INTO buyuk_tablo VALUES (?, ?, ?)", veriler)
                conn.commit()
                
            console.print("[green]✓ Veriler başarıyla RAM'de oluşturuldu.[/green]\n")
            
            console.print("[bold yellow]1. Adım: İndekssiz (Table Scan) Arama Gerçekleştiriliyor...[/bold yellow]")
            console.print("Sorgu: [cyan]SELECT * FROM buyuk_tablo WHERE deger = 999999;[/cyan]")
            
            start_time = time.perf_counter_ns()
            c.execute("SELECT * FROM buyuk_tablo WHERE deger = 999999;")
            res = c.fetchall()
            end_time = time.perf_counter_ns()
            
            no_index_time_ms = (end_time - start_time) / 1_000_000
            
            c.execute("EXPLAIN QUERY PLAN SELECT * FROM buyuk_tablo WHERE deger = 999999;")
            plan_no_index = c.fetchone()[3]
            
            console.print(f"Sorgu Sonucu: {res}")
            console.print(f"Çalışma Süresi: [bold red]{no_index_time_ms:.4f} ms[/bold red]")
            console.print(f"Sorgu Planı (Sorgu Motoru Davranışı): [bold red]{plan_no_index}[/bold red] (Tüm satırlar tek tek tarandı!)\n")
            
            console.print("[bold yellow]2. Adım: İndeks Oluşturuluyor...[/bold yellow]")
            console.print("Komut: [cyan]CREATE INDEX idx_deger ON buyuk_tablo(deger);[/cyan]")
            
            start_idx = time.perf_counter_ns()
            c.execute("CREATE INDEX idx_deger ON buyuk_tablo(deger);")
            end_idx = time.perf_counter_ns()
            
            console.print(f"İndeks Oluşturma Süresi: {(end_idx - start_idx)/1_000_000:.2f} ms\n")
            
            console.print("[bold yellow]3. Adım: İndeksli (Index Lookup) Arama Gerçekleştiriliyor...[/bold yellow]")
            console.print("Sorgu: [cyan]SELECT * FROM buyuk_tablo WHERE deger = 999999;[/cyan]")
            
            start_time = time.perf_counter_ns()
            c.execute("SELECT * FROM buyuk_tablo WHERE deger = 999999;")
            res = c.fetchall()
            end_time = time.perf_counter_ns()
            
            indexed_time_ms = (end_time - start_time) / 1_000_000
            
            c.execute("EXPLAIN QUERY PLAN SELECT * FROM buyuk_tablo WHERE deger = 999999;")
            plan_indexed = c.fetchone()[3]
            
            console.print(f"Sorgu Sonucu: {res}")
            console.print(f"Çalışma Süresi: [bold green]{indexed_time_ms:.4f} ms[/bold green]")
            console.print(f"Sorgu Planı (Sorgu Motoru Davranışı): [bold green]{plan_indexed}[/bold green] (Doğrudan indeks kullanıldı!)\n")
            
            hiz_kat = no_index_time_ms / (indexed_time_ms if indexed_time_ms > 0 else 0.0001)
            
            console.print(Panel(f"📊 [bold yellow]Performans Karşılaştırma Özeti:[/bold yellow]\n\n"
                                f" * İndekssiz Arama Süresi: [bold red]{no_index_time_ms:.4f} ms[/bold red]\n"
                                f" * İndeksli Arama Süresi: [bold green]{indexed_time_ms:.4f} ms[/bold green]\n"
                                f" * İndeksli sorgumuz yaklaşık [bold green]{hiz_kat:.1f} kat[/bold green] daha hızlı çalıştı!\n\n"
                                f"Bu pratik test, Lecture 12 dersindeki B+ Tree veya indeks yapıları kullanmanın disk/veri okuma maliyetlerini nasıl dramatik ölçüde düşürdüğünü kanıtlamaktadır.", border_style="bold green"))
            
            conn.close()
            Prompt.ask("\nSonraki adıma geçmek için [Enter]'a basın")
            
        elif secim == "5":
            # Lab 5: Relational Algebra to SQL
            console.print(Panel("[bold green]LAB 5: İlişkisel Cebirden SQL Sorgusuna Çeviri[/bold green]\n\n"
                                "Soru: Aşağıdaki İlişkisel Cebir (Relational Algebra) ifadesisinin SQL karşılığını yazınız.\n\n"
                                "  π_{isim}(σ_{yas < 30}(denizci))\n\n"
                                "[dim]İpucu: π izdüşüm (SELECT), σ seçim (WHERE) anlamına gelir.[/dim]", border_style="yellow"))
            
            while True:
                user_sql = read_multiline_sql("İlişkisel Cebir Eşdeğeri SQL")
                if user_sql.lower() == "iptal":
                    break
                
                # Kullanıcı sorgusunu çalıştıralım
                user_res, success = exec_query(user_sql, show_output=False)
                if not success:
                    continue
                
                ref_sql = "SELECT isim FROM denizci WHERE yas < 30;"
                ref_res, _ = exec_query(ref_sql, show_output=False)
                
                if set(user_res) == set(ref_res):
                    console.print(Panel("🎉 TEBRİKLER! İlişkisel cebir ifadesini SQL'e 100% doğru olarak çevirdiniz.\n"
                                        "SQL Karşılığı: SELECT isim FROM denizci WHERE yas < 30;", border_style="bold green"))
                    break
                else:
                    console.print("[bold red]❌ Yanlış Çeviri![/bold red] Sorgunuz beklenen satırları döndürmedi. Lütfen WHERE koşulunu ve SELECT alanını kontrol edin.")

        elif secim == "6":
            # Lab 6: ALTER TABLE DDL
            console.print(Panel("[bold green]LAB 6: Tablo Yapısını Güncelleme (ALTER TABLE DDL)[/bold green]\n\n"
                                "Senaryo: Veritabanında mevcut olan 'denizci' tablosuna, denizcilerin e-posta adreslerini saklayacak "
                                "'eposta' adında ve TEXT veri tipinde yeni bir kolon (column) eklemek istiyoruz.\n\n"
                                "Soru: Bu kolon ekleme işlemini yapacak ALTER TABLE DDL sorgusunu yazınız.", border_style="yellow"))
            
            while True:
                user_ddl = read_multiline_sql("Kolon ekleme DDL")
                if user_ddl.lower() == "iptal":
                    break
                
                # Test etmek için kiralama.db'de geçici tablo yapısı veya test_conn kullanalım
                test_conn = sqlite3.connect(":memory:")
                test_cursor = test_conn.cursor()
                test_cursor.execute("CREATE TABLE denizci (did INTEGER PRIMARY KEY, isim TEXT, yas INTEGER);")
                
                try:
                    test_cursor.execute(user_ddl)
                    test_cursor.execute("PRAGMA table_info(denizci);")
                    cols = test_cursor.fetchall()
                    
                    has_eposta = False
                    for col in cols:
                        if col[1] == "eposta" and col[2].upper() == "TEXT":
                            has_eposta = True
                            
                    if has_eposta:
                        console.print(Panel("🎉 TEBRİKLER! ALTER TABLE sorgunuz başarıyla çalıştı ve yeni sütunu ekledi.", border_style="bold green"))
                        test_conn.close()
                        break
                    else:
                        console.print("[bold red]❌ Eksik veya Hatalı Tanım![/bold red] 'eposta' kolonu TEXT tipiyle eklenmedi. Tekrar deneyin.")
                except sqlite3.Error as e:
                    console.print(f"[bold red]❌ SQL Sözdizimi Hatası:[/bold red] {e}\nTekrar deneyin.")
                finally:
                    test_conn.close()

        elif secim == "7":
            # Lab 7: CREATE INDEX DDL
            console.print(Panel("[bold green]LAB 7: İndeks Oluşturma (CREATE INDEX DDL)[/bold green]\n\n"
                                "Senaryo: 'denizci' tablosundaki denizcilerin 'yas' alanına göre yapılan arama ve sıralama "
                                "işlemlerini hızlandırmak istiyoruz. \n\n"
                                "Soru: 'denizci' tablosunun 'yas' kolonu üzerinde 'idx_denizci_yas' adında "
                                "bir performans indeksi oluşturacak SQL sorgusunu yazınız.", border_style="yellow"))
            
            while True:
                user_ddl = read_multiline_sql("İndeks oluşturma DDL")
                if user_ddl.lower() == "iptal":
                    break
                
                test_conn = sqlite3.connect(":memory:")
                test_cursor = test_conn.cursor()
                test_cursor.execute("CREATE TABLE denizci (did INTEGER PRIMARY KEY, isim TEXT, yas INTEGER);")
                
                try:
                    test_cursor.execute(user_ddl)
                    # sqlite_master tablosundan indeksi denetleyelim
                    test_cursor.execute("SELECT name, tbl_name, sql FROM sqlite_master WHERE type='index' AND name='idx_denizci_yas';")
                    idx_info = test_cursor.fetchone()
                    
                    if idx_info and idx_info[1] == "denizci" and "yas" in idx_info[2].lower():
                        console.print(Panel("🎉 TEBRİKLER! 'idx_denizci_yas' indeksi 'yas' kolonu üzerinde başarıyla oluşturuldu.", border_style="bold green"))
                        test_conn.close()
                        break
                    else:
                        console.print("[bold red]❌ Hatalı İndeks Tanımı![/bold red] İndeks ismi veya kolon eşleşmedi. Tekrar deneyin.")
                except sqlite3.Error as e:
                    console.print(f"[bold red]❌ SQL Sözdizimi Hatası:[/bold red] {e}\nTekrar deneyin.")
                finally:
                    test_conn.close()

        elif secim == "8":
            # Lab 8: BCNF Decomposition Tracing Lab
            console.print(Panel("[bold green]LAB 8: BCNF Ayrıştırma (Boyce-Codd Normal Form Decomposition) Labı[/bold green]\n\n"
                                "İlişki Şeması: R(A, B, C, D)\n"
                                "Fonksiyonel Bağımlılıklar (F):\n"
                                "  1) A -> BC\n"
                                "  2) C -> D\n\n"
                                "Soru: Bu şemayı BCNF Decomposition algoritması ile ayrıştırdığımızda BCNF normal formunda elde edilecek nihai tablo şemalarını yazın.\n"
                                "Önemli: BCNF ihlali olan C -> D üzerinden başlayın ve alt şemaları virgülle ayırarak alfabetik sırada yazın (Örn: ABC, CD).", border_style="yellow"))
            
            while True:
                user_ans = Prompt.ask("Nihai Şemalar (Örn: ABC, CD)").strip().upper().replace(" ", "")
                if user_ans.lower() == "iptal":
                    break
                user_schemas = set(user_ans.split(","))
                correct_schemas = {"ABC", "CD"}
                
                if user_schemas == correct_schemas:
                    console.print(Panel("🎉 MÜKEMMEL! BCNF Ayrıştırmasını başarıyla tamamladınız.\n\n"
                                        "Ayrıştırma Adımları:\n"
                                        "1) R(A,B,C,D) tablosunda C -> D bağımlılığı BCNF'i ihlal eder (çünkü C anahtar değildir, anahtar A'dır).\n"
                                        "2) C+ = {C, D} olduğundan tabloyu R1(C, D) ve R2(R - {D}) = R2(A, B, C) olarak böleriz.\n"
                                        "3) R1(C,D) tablosunda tek bağımlılık C -> D'dir. C anahtar olduğundan R1 BCNF'dedir.\n"
                                        "4) R2(A,B,C) tablosunda A -> BC bağımlılığı geçerlidir. A anahtar olduğundan R2 de BCNF'dedir.\n"
                                        "Nihai BCNF tabloları: ABC ve CD.", border_style="bold green"))
                    break
                else:
                    console.print("[bold red]❌ Hatalı Ayrıştırma![/bold red] Lütfen ihlalleri ve kolon kümesini tekrar kontrol ederek hesaplayın.")

        elif secim == "9":
            # Lab 9: External Merge Sort Cost Calculation Lab
            console.print(Panel("[bold green]LAB 9: Dış Bellek Sıralama (External Merge Sort) Maliyet Hesaplama Labı[/bold green]\n\n"
                                "Senaryo: Sıralanacak dosya N = 800 sayfadır.\n"
                                "Kullanılabilir RAM tampon bellek boyutu B = 10 sayfadır.\n\n"
                                "Hesaplamanız gerekenler:\n"
                                "1. Pass 0 sonrasında kaç run (sıralı parça) oluşur?\n"
                                "2. Toplam kaç merge pass (birleştirme adımı) gerekir?\n"
                                "3. Sıralama işleminin TOPLAM I/O (Disk Okuma/Yazma) maliyeti ne olur?\n\n"
                                "Soruları sırasıyla çözüp aralarına virgül koyarak yazın (Örn: 80, 2, 3200).", border_style="yellow"))
            
            while True:
                user_ans = Prompt.ask("Cevaplarınız (Format: RunSayisi, PassSayisi, ToplamIO)").strip().replace(" ", "")
                if user_ans.lower() == "iptal":
                    break
                
                try:
                    parts = user_ans.split(",")
                    run_ans = int(parts[0])
                    pass_ans = int(parts[1])
                    io_ans = int(parts[2])
                    
                    if run_ans == 80 and pass_ans == 2 and io_ans == 4800:
                        console.print(Panel("🎉 TEBRİKLER! Tüm hesaplamalarınız 100% doğrudur.\n\n"
                                            "Detaylı Çözüm:\n"
                                            " * Run Sayısı = ceil(N / B) = ceil(800 / 10) = 80 run.\n"
                                            " * Birleştirme Adım Sayısı (Merge Passes) = ceil(log_{B-1}(Run Sayısı)) = ceil(log_9(80)) = 2 merge pass.\n"
                                            " * Toplam Maliyet = 2 * N * (1 + Merge Passes) = 2 * 800 * (1 + 2) = 4800 I/O.", border_style="bold green"))
                        break
                    else:
                        hata_msg = "Hesaplamalarınızda hata var:\n"
                        if run_ans != 80:
                            hata_msg += f" - Run sayısını {run_ans} buldunuz, ancak ceil(N/B) = ceil(800/10) olmalı.\n"
                        if pass_ans != 2:
                            hata_msg += f" - Merge pass sayısını {pass_ans} buldunuz, ancak ceil(log_9(80)) olmalı.\n"
                        if io_ans != 4800:
                            hata_msg += f" - Toplam I/O maliyetini {io_ans} buldunuz, ancak 2 * N * (1 + Pass) olmalı.\n"
                        console.print(Panel(hata_msg, border_style="bold red"))
                except Exception as e:
                    console.print(f"[bold red]❌ Girdi Ayrıştırma Hatası:[/bold red] Lütfen cevabınızı '80, 2, 4800' formatında yazın.")

def run_exam_simulator():
    """Etkileşimli sınav soruları simülatörü (Çok Satırlı SQL Destekli)."""
    while True:
        console.print("\n[bold magenta]📝 SQL SINAV SORULARI SİMÜLATÖRÜ[/bold magenta]")
        for q in SORULAR:
            console.print(f"[bold yellow]{q['id']}.[/bold yellow] {q['baslik']}")
        console.print("[bold yellow]0.[/bold yellow] Ana Menüye Dön\n")
        
        secim = Prompt.ask("Çözmek istediğiniz sorunun numarası", choices=[str(i) for i in range(len(SORULAR) + 1)], default="0")
        
        if secim == "0":
            break
            
        soru = SORULAR[int(secim) - 1]
        
        console.print(Panel(f"[bold green]SORU {soru['id']}: {soru['baslik']}[/bold green]\n\n"
                            f"{soru['aciklama']}\n\n"
                            f"[bold cyan]İpucu:[/bold cyan] {soru['ipucu']}", 
                            border_style="yellow"))
        
        if soru['id'] in [1, 2, 3, 4]:
            console.print("[dim]İlgili tablolar: denizci, bot, rezervasyon. Şemayı şema menüsünden inceleyebilirsiniz.[/dim]")
        else:
            console.print("[dim]İlgili tablolar: student, enrolled. Şemayı şema menüsünden inceleyebilirsiniz.[/dim]")
            
        while True:
            user_sql = read_multiline_sql("Sınav Sorusu SQL")
            
            if user_sql.lower() == "iptal":
                break
                
            # Sorguyu çalıştır (Hata durumunda exec_query boş liste ve False döner)
            user_results, success = exec_query(user_sql, show_output=True)
            
            if not success:
                continue
                
            # Doğru sorguyu çalıştırıp karşılaştıralım
            ref_results, _ = exec_query(soru['dogru_sorgu'], show_output=False)
            
            user_set = set(user_results)
            ref_set = set(ref_results)
            
            if user_set == ref_set:
                console.print(Panel("🎉 TEBRİKLER! Sorgunuz doğru sonucu üretti. Sınav sorusunu başarıyla çözdünüz!", 
                                    border_style="bold green", title="Doğru Cevap!"))
                break
            else:
                console.print(Panel("❌ Üzgünüm, sorgunuz beklenen çıktıyı vermedi.\n\n"
                                    f"[bold red]Sizin Sonucunuz (Küme olarak):[/bold red] {user_set}\n"
                                    f"[bold green]Beklenen Sonuç (Küme olarak):[/bold green] {ref_set}\n\n"
                                    "Farklı satırlar döndürdünüz veya boş küme aldınız. Lütfen tekrar deneyin!", 
                                    border_style="bold red", title="Hatalı Sonuç"))
                
                tekrar = Confirm.ask("Tekrar denemek ister misiniz?")
                if not tekrar:
                    console.print(f"[bold yellow]Referans Doğru Sorgu:[/bold yellow] [green]{soru['dogru_sorgu']}[/green]")
                    break

def run_sql_prompt():
    """Canlı SQL konsolu (Çok Satırlı SQL Destekli)."""
    console.print(Panel("[bold yellow]⚡ CANLI SQL KONSOLU ⚡[/bold yellow]\n"
                        "Buraya SQL sorgularınızı yazabilirsiniz. \n"
                        "Çok satırlı sorgular yazabilir, sorgu sonuna ';' koyarak çalıştırabilirsiniz.\n"
                        "Çıkmak için 'exit' veya 'quit' yazın.",
                        border_style="green"))
    
    while True:
        try:
            sql = read_multiline_sql("Canlı Konsol SQL")
            if sql.strip().lower() in ["exit", "quit", "iptal"]:
                break
            if not sql.strip():
                continue
            exec_query(sql)
        except KeyboardInterrupt:
            console.print("\nKonsoldan çıkılıyor...")
            break

def main():
    check_license()
    init_db()
    
    while True:
        os.system("clear")
        print_banner()
        
        console.print("[bold yellow]1.[/bold yellow] 💻 Canlı SQL Prompt (Serbest Denemeler - Çok Satırlı)")
        console.print("[bold yellow]2.[/bold yellow] 📊 Tabloları, Şemaları ve Verileri İncele")
        console.print("[bold yellow]3.[/bold yellow] 🔬 Uygulamalı VTYS Laboratuvarları (Hands-on Labs - DDL & DML)")
        console.print("[bold yellow]4.[/bold yellow] ✍️ Teorik Test Simülatörü (Çoktan Seçmeli Sınav Soruları)")
        console.print("[bold yellow]5.[/bold yellow] 📝 SQL Sınav Sorularını Çöz ve Test Et (10 Soru)")
        console.print("[bold yellow]6.[/bold yellow] 📚 SQL & Veritabanı Yönetimi Konu Özetleri (Teori)")
        console.print("[bold yellow]0.[/bold yellow] ❌ Çıkış\n")
        
        secim = Prompt.ask("Seçiminiz", choices=["0", "1", "2", "3", "4", "5", "6"], default="0")
        
        if secim == "0":
            console.print("[bold yellow]emirberasoguk iyi çalışmalar ve sınavda başarılar diler![/bold yellow]")
            break
        elif secim == "1":
            run_sql_prompt()
        elif secim == "2":
            inspect_schemas()
            Prompt.ask("\nAna menüye dönmek için [Enter]'a basın")
        elif secim == "3":
            run_hands_on_labs()
        elif secim == "4":
            run_theory_quiz()
        elif secim == "5":
            run_exam_simulator()
        elif secim == "6":
            show_theory()

if __name__ == "__main__":
    main()
