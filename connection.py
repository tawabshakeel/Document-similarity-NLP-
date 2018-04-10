from flask import Flask,render_template
from pymongo import MongoClient
import main
import json
from collections import Counter
client = MongoClient('localhost:27017')
db = client.connectavo


app = Flask(__name__)

@app.route("/")  # Route 1 Returns the home page
def home():
   return render_template("home.html")

@app.route("/words_count/<book_id>")
def word_count(book_id):

    if book_id !='all':
        query = db.words.find_one({'book_id': book_id})
        if query:
            if query["words"]:
                print("containing ")
                result = query["words"]
                result = json.loads(result)
                return render_template("table.html", result=result, book=book_id)
            else:
                data = main.countingAllWords(book_id + ".txt")
                mongoQuery(book_id,data,1,0,0,0,0)
                return render_template("table.html", result=data, book=book_id)
        else:
            print("empty")
            try:
                data =main.countingAllWords(book_id+".txt")
                mongoQuery(book_id, data, 0, 0,0,0,0)
                return render_template("table.html", result=data, book=book_id)

            except IOError:
                print("Error")
    else:
        query = db.words.count()
        all_data=dict()
        if query == 3:
            result=db.words.find();
            for document in result:
               if document["words"]:
                    if document["book_id"] == "1":
                        all_data[document["book_id"]] = json.loads(document["words"])

                    elif document["book_id"] == "2":
                        all_data[document["book_id"]] = json.loads(document["words"])

                    elif document["book_id"] == "3":
                        all_data[document["book_id"]] = json.loads(document["words"])
               else :
                    data = main.countingAllWords(document["book_id"] + ".txt")
                    all_data[document["book_id"]]=data
                    mongoQuery(book_id, data, 1, 0, 0, 0, 0)


            A = Counter(all_data["1"])
            B = Counter(all_data["2"])
            C = Counter(all_data["3"])
            r = A + B + C
            # print(r)
            return render_template("all-data.html", result=r)

        else:
            print("some data missing")
            book1=  db.words.find_one({'book_id':'1'})
            book2 = db.words.find_one({'book_id': '2'})
            book3 = db.words.find_one({'book_id': '3'})
            print(book1)
            combined_data=dict()
            if book1 is None :
                print("none")
                data = main.countingAllWords("1" + ".txt")
                combined_data["1"]=data
                mongoQuery("1", data, 0, 0, 0, 0, 0)
            else:
                print("book1 exist")
                if book1["words"]:
                    print("book1 words exist")
                    combined_data["1"]=json.loads(book1["words"]);
                else:
                    print("book1 words dont exist")
                    data = main.countingAllWords("1" + ".txt")
                    combined_data["1"] = data
                    mongoQuery("1", data, 1, 0, 0, 0, 0)

            if book2 is None :
                print("book2 dont exist")
                data = main.countingAllWords("2" + ".txt")
                combined_data["2"] = data
                mongoQuery("2", data, 0, 0, 0, 0, 0)
            else:
                print("book2 exist")
                if book2["words"] :
                    print("book2 words exist")
                    combined_data["2"] = json.loads(book2["words"]);
                else:
                    print("book2 words dont exist")
                    data = main.countingAllWords("2" + ".txt")
                    combined_data["2"] = data
                    mongoQuery("2", data, 1, 0, 0, 0, 0)

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


            A = Counter(combined_data["1"])
            B = Counter(combined_data["2"])
            C = Counter(combined_data["3"])
            r = A + B + C
            return render_template("all-data.html", result=r)


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
   return render_template("home.html")



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


if __name__ == '__main__':
    app.run()
