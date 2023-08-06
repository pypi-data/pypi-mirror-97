from wildgram import wildgram
import Levenshtein as lev
import re
errorMessage = "documents needs to be a list of dictionaries in the form {text: 'text'}"

def isTheSameWord(word1, word2, threshold=0.75):
    test = stripWord(word1)
    test2 = stripWord(word2)
    if test == test2:
        return True
    if len(test) <= 3:
        return False
    if len(test2) <= 3:
        return False
    if test[0] != test2[0]:
        return False
    if lev.ratio(test, test2) < threshold:
        return False
    return True

def stripWord(word):
    ret = word.lower()
    for sb in ["ing$", "ness$", "tion$", "sion$"]:
        ret = re.sub(sb, "", ret)
    return ret

def getTokenLists(textarray):
    if not isinstance(textarray, list):
        raise Exception(errorMessage)
    ret = []
    for i in range(len(textarray)):
        app = []
        try:
            text = textarray[i]["text"]
        except:
            raise Exception(errorMessage)
        tokens = wildgram(text)
        docID = i
        if "docID" in textarray[i]:
            docID = textarray[i]["docID"]
        for tok in tokens:
            tok["docID"] = docID
            app.append(tok)
        ret.append(app)
    return ret


def getPhrases(tokenlists):
    frequency = {}
    for i in range(len(tokenlists)):
        tokens = tokenlists[i]
        for token in tokens:
            if token["tokenType"] == "noise":
                continue
            if token["tokenType"] != "token":
                if token["tokenType"] not in frequency:
                    frequency[token["tokenType"]] = []
                frequency[token["tokenType"]].append(token)
                continue
            if token["token"] not in frequency:
                frequency[token["token"]] = []
            frequency[token["token"]].append(token)

    phrases = sorted(frequency.items(), key=lambda item: len(item[1]), reverse=True)
    return phrases

def groupPhrasesBySimilarity(phrases, threshold=0.75):
    newdata = []

    while len(phrases) != 0:
        print("Unique keywords left...", len(phrases))
        key = phrases.pop(0)
        group = {"phrases": [key[0]], "tokens": key[1]}
        found = False
        indexes = []
        for i in range(len(phrases)):
            if isTheSameWord(key[0], phrases[i][0], threshold):
                group["phrases"].append(phrases[i][0])
                group["tokens"] = group["tokens"] + phrases[i][1]
                continue
            indexes.append(i)
        dat = []
        for index in indexes:
            dat.append(phrases[index])
        phrases = dat
        newdata.append(group)

    return newdata


def synopsis(documents, threshold=0.75):
    if not isinstance(documents, list):
        raise Exception(errorMessage)
    tokenlists = getTokenLists(documents)
    phrases = getPhrases(tokenlists)
    keywords = groupPhrasesBySimilarity(phrases, threshold)
    return keywords



## set of documents in the form [{"text": text}]
## returns set of topics [{"totalFrequency": freq, "phrases": [,,,]}]
