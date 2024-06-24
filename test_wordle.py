import lib
import pytest
import warnings


class TestFetchRemoteWords:
    def test_get_remote(self):
        assert lib.fetch_remote_word_list(), "Can't check remote word list,  check internet connection"

    def test_local_remote_match(self):
        if not lib.fetch_remote_word_list():
            pytest.skip("Skipping test as no internet connection available.")
        assert lib.check_remote_local_words_match(), "Local words don't match remote words!"


class TestMergeFeedback:
    pass
