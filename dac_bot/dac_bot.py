from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer as CoVe
import random

def read_data(dialog_file, dialog_act_file):
    """
    Read data and return the correct format for our bot.
    :param dialog_file: filepath
    :param dialog_act_file: filepath
    :return: list of tuples with (utterance, dialog_act)
    """
    with open(dialog_file, encoding="utf-8") as f:
        dialog_lines = f.readlines()

    with open(dialog_act_file, encoding="utf-8") as f:
        dialog_act_lines = f.readlines()

    utterance = []
    act = []

    for line in dialog_lines:
        utterance += line.split('__eou__')

    for line in dialog_act_lines:
        act += line.split(' ')

    utterance = [u for u in utterance if u != '\n']
    act = [a for a in act if a != '\n']

    return utterance, act

vectorizer = CoVe()
X_test, y_test = read_data('test/dialogues_test.txt', 'test/dialogues_act_test.txt')
X_train, y_train = read_data('train/dialogues_train.txt','train/dialogues_act_train.txt')
X_val, y_val = read_data('validation/dialogues_validation.txt', 'validation/dialogues_act_validation.txt')
X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)


mnb = MultinomialNB()

mnb.fit(X_train, y_train)
