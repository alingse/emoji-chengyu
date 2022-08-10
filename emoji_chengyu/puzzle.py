from dataclasses import dataclass
from random import choice, shuffle
from typing import Optional, Tuple, List

from .data import ChengyuManager, clean_tone
from .data import CommonChengyuManager, DefaultEmojiManager
from .data import ChengyuItem, EmojiItem


@dataclass(frozen=True)
class PuzzleItem:
    chengyu_item: ChengyuItem
    puzzle: Tuple[str]
    mask: Tuple[bool]

    @property
    def puzzle_str(self) -> str :
        return ''.join(self.puzzle)

    @property
    def mask_num(self) -> int:
        return sum(self.mask)

    def clone(self, reduce_mask: int = 0) -> 'PuzzleItem':
        reduce_mask = max(0, reduce_mask)
        mask_indexes = [i for i in range(len(self.mask)) if self.mask[i]]

        puzzle = list(self.puzzle)
        mask = list(self.mask)
        for i in mask_indexes[:reduce_mask]:
            mask[i] = False
            puzzle[i] = self.chengyu_item.word_list[i]

        return PuzzleItem(
            chengyu_item=self.chengyu_item,
            puzzle=tuple(puzzle),
            mask=tuple(mask))


def make_one_puzzle(chengyu_item: ChengyuItem) -> Optional[PuzzleItem]:
    puzzle = [None] * len(chengyu_item.word_list)
    mask = [False] * len(chengyu_item.word_list)

    word_emoji_map = {}
    emoji_word_map = {}

    def patch_puzzle(i: int, emoji_items: List[EmojiItem]):
        if not emoji_items or mask[i]:
            return

        word = chengyu_item.word_list[i]
        # 如果此文字之前已经有对应了, 则复用 emoji, ex: 冷言冷语
        if word in word_emoji_map:
            emoji_item = word_emoji_map[word]
        else:
            # 去掉已经被别的汉字使用过的重复 emoji
            emoji_items = list(filter(lambda x: x.emoji not in emoji_word_map, emoji_items))
            if not emoji_items:
                return
            emoji_item = choice(emoji_items)

        word_emoji_map[word] = emoji_item
        emoji_word_map[emoji_item.emoji] = word

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

    # TODO in/ing en/eng

    if not any(mask):
        return None

    for i, word in enumerate(chengyu_item.word_list):
        if not mask[i]:
            puzzle[i] = word

    return PuzzleItem(
        chengyu_item=chengyu_item,
        puzzle=puzzle,
        mask=mask)


def gen_puzzle(manager: ChengyuManager = CommonChengyuManager, search_count: int = 1000):
    chengyu_list = [item for item in manager.chengyu_list[:search_count]]
    if not chengyu_list:
        raise StopIteration

    shuffle(chengyu_list)

    for item in chengyu_list:
        puzzle = make_one_puzzle(item)
        if puzzle:
            yield puzzle
