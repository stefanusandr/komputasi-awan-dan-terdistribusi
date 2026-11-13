"""
Tugas 7 (opsional) - Simulasi Replikasi Dua Server (Jakarta & Bandung)

Mensimulasikan delay replikasi dan masalah inconsistent read,
lalu memperbaikinya dengan mekanisme Read-Your-Writes sederhana.
"""

import time
import threading

REPLICATION_DELAY = 2.0  # detik, simulasi lambatnya sinkronisasi antar server


class Replica:
    def __init__(self, name: str):
        self.name = name
        self.saldo: dict[str, float] = {}
        self.last_write_version: dict[str, int] = {}

    def write(self, user_id: str, saldo_baru: float, version: int):
        self.saldo[user_id] = saldo_baru
        self.last_write_version[user_id] = version
        print(f"[{self.name}] WRITE saldo {user_id} = {saldo_baru:.1f} (versi {version})")

    def read(self, user_id: str) -> float:
        return self.saldo.get(user_id, 0.0)


class ReplicationSystem:
    def __init__(self):
        self.jakarta = Replica("Jakarta")
        self.bandung = Replica("Bandung")
        self.version_counter = 0

    def top_up(self, user_id: str, jumlah: float):
        """Top-up selalu ditulis dulu ke server Jakarta (mis. server terdekat pelanggan)."""
        self.version_counter += 1
        version = self.version_counter
        saldo_baru = self.jakarta.read(user_id) + jumlah
        self.jakarta.write(user_id, saldo_baru, version)

        # TODO 1: replikasi ke Bandung TERTUNDA (simulasikan dengan
        # threading.Timer(REPLICATION_DELAY, ...) yang memanggil
        # self.bandung.write(user_id, saldo_baru, version) setelah delay.
        print(f"[REPLIKASI] Memulai proses replikasi asinkron ke server Bandung (delay {REPLICATION_DELAY} detik)...")
        timer = threading.Timer(
            REPLICATION_DELAY,
            self.bandung.write,
            args=(user_id, saldo_baru, version)
        )
        timer.daemon = True
        timer.start()

    def baca_saldo_naif(self, user_id: str, server: str) -> float:
        """Baca saldo TANPA mekanisme Read-Your-Writes - bisa saja stale."""
        replica = self.jakarta if server == "Jakarta" else self.bandung
        return replica.read(user_id)

    def baca_saldo_read_your_writes(self, user_id: str, server: str, versi_minimal: int, mode: str = "redirect") -> float:
        """TODO 2: implementasikan Read-Your-Writes -
        jika replika yang dituju versi datanya < versi_minimal (client pernah
        melihat versi lebih baru sebelumnya), tunggu/redirect ke replika yang
        sudah punya versi tersebut (di sini cukup simulasikan dengan polling
        sampai versi replika >= versi_minimal, atau redirect ke Jakarta)."""
        replica = self.jakarta if server == "Jakarta" else self.bandung
        versi_lokal = replica.last_write_version.get(user_id, 0)

        if versi_lokal < versi_minimal:
            print(f"[RYW Guard] Server {server} versi data={versi_lokal} < versi minimal klien={versi_minimal} (DATA STALE/KEDALUWARSA)!")
            if mode == "redirect":
                print(f"[RYW Guard] -> Tindakan: Meredirect pembacaan ke server Jakarta (Master / Up-to-date)...")
                return self.jakarta.read(user_id)
            elif mode == "wait":
                print(f"[RYW Guard] -> Tindakan: Menunggu (polling) replika {server} hingga tersinkronisasi...")
                while replica.last_write_version.get(user_id, 0) < versi_minimal:
                    time.sleep(0.1)
                print(f"[RYW Guard] -> Server {server} selesai tersinkronisasi ke versi {replica.last_write_version.get(user_id, 0)}.")
                return replica.read(user_id)

        print(f"[RYW Guard] Server {server} data mutakhir (versi {versi_lokal} >= {versi_minimal}). Pembacaan lokal aman.")
        return replica.read(user_id)


def main():
    system = ReplicationSystem()
    user_id = "user1"

    print("================================================================")
    print("=== Skenario 1: Pembacaan NAIF (Tanpa Read-Your-Writes) ===")
    print("================================================================")
    print(f"[*] Pelanggan '{user_id}' melakukan TOP-UP sebesar Rp 50.000 ke Server Jakarta...")
    system.top_up(user_id, 50000)

    print("\n[*] Pelanggan langsung memesan makanan via Server Bandung setelah 0.5 detik...")
    time.sleep(0.5)  # pelanggan langsung pesan makanan < REPLICATION_DELAY detik kemudian
    saldo_terbaca = system.baca_saldo_naif(user_id, "Bandung")
    print(f"[*] Hasil baca saldo dari Bandung (naif): Rp {saldo_terbaca:.1f}")
    print("[-] HASIL: Harusnya Rp 50.000, tapi karena delay replikasi, terbaca Rp 0.0 (BUG / Inconsistent Read!)")
    print("[-] DAMPAK: Transaksi pesanan makanan DITOLAK karena saldo dianggap tidak mencukupi.")

    print(f"\n[*] Menunggu sinkronisasi replikasi selesai ({REPLICATION_DELAY} detik)...")
    time.sleep(REPLICATION_DELAY + 0.5)
    print(f"[*] Saldo di Bandung setelah replikasi selesai: Rp {system.baca_saldo_naif(user_id, 'Bandung'):.1f} (Eventual Consistency tercapai)")

    print("\n================================================================")
    print("=== Skenario 2: Pembacaan dengan READ-YOUR-WRITES (Solusi) ===")
    print("================================================================")
    print(f"[*] Pelanggan '{user_id}' melakukan TOP-UP tambahan sebesar Rp 20.000 ke Server Jakarta...")
    system.top_up(user_id, 20000)
    versi_terakhir = system.version_counter
    print(f"[*] Token / Context Klien menyimpan metadata versi transaksi terakhir: Versi {versi_terakhir}")

    print("\n[*] Uji Kasus A (Pendekatan Redirect):")
    print("[*] Pelanggan mengakses Server Bandung setelah 0.5 detik membawa token Versi 2...")
    time.sleep(0.5)
    
    # TODO 3: panggil baca_saldo_read_your_writes dan tunjukkan hasilnya SELALU benar
    # walau dipanggil segera setelah top_up (< REPLICATION_DELAY detik).
    saldo_ryw_redirect = system.baca_saldo_read_your_writes(user_id, "Bandung", versi_terakhir, mode="redirect")
    print(f"[+] Hasil saldo terbaca (Read-Your-Writes - Redirect): Rp {saldo_ryw_redirect:.1f}")
    if saldo_ryw_redirect == 70000.0:
        print("[+] STATUS: SUKSES! Saldo terbaca mutakhir (Rp 70.000). Transaksi pesanan berhasil diproses!")

    print("\n[*] Uji Kasus B (Pendekatan Wait / Sync-on-Demand):")
    print("[*] Mensimulasikan klien yang bersedia menunggu sinkronisasi selesai:")
    saldo_ryw_wait = system.baca_saldo_read_your_writes(user_id, "Bandung", versi_terakhir, mode="wait")
    print(f"[+] Hasil saldo terbaca (Read-Your-Writes - Wait): Rp {saldo_ryw_wait:.1f}")
    if saldo_ryw_wait == 70000.0:
        print("[+] STATUS: SUKSES! Server Bandung berhasil menyajikan saldo yang konsisten setelah replikasi tiba.")


if __name__ == "__main__":
    main()
