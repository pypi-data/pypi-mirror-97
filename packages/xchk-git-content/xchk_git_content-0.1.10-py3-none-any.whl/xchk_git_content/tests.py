import unittest
import regex
from django.test import TestCase
from unittest.mock import Mock, patch, MagicMock
from xchk_regex_strategies.strats import RegexCheck
from xchk_core.templatetags.xchk_instructions import node_instructions_2_ul
from xchk_core.strats import StratInstructions, AT_LEAST_ONE_TEXT, ALL_OF_TEXT
from .contentviews import WhatIsGitView, GitStatusView

class WhatIsGitRegexCheckTest(TestCase):

    def test_short_non_dutch_language_link(self):
        text = r"""https://git-scm.com/book/en"""
        self.assertTrue(WhatIsGitView._incorrect_lang_regex.fullmatch(text))

    def test_long_non_dutch_language_link(self):
        text = r"""https://git-scm.com/book/en/v2"""
        self.assertTrue(WhatIsGitView._incorrect_lang_regex.fullmatch(text))

    def test_short_dutch_language_link(self):
        text = r"""https://git-scm.com/book/nl"""
        self.assertTrue(WhatIsGitView._accepted_regex.fullmatch(text))

    def test_long_dutch_language_link(self):
        text = r"""https://git-scm.com/book/nl/v2"""
        self.assertTrue(WhatIsGitView._accepted_regex.fullmatch(text))

    def test_non_link(self):
        text = r"""https://ubuntu.com"""
        self.assertFalse(WhatIsGitView._accepted_regex.match(text))

class GitStatusRegexCheckTest(TestCase):

    def test_submission_jan(self):
        text = r"""
On branch master
Your branch is up to date with 'origin/master'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   git_status_1

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   git_status_1
        """
        self.assertTrue(GitStatusView._accepted_regex.fullmatch(text))

if __name__ == '__main__':
    unittest.main()
