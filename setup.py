import io
from setuptools import setup


with io.open('README.md', encoding='utf-8') as f:
    readme = f.read()


setup(
    name='emoji-chengyu',
    version='0.0.5-a',
    url='https://github.com/alingse/emoji-chengyu',
    long_description_content_type='text/markdown',
    long_description=readme,
    author='alingse',
    author_email='alingse@foxmail.com',
    license='MIT',
    packages=['emoji_chengyu'],
    include_package_data=True,
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'emoji-chengyu-cli = emoji_chengyu.main:emoji_chengyu',
        ],
    },
)
