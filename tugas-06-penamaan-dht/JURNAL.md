# Jurnal Proses — Tugas 6

## Implementasi find_successor

- **Kesalahan pertama:** Lupa menangani kasus _wrap-around_ pada ring melingkar. Saat mencari successor dari key_hash yang nilainya lebih besar dari semua node yang ada di ring (misalnya key hash 200 pada ring dengan node terbesar 177), fungsi mengembalikan `None` alih-alih wrap ke node terkecil.
- **Cara memperbaikinya:** Menambahkan logika fallback di akhir iterasi — jika tidak ada node dengan hash ≥ key_hash ditemukan setelah iterasi seluruh sorted_nodes, maka kembalikan `sorted_nodes[0]` (node terkecil, karena ring melingkar).

- **Kesalahan kedua:** Pada awalnya menggunakan `>` (strictly greater) alih-alih `>=` (greater or equal) untuk membandingkan node_id dengan key_hash. Ini menyebabkan key yang hash-nya tepat sama dengan node_id tidak dianggap milik node tersebut.
- **Cara memperbaikinya:** Mengubah kondisi menjadi `nid >= key_hash` sesuai aturan Chord: successor adalah node dengan ID hash **terkecil yang lebih besar ATAU SAMA DENGAN** hash key.

## Implementasi join

- **Kesalahan:** Saat node baru bergabung, perlu mencari successor lama untuk menentukan key mana yang harus dipindahkan. Awalnya salah memanggil `find_successor(node_id)` yang mengembalikan node baru itu sendiri (karena sudah ditambahkan ke `self.nodes`).
- **Cara memperbaikinya:** Memanggil `find_successor((node_id + 1) % RING_SIZE)` agar mendapatkan node **setelah** node baru di ring, yang merupakan successor lama yang sebelumnya memegang key tersebut.

## Implementasi leave

- **Kesalahan:** Awalnya mencoba mencari successor baru sebelum menghapus node dari `self.nodes`, sehingga `find_successor()` masih mengembalikan node yang sedang keluar sebagai successor.
- **Cara memperbaikinya:** Urutan operasi diubah — hapus dulu node dari `self.nodes`, baru iterasi seluruh key di `self.data` dan panggil `find_successor()` untuk menentukan penanggung jawab baru.

## Skenario join/leave

### Hasil sebelum & sesudah node baru bergabung:

- **Sebelum (4 node):** Ring `[40] -> [102] -> [136] -> [177]`, kurir-002 (hash=28) di Node 40, kurir-001 (hash=50) di Node 102, kurir-003 (hash=132) di Node 136.
- **Sesudah (5 node, node-medan-1 id=123 bergabung):** Ring `[40] -> [102] -> [123] -> [136] -> [177]`. Tidak ada key yang berpindah karena tidak ada key dengan hash di rentang (102, 123].

### Hasil sebelum & sesudah node keluar:

- **Sebelum (5 node):** kurir-002 dipegang Node 40.
- **Sesudah (node-bandung-1/Node 40 keluar, 4 node tersisa):** Ring menjadi `[102] -> [123] -> [136] -> [177]`. kurir-002 (hash=28) berpindah ke Node 102 (successor baru). kurir-001 dan kurir-003 tetap di tempatnya.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal    | Tool AI              | Prompt yang diberikan                                                                                          | Ringkasan saran/ide AI                                                             | Bagaimana diolah jadi tulisan/kode sendiri                                                                                                                         |
| ---------- | -------------------- | -------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 2026-11-02 | Antigravity (Gemini) | Meminta bantuan brainstorming ide outline untuk analisis mengapa DHT lebih cocok dibanding flat naming dan DNS | AI menyarankan outline poin: SPOF, bottleneck, TTL caching DNS, consistent hashing | Poin-poin di-review, dielaborasi sendiri dengan penjelasan teknis spesifik ke kasus FoodGo (IP kurir dinamis), argumen ditulis ulang dengan konteks skenario nyata |
