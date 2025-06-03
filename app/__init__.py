"""
The Chromatic BaNANAs: Amanda Tan, Anastasia Lee, Naomi Lai, and Nia Lam
SoftDev
P05: Color Theory for Dummies
2025-06-06
"""
import os
import urllib
import json
import random
import pymongo
from urllib.request import Request, urlopen
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import Flask, render_template, request, redirect, session, flash
import db
from color import *

app = Flask(__name__)
app.secret_key = os.urandom(32)

uri = "mongodb+srv://anastasial25:lqRQwo37qTkbKnlG@softdev-p5.cvervwo.mongodb.net/?retryWrites=true&w=majority&appName=softdev-p5"

# Create a new client and connect to the server
client = MongoClient(uri, server_api = ServerApi('1'))

database = client['database']
user_collection = database['users']

@app.route('/', methods = ['GET', 'POST'])
def root():
    return redirect('/home')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if('username' in session):
        return render_template('home.html', logged_in = True)
    return render_template('home.html', logged_in = False)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if 'login' in request.form:
            user = user_collection.find_one({'username': username})
            if user and db.verify_user_login(username, password):
                session['username'] = username
                flash('Login successful.')
                return redirect('/home')
            else:
                flash('Invalid username or password.')

        elif 'register' in request.form:
            confirm_pass = request.form.get('confirm_pass')

            if password != confirm_pass:
                flash('Passwords do not match.')
            else:
                existing_user = user_collection.find_one({'username': username})
                if existing_user:
                    flash('Username already exists.')
                else:
                    db.insert_user_data(username, password)
                    session['username'] = username
                    flash('Registration successful.')
                    return redirect('/home')
    return render_template('login.html')

@app.route('/profile', methods = ['GET', 'POST'])
def profile():
    if ('username' in session):
        user = session['username']
        color_info = db.get_color_info(user)
        list = ["top", "bottom", "right", "left", "top right",
                "top left", "bottom right", "bottom left"]
        directions = ["", "", "", "", "", "", "", ""]
        directions[color_info[2]] = "checked"
        if request.method == 'POST':
            color1 = request.form['color1']
            color2 = request.form['color2']
            to = int(request.form['to'])
            db.update_color_info(user, color1, color2, to)
            color_info = db.get_color_info(user)
            directions = ["", "", "", "", "", "", "", ""]
            directions[to] = "checked"
        return render_template("profile.html", logged_in = True,
                               username = user, c1 = color_info[0],
                               c2 = color_info[1], d = directions,
                               dir = list[color_info[2]])
    else:
        return redirect('/login')

@app.route('/color', methods=['GET', 'POST'])
def color():
    colors = color_randomizer()
    print(colors)
    return render_template(
        "color.html",
        inner_left=colors["inner_left"],
        inner_right=colors["inner_right"],
        outer_left=colors["outer_left"],
        outer_right=colors["outer_right"],
        same=colors["same"]
    )

@app.route('/color/guess', methods=["POST"])
def handle_guess():
    guess = request.form["guess"]
    correct = request.form["correct"]

    result = "Correct!" if guess == correct else "Wrong :("
    return f"<h3>{result}</h3><p>Your guess: {guess} | Answer: {correct}</p><a href='/color'>Play Again</a>"

@app.route('/random', methods = ['GET', 'POST'])
def random_game():
    key = 'uWM9sQ5gmxuIo55YD6WvP2wa6w0gCi3gUeLc6qAY_T4'
    endpoint = 'https://api.unsplash.com/photos/random/?client_id=' + key
    req = Request(url=endpoint, headers={'User-Agent': 'Mozilla/6.0'})
    data = json.loads(urlopen(req).read())
    image_url = data.get('urls').get('full')

    hue = str(random.randint(0, 359)) + "deg"
    saturation = random.randint(1, 100)/100
    brightness = random.randint(1, 200)/100
    # print(hue)
    # print(saturation)
    # print(brightness)
    return render_template('random.html', link = 'url(' + image_url + ')', hue = hue, sat = saturation, bri = brightness)

@app.route('/random/guess', methods=["POST"])
def handle_adjustments():
    hue = request.form["hue"]
    saturation = request.form["saturation"]
    brightness = request.form["brightness"]

    return hue+" "+saturation+" "+brightness

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    session.pop('username', None)
    session.pop('password', None)
    return redirect("/home")

if __name__ == "__main__":
    app.debug = True
    app.run()
    #app.run(host='0.0.0.0')
