import regex as re
import string
import os
import numpy as np

STOPWORDS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
"you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves',
'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it',
"it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those',
'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with',
'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after',
'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over',
'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where',
'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other',
'some', 'such', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't',
'can', 'just',  'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y']

TOPICWORDS = [{"token": "no", "tokenType": "negation"},
{"token": "not", "tokenType": "negation"},{"token": "nor", "tokenType": "negation"},
{"token": "ain", "tokenType": "negation"},{"token": "aren", "tokenType": "negation"},
{"token": "aren't", "tokenType": "negation"},{"token": "couldn", "tokenType": "negation"},
{"token": "couldn't", "tokenType": "negation"},{"token": "didn", "tokenType": "negation"},
{"token": "didn't", "tokenType": "negation"},{"token": "doesn", "tokenType": "negation"},
{"token": "doesn't", "tokenType": "negation"},{"token": "hadn", "tokenType": "negation"},
{"token": "hadn't", "tokenType": "negation"},{"token": "hasn", "tokenType": "negation"},
{"token": "hasn't", "tokenType": "negation"},{"token": "haven", "tokenType": "negation"},
{"token": "haven't", "tokenType": "negation"},{"token": "isn", "tokenType": "negation"},
{"token": "isn't", "tokenType": "negation"},{"token": "mightn", "tokenType": "negation"},
{"token": "mightn't", "tokenType": "negation"},{"token": "mustn", "tokenType": "negation"},
{"token": "mustn't", "tokenType": "negation"},{"token": "needn", "tokenType": "negation"},
{"token": "needn't", "tokenType": "negation"},{"token": "shan", "tokenType": "negation"},
{"token": "shan't", "tokenType": "negation"},{"token": "shouldn", "tokenType": "negation"},
{"token": "shouldn't", "tokenType": "negation"},{"token": "wasn", "tokenType": "negation"},
{"token": "wasn't", "tokenType": "negation"},{"token": "weren", "tokenType": "negation"},
{"token": "weren't", "tokenType": "negation"},{"token": "won", "tokenType": "negation"},
{"token": "won't", "tokenType": "negation"},{"token": "don", "tokenType": "negation"},
{"token": "don't", "tokenType": "negation"},{"token": "wouldn", "tokenType": "negation"},
{"token": "wouldn't", "tokenType": "negation"},{"token": "denies", "tokenType": "negation"},
{"token": "denied", "tokenType": "negation"},{"token": "\d+", "tokenType": "numeric"},
{"token": "\d+\.\d+", "tokenType": "numeric"},{"token": "will", "tokenType": "future"},
"reveal", "revealed", "h/o", "s/p", "b.i.d.", "t.i.d.", "p.r.n.", "p.o.",
"p.r.", "a.m.", "a.s.", "c.c.", "n.p.o.", "o.d.", "o.s.", "o.u.", "q.s.",
"q.o.d.","t.i.d.", "t.i.n."]

JOINERWORDS = ["of", "in", "to", "on","than","at"]

def pullOutJoiners(merged, text, joinerwords):
    if len(joinerwords) == 0:
        return []
    ret = []
    joiners = "|".join(["(\s|^)"+stop+"(\s|$)" for stop in joinerwords])
    for i in range(len(merged)):
        match = merged[i]
        start = 0
        end = len(text)
        if not re.search("("+joiners+")", text[match[0]:match[1]]):
            continue
        if i > 0:
            start = merged[i-1][0]
        if i < len(merged)-1:
            end = merged[i+1][1]
        if start != merged[i][0] and end != merged[i][1]:
            ret.append((start,end, 'token'))
    return ret

def pullOutNoise(pattern, text, matches):
    matches = matches  + [(match.start(), match.end(), "noise") for match in pattern.finditer(text.lower(),overlapped=True)]
    matches = sorted(matches, key=lambda x: (x[0], x[1]))
    indexes = set(range(len(text)))
    for n in matches:
        indexes = indexes.difference(range(n[0], n[1]))
    prev = 0
    noise = []
    for i in range(len(matches)-1):
        if matches[i][1] < matches[i+1][0]:
            noise.append((matches[prev][0], matches[i][1], 'noise'))
            prev = i+1
    if prev < len(matches):
        noise.append((matches[prev][0], matches[-1][1], 'noise'))
    return noise, indexes

def pullOutTokens(indexes):
    indexes = list(indexes)
    if len(indexes) == 0:
        return []
    indexes = sorted(indexes)
    prev = indexes[0]
    ret = []
    for i in range(len(indexes)-1):
        if indexes[i]+1 != indexes[i+1]:
            ret.append((prev,indexes[i]+1, "token"))
            prev = indexes[i+1]
    ret.append((prev, indexes[-1]+1,"token"))
    return ret

def pullOutTopics(topics, text, indexes):
    ret = []
    punc = [x for x in string.punctuation]
    for topic in topics:
        token = topic
        tokenType = "token"
        if isinstance(topic, dict):
            token = topic["token"]
            tokenType = topic["tokenType"]
        for match in re.finditer("(\s|^)"+token+"(\s|"+"|\\".join(punc)+"\s|$)", text.lower(),overlapped=True):
            for top in re.finditer(token, text[match.start():match.end()].lower()):
                ret.append((top.start()+match.start(), top.end()+match.start(), tokenType))
            indexes = indexes.difference(range(match.start(), match.end()))
    return ret, indexes

def figureOutRegex(stopwords, size=2):
    punc = [x for x in string.punctuation]
    regex = '\n|[\s' + "|\\".join(punc)+ ']{'+ str(size)+',}'
    stops = "|".join(["(\s|^)"+stop+"(\s|$)" for stop in stopwords])
    if len(stops) != 0:
        regex = stops+'|'+regex
    prog = re.compile("("+regex+")")
    return prog

def filterAndSort(matches):
    ret = {}
    for match in matches:
        if match[0] not in ret:
            ret[match[0]] = {}
        if match[1] not in ret[match[0]]:
            ret[match[0]][match[1]] = match[2]
            continue
        if match[2] == "token":
            continue
        ret[match[0]][match[1]] = match[2]
    res = []
    for key in ret:
        for k in ret[key]:
            res.append((key, k, ret[key][k]))

    return sorted(res,key=lambda x: (x[0], x[1]) )


def getNoiseProfileLine(tokens, i):
    if i == -1:
        return ""
    line = tokens[i]["token"]
    if line.find(":") != -1:
        line = line[line.find(":")+1:]
    done = False
    for j in range(i+1, len(tokens)):
        if not done and tokens[j]["tokenType"] != "noise":
            line = line + "<TOKEN>"
        if tokens[j]["tokenType"] == "noise":
            if done and "\n" not in tokens[j]["token"]:
                continue
            done = True
            line = line + tokens[j]["token"]
            if "\n" in tokens[j]["token"]:
                return line
    return line

def assignParents(tokens):
    commonorder = [";", "\. ", "\n",":\n", "\|", "-", ": "]

    order = [(":\n",["\n", "root"]), ("\n", [":\n", "root"]),
    ("\. ", ["\n", ":\n"]), (";", ["\. ", "\n",":\n"]), (": ", ["\n", "\. ", ";"]),
    (",", commonorder), ("-",commonorder), ("\|",commonorder),
    ("(\s|^)and(\s|^)", commonorder), ("(\s|^)or(\s|^)",commonorder),
    ("(\s|^)by(\s|^)", commonorder), ("(\s|^)in(\s|^)",commonorder),
    ("(\s|^)on(\s|^)", commonorder), ("(\s|^)was(\s|^)",commonorder),
    ("(\s|^)is(\s|^)", commonorder), ("(\s|^)but(\s|^)", commonorder)]

    lastKnown = {}
    lastKnownKeys = [ord[0] for ord in order] + ["root", "newLineAny"]
    for key in lastKnownKeys:
        lastKnown[key] = -1

    for i in range(len(tokens)):
        if tokens[i]["tokenType"] != "noise":
            prev = np.amax(np.array(list(lastKnown.values())))
            tokens[i]["parent"] = prev
            continue
        snip = tokens[i]["token"]
        done = False
        for ord in order:
            if re.search(ord[0], tokens[i]["token"].lower()):
                prev = np.amax(np.array(list([lastKnown[r] for r in ord[1]])))
                ## if its a plain new line, determining if it should return to root.
                if "\n" in snip and ":" not in snip:
                    line = getNoiseProfileLine(tokens, i)
                    line2 = getNoiseProfileLine(tokens, lastKnown["newLineAny"])
                    if line.strip() != line2.strip():
                        prev = -1
                if "\n" in snip:
                    lastKnown["newLineAny"] = i
                tokens[i]["parent"] = prev
                lastKnown[ord[0]] = i
                done = True
                break
        if done:
            continue
        prev = np.amax(np.array(list(lastKnown.values())))
        tokens[i]["parent"] = prev
    return tokens

def createRangesFromProg(prog, topics, text, joinerwords, noise=[],ranges=[]):
    noise, leftover = pullOutNoise(prog, text, noise)
    topics, leftover = pullOutTopics(topics, text, leftover)
    tokens = pullOutTokens(leftover)
    merged = sorted(noise + tokens + topics, key=lambda x: (x[0], x[1]))
    ranges = ranges + pullOutJoiners(merged, text, joinerwords) + tokens + topics
    return noise, ranges

def createToken(start, end, type, text, index):
    return {"startIndex": start, "endIndex":end, "token":text[start:end], "tokenType": type, "index": index}

def wildgram(text, stopwords=STOPWORDS, topicwords=TOPICWORDS, include1gram=True, joinerwords=JOINERWORDS, returnNoise=True, includeParent=True):
    # corner case for inappropriate input
    if not isinstance(text, str):
        raise Exception("What you just gave wildgram isn't a string, mate.")
    if not returnNoise and includeParent:
        raise Exception("Parent is based on noise index, you need to set returnNoise to True in order to have includeParent be True. Otherwise set both to False.")

    prog = figureOutRegex(stopwords)
    noise, ranges = createRangesFromProg(prog, topicwords, text,joinerwords)

    if include1gram:
        prog1gram = figureOutRegex(stopwords, 1)
        noise, ranges = createRangesFromProg(prog1gram, [], text, joinerwords, noise,ranges)

    if returnNoise:
        ranges = ranges + noise

    ranges =filterAndSort(ranges)
    ret = []
    for r in ranges:
        app = createToken(r[0], r[1], r[2], text,len(ret))
        ret.append(app)

    if includeParent:
        ret = assignParents(ret)

    return ret
