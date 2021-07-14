import unittest


from emoji_chengyu.chengyu import gen_one_emoji_pair


class TestChengyu(unittest.TestCase):

    def test_gen_one_emoji_pair(self):
        pair = gen_one_emoji_pair()
        print(pair)
        assert pair
