from setuptools import setup


setup(
    name='emoji-chengyu',
    version='0.0.1',
    url='https://github.com/alingse/emoji-chengyu',
    description='',
    author='alingse',
    author_email='alingse@foxmail.com',
    license='MIT',
    packages=['emoji_chengyu'],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'emoji_chengyu = emoji_chengyu.main:emoji_chengyu',
        ],
    },
)
