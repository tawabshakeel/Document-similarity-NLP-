import nltk as nt
from collections import Counter
import  json
from collections import OrderedDict
def countingAllWords(name):
    counts = dict()
    try:
        for line in open ('books/'+name, 'r', encoding="utf-8-sig"):
          for word in line.split():
              word = word.lower()
              word = ''.join(filter(str.isalpha, word))
              if len(word) > 1:
                if word in counts:
                    counts[word] += 1
                else:
                    counts[word] = 1
    except:

        for line in open ('books/'+name, 'r', encoding=None):
          for word in line.split():
              word = word.lower()
              word = ''.join(filter(str.isalpha, word))
              if len(word) > 1 :
                if word in counts:
                    counts[word] += 1
                else:
                    counts[word] = 1

    return counts

# print(countingAllWords('3.txt'))



def separating_nouns_and_verbs(book):
    try:
        File = open('books/'+book,encoding = "ISO-8859-1")  # open file
    except:
        File = open('books/' + book, encoding=None)
    lines = File.read()  # read all lines
    sentences = nt.sent_tokenize(lines)  # tokenize sentences
    nouns = dict()  # empty to array to hold all nouns
    verbs= dict()

    for sentence in sentences:
        for word, pos in nt.pos_tag(nt.word_tokenize(str(sentence))):
            word = word.lower()
            word = ''.join(filter(str.isalpha, word))
            if len(word)> 1:
                if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
                    if word in  nouns:
                        nouns[word] += 1

                    else:
                        nouns[word] = 1

                elif (pos == 'VBP' or pos == 'VB' or pos == 'VBZ' ):
                    if word in  verbs:
                        verbs[word] += 1

                    else:
                        verbs[word] = 1

    return (nouns ,verbs)

#nouns,verbs=separating_nouns_and_verbs('3.txt')


def total_verbs_and_nouns(book):
    File = open('books/' + book, encoding = "ISO-8859-1")  # open file
    lines = File.read()  # read all lines
    sentences = nt.sent_tokenize(lines)  # tokenize sentences
    count = dict()  # empty to array to hold all nouns
    count["Nouns"]=0
    count["Verb"]=0
    count["document"]=book;

    for sentence in sentences:
        for word, pos in nt.pos_tag(nt.word_tokenize(str(sentence))):
            word = word.lower()
            word = ''.join(filter(str.isalpha, word))
            if len(word) > 1:
                if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
                    count["Nouns"] += 1
                elif(pos == 'VBP' or pos == 'VB' or pos == 'VBZ'):
                    count["Verb"] +=1


    return count


def combineDic():
    a=dict()
    b=dict()

    a["abc"]=2
    a["def"]=5

    b["abc"]=1
    b["def"]=3
    b["hello"]=1
    A=Counter(a)
    B=Counter(b)
    r=A + B



def nestedDic():
    my_dict=dict()
    new_dic=dict()
    new_dic["abc"]=1
    new_dic["def"]=2

    new_dic2 = dict()
    new_dic2["sabc"] = 1
    new_dic2["deffsfs"] = 2

    new_dic22 = dict()
    new_dic22["abc"] = 1
    new_dic22["def"] = 2

    new_dic33 = dict()
    new_dic33["sabc"] = 1
    new_dic33["deffsfs"] = 2

    my_dict["1"]=dict((("words",new_dic),("verbs",new_dic2)))
    my_dict["2"] = dict((("words", new_dic22), ("verbs", new_dic33)))
    print(my_dict)


#nestedDic()