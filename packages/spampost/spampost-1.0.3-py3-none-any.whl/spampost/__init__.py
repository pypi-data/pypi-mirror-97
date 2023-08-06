from bs4 import BeautifulSoup
from janome.tokenizer import Tokenizer
import unittest


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


def content_to_toks(content):
    soup = BeautifulSoup(content, 'html.parser')
    content = soup.get_text()
    content = replace_to_spaces(content)
    t = Tokenizer()
    toks = t.tokenize(content)
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


class Test(unittest.TestCase):
    def eq_is_eng_post(self, s, b, max_words=5):
        self.assertEqual(is_eng_post(s, max_words=max_words), b)

    def test_is_eng_post(self):
        self.eq_is_eng_post('これは日本語です。this is, a big heaven world.', True)
        return

        self.eq_is_eng_post('これは日本語です', False)
        self.eq_is_eng_post('これは日本語です\nこれは日本語です\nこれは日本語です', False)
        self.eq_is_eng_post('これは this 日本語 is です heaven.', False)
        self.eq_is_eng_post('this is a heaven world.', True)
        self.eq_is_eng_post('<a href="#">click me!</a> this is a heaven.', True)
        self.eq_is_eng_post('<a href="#">mp3</a>', False)
        self.eq_is_eng_post('<a href="#">mp3</a>', False, max_words=1)
        self.eq_is_eng_post('<a href="#">hello</a>', True, max_words=1)

        # russia
        self.eq_is_eng_post('<a href="#">Вы не могли бы мне помочь, пожалуйста?</a>', False)

    def eq_is_rus_post(self, s, b, max_words=5):
        self.assertEqual(is_rus_post(s, max_words=max_words), b)

    def test_is_rus_post(self):
        self.eq_is_rus_post('<a href="#">Вы</a>', False)
        self.eq_is_rus_post('<a href="#">Вы</a>', True, max_words=1)
        self.eq_is_rus_post('<a href="#">Вы, не. могли! Вы? не!</a>', True)
        self.eq_is_rus_post('<a href="#">Вы не могли бы мне помочь, пожалуйста?</a>', True)

    def eq_get_post_toks_len(self, s, n):
        self.assertEqual(get_post_toks_len(s), n)

    def test_get_post_toks_len(self):
        self.eq_get_post_toks_len('これは日本語です', 4)
        self.eq_get_post_toks_len('これは日本語です\nこれは日本語です\nこれは日本語です', 12)
        self.eq_get_post_toks_len('<a href="#">mp3</a>', 2)
        self.eq_get_post_toks_len('<a href="#">mp3 mp3</a>', 4)
        self.eq_get_post_toks_len('<a href="#">mp3 mp3 mp3 mp3</a>', 8)

    def eq_get_html_tags_len(self, s, n):
        self.assertEqual(get_html_tags_len(s), n)

    def test_get_html_tags_len(self):
        self.eq_get_html_tags_len('<a href="#">a</a>', 1)
        self.eq_get_html_tags_len('<a href="#">a</a><a href="#">a</a>', 2)
        self.eq_get_html_tags_len('<a href="#">a</a><a href="#">a</a><a href="#">a</a>', 3)

    def eq_is_spam_post(self, s, b):
        self.assertEqual(is_spam_post(s), b)

    def test_is_spam_post(self):
        self.eq_is_spam_post('こんにちは', True)
        self.eq_is_spam_post('こんにちは。いいお天気ですね。', False)
        self.eq_is_spam_post('''こんにちは。今日はあなた様のWebサイトを拝見しまして、ご連絡いたしました。
ぜひ私どものサイトにリンクを張らせていただきたいと思いまして、事後報告になりますが↓のURLからリンクをご確認ください。
httpx://xxxx.xxx
''', False)
        self.eq_is_spam_post('This', True)
        self.eq_is_spam_post('This is!', True)
        self.eq_is_spam_post('This is hello world!', True)
        self.eq_is_spam_post('Hi admin. My name is Bob. Are you fine?', True)
        self.eq_is_spam_post('<a href="#">mp3</a>', True)
        self.eq_is_spam_post('<a href="#">mp3 mp3</a>', True)
        self.eq_is_spam_post('<a href="#">mp3 mp3 mp3</a>', True)
        self.eq_is_spam_post('<a href="#">mp3 mp3 mp3 mp3</a>', True)
        self.eq_is_spam_post('<a href="#">This is hello world!</a>', True)
        self.eq_is_spam_post('<a href="#">Вы, не. могли!</a>', True)
        self.eq_is_spam_post('<a href="#">Вы не могли бы мне помочь, пожалуйста?</a>', True)
