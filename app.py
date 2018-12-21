from flask import Flask, render_template, request, jsonify
import sqlite3 as lite
from random import shuffle
from sqlalchemy  import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/countries-capitals'
db = SQLAlchemy(app)
countries = None
randomCapitals = None
question = 0
continent = ""

@app.route('/')
def index():
    """ Home page, load """
    global question
    global continent
    continent = "world"
    question = 0
    db.execute('''CREATE TABLE countries(id SERIAL PRIMARY KEY, country VARCHAR NOT NULL, continent VARCHAR NOT NULL,
                                 capital VARCHAR NOT NULL''')
    return render_template("index.html")


@app.route("/playGameAfrica")
def playGameAfrica():
    """ Select 10 africans countries and capitals that the user is going to be tested on"""
    global cur
    global countries
    global continent
    continent = "Africa"
    cur.execute('''SELECT DISTINCT Country, Capital FROM Countries WHERE Continent=?
      ORDER BY RANDOM() LIMIT 10''', (continent,))
    countries = cur.fetchall()
    continent = "Africa"

    return render_template("playGame.html")


@app.route("/playGameAmerica")
def playGameAmerica():
    """ Select 10 American countries and capitals that the user is going to be tested on"""

    global cur
    global countries
    global continent
    continent = "America"

    cur.execute('''SELECT DISTINCT Country, Capital FROM Countries WHERE Continent=?
    ORDER BY RANDOM()''',(continent,))
    countries = cur.fetchall()
    return render_template("playGame.html")



@app.route("/playGameAsia")
def playGameAsia():
    """ Select 10 Asian countries and capitals that the user is going to be tested on"""
    global cur
    global countries
    global continent
    continent = "Asia"
    cur.execute('''SELECT DISTINCT Country, Capital FROM Countries WHERE Continent=?
        ORDER BY RANDOM()''', (continent,))
    countries = cur.fetchall()
    return render_template("playGame.html")

@app.route("/playGameEurope")
def playGameEurope():
    """ Select 10 European countries and capitals that the user is going to be tested on"""

    global cur
    global countries
    global continent
    continent = "Europe"
    cur.execute('''SELECT DISTINCT Country, Capital FROM Countries WHERE Continent=?
        ORDER BY RANDOM()''', (continent,))
    countries = cur.fetchall()
    return render_template("playGame.html")

@app.route("/playGameOceania")
def playGameOceania():
    """ Select 10 Oceania countries and capitals that the user is going to be tested on"""
    global continent
    global cur
    global countries
    continent = "Oceania"
    cur.execute('''SELECT DISTINCT Country, Capital FROM Countries WHERE Continent=?
        ORDER BY RANDOM()''', (continent,))
    countries = cur.fetchall()
    return render_template("playGame.html")

@app.route("/playGameWord")
def playGameWorld():
    """ Select 10  countries and capitals from any continent  that the user is going to be tested on"""
    global cur
    global countries
    cur.execute('''SELECT DISTINCT Country, Capital FROM Countries  ORDER BY RANDOM()''')
    countries = cur.fetchall()
    return render_template("playGame.html")



@app.route('/playGame', methods = ["GET", "POST"])
def playGame():
    """ User play game, 10 questions """
    global question
    global randomCapitals
    if request.method == "POST":

        print(question)
        #if 10 question has been asked, go to the result page
        if question  == 10:
            print("yes")
            finalScore = request.form["finalScore"]
            return jsonify({"score": finalScore})

        #country
        country = countries[question][0]
        cur = con.cursor()

        #select 3 randoms capitals for the question(multiple choice)
        if continent != "world":
            cur.execute('''SELECT DISTINCT Capital  FROM Countries WHERE Continent=? AND NOT Country =?
                  ORDER BY RANDOM() LIMIT 3''', (continent, country))
        else:
            cur.execute('''SELECT DISTINCT Capital  FROM Countries
                              ORDER BY RANDOM() LIMIT 3''')
        cap = cur.fetchall()
        capitals = []

        #put all the 4 capitals in array called capitals and suffle it
        for e in cap:
            capitals.append(e[0])
        capitals.append(countries[question][1])
        shuffle(capitals)
        question +=1
        return jsonify({"country" : country, "capitals" : capitals, "number" :  question})

    return render_template("playGame.html")

@app.route('/helper')
def helper():
    """ helper function that rsturn the right answer of an answer  to json, user will never have to deal with it"""
    answer = countries[question-1][1].replace(" ", "")
    return jsonify({"answer":answer})

@app.route("/aboutMe")
def aboutMe():
    return render_template("aboutMe.html")

if __name__ == '__main__':
    app.debug = True
    app.run()
