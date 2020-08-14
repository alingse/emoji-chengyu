
from random import choice

from .data import DataSource


def gen_one_pair():
    chengyu_item = choice(DataSource.chengyu_list)
    words = list(chengyu_item['word'])
    emojis = [None] * len(words)

    # 1. 先按文字对应
    for i, word in enumerate(words):
        if word in DataSource.cn_emoji_map:
            emojis[i] = choice(choice(DataSource.cn_emoji_map[word])['words'])['word']

    # 2. 再按拼音匹配
    for i, word in enumerate(words):
        if emojis[i] is not None:
            continue
        # pinyin =
