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

        print(''.join(puzzle.puzzle))

    def test_gen_puzzle(self):
        pg = gen_puzzle()
        puzzle = next(pg)
        assert puzzle is not None
