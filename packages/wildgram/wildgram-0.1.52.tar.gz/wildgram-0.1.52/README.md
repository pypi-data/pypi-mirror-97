Wildgram tokenizes english text into "wild"-grams (tokens of varying word count)
that match closely to the the natural pauses of conversation. I originally built
it as the first step in an abstraction pipeline for medical language: since
medical concepts tend to be phrases of varying lengths, bag-of-words or bigrams
doesn't really cut it.

Wildgram works by measuring the size of the noise (stopwords, punctuation, and
whitespace) and breaks up the text against noise of a certain size
(it varies slightly depending on the noise).

Parameters:

text
Required: Yes
Default: No
What it is: the text you want to wildgram.

stopwords
Required: No
Default: STOPWORDS list (importable, mostly based on NLTK's stop word list)
What it is: a list of stop words that you want to mark as noise, that will act as breaks between tokens.
Custom Override: a list of strings that you want to split on.

topicwords
Required: No
Default: TOPICWORDS list (importable, mostly based on NLTK's stop word list)
What it is: a list of stop words that you want to mark as tokens because they have meaning, but often serve to break up larger pieces of text. Examples include numbers, negation words like "won't", etc.
Custom Override: a list of strings that you want to split on.

include1gram
Required: No
Default: True
What it is: when set to true, wildgram will also return every individual word or token as well as any phrases it finds.
Custom Override: Boolean (false). When set to false, wildgram will only return the phrases it finds, not 1grams as well.

joinerwords
Required: No
Default: JOINERWORDS list (importable, words like "of")
What it is: a list of stop words (must also be included in stop word list if overridden) that join two phrases together. Example: "shortness of breath" -> "shortness", "breath", "shortness of breath".
Custom Override: a list of strings you want to join on. WORDS MUST BE IN STOPWORDS LIST FOR THIS TO WORK. The assumption is you wouldn't want a joiner word that is also a topic word.

returnNoise
Required: No
Default: True
What it is: when set to true, wildgram will also return each individual noise token it created to find the phrases.
Custom Override: Boolean (false). When set to false, it will not return the noise tokens.


includeParent
Required: No
Default: True
What it is: when set to true, wildgram will also return the "parent" of the token, in a pseudo-dependency tree.
This tree is generated using a ranked list of the prior (in the text) styles of punctuation to approximate
the relationships between tokens. Noise tokens act as branching nodes while normal tokens can only be leaf nodes,
so in practice this is used to determine the "uncles" of the token. Examples of how this might be useful is
linking list like elements under a larger heading or figuring out the unit of a number based on the context (which may not be on the same line). Since noise tokens are the branching nodes, returnNoise must be set to true if includeParent is true.
Custom Override: Boolean (false). When set to false, it will not return the parent.


Returns:
a list of dictionaries, each dictionary in the form:
```python
example = {
"startIndex": 0,
"endIndex", 5,
"token": "hello",
"tokenType": "token" # if noise, token type is "noise"
"index": 0,
"parent": -1 # parent is only given if includeParent is set to true, not otherwise.
}
```
The list is sorted in ascending (smallest->largest) order for the startIndex, then the endIndex.


Example code:

```python
from wildgram import wildgram
ranges = wildgram("and was beautiful", returnNoise=False, includeParent=False)

#[{
#"startIndex": 8,
#"endIndex", 17,
#"token": "beautiful",
#"tokenType": "token",
# "index": 0
#}]

from wildgram import wildgram
ranges = wildgram("and was beautiful day")
print(ranges)
'''
[{
  "startIndex": 0,
  "endIndex": 8,
  "token": "and was ",
  "tokenType": "noise",
  "index": 0,
  "parent": -1
},
{
  "startIndex": 8,
  "endIndex": 17,
  "token": "beautiful",
  "tokenType": "token",
  "index": 1,
  "parent": 0
},
{
  "startIndex": 8,
  "endIndex": 21,
  "token": "beautiful day",
  "tokenType": "token",
  "index": 2,
  "parent": 0
},
{
  "startIndex": 17,
  "endIndex": 18,
  "token": " ",
  "tokenType": "noise",
  "index": 3,
  "parent": 0
},
{
  "startIndex": 18,
  "endIndex": 21,
  "token": "day",
  "tokenType": "token",
  "index": 4,
  "parent": 0
}
]
'''
```
That's all folks!
