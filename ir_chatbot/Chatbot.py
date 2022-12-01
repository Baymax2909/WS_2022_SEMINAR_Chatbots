from sklearn.feature_extraction.text import CountVectorizer as CoVe
from sklearn.metrics.pairwise import cosine_similarity


def retrive_most_similar(cv, model, query):
    query_vec = cv.transform([query]).toarray()
    sim = cosine_similarity(query_vec, model)
    idx = sim.argmax()

    return idx


with open('dialogues_text.txt', encoding="utf-8") as f:
    lines = f.readlines()

utterances = []

for line in lines:
    utterances += line.split('__eou__')

utterances = [u for u in utterances if u != '\n']

vectorizer = CoVe()

x = vectorizer.fit_transform(utterances)

question = input("Talk to the bot:")
result = retrive_most_similar(vectorizer, x.toarray(), question)
print("Response: " + utterances[result + 1])
