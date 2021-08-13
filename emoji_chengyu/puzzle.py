from dataclasses import dataclass
from random import choice, shuffle
from typing import Tuple

from .data import clean_tone
from .data import DefaultChengyuManager, CommonChengyuManager, DefaultEmojiManager
from .data import ChengyuItem


@dataclass(frozen=True)
class PuzzleItem:
    chengyu_item: ChengyuItem
    puzzle: Tuple[str]
    mask: Tuple[bool]


def make_one_puzzle(chengyu_item):
    puzzle = [None] * len(chengyu_item.word_list)
    mask = [False] * len(chengyu_item.word_list)

    # word_emoji_map = {}
    def patch_puzzle(i, emoji_items):
        if not emoji_items or mask[i]:
            return

        # TODO: word-emoji equal
        # word = chengyu_item.word_list[i]
        emoji_item = choice(emoji_items)
        puzzle[i] = emoji_item.emoji
        mask[i] = True

    # 1. 先按文字对应
    for i, word in enumerate(chengyu_item.word_list):
        emoji_items = DefaultEmojiManager.get_by_word(word)
        patch_puzzle(i, emoji_items)

    # 2. 再按拼音匹配
    for i, pinyin in enumerate(chengyu_item.pinyin_list):
        emoji_items = DefaultEmojiManager.get_by_pinyin(pinyin)
        patch_puzzle(i, emoji_items)

    # 3. 再按去掉 tone 匹配
    for i, pinyin in enumerate(chengyu_item.pinyin_list):
        emoji_items = DefaultEmojiManager.get_by_pinyin(clean_tone(pinyin))
        patch_puzzle(i, emoji_items)

    if not any(mask):
        return None

    for i, word in enumerate(chengyu_item.word_list):
        if not mask[i]:
            puzzle[i] = word

    return PuzzleItem(
        chengyu_item=chengyu_item,
        puzzle=puzzle,
        mask=mask)


def gen_puzzle(only_common=True, search_count=1000):
    manager = DefaultChengyuManager
    if only_common:
        manager = CommonChengyuManager

    chengyu_list = [
        item
        for item in manager.chengyu_list[:search_count]
    ]
    if not chengyu_list:
        raise StopIteration

    shuffle(chengyu_list)

    for item in chengyu_list:
        puzzle = make_one_puzzle(item)
        if puzzle:
            yield puzzle
