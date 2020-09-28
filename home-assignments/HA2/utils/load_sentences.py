import re


PAD_word_idx = 0
SOS_word_idx = 1
EOS_word_idx = 2


class Lang:
    def __init__(self, name):
        self.name = name
        self.word2index = {'PAD': PAD_word_idx, 'SOS': SOS_word_idx, 'EOS': EOS_word_idx}
        self.word2count = {}
        self.index2word = {PAD_word_idx: "PAD", SOS_word_idx: "SOS", EOS_word_idx: "EOS"}
        self.n_words = 3  # Count PAD, SOS, EOS

    def add_sentence(self, sentence):
        for word in sentence.split(' '):
            self.add_word(word)

    def add_word(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1


def normalize_string(s):
    s = s.lower()
    s = re.sub(r'[^\w+]+', r' ', s)
    s = re.sub(r'[0-9]+', r'', s)
    s = s.strip()
    return s


def uses_only_common_words(s, common_words):
    for word in s.split():
        if word not in common_words:
            return False
    return True


def filter_pair(p, max_len, common_input_words, common_output_words):
    return len(p[0].split(' ')) <= max_len and \
           len(p[1].split(' ')) <= max_len and \
           uses_only_common_words(p[0], common_input_words) and \
           uses_only_common_words(p[1], common_output_words)


def get_data_from_file(filename):
    # Read the file and split into lines
    lines = open(filename, encoding='utf-8').read().strip().split('\n')

    # Split every line into pairs and normalize
    pairs = [[normalize_string(s) for s in l.split('\t')] for l in lines]

    # Create temporary Langs
    temp1 = Lang('english')
    temp2 = Lang('spanish')
    for pair in pairs:
        temp1.add_sentence(pair[0])
        temp2.add_sentence(pair[1])

    # Compute common words for each language (used more than THRESHOLD times)
    THRESHOLD = 50
    common_input_words = {word for word in temp1.word2count.keys() if temp1.word2count[word] > THRESHOLD}
    common_output_words = {word for word in temp2.word2count.keys() if temp2.word2count[word] > THRESHOLD}

    # Filter sentences
    MAX_LEN = 9
    pairs = [pair for pair in pairs if filter_pair(pair, MAX_LEN, common_input_words, common_output_words)]

    # Create Lang objects for the filtered sentences
    input_lang = Lang('English')
    output_lang = Lang('Spanish')
    for pair in pairs:
        input_lang.add_sentence(pair[0])
        output_lang.add_sentence(pair[1])

    return pairs, input_lang, output_lang
