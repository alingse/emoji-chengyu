import json
import pathlib
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Mapping, Optional, Tuple

TONE_MAP = {
    "ā": "a",
    "á": "a",
    "ǎ": "a",
    "à": "a",
    "ē": "e",
    "é": "e",
    "ě": "e",
    "è": "e",
    "ī": "i",
    "í": "i",
    "ǐ": "i",
    "ì": "i",
    "ō": "o",
    "ó": "o",
    "ǒ": "o",
    "ò": "o",
    "ū": "u",
    "ú": "u",
    "ǔ": "u",
    "ù": "u",
    "ü": "v",
    "ǖ": "v",
    "ǘ": "v",
    "ǚ": "v",
    "ǜ": "v"
}


DATA_DIR = 'data'
CHENGYU_JSON = 'chengyu.json'
CHENGYU_COUNT_JSON = 'chengyu.count.json'
EMOJI_CN_JSON = 'emoji.cn.json'
CN_COMMA = '，'


def clean_tone(origin: str) -> str:
    rs = None
    for i, c in enumerate(origin):
        if c in TONE_MAP:
            if rs is None:
                rs = list(origin)

            rs[i] = TONE_MAP[c]
    if rs is None:
        return origin
    return ''.join(rs)


def split_pinyin(origin: str) -> Tuple[str]:
    rs = []
    last = ''
    for c in origin:
        if c == ' ' and last:
            rs.append(last)
            last = ''
        elif c == CN_COMMA:
            rs.append(last)
            rs.append(c)
            last = ''
        else:
            last += c
    if last:
        rs.append(last)
    return tuple(rs)


@dataclass(frozen=True)
class ChengyuItem:
    word: str
    pinyin: str
    word_list: Tuple[str]
    pinyin_list: Tuple[str]
    used_count: int

    @property
    def is_common(self) -> bool:
        return self.used_count > 0

    @property
    def word_length(self) -> int:
        return len(self.word_list)


def load_chengyu_data() -> List[ChengyuItem]:
    data_path = pathlib.Path(__file__).parent.joinpath(DATA_DIR)

    with open(data_path.joinpath(CHENGYU_COUNT_JSON)) as f:
        chengyu_count_map = json.load(f)

    def make_chengyu_item(raw_data):
        word = raw_data['word']
        pinyin = raw_data['pinyin']
        word_list = tuple(list(word))
        pinyin_list = split_pinyin(pinyin)
        # bad data
        if len(word_list) != len(pinyin_list):
            return None

        used_count = chengyu_count_map.get(word, 0)
        return ChengyuItem(
            word=word,
            pinyin=pinyin,
            word_list=word_list,
            pinyin_list=pinyin_list,
            used_count=used_count)

    chengyu_list: List[ChengyuItem] = []
    with open(data_path.joinpath(CHENGYU_JSON)) as f:
        for line in f:
            raw_dict = json.loads(line)
            item = make_chengyu_item(raw_dict)
            if item:
                chengyu_list.append(item)

    return chengyu_list


class ChengyuManager:

    def __init__(self, chengyu_list: List[ChengyuItem]):
        self.chengyu_list = chengyu_list
        self._word_map: Mapping[str, ChengyuItem]= {}
        for item in chengyu_list:
            self._word_map[item.word] = item

    def get_by_word(self, word: str) -> Optional[ChengyuItem]:
        return self._word_map.get(word)


chengyu_list = load_chengyu_data()
common_chengyu_list = list(filter(lambda item: item.is_common and item.word_length == 4, chengyu_list))


DefaultChengyuManager = ChengyuManager(chengyu_list)
CommonChengyuManager = ChengyuManager(common_chengyu_list)


@dataclass(frozen=True)
class EmojiWordItem:
    word: str
    pinyin: str


@dataclass(frozen=True)
class EmojiItem:
    emoji: str
    words: List[EmojiWordItem]


def load_emoji_data() -> List[EmojiItem]:
    data_path = pathlib.Path(__file__).parent.joinpath(DATA_DIR)

    def make_emoji_item(raw_data: dict) -> EmojiItem:
        words = []
        for raw_word in raw_data['words']:
            word_item = EmojiWordItem(
                word=raw_word['word'],
                pinyin=raw_word['pinyin'])
            words.append(word_item)
        return EmojiItem(
            emoji=raw_data['emoji'],
            words=words)

    emoji_list : List[EmojiItem] = []

    with open(data_path.joinpath(EMOJI_CN_JSON)) as f:
        for line in f:
            raw_dict = json.loads(line)
            emoji_item = make_emoji_item(raw_dict)
            emoji_list.append(emoji_item)

    return emoji_list


class EmojiManager:

    def __init__(self, emoji_list: List[EmojiItem]):
        self.emoji_list : List[EmojiItem] = emoji_list
        self._emoji_map : Mapping[str, EmojiItem] = {}
        self._word_map : Mapping[str, List[EmojiItem]] = defaultdict(list)
        self._pinyin_map : Mapping[str, List[EmojiItem]] = defaultdict(list)

        for item in emoji_list:
            self._emoji_map[item.emoji] = item
            for word_item in item.words:
                self._word_map[word_item.word].append(item)
                self._pinyin_map[word_item.pinyin].append(item)
                self._pinyin_map[clean_tone(word_item.pinyin)].append(item)

    def get_by_word(self, word: str) -> Optional[List[EmojiItem]]:
        return self._word_map.get(word)

    def get_by_pinyin(self, pinyin: str) -> Optional[List[EmojiItem]]:
        return self._pinyin_map.get(pinyin)


DefaultEmojiManager = EmojiManager(load_emoji_data())
