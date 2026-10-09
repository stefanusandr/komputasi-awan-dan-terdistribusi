"""
Tugas 4 - Jalur B: Publisher (simulasi modul Pembayaran)
Pastikan `docker compose up -d` sudah jalan sebelum menjalankan file ini.
"""

import pika
import json
import time

QUEUE_NAME = "pembayaran_berhasil"


def main():
    # Buat koneksi ke RabbitMQ di localhost
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()

    # Deklarasikan queue dengan durable=True supaya pesan tidak hilang
    # walau RabbitMQ restart
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    print(f"Publisher terhubung ke RabbitMQ. Mengirim 3 event ke queue '{QUEUE_NAME}'...\n")

    for i in range(1, 4):
        pesan = {
            "user_id": f"user{i}",
            "jumlah": 20000 * i,
            "timestamp": time.time(),
        }
        # Publish pesan ke queue dengan delivery_mode=2 (persistent)
        # agar pesan tetap tersimpan di disk meskipun RabbitMQ restart
        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=json.dumps(pesan),
            properties=pika.BasicProperties(
                delivery_mode=2,  # persistent message
            ),
        )
        print(f"  Event terkirim: {pesan}")
        time.sleep(1)

    # Tutup koneksi setelah selesai
    connection.close()
    print("\nPublisher selesai mengirim event. Koneksi ditutup.")


if __name__ == "__main__":
    main()

