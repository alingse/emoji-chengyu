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

    with io.open(chengyu_filepath, 'w') as f:
        for x in idioms:
            idiom = {}
            idiom['word'] = x['word']
            idiom['pinyin'] = x['pinyin']
            f.write(json.dumps(idiom, ensure_ascii=False))
            f.write('\n')


def load_word_map():
    with io.open(temp_word_filepath, 'r') as f:
        words = json.load(f)

    word_map = defaultdict(list)
    for x in words:
        word_map[x['word']].append(x['pinyin'])
    return word_map


def load_emoji_map():
    with io.open(temp_emoji_filepath, 'r') as f:
        emojis = json.load(f)

    emoji_map = {}
    for key, value in emojis.items():
        emoji = {}
        emoji['name'] = key
        emoji['keywords'] = value['keywords']
        emoji['category'] = value['category']
        emoji_map[value['char']] = emoji
    return emoji_map


def mark_one_emoji(emoji, emoji_map, word_map):
    print(f'this emoji is {emoji}')
    print(f'category: {emoji_map[emoji]["category"]}')
    print(f'keywords: {emoji_map[emoji]["keywords"]}')

    flag = None
    words = []

    while True:
        word = input('input cn word:')
        if word == '':
            print('will try next emoji')
            flag = 'next'
            break
        if word == 'exit':
            print('will exit.')
            flag = 'exit'
            break

        if word not in word_map:
            print(f'word {word} have no data')
            continue

        pinyins = word_map[word]
        if len(pinyins) > 1:
            print('wraning word have multi pinyin', pinyins)
            indexes = input('entry 1 2 3... to chose:')
            indexes = map(int, indexes.split(' '))
            pinyins = [pinyins[i] for i in indexes]

        one_word = {}
        one_word['word'] = word
        one_word['pinyins'] = pinyins
        words.append(one_word)
    return flag, words


def mark_emoji():
    marked_emoji_map = {}
    marks = []

    if os.path.exists(marked_emoji_filepath):
        with io.open(marked_emoji_filepath, 'r') as f:
            for line in f:
                mark = json.loads(line)
                marks.append(mark)
                marked_emoji_map[mark['emoji']] = True

    word_map = load_word_map()
    emoji_map = load_emoji_map()

    for emoji in emoji_map:
        # 只标记新的
        if emoji in marked_emoji_map:
            continue

        flag, words = mark_one_emoji(
            emoji=emoji,
            emoji_map=emoji_map,
            word_map=word_map)

        if flag == 'exit':
            break
        mark = {}
        mark['emoji'] = emoji
        mark['words'] = words
        marks.append(mark)
        marked_emoji_map[emoji] = True

    with io.open(marked_emoji_filepath, 'w') as f:
        for mark in marks:
            f.write(json.dumps(mark, ensure_ascii=False))
            f.write('\n')


def edit_emoji():
    pass


def main():
    if len(sys.argv) == 1:
        print('python3 make-data.py [idiom|emoji|word]')
        print('python3 make-data.py emoji [mark|edit]')
        return
    elif sys.argv[1] == 'idiom':
        make_idiom()
        return
    elif sys.argv[1] == 'word':
        word_map = load_word_map()
        print(len(word_map))
        return
    elif sys.argv[1] == 'emoji':
        if len(sys.argv) == 2:
            emoji_map = load_emoji_map()
            print(len(emoji_map))
            return
        elif sys.argv[2] == 'mark':
            mark_emoji()
            return
        elif sys.argv[2] == 'edit':
            edit_emoji()
            return


if __name__ == '__main__':
    main()
