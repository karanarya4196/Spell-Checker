# Import Libraries

import operator
import re

# Read File

f = open("text.txt", "r")
lines = f.read()

# Text Preprocessing
# Regular Expression is used to remove punctuations, symbols, one letter words to retain all aphabetic characters

lines = re.sub('\s+', ' ', lines)
pattern = re.compile('([^\s\w]|_)+')
lines = pattern.sub('', lines)
lines = re.sub(r'[0-9]+', '', lines)
lines = re.sub(r'[,.:@#?!&$]', ' ', lines)
words = lines.split(' ')
words = [x for x in words if x]
corpus = [s for s in words if len(s) > 1]

# Logic Implementation
# Given an input word from the user, the wordSplitSet function generates a list of tuples with all possible combinations of the input word

# Exhaustive list of word suggestions for one letter error cases
# 1. The words are juggled/ re-assembled
# 2. Additional alphabetic characters are added at various positions of all combinations
# 3. In the case of repetitive characters, replacement is done instead of addition
# 4. Alphabetic characters are also deleted to generate more suggestions


def oneLetterSuggestions(word):
    
    def wordSplitSet(word):
        wordLength = len(word) + 1
        splitWordSet = []
        for index in range(wordLength):
            splitWordSet.append(tuple((word[:index], word[index:])))
        return splitWordSet
    splitWordSet = wordSplitSet(word)
    
    def rightTupleDeletion(splitWordSet):
        deleteTupleList = []
        for index in splitWordSet:
            if index[1] != '':
                deleteTupleList.append(index[0] + index[1][1:])
        return deleteTupleList

    deleteTupleList = rightTupleDeletion(splitWordSet)
    
    
    def jugglingLetters(splitWordSet):
        jugglingWordSet = []
        for index in splitWordSet:
            if len(index[1]) > 1:
                jugglingWordSet.append(index[0] + index[1][1] + index[1][0] + index[1][2:])

        return jugglingWordSet


    jugglingWordSet = jugglingLetters(splitWordSet)
    
    
    def replaceAlphabets(splitWordSet):
        replaceAlphabetList = []
        alphabets = 'abcdefghijklmnopqrstuvwxyz'
        for index in splitWordSet:
            if index[1] != '':
                for a in alphabets:
                    replaceAlphabetList.append(index[0] + a + index[1][1:])

        return replaceAlphabetList

    replaceAlphabetList = replaceAlphabets(splitWordSet)
    
    def addAlphabets(splitWordSet):
        addAlphabetList = []
        alphabets = 'abcdefghijklmnopqrstuvwxyz'
        for index in splitWordSet:
            if index[1] != '':
                for a in alphabets:
                    addAlphabetList.append(index[0] + a + index[1])

        return addAlphabetList

    addAlphabetList = addAlphabets(splitWordSet)
    
    exhaustiveWordSet = set(addAlphabetList + replaceAlphabetList + jugglingWordSet + deleteTupleList)
    return exhaustiveWordSet


# Exhaustive list of word suggestions for two letter error cases

def twoLetterSuggestions(word):
    for word1 in oneLetterSuggestions(word):
        for word2 in oneLetterSuggestions(word1):
            return word2
        

# Looking up for the word in the corpus

def exhaustiveWordSetLookUp(exhaustiveWordSet):
    wordLookUp = []
    for w in exhaustiveWordSet:
        if w in corpus:
            wordLookUp.append(w)    
    return set(wordLookUp)


# Creating a dictionary with the word suggestion as the 'key' and its probabilty of occurence as the 'value'

def spellSuggestions(word, wordLookUp):
    wordSuggestions = exhaustiveWordSetLookUp([word])
    wordSuggestions.update(wordLookUp)
    wordSuggestions.update([word])
    wordProbabilityDict = {}
    for w in wordSuggestions:
        if w in corpus:
            wordProbabilityDict.update({w: (float(corpus.count(w)) / len(corpus))})
    return (wordProbabilityDict)


# Provides the best two possible word suggestions based on the concept of probability
# Multiple cases are handled
# 1. When the word is not present in the corpus
# 2. When the word is present, but has incorect spelling
# 3. When the word is present, but has possibly a correct spelling
# 4. When the word is present with correct spelling, but with second best frequency in the corpus

def spellChecker(word, wordLookUp): 
    wordProbabilityDict = spellSuggestions(word, wordLookUp)
    wordProbabilityList = (sorted(wordProbabilityDict.items(), key=operator.itemgetter(1), reverse=True))
    if not wordProbabilityDict:
        print('The word ' + word + ' is not present in the corpus!')
    else:
        if len(wordProbabilityList) >= 2:
            if word == wordProbabilityList[0][0]:
                print('The input word ' + word + ' is correctly spelt! The other suggestion to consider is '+ wordProbabilityList[1][0] + '!')
            elif word == wordProbabilityList[1][0]:
                print('The best suggestion for the input word ' + word + ' is ' + wordProbabilityList[0][0] + '!' + ' However, ' + word + ' may also be spelled correctly!')
            else:
                print('The best suggestion for the input word ' + word + ' is ' + wordProbabilityList[0][0] + '!' + ' The second best suggestion is ' + wordProbabilityList[1][0] + '!')
        else:
            if word == wordProbabilityList[0][0]:
                print('The input word ' + word + ' is correctly spelt!')
            else:
                print('The best suggestion for the input word ' + word + ' is ' + wordProbabilityList[0][0] + '!')
    
# The main function to call all other functions

def getSpellChecker(input_text):
    exhaustiveWordSet = oneLetterSuggestions(input_text)
    twoExhaustiveWordSet = twoLetterSuggestions(input_text)
    
    # The ultimate suggestion list

    exhaustiveWordSet.update(twoExhaustiveWordSet)
    wordLookUp = exhaustiveWordSetLookUp(exhaustiveWordSet)
    spellChecker(input_text, wordLookUp)


# Case I: Word not present. Example input: karan
# Case II: Word present with incorrect spelling. Example input: provde
# Case III: Word present with correct spelling. Example input: drove
# Case IV: Word present with correct spelling but with second best frequency in the corpus. Example input: prove


input_text = input('Enter your word: ')
getSpellChecker(input_text)
