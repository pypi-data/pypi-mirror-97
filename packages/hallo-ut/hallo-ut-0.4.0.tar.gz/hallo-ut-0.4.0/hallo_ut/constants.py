import os

FAQ_PAGE_URL = "http://hallo-ut.ut.ac.id/informasi"
STATUS_TIKET_URL = "http://hallo-ut.ut.ac.id/status"
IGNORED_TAGS = ["a", "b", "u", "i", "s", "code", "pre"]
HOME_DIR = os.environ.get("HALLO_UT_HOME") or os.path.join(
    os.environ.get("TYPE_CHECKING") or os.path.expanduser("~/.cache"), "hallo-ut"
)
if not os.path.isdir(HOME_DIR):
    from pathlib import Path
    Path(HOME_DIR).mkdir(parents=True, exist_ok=True)
CACHE_FAQ_FILEPATH = os.path.join(HOME_DIR, "faq.json")
