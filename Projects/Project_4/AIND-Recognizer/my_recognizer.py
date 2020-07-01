import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    # TODO implement the recognizer
    # return probabilities, guesses

    for i in range(test_set.num_items):
        probabilities.append(dict())
        X, lenghts = test_set.get_item_Xlengths(i)
        for word, model in models.items():
            try:
                score = model.score(X, lenghts)
            except:
                score = float('-inf')

            probabilities[i][word] = score

    for i in range(len(probabilities)):
        guesses.append("")
        best_score = float('-inf')
        for word, score in probabilities[i].items():
            if score > best_score:
                best_score = score
                guesses[i] = word

    return probabilities, guesses
