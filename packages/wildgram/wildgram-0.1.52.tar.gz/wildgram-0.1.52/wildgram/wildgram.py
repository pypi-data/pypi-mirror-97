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

TOPICWORDS = ["no","not","nor",'ain', 'aren', "aren't", 'couldn', "couldn't",
'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't",
'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn',
"mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't",
'wasn', "wasn't", 'weren', "weren't", 'won', "won't",'don', "don't",'wouldn',
"wouldn't", "\d+","\d+\.\d+", "will","reveal", "revealed", "h/o", "s/p","denies"
, "denied", "b.i.d.", "t.i.d.", "p.r.n.", "p.o.", "p.r.", "a.m.", "a.s.", "c.c.",
"n.p.o.", "o.d.", "o.s.", "o.u.", "q.s.", "q.o.d.","t.i.d.", "t.i.n."]

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

def pullOutNoise(pattern, text):
    matches = [(match.start(), match.end(), "noise") for match in pattern.finditer(text.lower(),overlapped=True)]
    indexes = set(range(len(text)))
    for n in matches:
        indexes = indexes.difference(range(n[0], n[1]))
    prev = 0
    noise = []
    for i in range(len(matches)-1):
        if matches[i][1] <= matches[i+1][0]:
            noise.append((matches[prev][0], matches[i][1], 'noise'))
            prev = i+1
    if prev < len(matches):
        noise.append((matches[prev][0], matches[-1][1], 'noise'))
    return noise, indexes

def indexesToSnippets(indexes):
    indexes = list(indexes)
    if len(indexes) == 0:
        return []
    if len(indexes) == 1:
        return [text[indexes[0]]]
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
    for topic in topics:
        for match in re.finditer("(\s|^)"+topic+"(\s|$)", text.lower(),overlapped=True):
            for top in re.finditer(topic, text[match.start():match.end()].lower()):
                ret.append((top.start()+match.start(), top.end()+match.start(), "token"))
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
    matches, leftover = pullOutNoise(prog, text)
    topics, leftover = pullOutTopics(topics, text, leftover)
    tokens = indexesToSnippets(leftover)
    merged = sorted(matches + tokens + topics, key=lambda x: (x[0], x[1]))
    ranges = ranges + pullOutJoiners(merged, text, joinerwords) + tokens + topics
    noise = noise+ matches
    return noise, ranges

def createToken(start, end, type, text, index):
    return {"startIndex": start, "endIndex":end, "token":text[start:end], "tokenType": type, "index": index}

def wildgram(text, stopwords=STOPWORDS, topicwords=TOPICWORDS, include1gram=True, joinerwords=JOINERWORDS, returnNoise=True, includeParent=True):
    # corner case for inappropriate input
    if not isinstance(text, str):
        raise Exception("What you just gave wildgram isn't a string, mate.")
    if not returnNoise and includeParent:
        raise Exception("Parent is based on noise index, you need to set returnNoise to True in order to have includeParent be True. Otherwise set both to False.")

    if text.isspace() and not returnNoise:
        return []
    if text.isspace() and returnNoise:
        return [createToken(0, len(text), "noise", text, 0)]

    prog = figureOutRegex(stopwords)
    noise, ranges = createRangesFromProg(prog, topicwords, text,joinerwords)

    if include1gram:
        prog1gram = figureOutRegex(stopwords, 1)
        noise, ranges = createRangesFromProg(prog1gram, [], text, joinerwords, noise,ranges)

    if returnNoise:
        ranges = ranges + noise

    ranges =sorted(list(set(ranges)), key=lambda x: (x[0], x[1]))
    ret = []
    for r in ranges:
        app = createToken(r[0], r[1], r[2], text,len(ret))
        if len(ret) == 0 or ret[-1]["tokenType"] != "noise" or r[2] != "noise":
            ret.append(app)
            continue
        if ret[-1]["endIndex"] >= r[0]:
            if ret[-1]["endIndex"] < r[1]:
                ret[-1] = createToken(ret[-1]["startIndex"], r[1], "noise", text,len(ret)-1)
                continue
        ret.append(app)

    if includeParent:
        ret = assignParents(ret)

    return ret
