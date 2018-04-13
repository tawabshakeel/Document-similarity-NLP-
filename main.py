import nltk as nt
import gensim
from nltk.tokenize import word_tokenize
import operator
import heapq
import re


#Counting_ALL_words function is used to calculate the count the words present in the book
# parameters ---> book_id
# return -------> dictionary
def countingAllWords(name):
    counts = dict()             # dictionary is created with a name of counts to store words with number of occurance i.e {"apple":"2","door":"4"}
    try:
        for line in open ('books/'+name, 'r', encoding="utf-8-sig"):             # file is opened using encoding utf-8-sig and each line is read and stored in line variable
          for word in line.split():            # words are split from each line
              word = word.lower()              # words are tranformed into lower format i.e Apple would be turned into apple to make sure case sensitive words are consider same
              word = ''.join(filter(str.isalpha, word))         # special characters words are removed from word
              if len(word) > 1:            # i am taking words which have length more than 1 i.e i am discarding words like "a"- considering them as characters not words
                if word in counts:         # checking word in the dictionary
                    counts[word] += 1       # if word exist occurance of word is increased by 1
                else:
                    counts[word] = 1        # if word don't exist word is added in dictionary with occurance equals to 1
    except:

        for line in open ('books/'+name, 'r', encoding=None):       # try catch applied some time error in opening file due to encoding so adding encoding None
          for word in line.split():         # same as above code
              word = word.lower()
              word = ''.join(filter(str.isalpha, word))
              if len(word) > 1 :
                if word in counts:
                    counts[word] += 1
                else:
                    counts[word] = 1

    return counts
# couting occurance of each verb and nouns {"apple":"3"},{"run":"3"}
#params--> book_id
#return--> nound and verbs dictionary
def separating_nouns_and_verbs(book):
    try:
        File = open('books/'+book,encoding = "ISO-8859-1")  # open file this time with ISO-8859-1 encoding time
    except:
        File = open('books/' + book, encoding=None)
    lines = File.read()  # read all lines
    sentences = nt.sent_tokenize(lines)  # tokenize sentences
    nouns = dict()  # empty  dictionary to hold all nouns
    verbs= dict()   ## empty  array to hold all verbs

    for sentence in sentences:
        for word, pos in nt.pos_tag(nt.word_tokenize(str(sentence))):  # taking out words and word tpye we
            word = word.lower()
            word = ''.join(filter(str.isalpha, word))
            if len(word) > 1:
                if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'): #NN-->a noun , NNP--> Proper Nouns ,NNS -->Common noun plural form,  NNPS-->Proper Noun Plural Form
                    if word in  nouns:   # checking word exist in noun dict
                        nouns[word] += 1  # if exist incrementing by 1

                    else:
                        nouns[word] = 1

                elif (pos == 'VBP' or pos == 'VB' or pos == 'VBZ' ): # VB --> verb , VBP --> Verb non-3rd person singular present forms,, VBZ-->Verb 3rd person singular present form
                    if word in  verbs:# checking word exist in verbs dict
                        verbs[word] += 1# if exist incrementing by 1

                    else:
                        verbs[word] = 1

    return (nouns ,verbs)



#counting nouns and verbs i.e {"Nouns":"25000",Verbs:"5000" }
#return dictionary
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


# sentence similarity when user input the string
# params book_id ,string (user input)
# returs most similar sentence and most dissimilar sentence

def sentence_similarity(book,string):

    try:
        File = open('books/'+book,encoding = "ISO-8859-1")  # open file
    except:
        File = open('books/' + book, encoding=None)
    lines = File.read()  # read all lines

    sentences = nt.sent_tokenize(lines) # tokenizing document using nltk into sentences
    gen_docs = [[ "".join(filter(str.isalpha,w.lower()))  for w in word_tokenize(text)] # list of sentences with each sentences is list of tokens word_tokenzie()--> provides listof tokens
                for text in sentences]
    dictionary = gensim.corpora.Dictionary(gen_docs) # converting the list of tokens into dictionary
    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs] # A corpus is a list of bags of words. A bag-of-words representation for a document just lists the number of times each word occurs in the document.
    tf_idf = gensim.models.TfidfModel(corpus) #a tf-idf model from the corpus. Note that num_nnz is the number of tokens.


    sims = gensim.similarities.Similarity('books/', tf_idf[corpus],num_features=len(dictionary)) #tf-idf stands for term frequency-inverse document frequency. Term frequency is how often the word shows up in the document and inverse document fequency scales the value by how rare the word is in the corpus.
    query_doc = [w.lower() for w in word_tokenize(string)] #string is user inputed sentence. tokenzing the sentence
    query_doc_bow = dictionary.doc2bow(query_doc) # create tuple of above tokenized string in the form of i.e [(1,2),(2,3),(3,4)]
    query_doc_tf_idf = tf_idf[query_doc_bow] #get tokens which are significant ,using this we can find sentence is similar to which sentence

    index, value = max(enumerate(sims[query_doc_tf_idf]), key=operator.itemgetter(1)) #getting the index ,value of maximum token for most similar sentence
    min_index, min_value = min(enumerate(sims[query_doc_tf_idf]), key=operator.itemgetter(1))#getting the index ,value of minimum token for most similar sentence

    print(sum(sims[query_doc_tf_idf]))
    return (sentences[index],sentences[min_index]) # getting similar and dissimilar sentece using above indexes

#sentence_similarity("1.txt","hello i am tawab")
def sentence_similarity_matrix(book):
    try:
        File = open('books/' + book, encoding="ISO-8859-1")  # open file
    except:
        File = open('books/' + book, encoding=None)
    lines = File.read()  # read all lines

    sentences = nt.sent_tokenize(lines)  # tokenizing document using nltk into sentences
    sentences = [s.lower() for s in sentences if len(s) > 10 and  not s.isdigit()]

    gen_docs = [["".join(filter(str.isalpha, w.lower())) for w in nt.word_tokenize(text)  ]
                # list of sentences with each sentences is list of tokens word_tokenzie()--> provides listof tokens
                for text in sentences]
    dictionary = gensim.corpora.Dictionary(gen_docs)  # converting the list of tokens into dictionary
    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]  # A corpus is a list of bags of words. A bag-of-words representation for a document just lists the number of times each word occurs in the document.
    tf_idf = gensim.models.TfidfModel(corpus)  # a tf-idf model from the corpus. Note that num_nnz is the number of tokens.
    sims = gensim.similarities.Similarity('books/', tf_idf[corpus], num_features=len(
        dictionary))  # tf-idf stands for term frequency-inverse document frequency. Term frequency is how often the word shows up in the document and inverse document fequency scales the value by how rare the word is in the corpus.
    scores = dict()


    for idx, text in enumerate(sentences):
                query_doc = ["".join(filter(str.isalpha, w.lower())) for w in word_tokenize(text)]
                query_doc_bow = dictionary.doc2bow(query_doc)
                query_doc_tf_idf = tf_idf[query_doc_bow]
                data=sims[query_doc_tf_idf]
                total=sum(data);
                scores[idx]=total
            #   index = heapq.nlowest(10, range(len(sims[query_doc_bow])), sims[query_doc_bow].take)
            #   abc[idx] = index
    min_index=heapq.nsmallest(10,range(len(scores)),scores.get)
    max_index=heapq.nlargest(10,range(len(scores)),scores.get)
    similar_sentences=dict()
    dis_similar_sentences=dict()
    for idx,index in enumerate(min_index):
         dis_similar_sentences[idx+1]=sentences[index]

    for idx,index in enumerate(max_index):
         similar_sentences[idx+1]=sentences[index]
    return dis_similar_sentences,similar_sentences








