"""
Tugas 3 - Simulasi Pesanan Masuk dengan Multithreading

Skeleton ini sengaja belum lengkap. Isi bagian bertanda TODO.
Jangan mengubah nama fungsi (dipakai untuk pengecekan otomatis oleh asisten).
"""

import threading
import random
import time

NUM_ORDERS = 100        # jumlah pesanan simulasi yang masuk
NUM_WORKERS = 10        # jumlah thread pekerja

# Counter bersama untuk menghitung total pesanan yang berhasil diproses.
# Sengaja rawan race condition jika diakses tanpa proteksi.
processed_count = 0

# TODO 1: Buat objek Lock di sini untuk melindungi `processed_count`.
lock = threading.Lock()


def process_order(order_id: int) -> None:
    """Proses satu pesanan. Dipanggil oleh tiap thread pekerja."""
    global processed_count

    # Simulasikan kerja nyata (mis. validasi, hitung total harga)
    time.sleep(random.uniform(0.001, 0.01))

    # TODO 2: Tambahkan increment `processed_count` DI SINI.
    # Langkah 2 (Perbaikan dengan Lock): Critical section dilindungi dengan threading.Lock()
    with lock:
        current = processed_count
        time.sleep(0.0001)  # Simulasi jeda mikro, aman karena berada dalam lock
        processed_count = current + 1


def worker(order_ids: list) -> None:
    """Satu thread pekerja memproses sekumpulan order_id."""
    for order_id in order_ids:
        process_order(order_id)


def main() -> None:
    order_ids = list(range(1, NUM_ORDERS + 1))

    # TODO 3: Bagi `order_ids` menjadi NUM_WORKERS bagian, buat satu
    # threading.Thread per bagian yang menjalankan `worker(...)`,
    # start semua thread, lalu join semua thread sebelum lanjut.
    threads = []
    chunk_size = len(order_ids) // NUM_WORKERS
    for i in range(NUM_WORKERS):
        start_idx = i * chunk_size
        end_idx = (i + 1) * chunk_size if i < NUM_WORKERS - 1 else len(order_ids)
        chunk = order_ids[start_idx:end_idx]
        t = threading.Thread(target=worker, args=(chunk,), name=f"Worker-{i+1}")
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"Total pesanan diproses: {processed_count} (seharusnya {NUM_ORDERS})")
    if processed_count != NUM_ORDERS:
        print("RACE CONDITION TERDETEKSI - lengkapi TODO 1 & TODO 2 dengan Lock!")


if __name__ == "__main__":
    main()
