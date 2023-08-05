from pypinyin import lazy_pinyin
import string

from . import strutils
from . import listutils

def to_pinyin(value, clean=True, clean_chars=string.ascii_letters + string.digits):
    words = lazy_pinyin(value)
    words = listutils.replace(words, {"lve": "lue"})
    title = " ".join([x.capitalize() for x in words])
    result = strutils.camel(title, clean=clean, clean_chars=clean_chars)
    return result
