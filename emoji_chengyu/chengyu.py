
from random import choice

from .data import DataSource


def gen_one_pair():
    # 随机选一个成语
    chengyu_item = choice(DataSource.chengyu_list)
    words = chengyu_item['words']
    pinyins = chengyu_item['pinyins']
    emojis = [None] * len(words)

    # 1. 先按文字对应
    for i, word in enumerate(words):
        if word in DataSource.cn_emoji_map:
            emoji_items = DataSource.cn_emoji_map[word]
            emoji_item = choice(emoji_items)
            emojis[i] = emoji_item['emoji']

    # 2. 再按拼音匹配
    for i, word in enumerate(words):
        if emojis[i] is not None:
            continue
        pinyin = pinyins[i]
        if pinyin in DataSource.pinyin_emoji_map:
            emoji_items = DataSource.pinyin_emoji_map[pinyin]
            emoji_item = choice(emoji_items)
            emojis[i] = emoji_item['emoji']

    # 3. 再按去掉 tone 匹配
    for i, word in enumerate(words):
        if emojis[i] is not None:
            continue
        pinyin = pinyins[i]
        pinyin2 = DataSource.clean_tone(pinyin)
        if pinyin2 in DataSource.pinyin_emoji_map:
            emoji_items = DataSource.pinyin_emoji_map[pinyin2]
            emoji_item = choice(emoji_items)
            emojis[i] = emoji_item['emoji']

    # 4. TODO 按照谐音
    # yin ying

    if not any(emojis):
        return

    emojis2 = list(emojis)
    for i in range(len(emojis)):
        if emojis[i] is None:
            emojis2[i] = words[i]

    pair = {
        'words': words,
        'emojis': emojis,
        'word': ''.join(words),
        'emoji': ''.join(emojis2),
        'origin': chengyu_item,
    }
    return pair
