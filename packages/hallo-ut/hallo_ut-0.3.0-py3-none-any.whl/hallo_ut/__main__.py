import sys
import re

from argparse import ArgumentParser
from typing import List

from . import HalloUt


def main():
    parser = ArgumentParser(
        prog="hallo-ut",
        description="Layanan Informasi Universitas Terbuka",
    )
    parser.add_argument(
        "pertanyaan",
        type=str,
        nargs="+",
        help="pertanyaan tentang Universitas Terbuka",
    )
    args = parser.parse_args()
    pertanyaan: List[str] = getattr(args, "pertanyaan", list())
    if not pertanyaan:
        return
    hallo = HalloUt()
    match = re.match(r"^(W\d{10}-\d{8})$", " ".join(pertanyaan))
    if match:
        for group in match.groups():
            if not group:
                continue
            tiket = hallo.status_tiket(group)
            print(str(tiket))
        return
    results = hallo.faq(" ".join(pertanyaan))
    if results:
        print(f"Ditemukan {len(results)} jawaban yang mungkin cocok.")
    else:
        print(f"Jawaban tidak ditemukan.")
        return
    for faq in results:
        print("\n")
        print(faq)


if __name__ == "__main__":
    sys.exit(main())
