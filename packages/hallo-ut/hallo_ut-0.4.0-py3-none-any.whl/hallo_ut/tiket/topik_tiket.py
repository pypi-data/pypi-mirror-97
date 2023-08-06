from enum import Enum


class TopikTiket(Enum):
    INFO_UT = 1, "Info UT"
    IJAZAH = 8, "Ijazah"
    BEASISWA = 9, "Beasiswa"
    BAHAN_AJAR = 10, "Bahan Ajar"
    ALIH_KREDIT_MATA_KULIAH = 11, "Alih Kredit Mata Kuliah"
    KELULUSAN_YUDISIUM = 13, "Kelulusan/Yudisium"
    NILAI = 14, "Nilai"
    UJIAN = 15, "Ujian"
    BEDA_TANDA_TANGAN = 17, "Beda Tanda Tangan"
    EMAIL_E_CAMPUS = 19, "Email e-campus"
    FORLAP_DIKTI = 21, "Forlap Dikti"
    KTME = 23, "KTME"
    KARIL = 25, "Karil"
    LKAM = 28, "LKAM"
    LATIHAN_MANDIRI = 30, "Latihan Mandiri"
    NILAI_ADA_TP_TDK_TERBIT_DI_LKAM = 33, "Nilai ada tp tdk terbit di LKAM"
    PMKM = 35, "PMKM"
    PEMBAYARAN_SPP = 37, "Pembayaran SPP"
    PEMBEBASAN_MATAKULIAH = 39, "Pembebasan Matakuliah"
    PENAWARAN_KERJASAMA = 41, "Penawaran Kerjasama"
    PENGEMBALIAN_SPP = 43, "Pengembalian SPP"
    PENGGUGURAN_MATAKULIAH = 45, "Pengguguran Matakuliah"
    PENUNDAAN_YUDISIUM = 47, "Penundaan Yudisium"
    PERSETUJUAN_ALIH_KREDIT = 49, "Persetujuan Alih Kredit"
    PERUBAHAN_DATA_PRIBADI = 51, "Perubahan Data Pribadi"
    PINDAH_PROGRAM_STUDI = 53, "Pindah Program Studi"
    PINDAH_UPBJJ = 55, "Pindah UPBJJ"
    PRAKTEK_PRAKTIKUM = 57, "Praktek/Praktikum"
    PROGRAM_SERTIFIKAT = 59, "Program Sertifikat"
    REGISTRASI = 61, "Registrasi"
    RUANG_BACA_VIRTUAL = 63, "Ruang Baca Virtual"
    SUKET_ALUMNI = 65, "Suket Alumni"
    SUKET_KELULUSAN = 67, "Suket Kelulusan"
    SUKET_MAHASISWA_AKTIF = 69, "Suket Mahasiswa Aktif"
    SUKET_PENONAKTIFAN_PINDAH = 71, "Suket Penonaktifan (Pindah)"
    TIDAK_PUAS_NILAI_UAS = 73, "Tidak puas nilai UAS"
    TUTORIAL_TUGAS = 75, "Tutorial/Tugas"
    WISUDA_UPI = 78, "Wisuda/UPI"
    OFFICE_365 = 87, "Office 365"
    TAP_TUGAS_AKHIR_PROGRAM = 91, "TAP (Tugas Akhir Program)"
    FAKULTAS_DAN_PROGRAM_STUDI = 92, "Fakultas dan Program Studi"
    MAHASISWA_UT = 93, "Mahasiswa UT"
    TUGAS_MATAKULIAH_REMEDIASI = 95, "Tugas Matakuliah (Remediasi)"
    UAS_UJIAN_AKHIR_SEMESTER = 97, "UAS (Ujian Akhir Semester)"
    UANG_KULIAH_SPP = 99, "Uang kuliah/SPP"

    def __str__(self) -> str:
        return self.value[1]

    @property
    def id(self) -> int:
        return self.value[0]
