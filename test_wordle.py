import lib
import pytest
import warnings


class TestRemoteWords:
    def test_fetch_remote_words_list(self):
        assert lib.fetch_remote_word_list(), "Can't check remote word list,  check internet connection"

    def test_local_remote_match(self):
        if not lib.fetch_remote_word_list():
            pytest.skip("Skipping test as no internet connection available.")
        assert lib.check_remote_local_words_match(), "Local words don't match remote words!"


class TestGuessCheck:
    def test_greens(self):
        f = lib.get_guess_feedback('aaaaa', 'aaaaa')
        assert f.greens == ['a', 'a', 'a', 'a', 'a']
        assert f.yellows == [[], [], [], [], []]
        assert f.grays == set()

    def test_yellows(self):
        f = lib.get_guess_feedback('abbbb', 'baaaa')
        assert f.greens == [None, None, None, None, None]
        assert f.yellows == [['a'], ['b'], [], [], []]
        assert f.grays == set(['b'])

    def test_double_yellows(self):
        f = lib.get_guess_feedback('aabbb', 'bbaaa')
        assert f.greens == [None, None, None, None, None]
        assert f.yellows == [['aa'], ['aa'], ['bb'], ['bb'], []]
        assert f.grays == set(['b'])

    def test_double_yellows_alternating(self):
        f = lib.get_guess_feedback('ababa', 'babab')
        assert f.greens == [None, None, None, None, None]
        assert f.yellows == [['aa'], ['bb'], ['aa'], ['bb'], []]
        assert f.grays == set(['a'])

    def test_triple_yellows(self):
        f = lib.get_guess_feedback('bbaaa', 'aaabb')
        assert f.greens == [None, None, 'a', None, None]
        assert f.yellows == [['bb'], ['bb'], [], ['aaa'], ['aaa']]
        assert f.grays == set()

    def test_quadruple_yellows(self):
        f = lib.get_guess_feedback('baaaa', 'aaaab')
        assert f.greens == [None, 'a', 'a', 'a', None]
        assert f.yellows == [['b'], [], [], [], ['aaaa']]
        assert f.grays == set()

    def test_all_yellows(self):
        f = lib.get_guess_feedback('abcde', 'bcdea')
        assert f.greens == [None, None, None, None, None]
        assert f.yellows == [['a'], ['b'], ['c'], ['d'], ['e']]
        assert f.grays == set()

    def test_gray_before_green1(self):
        f = lib.get_guess_feedback('bbfff', 'abcde')
        assert f.greens == [None, 'b', None, None, None]
        assert f.yellows == [[], [], [], [], []]
        assert f.grays == set(['b', 'f'])

    def test_gray_before_two_greens(self):
        f = lib.get_guess_feedback('aaabb', 'caacc')
        assert f.greens == [None, 'a', 'a', None, None]
        assert f.yellows == [[], [], [], [], []]
        assert f.grays == set(['a', 'b'])

    def test_gray_before_four_greens(self):
        f = lib.get_guess_feedback('aaaaa', 'caaaa')
        assert f.greens == [None, 'a', 'a', 'a', 'a']
        assert f.yellows == [[], [], [], [], []]
        assert f.grays == set(['a'])

    def test_gray_and_yellow_before_green(self):
        f = lib.get_guess_feedback('aaabb', 'ccaac')
        assert f.greens == [None, None, 'a', None, None]
        assert f.yellows == [['aa'], [], [], [], []]
        assert f.grays == set(['a', 'b'])

    def test_quadruple_yellow_with_gray(self):
        f = lib.get_guess_feedback('acaaa', 'aaaab')
        assert f.greens == ['a', None, 'a', 'a', None]
        assert f.yellows == [[], [], [], [], ['aaaa']]
        assert f.grays == set(['c'])

    def test_yellow_gray_greens(self):
        f = lib.get_guess_feedback('aaaab', 'ccaaa')
        assert f.greens == [None, None, 'a', 'a', None]
        assert f.yellows == [['aaa'], [], [], [], []]
        assert f.grays == set(['a', 'b'])

    def test_random1(self):
        f = lib.get_guess_feedback('clarc', 'crazy')
        assert f.greens == ['c', None, 'a', None, None]
        assert f.yellows == [[], [], [], ['r'], []]
        assert f.grays == set(['l', 'c'])

    def test_random2(self):
        f = lib.get_guess_feedback('crazy', 'clarc')
        assert f.greens == ['c', None, 'a', None, None]
        assert f.yellows == [[], ['r'], [], [], []]
        assert f.grays == set(['z', 'y'])

    def test_random3(self):
        f = lib.get_guess_feedback('puppy', 'pippi')
        assert f.greens == ['p', None, 'p', 'p', None]
        assert f.yellows == [[], [], [], [], []]
        assert f.grays == set(['u', 'y'])

    def test_undid(self):
        f = lib.get_guess_feedback('dread', 'undid')
        assert f.greens == [None, None, None, None, 'd']
        assert f.yellows == [['dd'], [], [], [], []]
        assert f.grays == set(['r', 'e', 'a'])

    def test_erect(self):
        f = lib.get_guess_feedback('enter', 'erect')
        assert f.greens == ['e', None, None, None, None]
        assert f.yellows == [[], [], ['t'], ['ee'], ['r']]
        assert f.grays == set(['n'])
