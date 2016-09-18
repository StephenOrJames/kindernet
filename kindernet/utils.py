import re
import unicodedata


def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub("[^\w\s-]", "", text).strip().lower()
    return re.sub("[-\s]+", "-", text)
