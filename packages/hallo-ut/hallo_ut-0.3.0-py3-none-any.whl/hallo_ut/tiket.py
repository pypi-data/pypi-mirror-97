import attr
import requests
from bs4 import BeautifulSoup, Tag
from typing import List

from .constants import STATUS_TIKET_URL


def status_from_page_top(section: Tag) -> bool:
    span: Tag = section.find("span")
    return "OPEN" in span.getText()


@attr.dataclass(slots=True)
class Tiket:
    status: bool
    judul: str
    nama: str
    email: str
    topik: str
    nomer: str
    pesan: str

    def __str__(self) -> str:
        text = f"Judul: {self.judul}\n"
        text += f"Nama: {self.nama}\n"
        text += f"Email: {self.email}\n"
        text += f"Topik: {self.topik}  "
        text += f"Nomer Ticket: {self.nomer}\n"
        text += "Pesan:\n\n" + self.pesan
        return text

    def __bool__(self) -> bool:
        return self.status

    @classmethod
    def from_noticket(cls, noticket: str) -> "Tiket":
        params = {"noticket": noticket}
        res = requests.get(STATUS_TIKET_URL, params=params)
        if not res.ok or not res.text or "Tiket Tidak Ditemukan" in res.text:
            raise ValueError("Tiket tidak ditemukan atau Hallo-ut tidak bisa dihubungi")
        soup = BeautifulSoup(res.text, "html.parser")
        status = status_from_page_top(soup.find("section", class_="page-top"))
        return cls.from_table(
            table=soup.find("table"),
            status=status,
        )

    @classmethod
    def from_table(cls, table: Tag, status: bool) -> "Tiket":
        tr_tags: Tag = table.find_all("tr")
        judul, nama, email, topik, nomer, pesan = "", "", "", "", "", ""
        nama = tr_tags[0].contents[5].getText()
        judul = tr_tags[0].contents[13].getText()
        email = tr_tags[1].contents[5].getText()
        topik = tr_tags[1].contents[13].getText()
        nomer = tr_tags[2].contents[5].getText()
        pesan = str(tr_tags[2].contents[13])
        return cls(
            status=status,
            judul=judul,
            nama=nama,
            email=email,
            topik=topik,
            nomer=nomer,
            pesan=pesan,
        )
