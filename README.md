<h1 align="center"> Tugas Besar 3 IF2211 Strategi Algoritma </h1>
<h2 align="center">Semester II Tahun 2024/2025</h2>
<h2 align="center">  Pemanfaatan Pattern Matching untuk Membangun Sistem ATS Berbasis CV Digital </h2>

<p align="center">
  <img src="doc/signhere.gif" alt="RushHourSolver"/>
</p>

## Daftar Isi
- [Deskripsi Program](#deskripsi-program)
- [Penjelasan Algoritma](#penjelasan-algoritma)
- [Struktur Project](#Struktur-Project)
- [Requirements](#requirements)
- [Cara Mengkompilasi dan Menjalankan Program](#Cara-Mengkompilasi-dan-Menjalankan-Program)
- [Author](#author)

## Deskripsi Program
Program SignHire ini merupakan aplikasi desktop berbasis python yang memiliki fitur utama pencarian detail cv pelamar berdasarkan kata kunci tertentu. Pada program ini, kami menerapkan dual-phase matching approach dimana program melakukan exact matching terlebih dahulu menggunakan algoritma yang dipilih pengguna, kemudian jika exact match tidak menghasilkan kecocokan yang memadai, program akan melanjutkan pencarian dengan fuzzy matching menggunakan Levenshtein Distance. Pencarian exact matching ini dilakukan menggunakan algoritma Knuth Morris Pratt (KMP), Boyer-Moore, dan Aho Corasick. 

## Penjelasan Algoritma
#### 1. Algoritma Knuth-Morris-Pratt (KMP)
Algoritma KMP merupakan algoritma pencarian string yang efisien untuk menemukan kemunculan suatu pola dalam teks. Algoritma ini melakukan praproses pada pola untuk membentuk tabel Longest Prefix Suffix (LPS) yang memungkinkan pergeseran pola yang efisien saat terjadi ketidakcocokan, sehingga tidak perlu pemeriksaan ulang karakter yang telah dicocokkan. Kompleksitas waktu: O(m + n).

#### 2. Algoritma Boyer Moore
Boyer-Moore adalah algoritma pencocokan pola yang mencocokkan karakter dari belakang pola (kanan ke kiri) sambil memindai teks dari kiri ke kanan. Algoritma ini menggunakan looking-glass technique dan character-jump technique dengan memanfaatkan last occurrence function untuk menentukan pergeseran pola yang optimal saat terjadi ketidakcocokan, sehingga dapat melompati bagian teks yang tidak mungkin cocok.

#### 3. Algoritma Aho-Corasick
Aho-Corasick merupakan algoritma string matching yang menggunakan struktur data trie untuk pencarian multiple pattern secara simultan. Algoritma ini membangun trie dari semua keyword dan menggunakan failure function untuk navigasi efisien. Ketika terjadi ketidakcocokan, algoritma menggunakan failure function untuk melanjutkan pencarian tanpa mengulang dari awal, sehingga sangat efisien untuk mencari beberapa kata kunci sekaligus.

#### 4. Fuzzy Matching: Levenshtein Distance
Levenshtein Distance mengukur tingkat kesamaan antara dua string dengan menghitung jumlah minimum operasi edit (penambahan, penghapusan, substitusi) yang diperlukan untuk mengubah satu string menjadi string lainnya. Implementasi menggunakan pendekatan dynamic programming dengan array biaya untuk menyimpan nilai perubahan minimum, sehingga dapat menangani variasi ejaan dan typo dalam pencarian CV.

#### 5. Regular Expression (Regex)
Regular Expression menggunakan pola khusus dengan notasi standar regex untuk mencocokkan kombinasi karakter dalam string. Dalam aplikasi ini, regex digunakan untuk mengenali dan memproses format data tertentu dalam CV seperti email, nomor telepon, atau pola teks spesifik lainnya.

## Struktur Project
```
Tubes3_SigningOut
├── data/                        # Folder untuk file hasil kompilasi 
├── doc/
│   └── laporan.pdf             # Laporan tugas dalam format PDF
├── src/                        # Folder source code utama
│   ├── controller/       
│   │   ├── cv_data_manager.py
│   │   ├── db_setup.py
│   │   └── seeder.py
│   ├── gui/ 
│   │   ├── assets/
│   │   ├── components/
│   │   │   ├── about_page.py
│   │   │   ├── cv_summary_window.py
│   │   │   ├── developer_page.py
│   │   │   ├── home_page.py
│   │   │   ├── main_window.py
│   │   │   └── splash_screen.py
│   ├── model/
│   │   ├── aho_corassick.py
│   │   ├── boyer_moore.py
│   │   ├── encryptor.py
│   │   ├── knuth_morris_pratt.py
│   │   ├── levenshtein_distance.py
│   │   └── regex.py
│   └── app.py
├── README.md                  # Dokumentasi utama proyek
└── run.bat                    # Tool untuk compile dan run program
```

## Requirements
<div>
    <table>
      <tr>
        <td>No</td>
        <td>Requirement</td>
        <td>Fungsi</td>
      </tr>
      <tr>
        <td>1</td>
        <td>mysql-connector-python</td>
        <td>Koneksi database MySQLn</td>
      </tr>
      <tr>
        <td>2</td>
        <td>customtkinter</td>
        <td>Interface GUI modern</td>
      </tr>
      <tr>
        <td>3</td>
        <td>faker</td>
        <td>Generate data dummy</td>
      </tr>
    </table>
</div>

## Cara Mengkompilasi dan Menjalankan Program
##### Setup Database
1. Masuk ke mysql dengan perintah berikut diikuti dengan input password
   ```
      mysql -u root -p
   ```
2. Tambahkan user dan database baru pada mysql 
    ```
       CREATE USER 'cv_app'@'localhost' IDENTIFIED BY 'signingout';
       CREATE DATABASE cv_db;
       GRANT ALL PRIVILEGES ON cv_db.* TO 'cv_app'@'localhost';
       FLUSH PRIVILEGES;
   ```
##### Cara Menjalankan Program
1. Clone repository
   ```
    git clone https://github.com/naylzhra/Tubes3_SigningOut.git
   ```
2. Buka folder repository kemudian jalankan run.bat (sangat disarankan jika menjalankan program untuk pertama kali) 
   ```
    ./run.bat
   ```
3. Alternatif: Jika sebelumnya sudah pernah melakukan seeding data, pengguna dapat langsung menjalankan app dengan perintah berikut 
   ```
     python src/app.py
   ```

## Author
<table>
  <tr>
    <td align="center">
      <a href="https://github.com/najwakahanifatima">
        <img src="https://avatars.githubusercontent.com/najwakahanifatima" width="80" style="border-radius: 50%;" /><br />
        <span><b>Najwa Kahani Fatima</br> 13523043</b></span>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/naylzhra">
        <img src="https://avatars.githubusercontent.com/naylzhra" width="80" style="border-radius: 50%;" /><br />
        <span><b>Nayla Zahira</br> 13523079</b></span>
      </a>
    </td>
        <td align="center">
      <a href="https://github.com/mineraleee">
        <img src="https://avatars.githubusercontent.com/mineraleee" width="80" style="border-radius: 50%;" /><br />
        <span><b>Heleni Gratia</br> 13523107</b></span>
      </a>
    </td>
  </tr>
</table>

<div>
  <strong>Strategi Algoritma IF2211 - Institut Teknologi Bandung</strong><br>
  <em>Sistem ATS Modern dengan Pattern Matching yang Efisien</em>
</div>
