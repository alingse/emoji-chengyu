import unittest


from emoji_chengyu.data import DefaultChengyuManager
from emoji_chengyu.data import CommonChengyuManager
from emoji_chengyu.data import DefaultEmojiManager

from emoji_chengyu.data import clean_tone
from emoji_chengyu.data import split_pinyin


class TestData(unittest.TestCase):

    def test_load_on_init(self):
        assert len(DefaultChengyuManager.chengyu_list) > 0
        assert len(CommonChengyuManager.chengyu_list) > 0
        assert len(DefaultEmojiManager.emoji_list) > 0

    def test_clean_tone(self):
        self.assertEqual(clean_tone('nihao'), 'nihao')
        self.assertEqual(clean_tone('dòu'), 'dou')
        self.assertEqual(clean_tone('zǒu gǒu'), 'zou gou')

    def test_split_pinyin(self):
        pinyin = "ān bù lí mǎ，jiǎ bù lí shēn"
        assert len(split_pinyin(pinyin)) == 9
