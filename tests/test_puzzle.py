import unittest


from emoji_chengyu.data import DefaultChengyuManager
from emoji_chengyu.puzzle import make_one_puzzle
from emoji_chengyu.puzzle import gen_puzzle


class TestChengyu(unittest.TestCase):

    def test_make_one_puzzle(self):
        chengyu_item = DefaultChengyuManager.get_by_word('左思右想')
        assert chengyu_item is not None

        puzzle = make_one_puzzle(chengyu_item)
        assert puzzle is not None

        print(puzzle.puzzle_str)

    def test_make_one_puzzle_with_same(self):
        chengyu_item = DefaultChengyuManager.get_by_word('冷言冷语')
        puzzle = make_one_puzzle(chengyu_item)
        assert puzzle.puzzle[0] == puzzle.puzzle[2]

        chengyu_item = DefaultChengyuManager.get_by_word('赫赫炎炎')
        puzzle = make_one_puzzle(chengyu_item)
        assert puzzle.puzzle[0] == puzzle.puzzle[1]
        assert puzzle.puzzle[2] == puzzle.puzzle[3]

    def test_gen_puzzle(self):
        pg = gen_puzzle(manager=DefaultChengyuManager, search_count=1000)
        puzzle = next(pg)
        assert puzzle is not None

    def test_make_and_clone(self):
        chengyu_item = DefaultChengyuManager.get_by_word('冷言冷语')
        puzzle = make_one_puzzle(chengyu_item)
        puzzle2 = puzzle.clone(reduce_mask=4)
        assert puzzle2.puzzle_str == chengyu_item.word
        assert puzzle2.mask_num == 0

        puzzle3 = puzzle.clone(reduce_mask=1)
        assert puzzle3.puzzle[0] == '冷'
        assert puzzle3.mask_num == 3
