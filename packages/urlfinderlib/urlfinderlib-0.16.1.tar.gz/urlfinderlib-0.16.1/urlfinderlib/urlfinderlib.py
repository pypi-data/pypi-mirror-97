import magic
import re
import string

from typing import Set, Union

import urlfinderlib.finders as finders
import urlfinderlib.helpers as helpers

from urlfinderlib.url import URL, URLList


def get_url_permutations(url: str) -> Set[str]:
    return URL(url).permutations


def find_urls(blob: Union[bytes, str], base_url: str = '', mimetype: str = '') -> Set[str]:
    if isinstance(blob, str):
        blob = blob.encode('utf-8', errors='ignore')

    if not mimetype:
        mimetype = magic.from_buffer(blob)
    mimetype = mimetype.lower()

    urls = []

    if 'rfc 822' in mimetype or 'mail' in mimetype:
        return set()
    elif 'html' in mimetype:
        blob = _unescape_ascii(blob)
        urls += finders.HtmlUrlFinder(blob, base_url=base_url).find_urls()
    elif 'vcalendar' in mimetype:
        urls += finders.IcalUrlFinder(blob).find_urls()
    elif 'xml' in mimetype:
        urls += finders.XmlUrlFinder(blob).find_urls()
    elif b'%PDF-' in blob[:1024]:
        urls += finders.PdfUrlFinder(blob).find_urls()
    elif 'text' in mimetype:
        if b'xmlns' in blob and b'</' in blob:
            urls += finders.XmlUrlFinder(blob).find_urls()
        elif _is_csv(blob):
            urls += finders.CsvUrlFinder(blob).find_urls()
        elif helpers.might_be_html(blob):
            urls += finders.HtmlUrlFinder(blob).find_urls()
            urls += finders.TextUrlFinder(blob).find_urls(strict=True)
        else:
            urls += finders.TextUrlFinder(blob).find_urls(strict=True)
    else:
        urls += finders.DataUrlFinder(blob).find_urls()

    return URLList([URL(u) for u in urls]).get_all_urls()


def _has_u_escaped_lowercase_bytes(blob: bytes) -> bool:
    return bool(re.search(r'\\u00[a-f0-9]{2}', blob.decode('utf-8', errors='ignore')))


def _has_u_escaped_uppercase_bytes(blob: bytes) -> bool:
    return bool(re.search(r'\\u00[A-F0-9]{2}', blob.decode('utf-8', errors='ignore')))


def _has_x_escaped_lowercase_bytes(blob: bytes) -> bool:
    return bool(re.search(r'\\x[a-f0-9]{2}', blob.decode('utf-8', errors='ignore')))


def _has_x_escaped_uppercase_bytes(blob: bytes) -> bool:
    return bool(re.search(r'\\x[A-F0-9]{2}', blob.decode('utf-8', errors='ignore')))


def _is_csv(blob: bytes) -> bool:
    lines = blob.decode('utf-8', errors='ignore').splitlines()[:2]
    for line in lines:
        if line.count(',') > 1:
            return True

    return False


def _unescape_ascii(blob: bytes) -> bytes:
    ascii_chars = string.ascii_letters + string.digits + string.punctuation

    if _has_u_escaped_lowercase_bytes(blob):
        for char in ascii_chars:
            escaped = f'\\u00{format(ord(char), "x")}'.encode('utf-8')
            blob = blob.replace(escaped, escaped.decode('unicode_escape').encode('utf-8'))

    if _has_u_escaped_uppercase_bytes(blob):
        for char in ascii_chars:
            escaped = f'\\u00{format(ord(char), "X")}'.encode('utf-8')
            blob = blob.replace(escaped, escaped.decode('unicode_escape').encode('utf-8'))

    if _has_x_escaped_lowercase_bytes(blob):
        for char in ascii_chars:
            escaped = f'\\x{format(ord(char), "x")}'.encode('utf-8')
            blob = blob.replace(escaped, escaped.decode('unicode_escape').encode('utf-8'))

    if _has_x_escaped_uppercase_bytes(blob):
        for char in ascii_chars:
            escaped = f'\\x{format(ord(char), "X")}'.encode('utf-8')
            blob = blob.replace(escaped, escaped.decode('unicode_escape').encode('utf-8'))

    return blob
