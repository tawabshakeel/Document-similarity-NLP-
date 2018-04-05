from collections import Counter;

def countingAllWords():
    counts = dict()
    for line in open ('books/4300-0.txt', 'r', encoding="utf8"):
      for word in line.split ():
          word = word.lower().replace('.','').replace('?','').replace('!','').replace(':','').replace(',','').replace(')','').replace('(','')
          if word in counts:
            counts[word] += 1
          else:
            counts[word] = 1

    return counts


def checking(str):
    counts = dict()
    for word in str.split():
        word=word.lower().replace('.','')
        if word in counts:
            print("already present")
            counts[word] += 1
        else:
            print("not present")
            counts[word] = 1
    return counts


print(countingAllWords())