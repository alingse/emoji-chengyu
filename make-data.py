import os
import sys
import io
import json
from collections import defaultdict


marked_emoji_filepath = './emoji_chengyu/data/emoji.cn.json'
chengyu_filepath = './emoji_chengyu/data/idiom.json'

temp_idiom_filepath = 'temp.idiom.json'
temp_word_filepath = 'temp.word.json'
temp_emoji_filepath = 'temp.emoji.json'


def make_idiom():
    with io.open(temp_idiom_filepath, 'r') as f:
        raw_content = f.read()

    idioms = json.loads(raw_content)
    idiom_map = {}
    for x in idioms:
        idiom_map[x['word']] = x['pinyin']

    with io.open(chengyu_filepath, 'w') as f:
        f.write(json.dumps(idiom_map, ensure_ascii=False))


def load_word_map():
    with io.open(temp_word_filepath, 'r') as f:
        words = json.load(f)


    word_map = defaultdict(list)
    for x in words:
        word_map[x['word']].append(x['pinyin'])
    return word_map


def mark_one_emoji(emoji, word_map):
    print('this emoji is', emoji['char'])
    print('category:', emoji['category'])
    print('keywords:', emoji['keywords'])

    flag = None
    words = []

    while True:
        word = input('input cn word:')
        if word == '':
            print('will try next emoji')
            flag = 'next'
            break
        if word == 'exit':
            print('will save and exit.')
            flag = 'exit'
            break

        if word not in word_map:
            print('word have no data')
            continue

        pinyins = word_map[word]
        if len(pinyins) > 1:
            print('wraning word have multi pinyin', pinyins)
            indexes = input('entry 1 2 3... to chose:')
            indexes = map(int, indexes.split(' '))
            pinyins = [pinyins[i] for i in indexes]

        words.append((word, pinyins))
    return flag, words


def mark_emoji():
    with io.open(temp_emoji_filepath, 'r') as f:
        emoji_map = json.load(f)

    mark_emoji_map = {}
    if os.path.exists(marked_emoji_filepath):
        with io.open(marked_emoji_filepath, 'r') as f:
            mark_emoji_map = json.load(f)

    word_map = load_word_map()
    for _, emoji in emoji_map.items():
        if emoji['char'] in mark_emoji_map:
            continue

        flag, words = mark_one_emoji(emoji, word_map)
        if words:
            mark_emoji_map[emoji['char']] = dict(words)

        if flag == 'exit':
            break
        elif flag == 'next':
            continue

    with io.open(marked_emoji_filepath, 'w') as f:
        f.write(json.dumps(mark_emoji_map, ensure_ascii=False))


def edit_emoji():
    pass


def main():
    if len(sys.argv) == 1:
        print('python3 make-data.py [idiom|emoji]')
        print('python3 make-data.py emoji [mark|edit]')
    if sys.argv[1] == 'idiom':
        make_idiom()
        return
    if sys.argv[1] == 'word':
        word_map = load_word_map()
        print(word_map)
    if sys.argv[1] == 'emoji':
        if sys.argv[2] == 'mark':
            mark_emoji()
            return
        if sys.argv[2] == 'edit':
            edit_emoji()
            return


if __name__ == '__main__':
    main()
