import unittest


from emoji_chengyu.data import DataSource


class TestDataSource(unittest.TestCase):

    def test_load_on_init(self):
        assert len(DataSource.emoji_map) > 0

    def test_clean_tone(self):
        assert DataSource.clean_tone('nihao') == 'nihao'
        assert DataSource.clean_tone('dòu') == 'dou'
        assert DataSource.clean_tone('zǒu gǒu') == 'zou gou'

    def test_split_chengyu_pinyin(self):
        pinyin = "ān bù lí mǎ，jiǎ bù lí shēn"
        # print(DataSource.split_chengyu_pinyin(pinyin))
        assert len(DataSource.split_chengyu_pinyin(pinyin)) == 9

    def test_all_split(self):
        for chengyu_item in DataSource.chengyu_list:
            pys = DataSource.split_chengyu_pinyin(chengyu_item['pinyin'])
            words = list(chengyu_item['word'])

            # print(pys, words)
            assert len(pys) == len(words)
