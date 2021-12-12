import gensim.downloader as api
import csv
from random import randrange

modelName = "word2vec-google-news-300"

# Same Corpora, different embeddings sizes
# modelName = "glove-wiki-gigaword-50"
# modelName = "glove-wiki-gigaword-300"

# Different Corpora, same embedding sizes
# modelName = "glove-twitter-100"
# modelName = "glove-wiki-gigaword-100"

model = api.load(modelName)
sizeOfVocab = len(model.index_to_key)
guessed = 0
correct = 0
f = open(f'{modelName}-details.csv', "w")
with open('synonyms.csv', newline='\n') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        questionExists = True
        option1Exists = True
        option2Exists = True
        option3Exists = True
        option4Exists = True
        try:
            model[row["question"]]
        except KeyError:
            questionExists = False
        try:
            model[row["0"]]
        except KeyError:
            option1Exists = False
        try:
            model[row["1"]]
        except KeyError:
            option2Exists = False
        try:
            model[row["2"]]
        except KeyError:
            option3Exists = False
        try:
            model[row["3"]]
        except KeyError:
            option4Exists = False

        label = ""
        guess = ""
        s1 = -10000
        s2 = -10000
        s3 = -10000
        s4 = -10000

        if questionExists and option1Exists:
            s1 = model.similarity(row["question"], row["0"])
        if questionExists and option2Exists:
            s2 = model.similarity(row["question"], row["1"])
        if questionExists and option3Exists:
            s3 = model.similarity(row["question"], row["2"])
        if questionExists and option4Exists:
            s4 = model.similarity(row["question"], row["3"])

        if not questionExists or (not option1Exists and not option2Exists and not option3Exists and not option4Exists):
            label = "guess"
            guessIndex = randrange(4)
            guess = row[str(guessIndex)]
            guessed += 1
        else:
            if s1 > s2 and s1 > s3 and s1 > s4:
                guess = row["0"]
                if row["0"] == row["answer"]:
                    label = "correct"
                    correct += 1
                else:
                    label = "wrong"
            if s2 > s1 and s2 > s3 and s2 > s4:
                guess = row["1"]
                if row["1"] == row["answer"]:
                    label = "correct"
                    correct += 1
                else:
                    label = "wrong"
            if s3 > s2 and s3 > s1 and s3 > s4:
                guess = row["2"]
                if row["2"] == row["answer"]:
                    label = "correct"
                    correct += 1
                else:
                    label = "wrong"
            if s4 > s2 and s4 > s3 and s4 > s1:
                guess = row["3"]
                if row["3"] == row["answer"]:
                    label = "correct"
                    correct += 1
                else:
                    label = "wrong"

        f.write(f'{row["question"]}, ')
        f.write(f'{row["answer"]}, ')
        f.write(f'{guess}, ')
        f.write(f'{label}\n')

analysis = open('analysis.csv', "a")
analysis.write(f'{modelName}, ')
analysis.write(f'{sizeOfVocab}, ')
analysis.write(f'{correct}, ')
analysis.write(f'{80-guessed}, ')
analysis.write(f'{correct/(80-guessed)}\n')
