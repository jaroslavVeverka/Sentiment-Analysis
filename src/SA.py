from tabulate import tabulate

# nacteni souboru s vetami a s pozitivnimi a negativnimi slovy
file = open('C://Users/jarda/OneDrive - Vysoká škola ekonomická v Praze/2. semestr ZWT/4IZ470 - Dolování znalostí z '
            'webu/cvika/DU_AS/sentences.txt')

positiveVocabulary = open('C://Users/jarda/OneDrive - Vysoká škola ekonomická v Praze/2. semestr ZWT/4IZ470 - '
                          'Dolování znalostí z webu/cvika/DU_AS/bing-positive-words.txt')

negativeVocabulary = open('C://Users/jarda/OneDrive - Vysoká škola ekonomická v Praze/2. semestr ZWT/4IZ470 - '
                          'Dolování znalostí z webu/cvika/DU_AS/bing-negative-words.txt')


# trida Sentence pro ulozeni informaci o vete behem analyzy
class Sentence:

    # konstruktor tridy
    def __init__(self, id, text):
        self.id = id
        self.text = text
        self.words = []
        self.numOfPositivWords = 0
        self.numOfNegativWords = 0
        self.opinion = 'NA'

    # metoda pro urceni vysledneho hodnoceni vety
    def setopinion(self):
        s = 0
        if self.numOfPositivWords or self.numOfNegativWords != 0:
            s = self.numOfPositivWords / (self.numOfPositivWords + self.numOfNegativWords)

            if s > 0.5:
                self.opinion = 1
            else:
                self.opinion = 0


def preprocessdata(file, positiveVocabulary, negativeVocabulary):
    # vlozeni pozitivnich slov do listu
    positiveTerms = []
    for line in positiveVocabulary:
        positiveTerms.append(line.strip())

    # vlozeni negativnich slov do listu
    negativeTerms = []
    for line in negativeVocabulary:
        negativeTerms.append(line.strip())

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

    return sentences, positiveTerms, negativeTerms


def executeclassification():
    # porovnani jednotlivych slov v jednotlivych vetach s listy pozitivnich a negativnich slov
    for sentence in sentences:
        for word in sentence.words:
            if word in positiveTerms:
                sentence.numOfPositivWords = sentence.numOfPositivWords + 1
                continue
            if word in negativeTerms:
                sentence.numOfNegativWords = sentence.numOfNegativWords + 1
                continue
        sentence.setopinion()


def printresults():
    table = []
    for sentence in sentences:
        result = [sentence.id, sentence.numOfPositivWords, sentence.numOfNegativWords, sentence.opinion]
        table.append(result)

    # vytvoreni samotne tabulky s vysledky analyzy
    print(tabulate(table, headers=["ID", "Number of positive words", "Number of negative words", "Opinion"]))


sentences, positiveTerms, negativeTerms = preprocessdata(file, positiveVocabulary, negativeVocabulary)
executeclassification()
printresults()
