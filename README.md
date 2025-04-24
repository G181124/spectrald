### **Langkah-langkah Penginstalan dan Penggunaan SpectraLD**

#### **1. Clone Repository**
   - Pertama, clone repository **SpectraLD** dari GitHub ke komputer Anda dengan perintah:
     ```bash
     git clone https://github.com/username/spectrald
     ```
     Gantilah `username` dengan nama pengguna GitHub yang sesuai.

#### **2. Memberikan Izin Eksekusi pada Skrip `run.sh`**
   - Setelah clone selesai, masuk ke direktori proyek dan berikan izin eksekusi pada file `run.sh` dengan perintah:
     ```bash
     chmod +x run.sh
     ```

#### **3. Menjalankan Tool SpectraLD**
   - Setelah semuanya siap, Anda dapat menjalankan tools **SpectraLD** menggunakan perintah berikut untuk mencari **username**:
     ```bash
     ./run.sh --username username
     ```
     Gantilah `username` dengan nama pengguna yang ingin Anda cari. Jika Anda ingin mencari lebih dari satu username, Anda dapat menambahkannya dengan spasi, seperti:
     ```bash
     ./run.sh --username username1 username2 username3
     ```

#### **4. Menambahkan Opsi `--verbose` untuk Menampilkan Metadata**
   - Jika Anda ingin melihat informasi tambahan seperti bio, link, dan gambar, Anda bisa menggunakan opsi `--verbose`:
     ```bash
     ./run.sh --username username --verbose
     ```

#### **5. Mengaktifkan Mode Cepat dengan `--fast` (Multithreading)**
   - Untuk meningkatkan kecepatan pencarian dengan menggunakan multithreading, Anda dapat menggunakan opsi `--fast`:
     ```bash
     ./run.sh --username username --fast
     ```

#### **6. Menggabungkan Opsi `--verbose` dan `--fast`**
   - Anda bisa menggabungkan kedua opsi tersebut untuk menjalankan pencarian lebih cepat sekaligus menampilkan metadata tambahan:
     ```bash
     ./run.sh --username username --verbose --fast
     ```

---

### **Output Hasil Pencarian**
- Hasil pencarian akan disimpan dalam folder **`hasil/`**, dengan nama file yang mencakup **username** dan **timestamp**:
  - Contoh nama file:
    ```
    hasil/username_2025-04-07_10-33-56.txt
    ```

- Hasil ini akan mencakup informasi tentang status **200** (ditemukan) atau **404** (tidak ditemukan) untuk setiap platform yang diperiksa.

---

### **Contoh Penggunaan**:
Jika Anda menjalankan perintah berikut:
```bash
./run.sh --username mrbeast --fast
```
Anda akan melihat output seperti ini:
```
--- Mencari untuk username: mrbeast ---
[+] Facebook      → ✅ https://www.facebook.com/mrbeast
[+] Instagram     → ✅ https://www.instagram.com/mrbeast
[+] TikTok        → ✅ https://www.tiktok.com/@mrbeast
...
[✓] Pencarian selesai — 16 hasil ditemukan.
📁 Hasil disimpan di: hasil/mrbeast_2025-04-07_10-33-56.txt
```

---

### **Penjelasan Singkat Opsi**:
- **`--username`**: Tentukan satu atau lebih username yang ingin dicari.
- **`--verbose`**: Menampilkan metadata tambahan (bio, link, gambar).
- **`--fast`**: Mengaktifkan pencarian cepat dengan multithreading.
