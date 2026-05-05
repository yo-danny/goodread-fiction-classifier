import string
from langdetect import detect


def genre_binarizer(genres):
    genre_list = genres.lower().split("|")
    if "fiction" in genre_list:
        return 1
    elif "nonfiction" in genre_list:
        return 0
    return None


def add_space_case(desc):
    upd_desc = ""
    for i in range(len(desc) - 1):
        upd_desc += desc[i]
        if desc[i] in string.ascii_lowercase and desc[i + 1] in string.ascii_uppercase:
            upd_desc += " "
    upd_desc += desc[-1]
    return upd_desc


def remove_punctuation(desc):
    desc = add_space_case(desc)
    desc = desc.lower()
    valid_chars = string.ascii_letters + string.digits + " "
    desc = "".join([c if c in valid_chars else " " for c in desc])
    return desc


def clean_text(text):
    return remove_punctuation(text)


def is_english(text):
    try:
        return detect(text) == "en"
    except:
        return False
