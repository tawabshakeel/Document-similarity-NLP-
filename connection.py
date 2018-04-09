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
                    data = main.countingAllWords(document["books_id"] + ".txt")
                    all_data[document["books_id"]]=data
                    mongoQuery(book_id, data, 1, 0, 0, 0, 0)


            A = Counter(all_data["1"])
            B = Counter(all_data["2"])
            C = Counter(all_data["3"])
            r = A + B + C
            # print(r)
            return render_template("all-data.html", result=r)

        else:
            print("some data missing")
            book1=   db.words.find_one({'books_id':'1'})
            book2 = db.words.find_one({'books_id': '2'})
            book3 = db.words.find_one({'books_id': '3'})
            print(book1)
            combined_data=dict()
            if book1 is None :
                print("none")
                data = main.countingAllWords("1" + ".txt")
                combined_data["1"]=data
                mongoQuery("1", data, 1, 0, 0, 0, 0)
            else:
                combined_data["1"]=json.loads(book1["words"]);

            if book2 is None :
                data = main.countingAllWords("2" + ".txt")
                combined_data["2"] = data
                mongoQuery("2", data, 1, 0, 0, 0, 0)
            else:
                combined_data["2"] = json.loads(book2["words"]);

            if book3 is None:
                data = main.countingAllWords("3" + ".txt")
                combined_data["3"] = data
                mongoQuery("3", data, 1, 0, 0, 0, 0)
            else:
                combined_data["3"] = json.loads(book3["words"]);

            A = Counter(combined_data["1"])
            B = Counter(combined_data["2"])
            C = Counter(combined_data["3"])
            r = A + B + C
            return render_template("all-data.html", result=r)


@app.route("/verbs_count/<book_id>")
def Verbs_Nouns_Count(book_id):
    if book_id != 'All':
        query = db.words.find_one({'book_id': book_id})
        if query:
            if query["verbs"]:
                print("in verbs")
                verbs = json.loads(query["verbs"])
                nouns = json.loads(query["nouns"])
                count =json.loads(query["verbs-nouns-count"])
                return render_template("verbs_nouns.html", nouns=nouns, verbs=verbs,count=count, book=book_id)
            else:
                nouns,verbs=main.separating_nouns_and_verbs(book_id + ".txt")
                count=main.total_verbs_and_nouns(book_id + ".txt")
                mongoQuery(book_id, 0, 1, 1, nouns,verbs,count)
                return render_template("verbs_nouns.html", nouns=nouns, verbs=verbs,count=count, book=book_id)

        else:
            nouns,verbs = main.separating_nouns_and_verbs(book_id + ".txt")
            count = main.total_verbs_and_nouns(book_id + ".txt")
            mongoQuery(book_id, 0, 0, 1, nouns,verbs,count)
            return render_template("verbs_nouns.html", nouns=nouns, verbs=verbs,count=count, book=book_id)



    else:
        print("All")



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
