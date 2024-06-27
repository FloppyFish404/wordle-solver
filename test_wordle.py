import lib
import pytest
import warnings
import random


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
        assert f.grays == set(['bb'])

    def test_double_yellows(self):
        f = lib.get_guess_feedback('aabbb', 'bbaaa')
        assert f.greens == [None, None, None, None, None]
        assert f.yellows == [['aa'], ['aa'], ['bb'], ['bb'], []]
        assert f.grays == set(['bbb'])

    def test_double_yellows_alternating(self):
        f = lib.get_guess_feedback('ababa', 'babab')
        assert f.greens == [None, None, None, None, None]
        assert f.yellows == [['aa'], ['bb'], ['aa'], ['bb'], []]
        assert f.grays == set(['aaa'])

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
        assert f.grays == set(['bb', 'f'])

    def test_gray_before_two_greens(self):
        f = lib.get_guess_feedback('aaabb', 'caacc')
        assert f.greens == [None, 'a', 'a', None, None]
        assert f.yellows == [[], [], [], [], []]
        assert f.grays == set(['aaa', 'b'])

    def test_gray_before_four_greens(self):
        f = lib.get_guess_feedback('aaaaa', 'caaaa')
        assert f.greens == [None, 'a', 'a', 'a', 'a']
        assert f.yellows == [[], [], [], [], []]
        assert f.grays == set(['aaaaa'])

    def test_gray_and_yellow_before_green(self):
        f = lib.get_guess_feedback('aaabb', 'ccaac')
        assert f.greens == [None, None, 'a', None, None]
        assert f.yellows == [['aa'], [], [], [], []]
        assert f.grays == set(['aaa', 'b'])

    def test_quadruple_yellow_with_gray(self):
        f = lib.get_guess_feedback('acaaa', 'aaaab')
        assert f.greens == ['a', None, 'a', 'a', None]
        assert f.yellows == [[], [], [], [], ['aaaa']]
        assert f.grays == set(['c'])

    def test_yellow_gray_greens(self):
        f = lib.get_guess_feedback('aaaab', 'ccaaa')
        assert f.greens == [None, None, 'a', 'a', None]
        assert f.yellows == [['aaa'], [], [], [], []]
        assert f.grays == set(['aaaa', 'b'])

    def test_random1(self):
        f = lib.get_guess_feedback('clarc', 'crazy')
        assert f.greens == ['c', None, 'a', None, None]
        assert f.yellows == [[], [], [], ['r'], []]
        assert f.grays == set(['l', 'cc'])

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


class TestPossibleAnswer:
    def test_empty(self):
        f = lib.Feedback()
        assert lib.possible_answer(f, 'hello')

    def test_green_T(self):
        f = lib.Feedback()
        f.greens = ['h', 'e', 'l', 'l', 'o']
        assert lib.possible_answer(f, 'hello')

    def test_green_F(self):
        f = lib.Feedback()
        f.greens = ['h', 'e', 'l', 'p', 'o']
        assert not lib.possible_answer(f, 'hello')

    def test_green_half(self):
        f = lib.Feedback()
        f.greens = ['h', None, 'l', None, 'o']
        assert lib.possible_answer(f, 'hello')

    def test_yel_used(self):
        f = lib.Feedback()
        f.yellows = [['e'], ['l'], ['o'], ['h'], ['l']]
        assert lib.possible_answer(f, 'hello')

    def test_yel_notused(self):
        f = lib.Feedback()
        f.yellows = [['e'], ['l'], ['o'], ['h'], ['l']]
        assert not lib.possible_answer(f, 'jello')

    def test_yel_used_doub(self):
        f = lib.Feedback()
        f.yellows = [['e'], ['ll'], ['o'], ['h'], ['ll']]
        assert lib.possible_answer(f, 'hello')

    def test_yel_notused_doub(self):
        f = lib.Feedback()
        f.yellows = [['e'], ['ll'], ['o'], ['h'], ['ll']]
        assert not lib.possible_answer(f, 'helpo')

    def test_yel_used_triple(self):
        f = lib.Feedback()
        f.yellows = [['rrr'], [], [], ['rr'], []]
        assert lib.possible_answer(f, 'error')

    def test_yel_notused_triple(self):
        f = lib.Feedback()
        f.yellows = [['rrr'], [], [], ['rr'], []]
        assert not lib.possible_answer(f, 'order')

    def test_yel_used_quad(self):
        f = lib.Feedback()
        f.yellows = [[], [], ['oooo'], [], []]
        assert lib.possible_answer(f, 'oowoo')

    def test_yel_notused_quad(self):
        f = lib.Feedback()
        f.yellows = [[], ['ffff'], [], [], []]
        assert not lib.possible_answer(f, 'fluff')

    def test_yel_undid(self):
        f = lib.Feedback()
        f.yellows = [['dd'], ['u'], ['n'], ['dd'], []]
        assert lib.possible_answer(f, 'undid')

    def test_yel_inplace(self):
        f = lib.Feedback()
        f.yellows = [['h'], ['e'], ['ll'], ['ll'], ['o']]
        assert not lib.possible_answer(f, 'hello')

    def test_gray_used(self):
        f = lib.Feedback()
        f.grays.add('e')
        assert not lib.possible_answer(f, 'hello')

    def test_double_gray_not_used(self):
        f = lib.Feedback()
        f.grays.add('ee')
        assert lib.possible_answer(f, 'hello')

    def test_double_gray_used(self):
        f = lib.Feedback()
        f.grays.add('ll')
        assert not lib.possible_answer(f, 'hello')

    def test_quad_gray_not_used(self):
        f = lib.Feedback()
        f.grays.add('pppp')
        assert lib.possible_answer(f, 'pippy')

    def test_quad_gray_used(self):
        f = lib.Feedback()
        f.grays.add('eeee')
        assert not lib.possible_answer(f, 'eevee')

    def test_gray_notused(self):
        f = lib.Feedback()
        f.grays = set(['b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                       'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                       't', 'u', 'v', 'w', 'x', 'y', 'z'])
        assert lib.possible_answer(f, 'aaaaa')

    def test_gray_and_yel(self):
        f = lib.Feedback()
        f.yellows = [['e'], ['ll'], ['h'], ['o'], ['ll']]
        f.grays = set(['ee', 'lll', 'hh', 'oo'])
        assert lib.possible_answer(f, 'hello')

    def test_green_yel_gray_hello(self):
        f = lib.Feedback()
        f.greens = [None, None, 'l', None, 'o']
        f.yellows = [['ll'], ['h'], ['e'], ['o'], []]
        f.grays = set(['a', 'i', 's', 't', 'b', 'ee', 'oo'])
        assert lib.possible_answer(f, 'hello')

    def test_fight(self):
        f = lib.Feedback()
        f.greens = [None, None, None, None, 't']
        f.yellows = [[], ['h'], [], ['t'], []]
        f.grays = set(['o', 'l', 's', 'f', 'a', 'u', 'r', 'n', 'e', 'w'])
        assert not lib.possible_answer(f, 'fight')


class TestPerformance:
    def test_performance_get_guess_feedback(self, benchmark):
        words = lib.get_local_words_list()
        guesses = random.sample(words, 5)

        def benchmark_feedback():
            for guess in guesses:
                for answer in words:
                    lib.get_guess_feedback(guess, answer)
        benchmark(benchmark_feedback)

    def test_performance_possible_answer(self, benchmark):
        words = lib.get_local_words_list()
        f1, f2, f3, f4 = lib.Feedback(), lib.Feedback(), lib.Feedback(), lib.Feedback()
        f2.greens = ['r', None, None, None, None]
        f3.yellows[2] = ['ll']
        f4.grays = set(['z', 'll', 'o'])
        feedbacks = [f1, f2, f3, f4]

        def benchmark_feedback():
            for f in feedbacks:
                for word in words:
                    lib.possible_answer(f, word)
        benchmark(benchmark_feedback)


class TestIntegration:
    def test_erect_integration(self):
        pass
        # answer = 'erect'
        # feedback = mf(gc('roate', 'erect'), gc('enter', 'erect'), 2)
        # exp = True
        # assert pa(feedback, answer) == exp
