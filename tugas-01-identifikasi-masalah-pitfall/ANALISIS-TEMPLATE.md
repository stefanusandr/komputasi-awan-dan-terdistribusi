# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [kelompok 3]

| Nama | NIM | Kontribusi |
|---|---|---|
| [Stefanus Andri Hendrawan] | [103072400115] | [pitfall 1] |
| [nama 2] | [nim] | [pitfall/bagian yang dikerjakan] |
| [nama 3] | [nim] | [pitfall/bagian yang dikerjakan] |

## Pitfall 1: [he network is reliable] — ditulis oleh [Stefanus Andri hendrawan]

**Bukti di skenario:** [" # network is always reliable, no need for retry "]

**Kenapa ini keliru:** [dalam koneksi akan selalu ada yang namanya paket hilang]

**Dampak ke FoodGo:** [jika koneksi pembayaran mengalami paket hilang atau drop, maka prosesnya akan menggantung tanpa adanya pemulihan]

**Solusi desain awal:** [berikan jarak pada setiap panggilan jaringan agar saat terjadi pembayaran gagal karena kendala jaringan maka sistem akan secara otomatis akan melakukan percobaan ulang]

**Trade-off:** [developer harus merubah kode agar saat kode gagal dan melakukan percobaan maka proses tidak akan menggantung]

---

## Pitfall 2: [Latency is Zero] — ditulis oleh [nama]

**Bukti di skenario:** [.tidak ada timeout sama sekali pada pemanggilan antar service (modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu)." dan "Aplikasi jadi sangat lambat, beberapa permintaan timeout]

**Kenapa ini keliru:** [          ]

**Dampak ke FoodGo:** [          ]

**Solusi desain awal:**  [        ]

**Trade-off:** [        ]

---

## Pitfall 3: [Single Point of Failure] — ditulis oleh [nama]

**Bukti di skenario:** [        ]

**Kenapa ini keliru:** [          ]

**Dampak ke FoodGo:** [          ]

**Solusi desain awal:**  [        ]

**Trade-off:** [        ]

---

## Kesimpulan Kelompok

[kegagalan sistem yang pada foodGo pada saat traffic sedang tinggi itu dikarenakan kesalahan pada design yang ada dalam jaringan dan arsitektur sistem terdistribusi, seperti : 
1. menganggap jaringan selalu andal yang membuat sistem tidak siap saat terjadi paket hilang atau drop
2. mengabaikan Latency dan tidak melakukan timeout pada pemanggilan antar service 
3. menggunakan design Single Point of Failure yang menyebabkan modul pembayaran menjadi bottleneck yang dimana akan membuat beban di suatu modul dan akan langsung melumpuhkan seluruh server] 