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


def test_python_version():
    import sys
    assert sys.version_info >= (3, 10), "Python version is less than 3.10"

    def test_len_3(self):
        guesses = ['aaaaa', 'bbbbb', 'ccccc', 'ddddd', 'eeeee']
        answers = ['abbda', 'ccaab', 'ababc']
        common = lib.CommonLetters(answers)
        smart_guesses = common.get_smart_guesses(guesses, 3)
        assert smart_guesses == ['aaaaa', 'bbbbb', 'ccccc']
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


class TestMergeFeedback:
    def test_merge_to_empty(self):
        new = lib.Feedback()
        new.greens = ['a', None, None, None, None]
        new.yellows = [[], ['o'], [], [], []]
        new.grays = set(['b'])

        f = lib.Feedback()

        f.merge(new)
        assert f.greens == ['a', None, None, None, None]
        assert f.yellows == [[], ['o'], [], [], []]
        assert f.grays == set(['b'])

    def test_merge_with_empty(self):
        new = lib.Feedback()

        f = lib.Feedback()
        f.greens = ['a', None, None, None, None]
        f.yellows = [[], ['o'], [], [], []]
        f.grays = set(['b'])

        f.merge(new)
        assert f.greens == ['a', None, None, None, None]
        assert f.yellows == [[], ['o'], [], [], []]
        assert f.grays == set(['b'])

    def test_merge_with_same(self):
        greens = ['a', None, 'c', None, 'y']
        yellows = [['d'], ['o'], [], [], []]
        grays = set(['b', 'x', 'z'])

        new = lib.Feedback()
        new.greens = greens
        new.yellows = yellows
        new.grays = grays

        f = lib.Feedback()
        f.greens = greens
        f.yellows = yellows
        f.grays = grays

        f.merge(new)
        assert f.greens == greens
        assert f.yellows == yellows
        assert f.grays == grays

    def test_merge_greens(self):
        new = lib.Feedback()
        new.greens = [None, 'b', 'c', None, 'e']

        f = lib.Feedback()
        f.greens = ['a', None, 'c', None, 'e']

        f.merge(new)
        assert f.greens == ['a', 'b', 'c', None, 'e']

    def test_merge_nonmatching_greens(self):
        new = lib.Feedback()
        new.greens = ['a', 'b', 'c', 'z', 'e']

        f = lib.Feedback()
        f.greens = ['a', 'b', 'c', 'd', 'e']

        with pytest.raises(ValueError):
            f.merge(new)

    def test_merge_yellows(self):
        new = lib.Feedback()
        new.yellows = [[], ['b'], [], ['e'], ['aaaa', 'b']]

        f = lib.Feedback()
        f.yellows = [['a'], ['bb'], [], [], ['aaa', 'b', 'f', 'eee']]

        f.merge(new)
        [yel.sort() for yel in f.yellows]
        assert f.yellows == [['a'], ['bb'], [], ['e'], ['aaaa', 'b', 'eee', 'f']]

#    This check functionality has performance cost and wasn't implemented
#    it isn't stricly necessary
#    def test_merge_grays_conflict(self):
#        new = lib.Feedback()
#        new.grays = set(['a'])
#
#        f = lib.Feedback()
#        f.grays = set(['aa'])
#
#        with pytest.raises(ValueError):
#            f.merge(new)

    def test_merge_grays(self):
        new = lib.Feedback()
        new.grays = set(['a', 'bb', 'c', 'd'])

        f = lib.Feedback()
        f.grays = set(['a', 'bb', 'd', 'e', 'f'])

        f.merge(new)
        assert f.grays == set(['a', 'bb', 'c', 'd', 'e', 'f'])

    def test_merge_lots(self):
        new = lib.Feedback()
        new.greens = ['a', 'b', None, None, None]
        new.yellows = [[], [], ['d'], [], []]
        new.grays = set(['n', 'o'])

        f = lib.Feedback()
        f.greens = ['a', None, None, None, 'e']
        f.yellows = [['e'], [], ['b'], ['d', 'a'], []]
        f.grays = set(['f', 'g', 'h', 'i', 'j', 'k', 'l', 'm'])

        f.merge(new)
        [yel.sort() for yel in f.yellows]
        assert f.greens == ['a', 'b', None, None, 'e']
        assert f.yellows == [['e'], [], ['b', 'd'], ['a', 'd'], []]
        assert f.grays == set(['f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o'])


class TestIsSameFeedback:
    def test_empty(self):
        f1 = lib.Feedback()
        f2 = lib.Feedback()
        assert f1 == f2
        assert f2 == f1

    def test_all_same(self):
        f1 = lib.Feedback()
        f1.greens = ['a', None, 'c', 'd', None]
        f1.yellows = [['a'], [], ['c', 'dd'], [], ['e', 'f', 'a']]
        f1.grays = set(['ppp', 'oo', 'c', 'b', 'a'])
        f2 = lib.Feedback()
        f2.greens = ['a', None, 'c', 'd', None]
        f2.yellows = [['a'], [], ['dd', 'c'], [], ['e', 'f', 'a']]
        f2.grays = set(['a', 'b', 'c', 'oo', 'ppp'])
        assert f1 == f2
        assert f2 == f1

    def test_diff_greens(self):
        f1 = lib.Feedback()
        f1.greens = ['a', None, 'c', 'd', 'e']
        f2 = lib.Feedback()
        f2.greens = ['a', None, 'c', 'd', None]
        assert not f1 == f2
        assert not f2 == f1

    def test_diff_yellows(self):
        f1 = lib.Feedback()
        f1.yellows = [['a'], [], ['c', 'd'], [], ['e', 'f', 'a']]
        f2 = lib.Feedback()
        f2.yellows = [['a'], [], ['d', 'c'], [], ['e', 'ff', 'a']]
        assert not f1 == f2
        assert not f2 == f1

    def test_diff_grays(self):
        f1 = lib.Feedback()
        f1.grays = set(['ppp', 'oo', 'c', 'b', 'a'])
        f2 = lib.Feedback()
        f2.grays = set(['a', 'b', 'c', 'o', 'ppp'])
        assert not f1 == f2
        assert not f2 == f1


class TestFindSmartGuesses:
    def test_len_3(self):
        guesses = ['aaaaa', 'bbbbb', 'ccccc', 'ddddd', 'eeeee']
        answers = ['abbda', 'ccaab', 'ababc']
        common = lib.CommonLetters(answers)
        smart_guesses = common.get_smart_guesses(guesses, 3)
        assert smart_guesses == ['aaaaa', 'bbbbb', 'ccccc']

    def test_repeat_letters(self):
        guesses = ['laugh', 'crime', 'fight', 'lawns', 'lines']
        answers = ['light', 'wight', 'sight', 'night']
        common = lib.CommonLetters(answers)
        smart_guesses = common.get_smart_guesses(guesses, 3)
        assert smart_guesses == ['lawns', 'lines', 'laugh']

    def test_similar_words_pivot(self):
        answers = ['agape', 'agate', 'agave']
        words = lib.get_all_words_list()
        common = lib.CommonLetters(answers)
        smart_guesses = common.get_smart_guesses(words, 10)
        assert smart_guesses[0] == 'pivot'

    def test_similar_words_ight(self):
        answers = ['fight', 'light', 'aight', 'kight', 'eight']
        words = lib.get_all_words_list()
        common = lib.CommonLetters(answers)
        smart_guesses = common.get_smart_guesses(words, 10)
        assert smart_guesses[0] == 'flake'

    def test_entire_answer_pool(self):
        answers = lib.get_answer_list()
        words = lib.get_all_words_list()
        common = lib.CommonLetters(answers)
        smart_guesses = common.get_smart_guesses(words, 10)
        assert smart_guesses[0] == 'soare'


class TestFindExactBestGuess:
    def test_one_answer(self):
        guesses = ['right']
        answers = ['right']
        best = lib.find_exact_best_guess(guesses, answers)
        assert best == 'right'

    def test_two_answer(self):
        guesses = ['right', 'wrong']
        answers = ['right']
        best = lib.find_exact_best_guess(guesses, answers)
        assert best == 'right'

    def test_same_scores(self):
        guesses = ['night', 'sight', 'light', 'lawns']
        answers = ['night', 'sight', 'light']
        # night scenarios = {1:1, 2:1, 3:1} = 2
        # sight scenarios = {1:1, 2:1, 3:1} = 2
        # light scenarios = {1:1, 2:1, 3:1} = 2
        # lawns scenarios = {2:3}           = 2
        best = lib.find_exact_best_guess(guesses, answers)
        assert best == 'night' or best == 'lawns'

    def test_mutually_exclusive_answerpool_short(self):
        guesses = ['aaaaa', 'bbbbb', 'ccccc', 'ddddd']
        answers = ['aaaaa', 'bbbbb', 'ccccc', 'ddddd']
        best = lib.find_exact_best_guess(guesses, answers)
        assert best == 'aaaaa'

    def test_mutually_exclusive_answerpool_mid(self):
        guesses = ['aaaaa', 'bbbbb', 'ccccc', 'ddddd', 'abcde']
        answers = ['aaaaa', 'bbbbb', 'ccccc', 'ddddd']
        best = lib.find_exact_best_guess(guesses, answers)
        assert best == 'abcde'

    def test_mutually_exclusive_answerpool_long(self):
        guesses = ['aaaaa', 'bbbbb', 'ccccc', 'ddddd', 'eeeee',
                   'fffff', 'ggggg', 'abcde']
        answers = ['aaaaa', 'bbbbb', 'ccccc', 'ddddd', 'eeeee',
                   'fffff', 'ggggg']
        best = lib.find_exact_best_guess(guesses, answers)
        assert best == 'abcde'

    def test_mutually_exclusive_answerpool_4(self):
        guesses = ['aaaaa', 'bbbbb', 'ccccc', 'ddddd', 'eeeee',
                   'abcee', 'abcde']
        answers = ['aaaaa', 'bbbbb', 'ccccc', 'ddddd', 'eeeee',
                   'abcee']
        best = lib.find_exact_best_guess(guesses, answers)
        assert best == 'abcee'  # not calculated but I think its right

    # test takes ~ 5-10 min
    #def test_similar_words(self):
    #    ANSWER = 'mated'
    #    words = lib.get_all_words_list()
    #    f = lib.get_guess_feedback('roate', ANSWER)
    #    f.merge(lib.get_guess_feedback('sated', ANSWER))
    #    guesses_tried = set(['roate', 'sated'])
    #    possible_answers = ['bated', 'dated', 'fated', 
    #                        'gated', 'hated', 'mated']
    #    smart_guesses = lib.filter_guess_pool(words, possible_answers, 100)
    #    g = lib.find_exact_best_guess(words, possible_answers, f, 
    #                                  guesses_tried, smart_guesses)
    #    # g == 'baghs' 

    def test_many_similar_answers(self):
        answers = ['aeons', 'aeros', 'aloes', 'alose', 'arose',
                   'neosa', 'oases', 'oaves', 'oxeas', 'paseo',
                   'psoae', 'soare', 'soave', 'stoae', 'toeas',
                   'zoeas']
        guesses = answers
        lib.find_exact_best_guess(guesses, answers)


class TestFindApproximateBestGuess:
    def test_subset_wordpool(self):
        answers = lib.get_answer_list()
        words = lib.get_all_words_list()
        common = lib.CommonLetters(answers)
        smart_guesses = common.get_smart_guesses(words, 10)
        subset_answers = []
        for i, ans in enumerate(answers):
            if i % 10 == 0:
                subset_answers.append(ans)

        best = lib.find_approximate_best_guess(smart_guesses, subset_answers)
        assert best == 'roate'


class TestTurnsUntilSolved:
    def test_guess_right_answer(self):
        answerpool = ['apple']
        guesspool = ['apple']
        turns = lib.turns_until_solved('apple', guesspool, answerpool)
        assert turns == 1

    def test_guess_wrong_answer(self):
        answerpool = ['apple']
        guesspool = ['plank', 'apple']
        turns = lib.turns_until_solved('plank', guesspool, answerpool)
        assert turns == 2

    def test_two_answers(self):
        answerpool = ['oneor', 'twooo']
        guesspool = ['twooo', 'oneor']
        turns = lib.turns_until_solved('oneor', guesspool, answerpool)
        assert turns == 1.5

    def test_guess_three_answers(self):
        answerpool = ['light', 'night', 'sight']
        guesspool = ['light', 'night', 'sight']
        turns = lib.turns_until_solved('light', guesspool, answerpool)
        assert turns == 2

    def test_nonanswer_three(self):
        answerpool = ['light', 'night', 'sight']
        guesspool = ['light', 'night', 'sight', 'lawns']
        turns = lib.turns_until_solved('lawns', guesspool, answerpool)
        assert turns == 2

    def test_nonanswer_four(self):
        answerpool = ['light', 'night', 'sight', 'might']
        guesspool = ['light', 'night', 'sight', 'lawns']
        turns = lib.turns_until_solved('lawns', guesspool, answerpool)
        assert turns == 2
        # scenarios = {1:0, 2:4}

    def test_abcd(self):
        answerpool = ['aaaaa', 'bbbbb', 'ccccc', 'ddddd']
        guesspool = ['aaaaa', 'bbbbb', 'ccccc', 'ddddd']
        turns = lib.turns_until_solved('aaaaa', guesspool, answerpool)
        assert turns == 2.5
        # scenarios = {1:1, 2:1, 3:1, 4:1}       10/4 = 2.5
        #          -> {1:1, 3:3}

    def test_four(self):
        f = lib.Feedback()
        f.grays = set(['p', 'o', 'y'])
        answerpool = ['smile', 'catch', 'great', 'smash']
        guesspool = ['smile', 'catch', 'great', 'smash']
        turns = lib.turns_until_solved('smile', guesspool, answerpool, f, turn=2)
        assert turns == 2.75
        # scenarios = {2:1, 3:3}       11/4 = 3
        # 2 turn - smile                (right answer)
        # 3 turn - smash, great, catch  (only possible answer is itself)

    def test_len7_all2turns(self):
        guesspool = lib.get_all_words_list()
        answerpool = ['smile', 'frown', 'catch', 'great', 'throw', 'smash']
        turns = lib.turns_until_solved('cgtsa', guesspool, answerpool)
        assert turns == 2

    def test_len7_some2turns(self):
        guesspool = lib.get_all_words_list()
        answerpool = ['smile', 'frown', 'catch', 'great', 'throw', 'smash']
        turns = lib.turns_until_solved('grope', guesspool, answerpool)
        assert round(turns, 3) == 2.167

    def test_kondo(self):
        guesspool = ['smile', 'catch', 'great', 'smash', 'kondo']
        answerpool = ['smile', 'catch', 'great', 'smash']
        turns = lib.turns_until_solved('kondo', guesspool, answerpool)
        assert turns == 2.75
        # {2:1, 3:3} -> 11/4 -> 2.75

    def test_all_guesses(self):
        guesspool = lib.get_all_words_list()
        answerpool = ['smile', 'frown', 'catch', 'great', 'throw', 'smash']
        turns = lib.turns_until_solved('poopy', guesspool, answerpool)
        assert round(turns, 3) == 2.583

    def test_afore_answers(self):
        answers = ['agape', 'agate', 'agave']
        words = lib.get_all_words_list()
        turns = lib.turns_until_solved('xxxxx', words, answers)
        assert turns == 3.0

    def test_afore2_answers(self):
        answers = ['afoot', 'afore', 'afoul', 'agape', 'agate',
                   'agave']
        words = lib.get_all_words_list()
        turns = lib.turns_until_solved('afore', words, answers)
        assert turns == 2.5

    def test_similar_answers(self):
        answerpool = ['aeons', 'aeros', 'aloes', 'alose', 'arose',
                      'neosa', 'oases', 'oaves', 'oxeas', 'paseo',
                      'psoae', 'soare', 'soave', 'stoae', 'toeas',
                      'zoeas']
        guesspool = lib.get_all_words_list()
        turns = lib.turns_until_solved('aloes', guesspool, answerpool)
        assert turns < 2.5

    def test_abode_first_36_answers(self):
        answers = lib.get_answer_list()[:36]
        words = lib.get_all_words_list()

        common = lib.CommonLetters(answers)
        smart_guesses = common.get_smart_guesses(words, 100)
        guess = smart_guesses[0]  # abode
        lib.turns_until_solved(guess, smart_guesses, answers)

    def test_large_subset_answers(self):
        guesspool = lib.get_all_words_list()
        answerpool = lib.get_answer_list()
        subset_answers = []
        for i, answer in enumerate(answerpool):
            if i % 100 == 0:
                subset_answers.append(answer)

        turns = lib.turns_until_solved('roate', guesspool, subset_answers)
        assert turns < 2.5

    def test_large_subset_answers_guess_only_answers(self):
        guesspool = []
        answerpool = lib.get_answer_list()
        subset_answers = []
        for i, answer in enumerate(answerpool):
            if i % 10 == 0:
                subset_answers.append(answer)

        turns = lib.turns_until_solved('roate', guesspool, subset_answers)
        assert turns < 3.0

    def test_random_subset_30_guess_answers_only(self):
        random.seed(42)
        words = lib.get_all_words_list()
        answerpool = []
        max_size = 30
        for i in range(max_size):
            answerpool.append(random.choice(words))
        best_guess = lib.find_best_guess(answerpool, answerpool)
        lib.turns_until_solved(best_guess, answerpool, answerpool)

    def test_random_subset_15_all_guesses(self):
        random.seed(42)
        words = lib.get_all_words_list()
        answerpool = []
        max_size = 15
        for i in range(max_size):
            answerpool.append(random.choice(words))
        best_guess = lib.find_best_guess(words, answerpool)
        lib.turns_until_solved(best_guess, words, answerpool)

class TestIntegration:
    def test_erect_integration(self):
        pass
        # answer = 'erect'
        # feedback = mf(gc('roate', 'erect'), gc('enter', 'erect'), 2)
        # exp = True
        # assert pa(feedback, answer) == exp


class TestPerformance:
    def test_performance_get_guess_feedback(self, benchmark):
        words = lib.get_all_words_list()
        guesses = random.sample(words, 5)

        def benchmark_feedback():
            for guess in guesses:
                for answer in words:
                    lib.get_guess_feedback(guess, answer)
        benchmark(benchmark_feedback)

    def test_performance_possible_answer(self, benchmark):
        words = lib.get_all_words_list()
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

    def test_performance_merge(self, benchmark):
        f0 = lib.Feedback()
        f1 = lib.get_guess_feedback('azcze', 'abcdd')  # greens
        f2 = lib.get_guess_feedback('bcdea', 'abcdd')   # yellows
        f3 = lib.get_guess_feedback('dddaa', 'abcdd')  # multiyels
        f4 = lib.get_guess_feedback('fghij', 'abcdd')  # grays
        feedbacks = [f0, f1, f2, f3, f4]

        def benchmark_merge():
            for fb1 in feedbacks:
                for fb2 in feedbacks:
                    fb1.merge(fb2)
        benchmark(benchmark_merge)
