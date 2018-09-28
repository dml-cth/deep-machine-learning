import numpy as np
import pickle
import copy
import spacy
import os
from functools import reduce


def test_char_onehot(char_to_onehot, chars):
    c = 'few' if len(char_to_onehot) < len(chars) else 'many'
    assert(len(char_to_onehot) == len(chars)), "There are too {0} entries in `char_to_onehot`".format(c)

    dim0 = np.sum(np.array(list(char_to_onehot.values())), axis=0)
    dim1 = np.sum(np.array(list(char_to_onehot.values())), axis=1)

    assert(np.sum(dim1 == 1) == len(chars)), "Some of the character vectors of `char_to_onehot` are not one hot"
    assert(np.sum(dim0 == 1) == len(chars)), "Some of the one hot vectors in `char_to_onehot` are not unique"

    assert(sorted(chars) == sorted(list(char_to_onehot.keys()))), "The keys of `char_to_onehot` doesnt correspond to the characters of `chars`"
    
    print('Test passed')


class DummyRNN:
    def __init__(self):
        pass


def test_init_routine(init_routine):

    rnn = DummyRNN()
    init_routine(rnn, 10, 9, 8)

    # Check input_dim
    assert (rnn.input_dim == 10), "`input_dim` doesnt contain the input dimension, \nExpected: 10\nActual: {0}".format(
        rnn.input_dim)

    # Check h_start
    assert ('h_start' in rnn.cache), "the key `h_start` doesnt exist in `cache`"
    assert (rnn.cache['h_start'].shape == (
    1, 9)), "the value of `h_start` in cache should be initialized with shape (1, hidden_dim)"
    assert (np.sum(
        rnn.cache['h_start']) == 0), "the values of `h_start` in cache should be all zeros,\nActual:\n{0}".format(
        rnn.cache['h_start'])

    # Check b_h
    assert (rnn.b_h.shape == (
    1, 9)), "the value of `b_h` should be initialized with shape (1, hidden_dim),\nExpected: {0}\nActual: {1}".format(
        (1, 9), rnn.b_h.shape)
    assert (np.sum(rnn.b_h) == 0), "the values of `b_h` should be all zeros,\nActual: {0}".format(rnn.b_h)

    # Check b_y
    assert (rnn.b_y.shape == (
    1, 8)), "the value of `b_y` should be initialized with shape (1, output_dim),\nExpected: {0}\nActual: {1}".format(
        (1, 8), rnn.b_y.shape)
    assert (np.sum(rnn.b_y) == 0), "the values of `b_y` should be all zeros,\nActual: {0}".format(rnn.b_y)

    mean_w_hh = 0
    mean_w_xh = 0
    mean_w_hy = 0
    std_w_hh = 0
    std_w_xh = 0
    std_w_hy = 0

    for i in range(1000):
        input_dim = np.random.choice(10) + 1
        hidden_dim = np.random.choice(10) + 1
        output_dim = np.random.choice(10) + 1

        nn = DummyRNN()
        init_routine(nn, input_dim, hidden_dim, output_dim)

        mean_w_hh += np.mean(nn.W_hh)
        mean_w_xh += np.mean(nn.W_xh)
        mean_w_hy += np.mean(nn.W_hy)
        std_w_hh += np.std(nn.W_hh)
        std_w_xh += np.std(nn.W_xh)
        std_w_hy += np.std(nn.W_hy)

        # W_hh shape
        assert (nn.W_hh.shape == (hidden_dim,
                                  hidden_dim)), "the value of `W_hh` should be initialized with shape (hidden_dim, hidden_dim),\nExpected: {0}\nActual: {1}".format(
            (hidden_dim, hidden_dim), nn.W_hh.shape)
        # W_xh shape
        assert (nn.W_xh.shape == (input_dim,
                                  hidden_dim)), "the value of `W_xh` should be initialized with shape (input_dim, hidden_dim),\nExpected: {0}\nActual: {1}".format(
            (input_dim, hidden_dim), nn.W_xh.shape)
        # W_hy shape
        assert (nn.W_hy.shape == (hidden_dim,
                                  output_dim)), "the value of `W_hy` should be initialized with shape (hidden_dim, output_dim),\nExpected: {0}\nActual: {1}".format(
            (hidden_dim, output_dim), nn.W_hy.shape)

    # W_hh props
    assert np.abs(mean_w_hh / 1000) < 0.001, "The mean of `W_hh` is not close to 0,\nActual mean: {0}".format(
        mean_w_hh / 1000)
    assert np.abs(
        std_w_hh / 1000 - 0.01) < 0.005, "The std dev of `W_hh` is not close to 0.01,\nActual stddev: {0}".format(
        std_w_hh / 1000)

    # W_xh props
    assert np.abs(mean_w_xh / 1000) < 0.001, "The mean of `w_xh` is not close to 0,\nActual mean: {0}".format(
        mean_w_xh / 1000)
    assert np.abs(
        std_w_xh / 1000 - 0.01) < 0.005, "The std dev of `w_xh` is not close to 0.01,\nActual stddev: {0}".format(
        std_w_xh / 1000)

    # w_hy props
    assert np.abs(mean_w_hy / 1000) < 0.001, "The mean of `w_hy` is not close to 0,\nActual mean: {0}".format(
        mean_w_hy / 1000)
    assert np.abs(
        std_w_hy / 1000 - 0.01) < 0.005, "The std dev of `w_hy` is not close to 0.01,\nActual stddev: {0}".format(
        std_w_hy / 1000)

    print('test init passed')


def test_forward_prop_routine(init_routine, forward_prop_routine):
    np.random.seed(1)
    rnn = DummyRNN()
    init_routine(rnn, 10, 9, 10)

    # transposing every value from test_case from hereon because saved in different format
    test_case = pickle.load(open('utils/tests/simple_rnn_test_case.pkl', 'rb'))

    # W_hz and b_z has changed name since saved this file
    test_case['gradients']['W_hy'] = test_case['gradients']['W_hz']
    test_case['gradients']['b_y'] = test_case['gradients']['b_z']
    del test_case['gradients']['b_z']
    del test_case['gradients']['W_hz']

    test_case['input'] = list(map(np.transpose, test_case['input']))
    a = forward_prop_routine(rnn, test_case['input'])

    assert (len(
        a) == 10), "The number of output predictions should be equal to the number of input words. \nInput:{1}\nExpected: 10\nActual: {0}".format(
        len(a), test_case['input'])
    assert (a[0].shape == (1, 10)), "The shape of a predicted word is wrong. \nExpected: (1,10)\nActual: {0}".format(
        a[0].shape)

    print('test passed, dimensions are correct')


def test_backward_prop_routine(init_routine, forward_prop_routine, backward_prop_routine):

    np.random.seed(1)
    dim_input = 20
    dim_output = 20
    dim_hidden = 20
    rnn = DummyRNN()
    init_routine(rnn, dim_input, dim_hidden, dim_output)
    rnn.forward_prop = forward_prop_routine
    rnn.backward_prop = backward_prop_routine
    test_case= {
        'X': [(np.random.rand(1, dim_input)-0.5)*5 for _ in range(2)],
        'Y': [softmax((np.random.rand(1, dim_output)-0.5)*5) for _ in range(2)]
    }

    test_passed = True
    epsilon = 1e-6
    Y_pred = forward_prop_routine(rnn, test_case['X'], reset_h=True)

    gradients = backward_prop_routine(rnn, test_case['Y'], Y_pred)

    # gradient check for one weight at a time
    for weight_name, grad in gradients.items():

        i = 0
        param_n = np.prod(grad.shape)
        grad_vec = np.zeros(param_n)
        approx_vec = np.zeros(param_n)

        differences = np.zeros(param_n)

        weight = getattr(rnn, weight_name)
        for (ix, iy), value in np.ndenumerate(weight):

            grad_vec[i] = grad[ix, iy]

            weight[ix, iy] += epsilon
            J_plus = cross_entropy(forward_prop_routine(rnn, test_case['X'], reset_h=True), test_case['Y'])

            weight[ix, iy] -= 2 * epsilon
            J_minus = cross_entropy(forward_prop_routine(rnn, test_case['X'], reset_h=True), test_case['Y'])

            weight[ix, iy] += epsilon
            approx_vec[i] = (J_plus - J_minus) / (2 * epsilon)

            differences[i] = grad_vec[i] - approx_vec[i]

            # Check if the terms match. If not, print error message and go to next weight
            percent = np.abs((grad_vec[i] - approx_vec[i]) / (approx_vec[i])) * 100
            if percent > 1:
                print('The gradient computed for dL/d{}({},{}) is incorrect.'.format(weight_name, 0, 0))
                print('No further terms in {} will be tested before you fix this error.'.format(weight_name))
                print('Provided:', grad_vec[i], '\tExpected:', approx_vec[i], '\t({}% off)\n'.format(percent))
                test_passed = False
                break

            i += 1
    if test_passed:
        print('Your BPTT implementation is correct.')


def test_apply_gradients_routine(init_routine, apply_gradients_routine):

    np.random.seed(1)
    rnn = DummyRNN()
    init_routine(rnn, 10, 9, 10)

    # transposing every value from test_case from hereon because saved in different format
    test_case = pickle.load(open('utils/tests/simple_rnn_test_case.pkl', 'rb'))

    # W_hz and b_z has changed name since saved this file
    test_case['gradients']['W_hy'] = test_case['gradients']['W_hz']
    test_case['gradients']['b_y'] = test_case['gradients']['b_z']
    del test_case['gradients']['b_z']
    del test_case['gradients']['W_hz']

    test_case['input'] = list(map(np.transpose, test_case['input']))

    # store old weights
    old_weights = {
        'W_xh': copy.copy(rnn.W_xh),
        'W_hh': copy.copy(rnn.W_hh),
        'W_hy': copy.copy(rnn.W_hy),
        'b_h': copy.copy(rnn.b_h),
        'b_y': copy.copy(rnn.b_y)
    }

    gradients = {k: np.transpose(v) for k, v in test_case['gradients'].items() }
    learning_rate = test_case['learning_rate']
    apply_gradients_routine(rnn, gradients, learning_rate)

    for weight, grad in gradients.items():
        updated_weight = old_weights[weight] - learning_rate * grad
        assert np.allclose(updated_weight, getattr(rnn, weight), rtol=1e-07, atol=1e-06), "Apply gradients not correctly implemented. `{0}` was updated incorrect for test case. \n{0} input gradient: \n{1}\nlearning rate: {4}\nExpected new weight: \n{2}\nActual new weight: \n{3}".format(weight, gradients[weight], updated_weight, getattr(rnn, weight), learning_rate)

    print('test apply gradients passed')


def cross_entropy(ys_pred, ys):
    sum = 0
    for y, y_pred in zip(ys, ys_pred):
        sum += -y*np.log(y_pred + 1e-10)
    return np.sum(sum)


def softmax(z):
    """ Implement the softmax activation function

    Arguments:
    z - the input of the activation function, shape (BATCH_SIZE, FEATURES) and type `numpy.ndarray`

    Returns:
    a - the output of the activation function, shape (BATCH_SIZE, FEATURES) and type `numpy.ndarray`
    """
    a = np.exp(z - np.max(z, axis=1, keepdims=True)) / np.exp(z - np.max(z, axis=1, keepdims=True)).sum(axis=1,
                                                                                                        keepdims=True)
    return a


def test_preprocess_line(f, uni_to_ascii):
    test_cases = [
        ("lol\t¡Socorro!   ¡Auxilio!", ['lol', 'socorro ! auxilio !']),
        ("i\t   ¡Órale!   ", ['i', 'orale !']),
        ("(Do men cry)?\t    ¿Los HOMBRES lloran?", ['do men cry ?', 'los hombres lloran ?']),
        ("no\tabcdefghijiklmnopqrstuvxyzåäöABCDEFGHIJKLMNOPQRSTUVXYZÅÄÖ.", ['no', 'abcdefghijiklmnopqrstuvxyzaaoabcdefghijklmnopqrstuvxyzaao .']),
        ("It happens.\tEso pasa.", ['it happens .', 'eso pasa .'])
    ]
    preprocessed_list = [f(test_case[0]) for test_case in test_cases]
    for preprocessed, test_case in zip(preprocessed_list, test_cases):
        assert(type(preprocessed) == list), "`preprocess_line` should return a list, returned {0}".format(type(preprocessed))
        assert(preprocessed == test_case[1]), "preprocess not correct. Expected: {0}, Actual: {1}".format(test_case[1], preprocessed)
    print('test passed')


def test_remove_long_sentences_and_shuffle(f, SEQ_MAX_LEN):
    test_cases = [[[
            "tom believed .",
            "dont you feel anything brother ?",
            "get the kid .",
            "ill catch up .",
            "had a smile .",
            "the baby has fallen asleep .",
            "situation is not hopeless .",
            "its nothing personal .",
            "this song ?",
            "the prophecy ."
        ],[
             "tom le creia .",
             "no sentis nada hermano ?",
             "lleva al nino .",
             "te alcanzare pronto .",
             "tenia una sonrisa .",
             "el bebe se ha dormido .",
             "la situacion no es desesperada .",
             "no es personal .",
             "esta cancion ?",
             "la profecia ."
        ]
    ], [[
            "tom believed .",
            "get the kid .",
            "ill catch up .",
            "had a smile .",
            "its nothing personal .",
            "this song ?",
            "the prophecy ."
        ],[
             "tom le creia .",
             "lleva al nino .",
             "te alcanzare pronto .",
             "tenia una sonrisa .",
             "no es personal .",
             "esta cancion ?",
             "la profecia ."
        ]
    ]]
    eng, spa = f(test_cases[0][0], test_cases[0][1])
    assert(len(eng) == len(spa)), "You have removed an uneven amount of sentences. Eng sentences: {0}, Spa sentences: {1}".format(len(eng), len(spa))
    c = 'few' if len(eng) > 7 else 'many'
    assert(len(eng) == 7), "You have pruned too {0} sentences. \nExpected:\n{1}\nActual:\n{2}".format(c,test_cases[1], [eng,spa] )

    shuffled = False
    for engs, spas, test_case_eng, test_case_spa in zip(eng, spa, test_cases[1][0], test_cases[1][1]):
        if engs != test_case_eng or spas != test_case_spa:
            shuffled = True
            break
    assert(shuffled), "You have not shuffled the data set"

    for engs, spas in zip(eng, spa):
        assert(engs in test_cases[1][0]), "You removed {0}, when it shouldn't have been removed. \nExpected:\n{1}\nActual:\n{2}".format(engs, test_cases[1], [eng, spa])
        assert(spas in test_cases[1][1]), "You removed {0}, when it shouldn't have been removed. \nExpected:\n{1}\nActual:\n{2}".format(spas, test_cases[1], [eng, spa])
        ix = test_cases[1][0].index(engs)
        assert(test_cases[1][0].index(engs) == test_cases[1][1].index(spas)), "You Spa and Eng sentences are not paired up correctly.  \nExpected:\n{0}\nActual:\n{1}".format(test_cases[1], [eng, spa])
    print('test passed')


def test_ix_word(eng_ix_to_word, eng_word_to_ix, spa_ix_to_word, spa_word_to_ix, eng, spa):
    assert(eng_ix_to_word[0] == 'ZERO'), "The first element of `eng_ix_to_word` is not ZERO"
    assert(eng_ix_to_word[-1] == 'UNK'), "The last element of `eng_ix_to_word` is not UNK"
    assert(spa_ix_to_word[0] == 'ZERO'), "The first element of `spa_ix_to_word` is not ZERO"
    assert(eng_ix_to_word[-1] == 'UNK'), "The last element of `spa_ix_to_word` is not UNK"

    eng_vocab = set([word for sentence in eng for word in sentence.split(' ')])
    spa_vocab = set([word for sentence in spa for word in sentence.split(' ')])



    assert(len(eng_vocab)+2 == len(eng_ix_to_word)), "`eng_ix_to_word` doesnt contain the entire vocabulary from `eng`"
    assert(len(spa_vocab)+2 == len(spa_ix_to_word)), "`spa_ix_to_word` doesnt contain the entire vocabulary from `spa`"
    assert(len(eng_vocab)+2 == len(eng_word_to_ix)), "`eng_word_to_ix` doesnt contain the entire vocabulary from `eng`"
    assert(len(spa_vocab)+2 == len(spa_word_to_ix)), "`spa_word_to_ix` doesnt contain the entire vocabulary from `spa`"

    for ix, word in enumerate(eng_ix_to_word):
        assert(eng_word_to_ix[word] == ix), "The word {0} of index {1} in `eng_ix_to_word` doesn't exist as a (key,value) pair in `eng_word_to_ix` ".format(word, ix)
    for ix, word in enumerate(spa_ix_to_word):
        assert(spa_word_to_ix[word] == ix), "The word {0} of index {1} in `spa_ix_to_word` doesn't exist as a (key,value) pair in `spa_word_to_ix` ".format(word, ix)
    print('test passed')


def test_X_Y(X,Y, eng_ix_to_word, spa_ix_to_word, eng, spa):
    sentences_X = [" ".join(map(lambda x : eng_ix_to_word[x], sentence)) for sentence in X]
    for sentence_eng in eng:
        assert(sentence_eng in sentences_X), "\"{0}\" doesnt have an index sentence representation in `X`".format(sentence_eng)
    sentences_Y = [" ".join(map(lambda x : spa_ix_to_word[x], sentence)) for sentence in Y]
    for sentence_spa in spa:
        assert(sentence_spa in sentences_Y), "\"{0}\" doesnt have an index sentence representation in `Y`".format(sentence_spa)
    print('test passed')


def test_X_Y_length(X,Y,SEQ_MAX_LEN):
    for s in X:
        assert(len(s) == SEQ_MAX_LEN), "The length of {0} of `X` is not {1}".format(s, SEQ_MAX_LEN)
        assert(reduce(lambda left, ix: 1 if ix != 0 and left != -1 else (0 if left == 0 else -1), s) != -1), "There exists a zero in the middle of the sentence: {0} from `X`".format(s)

    for s in Y:
        assert(len(s) == SEQ_MAX_LEN), "The length of {0} of `Y` is not {1}".format(s, SEQ_MAX_LEN)
        assert(reduce(lambda left, ix: 1 if ix != 0 and left != -1 else (0 if left == 0 else -1), s) != -1), "There exists a zero in the middle of the sentence: {0} from `Y`".format(s)

    print('test passed')


def test_Y_to_onehot(f):
    vec_len = 1000
    Y = np.random.choice(vec_len, (1000,10))
    Y_onehot = f(Y, vec_len)
    for s, s_onehot in zip(Y, Y_onehot):
        for w, w_onehot in zip(s, s_onehot):
            assert(np.sum(w_onehot) == 1), "The sum of a one hot vector should equal to 1, instead it is {0}\nActual one-hot: {1}".format(np.sum(w_onehot), w_onehot)
            assert(np.argmax(w_onehot) == w), "The one hot vector of {0} doesnt have its `1` at index {0}\nActual one-hot: {1}".format(w, w_onehot)
    print('test passed')


def test_predictions(translate, sentence, eng_word_to_ix, spa_ix_to_word, model):
    test_cases = [
        ['she is a singer .',  'ella es cantante .'],
        ['my opinion is irrelevant .', 'mi opinion es irrelevante .'],
        ['look out for pickpockets .' , 'ojo con los lanzas .'],
        ['this might just work .' , 'esto simplemente podria funcionar .'],
        ['these books are mine .' , 'estos libros son mios .'],
        ['the police are there .' , 'la policia esta alli.'],
        ['the car is very fast .' , 'el auto es muy rapido .'],
        ['thats a stupid idea .' , 'esa es una idea estupida .'],
        ['she opens the window .' , 'ella abre la ventana .'],
        ['nothing is happening .', 'no pasa nada .']
    ]
    # word embedding
    os.system('python -m spacy download es') # download embedding if needed
    nlp = spacy.load('es')

    for test_case in test_cases:
        pred = translate(test_case[0])

        s1, s2 = nlp(test_case[1]), nlp(pred)
        similarity = s1.similarity(s2)

        print('Input: "{0}" \nPrediction: "{1}" \nActual "{2}"\nSimilarity: {3}\n-----------------'.format(test_case[0], pred, test_case[1], similarity))
