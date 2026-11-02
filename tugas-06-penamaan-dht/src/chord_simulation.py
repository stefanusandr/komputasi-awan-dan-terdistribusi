"""
Tugas 6 - Simulasi Chord DHT (single-process, tanpa jaringan sungguhan)

Fungsi hashing & struktur data ring sudah disediakan.
Lengkapi TODO untuk lookup(), join(), dan leave().
"""

import hashlib

M_BITS = 8               # ruang identifier 0..255 (disederhanakan dari Chord asli yang pakai 160-bit)
RING_SIZE = 2 ** M_BITS


def hash_id(key: str) -> int:
    """Hash string (ID node atau ID kurir) ke ruang identifier 0..RING_SIZE-1."""
    digest = hashlib.sha1(key.encode()).digest()
    return int.from_bytes(digest, "big") % RING_SIZE


class ChordRing:
    def __init__(self):
        # node_id (hasil hash) -> alamat IP node tersebut
        self.nodes: dict[int, str] = {}
        # key kurir (hasil hash) -> IP kurir yang disimpan node yang bertanggung jawab
        self.data: dict[int, tuple[str, str]] = {}  # hash -> (kurir_id, ip_kurir)

    def join(self, node_name: str, node_ip: str):
        """Tambahkan node baru ke ring. Pindahkan data yang seharusnya
        menjadi tanggung jawab node baru ini dari successor lamanya."""
        node_id = hash_id(node_name)

        # TODO 1: tambahkan node_id -> node_ip ke self.nodes.
        self.nodes[node_id] = node_ip
        print(f"[JOIN] Node '{node_name}' (id={node_id}) bergabung, alamat {node_ip}")

        # TODO 2: cari successor LAMA dari node_id ini (successor sebelum node
        # baru bergabung, gunakan find_successor() — karena node baru sudah masuk,
        # successor-nya mungkin diri sendiri jika hanya 1 node, atau node lain).
        # Kita perlu cari node yang SEBELUMNYA bertanggung jawab atas key di sekitar node_id.
        # Caranya: cari successor dari (node_id + 1) % RING_SIZE agar tidak dapat diri sendiri.
        if len(self.nodes) > 1:
            old_successor_id = self.find_successor((node_id + 1) % RING_SIZE)

            # TODO 3: pindahkan semua key di self.data yang seharusnya menjadi
            # tanggung jawab node baru (key yang sekarang successor-nya adalah node_id,
            # bukan lagi old_successor) dari old_successor ke node baru.
            keys_to_transfer = []
            for key_hash, (kurir_id, ip_kurir) in self.data.items():
                responsible_node = self.find_successor(key_hash)
                if responsible_node == node_id:
                    keys_to_transfer.append(key_hash)

            for key_hash in keys_to_transfer:
                kurir_id, ip_kurir = self.data[key_hash]
                print(f"  -> Key '{kurir_id}' (hash={key_hash}) berpindah "
                      f"dari Node {old_successor_id} ({self.nodes[old_successor_id]}) "
                      f"ke Node {node_id} ({node_ip})")
        else:
            print(f"  -> Node pertama di ring, menjadi penanggung jawab semua key.")

    def leave(self, node_name: str):
        """Keluarkan sebuah node dari ring. Data yang dipegangnya harus
        berpindah ke successor-nya."""
        node_id = hash_id(node_name)

        if node_id not in self.nodes:
            print(f"[ERROR] Node '{node_name}' (id={node_id}) tidak ditemukan di ring")
            return

        leaving_ip = self.nodes[node_id]
        print(f"[LEAVE] Node '{node_name}' (id={node_id}, ip={leaving_ip}) keluar dari ring")

        # TODO 4: hapus node_id dari self.nodes.
        del self.nodes[node_id]

        if not self.nodes:
            print("  -> Ring kosong, tidak ada node tersisa.")
            return

        # TODO 5: cari successor BARU untuk tiap key yang tadinya dipegang
        # node ini, pindahkan ke successor tersebut.
        for key_hash, (kurir_id, ip_kurir) in self.data.items():
            new_successor_id = self.find_successor(key_hash)
            # Hanya cetak perpindahan untuk key yang tadinya dipegang node yang keluar
            # (yaitu key yang successor-nya berubah karena node_id dihapus)
            print(f"  -> Key '{kurir_id}' (hash={key_hash}) sekarang tanggung jawab "
                  f"Node {new_successor_id} ({self.nodes[new_successor_id]})")

    def find_successor(self, key_hash: int) -> int:
        """Cari node_id dengan nilai hash TERKECIL yang >= key_hash
        (successor menurut aturan Chord). Jika tidak ada, wrap-around
        ke node dengan hash terkecil di ring (karena ring melingkar)."""
        # TODO 6: implementasikan logika successor di atas menggunakan
        # self.nodes.keys(). Kembalikan node_id (bukan IP).
        if not self.nodes:
            return -1

        sorted_nodes = sorted(self.nodes.keys())

        # Cari node_id terkecil yang >= key_hash (linear scan pada ring terurut)
        for nid in sorted_nodes:
            if nid >= key_hash:
                return nid

        # Jika tidak ada yang >= key_hash, wrap-around ke node terkecil
        return sorted_nodes[0]

    def register_kurir(self, kurir_id: str, ip_kurir: str):
        """Simpan mapping ID Kurir -> IP di node yang bertanggung jawab."""
        key_hash = hash_id(kurir_id)
        # TODO 7: panggil find_successor(key_hash) untuk menentukan node
        # penanggung jawab, lalu simpan (kurir_id, ip_kurir) ke self.data[key_hash].
        responsible_node = self.find_successor(key_hash)
        self.data[key_hash] = (kurir_id, ip_kurir)
        print(f"[REGISTER] Kurir '{kurir_id}' (hash={key_hash}, ip={ip_kurir}) "
              f"-> disimpan di Node {responsible_node} ({self.nodes[responsible_node]})")

    def lookup(self, kurir_id: str) -> str | None:
        """Cari alamat IP terkini untuk sebuah ID Kurir."""
        key_hash = hash_id(kurir_id)
        # TODO 8: gunakan find_successor(key_hash) untuk menemukan node
        # penanggung jawab, lalu kembalikan ip_kurir dari self.data jika ada.
        responsible_node = self.find_successor(key_hash)
        if key_hash in self.data:
            kurir_id_stored, ip_kurir = self.data[key_hash]
            print(f"[LOOKUP] '{kurir_id}' (hash={key_hash}) -> ditemukan di Node "
                  f"{responsible_node} ({self.nodes[responsible_node]}), IP: {ip_kurir}")
            return ip_kurir
        else:
            print(f"[LOOKUP] '{kurir_id}' (hash={key_hash}) -> TIDAK DITEMUKAN")
            return None

    def print_ring_state(self):
        """Cetak kondisi ring saat ini: node dan data yang dipegang."""
        print("\n" + "=" * 60)
        print("STATUS RING CHORD")
        print("=" * 60)
        sorted_nodes = sorted(self.nodes.keys())
        print(f"Node aktif ({len(sorted_nodes)}): ", end="")
        print(" -> ".join(f"[{nid}]" for nid in sorted_nodes) +
              (f" -> [{sorted_nodes[0]}] (wrap)" if sorted_nodes else ""))
        print()

        for nid in sorted_nodes:
            # Cari key yang menjadi tanggung jawab node ini
            responsible_keys = []
            for key_hash, (kurir_id, ip_kurir) in self.data.items():
                if self.find_successor(key_hash) == nid:
                    responsible_keys.append((key_hash, kurir_id, ip_kurir))
            print(f"  Node {nid} ({self.nodes[nid]}):")
            if responsible_keys:
                for kh, kid, kip in responsible_keys:
                    print(f"    - {kid} (hash={kh}) -> {kip}")
            else:
                print(f"    - (tidak ada key)")
        print("=" * 60 + "\n")


def main():
    ring = ChordRing()

    # Skenario awal: 4 node bergabung
    print("=" * 60)
    print("SKENARIO: 4 NODE BERGABUNG KE RING")
    print("=" * 60)
    ring.join("node-jakarta-1", "10.0.0.1")
    ring.join("node-jakarta-2", "10.0.0.2")
    ring.join("node-bandung-1", "10.0.0.3")
    ring.join("node-surabaya-1", "10.0.0.4")

    ring.print_ring_state()

    # Daftarkan beberapa kurir
    print("=" * 60)
    print("SKENARIO: REGISTRASI KURIR")
    print("=" * 60)
    ring.register_kurir("kurir-001", "192.168.1.10")
    ring.register_kurir("kurir-002", "192.168.1.11")
    ring.register_kurir("kurir-003", "192.168.1.12")

    ring.print_ring_state()

    print("\n--- Lookup sebelum perubahan topologi ---")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))
    print("kurir-003 ->", ring.lookup("kurir-003"))

    print("\n" + "=" * 60)
    print("SKENARIO: NODE BARU BERGABUNG (node-medan-1)")
    print("=" * 60)
    ring.join("node-medan-1", "10.0.0.5")
    ring.print_ring_state()

    print("--- Lookup setelah node baru bergabung ---")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))
    print("kurir-003 ->", ring.lookup("kurir-003"))

    print("\n" + "=" * 60)
    print("SKENARIO: NODE KELUAR (node-bandung-1)")
    print("=" * 60)
    ring.leave("node-bandung-1")
    ring.print_ring_state()

    print("--- Lookup setelah node keluar ---")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))
    print("kurir-003 ->", ring.lookup("kurir-003"))


if __name__ == "__main__":
    main()
