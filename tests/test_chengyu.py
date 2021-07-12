import unittest


from emoji_chengyu.chengyu import gen_one_pair


class TestChengyu(unittest.TestCase):

    def test_gen_one_pair(self):
        pair = gen_one_pair()
        print(pair)
        assert pair
