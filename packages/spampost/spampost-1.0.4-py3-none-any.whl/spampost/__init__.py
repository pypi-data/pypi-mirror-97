from bs4 import BeautifulSoup
from janome.tokenizer import Tokenizer
import unittest


tokenizer = Tokenizer()


def remove_space_toks(toks):
    for tok in toks:
        if '空白' in tok.part_of_speech:
            pass
        else:
            yield tok


def replace_to_spaces(content):
    content = content.replace('\r\n', '\n')
    content = content.replace('\n', ' ')
    content = content.replace('.', ' ')
    content = content.replace(',', ' ')
    content = content.replace('!', ' ')
    content = content.replace('?', ' ')
    return content


def is_alpha(s):
    d = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for c in s:
        if c.upper() not in d:
            return False
    return True


def is_rus_alpha(s):
    d = 'АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя'
    for c in s:
        if c not in d:
            return False
    return True


def count_eng_toks(toks):
    n = 0
    for tok in toks:
        if is_alpha(tok) or tok.isdigit():
            n += 1
        else:
            n = 0
    return n


def count_rus_toks(toks):
    n = 0
    for tok in toks:
        if is_rus_alpha(tok) or tok.isdigit():
            n += 1
        else:
            n = 0
    return n


def remove_urls(content):
    s = ''
    buf = ''
    m = 0

    for c in content:
        if m == 0:
            if c == 'h':
                m = 100
                buf = c
            else:
                s += c
        elif m == 100:
            if c == 't':
                m = 200
                buf += c
            else:
                s += buf + c
                buf = ''
                m = 0
        elif m == 200:
            if c == 't':
                m = 300
                buf += c
            else:
                s += buf + c
                buf = ''
                m = 0
        elif m == 300:
            if c == 'p':
                m = 400
                buf += c
            else:
                s += buf + c
                buf = ''
                m = 0
        elif m == 400:
            if c == 's':
                m = 500
                buf += c
            elif c == ':':
                m = 600
                buf += c
            else:
                s += buf + c
                buf = ''
                m = 0
        elif m == 500:
            if c == ':':
                m = 600
                buf += c
            else:
                s += buf + c
                buf = ''
                m = 0
        elif m == 600:
            if c == '/':
                m = 700
                buf += c
            else:
                s += buf + c
                buf = ''
                m = 0
        elif m == 700:
            if c == '/':
                m = 800
                buf = ''
            else:
                s += buf + c
                buf = ''
                m = 0
        elif m == 800:  # read at spaces
            if c.isspace():
                s += c
                m = 0

    if len(buf):
        s += buf

    return s


def content_to_toks(content):
    soup = BeautifulSoup(content, 'html.parser')
    content = soup.get_text()
    content = remove_urls(content)
    content = replace_to_spaces(content)
    global tokenizer
    toks = tokenizer.tokenize(content)
    toks = remove_space_toks(toks)
    toks = [tok.surface for tok in toks]
    return toks


def is_eng_post(content, max_words=5):
    toks = content_to_toks(content)
    n = count_eng_toks(toks)
    return n >= max_words


def is_rus_post(content, max_words=5):
    toks = content_to_toks(content)
    n = count_rus_toks(toks)
    return n >= max_words


def get_post_toks_len(content):
    toks = content_to_toks(content)
    return len(toks)    


def get_html_tags_len(content):
    soup = BeautifulSoup(content, 'html.parser')
    nlen = 0
    for tag in soup.find_all():
        nlen += len(tag.contents)
    return nlen


def is_spam_post(
    content,
    min_tags_len=1,
    max_toks_len=5,
    eng_max_words=5,
    rus_max_words=5,
    check_eng=True,
    check_rus=True,
    ):
    if get_html_tags_len(content) >= min_tags_len:
        return True
    if get_post_toks_len(content) < max_toks_len:
        return True
    if check_eng and is_eng_post(content, max_words=eng_max_words):
        return True
    if check_rus and is_rus_post(content, max_words=rus_max_words):
        return True
    return False


