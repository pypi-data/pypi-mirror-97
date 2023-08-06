import attr
import bleach
import requests
from bs4 import BeautifulSoup, Tag
from requests_toolbelt import MultipartEncoder
from typing import List, Optional, BinaryIO

from hallo_ut.constants import STATUS_TIKET_URL, IGNORED_TAGS
from . import TopikTiket, PriorityTiket


def status_from_page_top(section: Tag) -> bool:
    span: Tag = section.find("span")
    return "OPEN" in span.getText()


class BaseTiket:
    TOPIK = TopikTiket
    PRIORITY = PriorityTiket


@attr.dataclass(slots=True)
class Tiket(BaseTiket):
    status: bool
    judul: str
    nama: str
    email: str
    topik: str
    nomer: str
    pesan: str

    def __str__(self) -> str:
        text = f"Judul: {self.judul}\n"
        text += "Status: "
        if self.status:
            text += "OPEN\n"
        else:
            text += "CLOSE\n"
        text += f"Nama: {self.nama}\n"
        text += f"Email: {self.email}\n"
        text += f"Topik: {self.topik}\n"
        text += f"Nomer Ticket: {self.nomer}\n"
        text += "Pesan:\n\n" + self.clean_pesan
        return text

    def __bool__(self) -> bool:
        return self.status

    @property
    def html(self) -> str:
        text = f'<a href="{self.url}">{self.judul}</a> [(]{self.topik}]\n'
        text += f"Status: {self.status_text} | Nomor: {self.nomer}\n"
        text += f"Nama: {self.nama} | Email: {self.email}\n"
        text += f"Pesan: {self.clean_pesan}"
        return text

    @property
    def status_text(self) -> str:
        return "OPEN" if self.status else "CLOSE"

    @property
    def clean_pesan(self) -> str:
        return bleach.clean(
            text=self.pesan.replace("<br/>", "\n"),
            tags=IGNORED_TAGS,
            strip=True,
        )

    @property
    def url(self) -> str:
        return f"http://hallo-ut.ut.ac.id/status?noticket={self.nomer}"

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

    @classmethod
    def create(
        cls,
        fullname: str,
        email: str,
        nohp: str,
        topik: TopikTiket,
        priority: PriorityTiket,
        subject: str,
        description: str,
        nim: Optional[str] = None,
        userfile: Optional[List[BinaryIO]] = None,
    ) -> "Tiket":
        session = requests.Session()
        session.headers[
            "User-Agent"
        ] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0"
        res = session.get("http://hallo-ut.ut.ac.id/create/ticket")
        if not res.ok or not res.text:
            raise Exception("Hallo-ut tidak dapat dihubungi")
        # TODO : Tambah 3 file gambar ke fields
        fields = {
            "fullname": fullname,
            "email": email,
            "nohp": nohp,
            "topik_id": str(topik.id),
            "priority_id": str(priority.id),
            "subject": subject,
            "Description": description,
            "nim": str(nim or ""),
        }
        m = MultipartEncoder(fields)
        headers = {
            "Content-Type": m.content_type,
            "Referer": res.url,
        }
        res = session.post(
            url="http://hallo-ut.ut.ac.id/ticket/post",
            data=m.to_string(),
            headers=headers,
        )
        if "=" not in res.url:
            raise Exception("Data yang dikirim tidak valid!")
        return cls.from_noticket(res.url.split("=")[-1])
