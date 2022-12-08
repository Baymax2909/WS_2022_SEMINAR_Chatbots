from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression


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


utterances, acts = read_data('./test/dialogues_test.txt', './test/dialogues_act_test.txt')

mnb = MultinomialNB()

mnb.fit