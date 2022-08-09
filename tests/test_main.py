import unittest

from click.testing import CliRunner

from emoji_chengyu.main import emoji_chengyu


class TestMain(unittest.TestCase):

    def test_emoji_chengyu(self):
        runner = CliRunner()
        result = runner.invoke(emoji_chengyu, [])
        assert result.exit_code == 0
        print(result.output)
