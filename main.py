import nltk as nt
from collections import Counter
import gensim
from nltk.tokenize import word_tokenize
import operator
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


#nestedDIc is a function just to check the working of dictionary
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


def sentence_similarity(book,string):
    try:
        File = open('books/'+book,encoding = "ISO-8859-1")  # open file
    except:
        File = open('books/' + book, encoding=None)
    lines = File.read()  # read all lines
    # ''.join(filter(str.isalpha, word))
    sentences = nt.sent_tokenize(lines)
    gen_docs = [[ "".join(filter(str.isalpha,w.lower()))  for w in word_tokenize(text)]
                for text in sentences]



    dictionary = gensim.corpora.Dictionary(gen_docs)
    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
    tf_idf = gensim.models.TfidfModel(corpus)

    sims = gensim.similarities.Similarity('books/', tf_idf[corpus],
                                          num_features=len(dictionary))
    query_doc = [w.lower() for w in word_tokenize(string)]
    query_doc_bow = dictionary.doc2bow(query_doc)
    query_doc_tf_idf = tf_idf[query_doc_bow]

    index, value = max(enumerate(sims[query_doc_tf_idf]), key=operator.itemgetter(1))
    min_index, min_value = min(enumerate(sims[query_doc_tf_idf]), key=operator.itemgetter(1))

    return (sentences[index],sentences[min_index])

# sentence_similarity("1.txt")

