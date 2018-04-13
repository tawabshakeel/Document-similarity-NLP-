from flask import Flask,render_template,request
from pymongo import MongoClient
import main
import json
from collections import Counter
client = MongoClient('localhost:27017') # Mongo Client created
db = client.connectavo # connectavo is database name


app = Flask(__name__)

@app.route("/")  # Route 1 Returns the home page
def home():
   return render_template("home.html")


# receives book_id 1,2,3 or can contains all
@app.route("/words_count/<book_id>") # Route 2 returns the word_count list
def word_count(book_id):

    if book_id !='all':     # check whether book_id  don't contains all
        query = db.words.find_one({'book_id': book_id})     # find complete collection with respect to book_id
        if query:   # if data is present in database
            if query["words"]:   # if words_count dictionary is present in database
                result = query["words"]
                result = json.loads(result)     # unstringify the string into dictionary
                return render_template("table.html", result=result, book=book_id)   # sending the dictionary to table.html where words_count would be printed in loop
            else: # if words_count is not present
                data = main.countingAllWords(book_id + ".txt")  # calling function written in main.py to calculate the word_count with respect to book_id
                mongoQuery(book_id,data,1,0,0,0,0)          # updating words against book_id in the database so that next time no need to call the main function again
                return render_template("table.html", result=data, book=book_id)
        else:
            try: # in case if no data is present in the database against book_id
                data =main.countingAllWords(book_id+".txt") # calling the main function to calculate word count
                mongoQuery(book_id, data, 0, 0,0,0,0) #inserting new record against book_id
                return render_template("table.html", result=data, book=book_id)

            except IOError: # exception in case of error in inserting in the db
                print("Error")
    else:# if the book_id contains all --> means user want to see all books words count merge together
        query = db.words.count() #counting the collection. If user has visiting all books word_count individually then the count would be 3 otherwise it would be less than 3
        all_data=dict() # dictaionary with a name of all_data to store every book total word_count
        if query == 3: # if all data is in the database
            result=db.words.find(); # find all three collections
            for document in result: # traversing the all three collection
               if document["words"]: # if words exist for each book
                    if document["book_id"] == "1":
                        all_data[document["book_id"]] = json.loads(document["words"]) # storing word_count of book 1 in all_data dict

                    elif document["book_id"] == "2":
                        all_data[document["book_id"]] = json.loads(document["words"]) # storing word_count of book 2 in all_data dict

                    elif document["book_id"] == "3":
                        all_data[document["book_id"]] = json.loads(document["words"]) # storing word_count of book 3 in all_data dict

               else : # for any book_id word_count is not present
                    data = main.countingAllWords(document["book_id"] + ".txt") # main function is called to find word_count for that book_id
                    all_data[document["book_id"]]=data # store word_count in the all_data dict
                    mongoQuery(book_id, data, 1, 0, 0, 0, 0) # update the database and store word_count for that book_id


            A = Counter(all_data["1"]) # combining all books word_count togther
            B = Counter(all_data["2"])
            C = Counter(all_data["3"])
            r = A + B + C # if book1 contains {"apple":"2"} if book 2 contains {"apple":"3"} and book 3 contains {"apple":"4"} now total would be {"apple":"9"}

            return render_template("all-data.html", result=r) # data is send to all-data html to print total word_count

        else: # if all data is not present in database --> count is less than 3
            book1 = db.words.find_one({'book_id':'1'}) # all books data is fetched from db
            book2 = db.words.find_one({'book_id': '2'})
            book3 = db.words.find_one({'book_id': '3'})

            combined_data=dict()
            if book1 is None : # if book1 collection is empty
                data = main.countingAllWords("1" + ".txt") # main function is called to find word_count
                combined_data["1"]=data # data is stored in combined_data dict
                mongoQuery("1", data, 0, 0, 0, 0, 0) # data is inserted in the db also
            else: # if book 1 data is not empty
                if book1["words"]: # if book 1 word_count is not empty
                    combined_data["1"]=json.loads(book1["words"]); #data is stored in combined_data dict no need to call db because data is already stored in db

                else:# if book 1 word_count is empty
                    data = main.countingAllWords("1" + ".txt") #main function is called to find word_count
                    combined_data["1"] = data # data is stored in combined_data dict
                    mongoQuery("1", data, 1, 0, 0, 0, 0) # data is updated in the db

            if book2 is None : # if book2 collection is empty
                data = main.countingAllWords("2" + ".txt") #main function is called to find word_count
                combined_data["2"] = data # data is stored in combined_data dict
                mongoQuery("2", data, 0, 0, 0, 0, 0) # data is inserted in the db
            else:
                if book2["words"] : # if book 2 word_count is not empty
                    combined_data["2"] = json.loads(book2["words"]);# data is stored in combined_data dict no need to call db because data is already stored in db
                else: # if book  2 word_count is empty
                    data = main.countingAllWords("2" + ".txt") ##main function is called to find word_count
                    combined_data["2"] = data # data is stored in combined_data dict
                    mongoQuery("2", data, 1, 0, 0, 0, 0) # data is updated in the db
          # same check in case of book 3
            if book3 is None:
                data = main.countingAllWords("3" + ".txt")
                combined_data["3"] = data
                mongoQuery("3", data, 0, 0, 0, 0, 0)
            else:
                if book3["words"] :
                    combined_data["3"] = json.loads(book3["words"]);
                else:
                    data = main.countingAllWords("3" + ".txt")
                    combined_data["3"] = data
                    mongoQuery("3", data, 1, 0, 0, 0, 0)


            A = Counter(combined_data["1"]) # combining all books word_count togther
            B = Counter(combined_data["2"])
            C = Counter(combined_data["3"])
            r = A + B + C
            return render_template("all-data.html", result=r)

# Route 3 to find verb_nouns_count in the book

@app.route("/verbs_count/<book_id>")
def Verbs_Nouns_Count(book_id):
    if book_id != 'all':
        query = db.words.find_one({'book_id': book_id})
        if query:
            if query["verbs"]:
                print("in verbs")
                verbs = json.loads(query["verbs"])
                nouns = json.loads(query["nouns"])
                count =json.loads(query["verbs-nouns-count"])
                return render_template("verbs_nouns.html", nouns=nouns, verbs=verbs,count=count, book=book_id)
            else:
                print("not verbs")
                nouns,verbs=main.separating_nouns_and_verbs(book_id + ".txt")
                count=main.total_verbs_and_nouns(book_id + ".txt")
                mongoQuery(book_id, 0, 1, 1, nouns,verbs,count)
                return render_template("verbs_nouns.html", nouns=nouns, verbs=verbs,count=count, book=book_id)

        else:
            print("empty record")
            nouns,verbs = main.separating_nouns_and_verbs(book_id + ".txt")
            count = main.total_verbs_and_nouns(book_id + ".txt")
            mongoQuery(book_id, 0, 0, 1, nouns,verbs,count)
            return render_template("verbs_nouns.html", nouns=nouns, verbs=verbs,count=count, book=book_id)



    else:
        book1 = db.words.find_one({'book_id': '1'})
        book2 = db.words.find_one({'book_id': '2'})
        book3 = db.words.find_one({'book_id': '3'})
        print(book1)
        combined_data = dict()

        nested_dict=dict()
        if book1 is None:
            print("book 1 dont exist")
            nouns, verbs = main.separating_nouns_and_verbs("1" + ".txt")
            count = main.total_verbs_and_nouns("1" + ".txt")
            combined_data["1"]=dict((("nouns",nouns),("verbs",verbs),("total_count",count)))
            mongoQuery("1", 0, 0, 1, nouns, verbs, count)

        else:
            print("book1 exist")
            if book1["nouns"]:
                combined_data["1"] = dict((("nouns", json.loads(book1["nouns"])), ("verbs", json.loads(book1["verbs"])), ("total_count", json.loads(book1["verbs-nouns-count"]))))
                print(combined_data)
            else:

                nouns, verbs = main.separating_nouns_and_verbs("1" + ".txt")
                count = main.total_verbs_and_nouns("1" + ".txt")
                combined_data["1"] = dict((("nouns", nouns), ("verbs", verbs), ("total_count", count)))
                mongoQuery("1", 0, 1, 1, nouns, verbs, count)

        if book2 is None:
            print("book2 dont exist")
            nouns, verbs = main.separating_nouns_and_verbs("2" + ".txt")
            count = main.total_verbs_and_nouns("2" + ".txt")
            combined_data["2"] = dict((("nouns", nouns), ("verbs", verbs), ("total_count", count)))
            mongoQuery("2", 0, 0, 1, nouns, verbs, count)
        else:
            print("book2 exist")
            if book2["verbs"]:
                print("book2 verbs exist")
                combined_data["2"] = dict((("nouns", json.loads(book2["nouns"])), ("verbs", json.loads(book2["verbs"])),
                                           ("total_count", json.loads(book2["verbs-nouns-count"]))))

            else:
                nouns, verbs = main.separating_nouns_and_verbs("2" + ".txt")
                count = main.total_verbs_and_nouns("2" + ".txt")
                combined_data["2"] = dict((("nouns", nouns), ("verbs", verbs), ("total_count", count)))
                mongoQuery("2", 0, 1, 1, nouns, verbs, count)

        if book3 is None:
            print("book 3 dont exist")
            nouns, verbs = main.separating_nouns_and_verbs("3" + ".txt")
            count = main.total_verbs_and_nouns("3" + ".txt")
            combined_data["3"] = dict((("nouns", nouns), ("verbs", verbs), ("total_count", count)))
            mongoQuery("3", 0, 0, 1, nouns, verbs, count)
        else:
            print("book 3 exist")
            if book3["verbs"]:
                print("book 3 verbs exist")
                combined_data["3"] = dict((("nouns", json.loads(book3["nouns"])), ("verbs", json.loads(book3["verbs"])),
                                           ("total_count", json.loads(book3["verbs-nouns-count"]))))
            else:
                nouns, verbs = main.separating_nouns_and_verbs("3" + ".txt")
                count = main.total_verbs_and_nouns("3" + ".txt")
                combined_data["3"] = dict((("nouns", nouns), ("verbs", verbs), ("total_count", count)))
                mongoQuery("3", 0, 1, 1, nouns, verbs, count)

        book1_nouns = Counter(combined_data["1"]["nouns"])
        book1_verbs = Counter(combined_data["1"]["verbs"])
        book1_total = Counter(combined_data["1"]["total_count"])

        book2_nouns = Counter(combined_data["2"]["nouns"])
        book2_verbs = Counter(combined_data["2"]["verbs"])
        book2_total = Counter(combined_data["2"]["total_count"])

        book3_nouns = Counter(combined_data["3"]["nouns"])
        book3_verbs = Counter(combined_data["3"]["verbs"])
        book3_total = Counter(combined_data["3"]["total_count"])

        # r = A + B + C
        nouns_total=book1_nouns+book2_nouns+book3_nouns
        verbs_total=book1_verbs+book2_verbs+book3_verbs
        book1_total.pop("document")
        book2_total.pop("document")
        book3_total.pop("document")
        total_sum = book1_total + book2_total + book3_total

        return render_template("all_nouns_verbs.html", nouns=nouns_total,verbs=verbs_total,count=total_sum )


@app.route("/top_10/<book_id>")
def Similar_Sentences(book_id):
    query = db.unique.find_one({'book_id': book_id})
    if query:
        if query["unique"]:
            result = query["unique"]
            result2 = query["similar"]
            result = json.loads(result)
            result2 = json.loads(result2)# unstringify the string into dictionary
            return render_template("top_unique_sentences.html", unique=result,similar=result2,book=book_id)  # sending the dictionary to table.html where words_count would be printed in loop
        else:
            unique,similar=main.sentence_similarity_matrix(book_id+".txt")
            mongo_Query_for_top_umique_sentences(book_id,unique,similar)
            return render_template("top_unique_sentences.html", unique=unique, similar=similar,book=book_id)  # sending the dictionary to table.html where words_count would be printed in loop

    else:
        unique, similar = main.sentence_similarity_matrix(book_id+".txt")
        mongo_Query_for_top_umique_sentences(book_id, unique, similar)
        return render_template("top_unique_sentences.html", unique=unique, similar=similar, book=book_id)

@app.route("/user_similar_sentence",methods=['GET'])
def user_similar_sentence():
    book_id=request.args.get("book_name")
    string=request.args.get("data")
    similar,dissimlar= main.sentence_similarity(book_id+".txt",string)
    print("returning data")
    print(similar)
    return render_template("user_sentence_similarity.html",book=book_id,sentence=string,similar=similar,dissimilar=dissimlar)



def mongoQuery(book_id,data,index,type,nouns,verbs,n_v_count):
    if type == 0:
        if index == 0 :
            db.words.insert_one(
                {
                    "book_id": book_id,
                    "words": json.dumps(data),
                    "verbs": '',
                    "nouns": '',
                    "verbs-nouns-count": ''


                }).inserted_id

        elif index == 1 :
            db.words.update(
                {book_id: book_id},
                {
                    "words": json.dumps(data)

                },

            )


    elif type == 1:
        if index == 0:
            db.words.insert_one(
                {
                    "book_id": book_id,

                    "words": '',
                    "verbs": json.dumps(verbs),
                    "nouns":json.dumps(nouns),
                    "verbs-nouns-count" : json.dumps(n_v_count)

                }).inserted_id

        elif index == 1:
            db.words.update(
                {book_id: book_id},
                {
                    "verbs": json.dumps(verbs),
                    "nouns":json.dumps(nouns),
                    "verbs-nouns-count" : json.dumps(n_v_count)
                },

            )
def mongo_Query_for_top_umique_sentences(book_id,unique,similar):
    db.unique.insert_one(
        {
            "book_id": book_id,
            "unique" :json.dumps(unique),
            "similar": json.dumps(similar)

        }).inserted_id


if __name__ == '__main__':
    app.run()
