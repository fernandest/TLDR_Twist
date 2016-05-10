import nltk
from nltk.collocations import *
import string


def printsentence(sentence, fileout):
    for i in range(0, len(sentence)): # beginning of a sentence
        if i == 0:
            fileout.write(sentence[i])
        elif i == len(sentence) - 1:            # end of a sentence
            fileout.write(sentence[i] + "\n\n")
                                            # punctuation
        elif string.punctuation.__contains__(sentence[i]) or (sentence[i] == '."') or (sentence[i] == ',"'):
            fileout.write(sentence[i])
        else:
            if sentence[i-1] == "'" or sentence[i-1] == '"':
                fileout.write(sentence[i])
            else:
                fileout.write(' ' + sentence[i])

# Pass in a list of cleaned sentences and a dictionary containing the score to allocate to each word
def scoresentences(sentenceList, wordscore):
    scoredSentences = []
    for i in sentenceList:
        score = 0
        for j in sentenceList[i]:
            wordscore[sentenceList[i][j]] += score

# Pass in a cleaned list of words; returns a dictionary containing <word, score> pairs
def scorewords(wordsList):
    return nltk.probability.FreqDist(wordsList())
    # Initial configuration is to score the words linearly by the amount of times



# Open text file and set it to raw
f = open('./texts/text1.txt')
raw = f.read()

# Assign the text to a corpus and extract the sentences and words from it
path = nltk.corpus.reader.plaintext.PlaintextCorpusReader("./texts", "text1.txt")
tokens = nltk.word_tokenize(raw)

sentences = path.sents()
words = path.words()
posWords = nltk.pos_tag(words)

posKeep = ["CD", "JJ", "JJR", "JJS", "NN", "NNS", "NNP", "NNPS", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]

cleanPosWords = []
for w in posWords:
    if w[1] in posKeep:
        cleanPosWords.append(w)

print cleanPosWords
print len(cleanPosWords)

fdist1 = nltk.probability.FreqDist(cleanPosWords)

vocabulary1 = fdist1.keys()
print vocabulary1[:25]

# Clean up the words by removing punctuation
noPunctuation = []
for w in words:
    if not string.punctuation.__contains__(w) and (w != '."') and (w != ',"'):
        noPunctuation.append(w)

# while counter < len(sentences):
   # for x in sentencePoints:
collocationsText = nltk.Text(tokens)

bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()
finder = TrigramCollocationFinder.from_words(noPunctuation)
finder.apply_freq_filter(3)
print finder.nbest(bigram_measures.pmi, 10)

sentenceToPrint = {0, 3, 4}
outFile = open('./tldr/outFile.txt', 'w')

for s in range(0, len(sentences)):
    if s in sentenceToPrint:
        printsentence(sentences[s], outFile)

outFile.close()
