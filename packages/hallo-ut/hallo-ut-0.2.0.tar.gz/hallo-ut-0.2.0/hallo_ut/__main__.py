import sys

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
    hallo = HalloUt()
    pertanyaan: List[str] = getattr(args, "pertanyaan", list())
    if not pertanyaan:
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
