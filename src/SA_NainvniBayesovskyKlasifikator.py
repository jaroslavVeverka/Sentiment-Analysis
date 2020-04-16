from tabulate import tabulate
import pandas as pd

# nacteni souboru s vetami a s pozitivnimi a negativnimi slovy
file = open('C://Users/jarda/OneDrive - Vysoká škola ekonomická v Praze/2. semestr ZWT/4IZ470 - Dolování znalostí z '
            'webu/cvika/DU_AS/sentences.txt')

# nacteni je nutne bez hlavicky!!! --> jen samotna slova
positiveVocabulary = pd.read_csv('C://Users/jarda/OneDrive - Vysoká škola ekonomická v Praze/2. semestr '
                                 'ZWT/4IZ470 - Dolování znalostí z webu/cvika/DU_AS/probDistPosSmoothing.csv',
                                 header=None)
positiveVocabulary = positiveVocabulary.set_index(0, drop=False)

# nacteni je nutne bez hlavicky!!! --> jen samotna slova
negativeVocabulary = pd.read_csv('C://Users/jarda/OneDrive - Vysoká škola ekonomická v Praze/2. semestr '
                                 'ZWT/4IZ470 - Dolování znalostí z webu/cvika/DU_AS/probDistNegSmoothing.csv',
                                 header=None)
negativeVocabulary = negativeVocabulary.set_index(0, drop=False)


# trida Sentence pro ulozeni informaci o vete behem analyzy
class Sentence:

    # konstruktor tridy
    def __init__(self, id, text):
        self.id = id
        self.text = text
        self.words = []
        self.probPositive = 'NA'
        self.probNegativ = 'NA'
        self.opinion = 'NA'

    def setopinion(self):
        if self.probPositive > self.probNegativ:
            self.opinion = 1
        else:
            self.opinion = 0


def preprocessdata(file):
    # vlozeni vet do listu jako objekty tridy Sentence
    sentences = []
    i = 1
    for line in file:
        sen = Sentence(i, line.strip())
        sentences.append(sen)
        i = i + 1

    # extrakce slov a jejich ulozeni do listu jako atribut words u kazdeho objektu Sentence
    for sentence in sentences:
        sentence.words = sentence.text.lower().replace('.', '').replace(',', '').split()

    return sentences


def executeclassification():
    for sentence in sentences:
        for word in sentence.words:

            if word in positiveVocabulary[0].tolist():
                if sentence.probPositive != 'NA':
                    sentence.probPositive = sentence.probPositive * positiveVocabulary.loc[word, 1]
                else:
                    sentence.probPositive = positiveVocabulary.loc[word, 1]

                print(positiveVocabulary.loc[word, 0:1])

            if word in negativeVocabulary[0].tolist():
                if sentence.probNegativ != 'NA':
                    sentence.probNegativ = sentence.probNegativ * negativeVocabulary.loc[word, 1]
                else:
                    sentence.probNegativ = negativeVocabulary.loc[word, 1]

                print(negativeVocabulary.loc[word, 0:1])
        sentence.setopinion()


def printresults():
    # vytvoreni vysledneho vystupu pro kazdou vetu
    table = []
    for sentence in sentences:
        result = [sentence.id, sentence.probPositive, sentence.probNegativ, sentence.opinion]
        table.append(result)

    # vytvoreni samotne tabulky s vysledky analyzy
    print(tabulate(table, headers=["ID", "P(positive|sentence)", "P(negative|sentence)", "Opinion"]))


sentences = preprocessdata(file)
executeclassification()
printresults()
