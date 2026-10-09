"""
Tugas 4 - Jalur A: RPC Client (simulasi modul Pesanan)
Jalankan server.py di terminal lain terlebih dahulu.
"""

import xmlrpc.client
import time


def main():
    # Buat ServerProxy ke server RPC di localhost port 8000
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000")

    # === Uji 1: Cek Saldo ===
    print("=" * 50)
    print("Memanggil cek_saldo('user1') ... menunggu respons sinkron")
    start = time.time()
    saldo = proxy.cek_saldo("user1")
    elapsed = time.time() - start
    print(f"  Saldo user1: Rp{saldo:,.0f}")
    print(f"  Waktu tempuh RPC: {elapsed:.4f} detik")
    print(f"  (Client MENUNGGU sampai server membalas — ini sifat sinkron RPC)")

    # === Uji 2: Proses Pembayaran Sukses ===
    print("\n" + "=" * 50)
    print("Memanggil proses_pembayaran('user1', 20000) ...")
    start = time.time()
    hasil = proxy.proses_pembayaran("user1", 20000)
    elapsed = time.time() - start
    print(f"  Hasil: {hasil}")
    print(f"  Waktu tempuh RPC: {elapsed:.4f} detik")

    # === Uji 3: Cek Saldo Setelah Pembayaran ===
    print("\n" + "=" * 50)
    print("Memanggil cek_saldo('user1') lagi setelah pembayaran ...")
    saldo_baru = proxy.cek_saldo("user1")
    print(f"  Saldo user1 sekarang: Rp{saldo_baru:,.0f}")

    # === Uji 4: Pembayaran dengan Saldo Tidak Cukup ===
    print("\n" + "=" * 50)
    print("Memanggil proses_pembayaran('user1', 999999) — saldo tidak cukup ...")
    hasil_gagal = proxy.proses_pembayaran("user1", 999999)
    print(f"  Hasil: {hasil_gagal}")

    # === Uji 5: Cek Saldo User Tidak Ada ===
    print("\n" + "=" * 50)
    print("Memanggil cek_saldo('user_tidak_ada') ...")
    saldo_kosong = proxy.cek_saldo("user_tidak_ada")
    print(f"  Saldo: Rp{saldo_kosong:,.0f} (user tidak terdaftar)")

    print("\n" + "=" * 50)
    print("Semua panggilan RPC selesai.")


if __name__ == "__main__":
    main()
