"""
Tugas 4 - Jalur A: RPC Server (simulasi modul Pembayaran)
Memakai xmlrpc.server dari Python standard library - tidak perlu install apa pun.
"""

from xmlrpc.server import SimpleXMLRPCServer

# Simulasi "database" saldo user
saldo_user = {
    "user1": 50000,
    "user2": 120000,
}


def cek_saldo(user_id: str) -> float:
    """Kembalikan saldo user_id saat ini."""
    # Jika user_id tidak ditemukan, kembalikan 0 (bukan raise error)
    # agar client tetap mendapat respons yang valid dan bisa menangani
    # kasus "user tidak ditemukan" di sisi client tanpa crash.
    if user_id in saldo_user:
        print(f"  -> cek_saldo('{user_id}') = {saldo_user[user_id]}")
        return saldo_user[user_id]
    else:
        print(f"  -> cek_saldo('{user_id}') = 0 (user tidak ditemukan)")
        return 0


def proses_pembayaran(user_id: str, jumlah: float) -> dict:
    """Kurangi saldo user sejumlah `jumlah`. Kembalikan status hasil."""
    # Validasi: user harus ada di database
    if user_id not in saldo_user:
        print(f"  -> proses_pembayaran('{user_id}', {jumlah}) GAGAL: user tidak ditemukan")
        return {"status": "gagal", "alasan": "user tidak ditemukan", "saldo_akhir": 0}

    # Validasi: saldo harus cukup
    if saldo_user[user_id] < jumlah:
        print(f"  -> proses_pembayaran('{user_id}', {jumlah}) GAGAL: saldo tidak cukup")
        return {
            "status": "gagal",
            "alasan": "saldo tidak cukup",
            "saldo_akhir": saldo_user[user_id],
        }

    # Kurangi saldo
    saldo_user[user_id] -= jumlah
    print(f"  -> proses_pembayaran('{user_id}', {jumlah}) SUKSES: saldo akhir = {saldo_user[user_id]}")
    return {"status": "sukses", "saldo_akhir": saldo_user[user_id]}


def main():
    server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
    # Daftarkan kedua fungsi agar bisa dipanggil via RPC
    server.register_function(cek_saldo, "cek_saldo")
    server.register_function(proses_pembayaran, "proses_pembayaran")
    print("RPC server modul Pembayaran berjalan di port 8000...")
    print("Tekan Ctrl+C untuk menghentikan server.\n")
    server.serve_forever()


if __name__ == "__main__":
    main()
