# emoji-chengyu
把成语转成 emoji 来猜谜的小玩具

## 起因

春节有朋友在微信发的谜题

## 原理

成语 --> 拼音 && Emoji --> 含义 --> 拼音

利用同音或者谐音, 通过拼音关联成语和 Emoji

Example:

喜上眉梢 <---> 😄👆🌹🔥

😄 --> 高兴 --> 喜
👆 --> 向上 --> 上
🌹 --> 玫瑰 --> 玫(眉)
🔥 --> 火焰 --> 烧(梢)


## 数据源

1. 成语

搜了下 github 有中华新华字典数据库 https://github.com/pwxcoo/chinese-xinhua MIT

而且包含了成语的拼音

2. emoji

emoji 转中文搜了下，有好几个

- https://github.com/Kenshin/emoji

    是个 Chrome 插件, 数据源在 https://github.com/Kenshin/emoji/blob/master/src/vender/emoji/zh_emoji.js , MIT 证书

- https://github.com/chroming/ch2emoji

    python 数据源在 https://github.com/chroming/ch2emoji/blob/master/emoji_pinyin_dict.py , 看不太懂。 无证书

- https://github.com/binderclip/emoji-cn

    未完成的项目

- https://github.com/techkang/zh2emoji

    好像和 ch2emoji 的数据源一样, https://github.com/techkang/zh2emoji/blob/master/emoji_dict_sim.py 作者说做了谷歌翻译

- https://github.com/gingerbeardman/Emojipedia

    英文 https://github.com/gingerbeardman/Emojipedia/blob/master/Emoji.xml

- https://github.com/notwaldorf/emoji-translate

    英文, https://github.com/notwaldorf/emoji-translate/blob/master/extension/emojis.json (有点意思, 将来可以做一个抽象话生成器)

- https://github.com/muan/emojilib

    英文, 这个不错，感觉可以在这个基础上用谷歌翻译


## TODO

1. 找到合适的数据源
