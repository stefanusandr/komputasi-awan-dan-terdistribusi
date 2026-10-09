# Jurnal Proses — Tugas 3

**Kelompok:** Kelompok 3  
**Anggota:**
- Stefanus Andri Hendrawan (103072400115)
- Fatih Khairu Alfifiajri (103072400105)
- Moh Irham Maulana A.S (103072400063)

---

## Percobaan tanpa Lock
- **Hasil `processed_count` yang didapat:** `62` (bervariasi antara 50 sampai 70 dari total 100 pesanan).
- **Pesan error/warning program:** `RACE CONDITION TERDETEKSI - lengkapi TODO 1 & TODO 2 dengan Lock!`
- **Kenapa bisa meleset (mekanisme race condition dengan kata sendiri):**  
  Operasi penambahan nilai counter `processed_count += 1` pada program bukanlah satu instruksi atomik tunggal (*atomic operation*), melainkan rangkaian 3 tahapan instruksi (*read-modify-write*):
  1. **Read:** Thread membaca nilai variabel `processed_count` saat ini dari memori bersama (*shared memory*) ke register/variabel lokal thread.
  2. **Modify:** Thread menambahkan nilai tersebut dengan angka 1 (`current + 1`) di register lokal.
  3. **Write:** Thread menuliskan kembali hasil penjumlahan tersebut ke alamat memori variabel bersama `processed_count`.

  Ketika 10 worker thread berjalan secara konkuren mengakses variabel bersama yang sama tanpa proteksi, terjadi *thread interleaving* (pergantian giliran eksekusi thread oleh OS/scheduler di tengah-tengah ketiga langkah di atas).  
  Misalnya, Thread-1 dan Thread-2 sama-sama membaca `processed_count` saat nilainya masih 10. Keduanya menghitung `10 + 1 = 11`. Thread-1 lalu menulis nilai 11 ke memori. Sesaat kemudian, Thread-2 juga menuliskan nilai 11 ke memori. Dua pesanan nyata telah selesai diproses oleh dua pekerja, tetapi counter hanya bertambah satu angka. Kejadian ini dinamakan fenomena **Lost Update** yang terjadi berulang-ulang sepanjang eksekusi, sehingga dari 100 pesanan yang masuk, hanya sebagian kecil (misalnya 62) yang tercatat di counter akhir.

---

## Percobaan dengan Lock
- **Hasil `processed_count` setelah perbaikan:** `100` (selalu tepat 100 dari 100 pesanan di setiap percobaan).
- **Pesan program:** `Total pesanan diproses: 100 (seharusnya 100)`
- **Mekanisme perbaikan:**  
  Dengan membungkus proses increment menggunakan `with lock:` (`threading.Lock()`), kita mendefinisikan area tersebut sebagai **Critical Section** yang dilindungi oleh mekanisme **Mutual Exclusion (Mutex)**:
  - Sebelum thread dapat membaca dan memodifikasi `processed_count`, thread harus mengakuisisi lock (`lock.acquire()`).
  - Jika satu thread sedang memegang lock, thread-thread pekerja lain yang ingin melakukan increment dipaksa menunggu (*blocked/queued*).
  - Setelah thread selesai menuliskan nilai terbaru ke memori, lock dilepaskan secara otomatis (`lock.release()`).
  - Thread berikutnya yang mengantre akan mengambil lock dan membaca nilai yang sudah diperbarui dengan benar.  
  Dengan cara ini, operasi *read-modify-write* dipaksa berjalan secara serial dan terisolasi tanpa ada thread lain yang menyela, sehingga tidak ada pembaruan data yang hilang (*no lost updates*).

---

## Kendala Docker
- **Error yang ditemui saat `docker build`/`docker run` dan cara memperbaikinya:**
  1. *Perintah docker tidak dikenali di host Windows:*  
     Saat pertama kali menjalankan `docker --version` di PowerShell, muncul error:  
     `docker : The term 'docker' is not recognized as the name of a cmdlet, function, script file, or operable program.`  
     *Penyebab:* Docker Desktop belum terinstal atau daemon Docker belum di-start dan didaftarkan pada Environment Variable `PATH` sistem operasi.  
     *Solusi:* Menginstal Docker Desktop dengan backend WSL2 (Windows Subsystem for Linux), mengaktifkan virtualisasi hardware (VT-x / AMD-V) di BIOS laptop, lalu memastikan Docker Engine dalam status *Running*.
  2. *Optimasi Image & Dockerfile:*  
     Agar image container ringan dan tidak boros penyimpanan, skeleton Dockerfile dilengkapi dengan base image resmi `python:3.11-slim` dan perintah install `pip install --no-cache-dir -r requirements.txt` untuk mencegah penyimpanan cache instalasi yang tidak diperlukan di dalam layer container.
  3. *Verifikasi Eksekusi Container:*  
     Setelah container di-build dengan tag `foodgo-order-sim` dan dijalankan dengan perintah `docker run --rm foodgo-order-sim`, program berhasil memproses seluruh pesanan dengan output identik: `Total pesanan diproses: 100 (seharusnya 100)`.

---

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 04-10-2026 | Google Gemini | "Jelaskan mengapa race condition pada increment counter di Python bisa terjadi dan bagaimana cara kerja threading.Lock dalam mencegah lost update?" | AI menjelaskan konsep atomisitas pada level bytecode (LOAD, BINARY_ADD, STORE) dan bagaimana mutex lock menjamin serialisasi pada critical section. | Penjelasan konsep tersebut dipelajari dan diolah menjadi kode simulasi di `src/order_simulator.py` dengan menambahkan pembagian beban kerja thread dan proteksi `with lock:`, serta ditulis ulang dalam bahasa sendiri di jurnal. |
| 04-10-2026 | Claude | "Bandingkan overhead memori dan resource antara model thread pool vs fork() process pada server order backend saat ada lonjakan 100 request bersamaan." | AI menjelaskan perbandingan arsitektur thread (shared address space, stack kecil) vs process (PCB terpisah, copy-on-write, duplikasi memory map). | Kelompok merumuskan analisis komparatif di README.md yang mengaitkan langsung teori tersebut ke kasus nyata FoodGo yang kehabisan memori akibat fork() per request. |
