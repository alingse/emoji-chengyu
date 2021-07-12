from setuptools import setup


setup(
    name='emoji-chengyu',
    version='0.0.2',
    url='https://github.com/alingse/emoji-chengyu',
    description='',
    author='alingse',
    author_email='alingse@foxmail.com',
    license='MIT',
    packages=['emoji_chengyu'],
    include_package_data=True,
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'emoji-chengyu-cli = emoji_chengyu.main:emoji_chengyu',
        ],
    },
)
