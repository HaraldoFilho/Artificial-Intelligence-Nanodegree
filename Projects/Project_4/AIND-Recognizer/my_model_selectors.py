import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on BIC scores
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        best_score = float('inf')
        best_n_components = self.max_n_components

        for n_components in range(self.min_n_components, self.max_n_components+1):
            try:
                model = self.base_model(n_components)
                p = pow(n_components, 2) + 2 * n_components * model.n_features - 1
                logL = model.score(self.X, self.lengths)
                logN = math.log(len(self.X))
                score = -2 * logL + p * logN
                if score < best_score:
                    best_score = score
                    best_n_components = n_components
            except:
                pass

        return self.base_model(best_n_components)


class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    https://pdfs.semanticscholar.org/ed3d/7c4a5f607201f3848d4c02dd9ba17c791fc2.pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on DIC scores
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        sum_other_words_score = 0
        best_score = float('-inf')
        best_n_components = self.max_n_components

        for n_components in range(self.min_n_components, self.max_n_components+1):
            try:
                this_word_model = self.base_model(n_components)
                this_word_score = this_word_model.score(self.X, self.lengths)
                for word in self.words:
                    if word != self.this_word:
                        try:
                            X, lengths = self.hwords[word]
                            model = GaussianHMM(n_components=n_components).fit(X, lengths)
                            sum_other_words_score += model.score(X, lengths)
                        except:
                            pass
                score = this_word_score - 1 / ((len(self.words) - 1) * sum_other_words_score)
                if score > best_score:
                    best_score = score
                    best_n_components = n_components
            except:
                pass

        return self.base_model(best_n_components)


class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection using CV
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        best_average_score = float('-inf')
        best_n_components = self.max_n_components
        split_method = KFold(n_splits=2)
        scores = []

        for n_components in range(self.min_n_components, self.max_n_components+1):
            try:
                for cv_train_idx, cv_test_idx in split_method.split(self.sequences):
                    train_X, train_lengths = combine_sequences(cv_train_idx, self.sequences)
                    test_X, test_lengths = combine_sequences(cv_test_idx, self.sequences)
                    model = GaussianHMM(n_components=n_components).fit(train_X, train_lengths)
                    logL = model.score(test_X, test_lengths)
                    scores.append(logL)
                average_score = statistics.mean(scores)
                if average_score > best_average_score:
                    best_average_score = average_score
                    best_n_components = n_components
            except:
                pass

        return self.base_model(best_n_components)
