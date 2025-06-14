<h1 align="center"> Tugas Besar 3 IF2211 Strategi Algoritma </h1>
<h1 align="center">  Pemanfaatan Pattern Matching untuk Membangun Sistem ATS Berbasis CV Digital </h1>

## Deskripsi Program
Program SignHire ini merupakan aplikasi desktop berbasis python yang memiliki fitur utama pencarian detail cv pelamar berdasarkan kata kunci tertentu. Pada program ini, kami menerapkan dual-phase matching approach dimana program melakukan exact matching terlebih dahulu menggunakan algoritma yang dipilih pengguna, kemudian jika exact match tidak menghasilkan kecocokan yang memadai, program akan melanjutkan pencarian dengan fuzzy matching menggunakan Levenshtein Distance. Pencarian exact matching ini dilakukan menggunakan algoritma Knuth Morris Pratt (KMP), Boyer-Moore, dan Aho Corasick. 

## Penjelasan Algoritma
#### 1. Algoritma KMP
..
#### 2. Algoritma Boyer Moore
..

## Requirement
<div>
    <table align="center">
      <tr>
        <td>No</td>
        <td>Requirement</td>
      </tr>
      <tr>
        <td>1</td>
        <td>mysql-connector-python</td>
      </tr>
      <tr>
        <td>2</td>
        <td>customtkinter</td>
      </tr>
      <tr>
        <td>3</td>
        <td>faker</td>
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

## Identitas Pembuat
<div>
    <table align="center">
      <tr>
        <td>NIM</td>
        <td>Nama</td>
      </tr>
      <tr>
        <td>13523043</td>
        <td>Najwa Kahani Fatima</td>
      </tr>
      <tr>
        <td>13523079</td>
        <td>Nayla Zahira</td>
      </tr>
      <tr>
        <td>13523107</td>
        <td>Heleni Gratia Meitrina Tampubolon</td>
      </tr>
    </table>
</div>
