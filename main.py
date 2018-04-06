import nltk as nt


def countingAllWords(str):
    counts = dict()
    for line in open ('books/'+str, 'r', encoding="utf8"):
      for word in line.split():
          word = word.lower().replace('.','').replace('?','').replace('!','').replace(':','').replace(',','').replace(')','').replace('(','')
          if word in counts:
            counts[word] += 1
          else:
            counts[word] = 1

    return counts

# print(countingAllWords('4300-0.txt'))



def separating_nouns_and_verbs(book) :
    File = open('books/'+book,encoding='utf8')  # open file
    lines = File.read()  # read all lines
    sentences = nt.sent_tokenize(lines)  # tokenize sentences
    nouns = dict()  # empty to array to hold all nouns
    verbs= dict()

    for sentence in sentences:
        for word, pos in nt.pos_tag(nt.word_tokenize(str(sentence))):
            word = word.lower()
            if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
                if word in  nouns:
                    nouns[word] += 1
                    print("containing")
                else:
                    nouns[word] = 1
                    print(" not containing")
            elif (pos == 'VBP' or pos == 'VB' or pos == 'VBZ' ):
                if word in  verbs:
                    verbs[word] += 1
                    print("containing")
                else:
                    verbs[word] = 1
                    print(" not containing")


    return (nouns ,verbs)

#nouns,verbs=separating_nouns_and_verbs('4300-0.txt')

