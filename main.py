import nltk
from nltk.collocations import *
from nltk.corpus import stopwords
import string
import math
import operator


def printsentence(sentence, fileout):
    for i in range(0, len(sentence)):  # beginning of a sentence
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


# Input: list of sentence indexes to be printed, list of sentences in article.
# Output: file containing the requested sentences
def printer(sentencescorelist, sentenceList, wordscorelist, wordList):
    outFile = open('./tldr/outFile.txt', 'w')
    for s in range(0, len(sentenceList)):
        if s in sentencescorelist:
            printsentence(sentenceList[s], outFile)
    outFile.write("Topics to research: ")

    topics = []
    numtopics = 3
    poswords = nltk.pos_tag(wordList)
    poskeep = ["NN", "NNS", "NNP", "NNPS"]

    while numtopics > 0:
        temp = max(wordscorelist.iteritems(), key=operator.itemgetter(1))[0]
        templist = [temp]
        templist = nltk.pos_tag(templist)
        if templist[0][1] in poskeep:
            numtopics -= 1
            topics.append(temp)
        del wordscorelist[temp]
    for i in range(0, len(topics)):
        if i != len(topics) - 1:
            outFile.write(topics[i] + ", ")
        else:
            outFile.write(topics[i])
    outFile.close()


# Input: dictionary containing the scores of each sentence in the article
# Output: list of sentences to be printed, stored by
def picksentences(sentencescores):
    pickedsentences = []
    numsentences = math.ceil(math.log(3.2 * len(sentencescores)))
    numsentences = int(numsentences)
    while numsentences >= 0:
        temp = max(sentencescores.iteritems(), key=operator.itemgetter(1))[0]
        pickedsentences.append(int(temp))
        del sentencescores[temp]
        numsentences -= 1
    return pickedsentences


# Pass in a list of cleaned sentences and a dictionary containing the score to allocate to each word
# Output: dictionary containing <sentence, score> pairs
def scoresentences(sentenceList, wordscore):
    scoredSentences = {}
    for i in range(0, len(sentenceList)):
        score = 0
        for j in range(0, len(sentenceList[i])):
            wordscore[sentenceList[i][j]] += score
        scoredSentences[i] = score
    return scoredSentences


# Pass in a cleaned list of words; returns a dictionary containing <word, score> pairs
def scorewords(wordsList):
    tim = nltk.probability.FreqDist(wordsList)
    return tim
    # Initial configuration is to score the words linearly by the amount of times it appears in the text


def cleansentences(dirtysentences, cleanwordslist):
    cleansentslist = []
    i = 0
    while i < len(dirtysentences):
        cleansentence = []
        j = 0
        while j < len(dirtysentences[i]):
            if dirtysentences[i][j] in cleanwordslist:
                cleansentence.append(dirtysentences[i][j])
            j += 1
        cleansentslist.append(cleansentence)
        i += 1
    return cleansentslist


def cleanwords(dirtywords):
    cleanwordlist = []
    for i in dirtywords:
        if i not in nltk.corpus.stopwords.words('english') and not string.punctuation.__contains__(i) and (i != '."')\
                and(i != ',"'):
            cleanwordlist.append(i)
    return cleanwordlist


def main():
    # Open text file and set it to raw
    f = open('./texts/text1.txt')
    raw = f.read()

    # Assign the text to a corpus and extract the sentences and words from it
    path = nltk.corpus.reader.plaintext.PlaintextCorpusReader("./texts", "text1.txt")
    tokens = nltk.word_tokenize(raw)

    # Generate sentence and word lists for the text
    sentences = path.sents()
    words = path.words()

    # Clean up words and sentences
    cleanedwords = cleanwords(words)
    cleansents = cleansentences(sentences, cleanedwords)

    # Assign a score to the words
    scoredwords = nltk.probability.FreqDist(cleanedwords)
    scoredsentences = scoresentences(cleansents, scoredwords)

    # Pick the highest scoring sentences
    worthysentences = picksentences(scoredsentences)

    # Print the chosen sentences to a file
    printer(worthysentences, sentences, scoredwords, cleanedwords)

    print "Done."

main()
