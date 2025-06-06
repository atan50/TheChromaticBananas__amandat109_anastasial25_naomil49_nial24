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
from flask_assets import Environment, Bundle
import db
from color import *


app = Flask(__name__)
assets = Environment(app)
bundles = {  # define nested Bundle
  'style': Bundle(
            'scss/style.scss',
            filters='pyscss',
            output='css/style.css',
  ),
  'color': Bundle(
            'scss/color.scss',
            filters='pyscss',
            output='css/color.css',
        )
}
assets.register(bundles)

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
        random_scores = db.get_random_scores(user)
        avg = 0
        check_random_scores = True
        if (len(random_scores) == 1):
            check_random_scores = False
        else:
            random_scores = random_scores[1:]
            for i in random_scores:
                avg = avg + i
            avg = avg/len(random_scores)
        color_scores = db.get_color_scores(user)
        total = color_scores[0] + color_scores[1]
        acc = 0
        if total != 0:
            acc = float(color_scores[0])/total
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
                               dir = list[color_info[2]], 
                               random_scores = random_scores,
                               check_random_scores = check_random_scores,
                               color_scores = color_scores,
                               acc = acc, avg = avg)
    else:
        return redirect('/login')

@app.route('/wheel', methods=['GET', 'POST'])
def wheel():
    if 'username' in session:
        return render_template('wheel.html', logged_in=True)
    return render_template('wheel.html')

@app.route('/color', methods=['GET', 'POST'])
def color():
    # message = None
    if request.method == 'POST':
        # colors
        inner_left = request.form.get("inner_left")
        inner_right = request.form.get("inner_right")
        outer_left = request.form.get("outer_left")
        outer_right = request.form.get("outer_right")
        correct = request.form.get("correct")
        guess = request.form.get("guess")
        guessed = True

        if guess == correct:
            flash("Correct! Yay :D", "correct")
        else:
            flash(f"Wrong :( The correct answer was {correct}.", "wrong")
        if 'username' in session:
            user = session['username']
            if guess == correct:
                db.update_color_scores(user, True)
            else:
                db.update_color_scores(user, False)
            return render_template(
            "color.html",
            logged_in = True,
            inner_left=inner_left,
            inner_right=inner_right,
            outer_left=outer_left,
            outer_right=outer_right,
            same=(correct == "same"),
            guessed=True
        )
        return render_template(
            "color.html",
            inner_left=inner_left,
            inner_right=inner_right,
            outer_left=outer_left,
            outer_right=outer_right,
            same=(correct == "same"),
            guessed=guessed
        )

    colors = color_randomizer()
    correct = 'same' if colors['same'] else 'different'
    if 'username' in session:
        return render_template(
        "color.html",
        logged_in = True,
        inner_left=colors["inner_left"],
        inner_right=colors["inner_right"],
        outer_left=colors["outer_left"],
        outer_right=colors["outer_right"],
        same=colors["same"],
        correct=correct,
        guessed=False
    )
    return render_template(
        "color.html",
        inner_left=colors["inner_left"],
        inner_right=colors["inner_right"],
        outer_left=colors["outer_left"],
        outer_right=colors["outer_right"],
        same=colors["same"],
        correct=correct,
        guessed=False
    )


key = open("./keys/key_unsplash.txt").readline()
endpoint = 'https://api.unsplash.com/photos/random/?client_id=' + key
req = Request(url=endpoint, headers={'User-Agent': 'Mozilla/6.0'})
data = json.loads(urlopen(req).read())
image_url = data.get('urls').get('full')

hue = random.randint(0, 359)
hue_str = str(hue) + "deg"
saturation = random.randint(50, 150)
brightness = random.randint(50, 150)
# print(hue)
# print(saturation)
# print(brightness)

@app.route('/random', methods = ['GET', 'POST'])
def random_game():
    if request.method == 'POST':
        h_guess = int(request.form['hue'])
        s_guess = int(request.form['saturation'])
        b_guess = int(request.form['brightness'])
        image_url = globals()['image_url']
        hue = globals()['hue']
        hue_str = globals()['hue_str']
        saturation = globals()['saturation']
        brightness = globals()['brightness']
        h_diff = float(min(abs(hue - h_guess), 360 - abs(hue - h_guess)))/180
        s_diff = float(abs(saturation - s_guess))/100
        b_diff = float(abs(brightness - b_guess))/100
        total_diff = h_diff + s_diff + b_diff
        if 'username' in session:
            user = session['username']
            db.update_random_scores(user, total_diff)
            return render_template('random.html', logged_in = True, link = 'url(' + image_url + ')', 
                               hue = hue_str, hue_num = hue, sat = saturation, bri = brightness, 
                               h_g = h_guess, s_g = s_guess, b_g = b_guess,
                               score = total_diff)
        return render_template('random.html', link = 'url(' + image_url + ')', 
                               hue = hue_str, hue_num = hue, sat = saturation, bri = brightness, 
                               h_g = h_guess, s_g = s_guess, b_g = b_guess,
                               score = total_diff)
    req = Request(url=endpoint, headers={'User-Agent': 'Mozilla/6.0'})
    data = json.loads(urlopen(req).read())
    globals()['image_url'] = data.get('urls').get('full')

    globals()['hue'] = random.randint(0, 359)
    globals()['hue_str'] = str(globals()['hue']) + "deg"
    globals()['saturation'] = random.randint(50, 150)
    globals()['brightness'] = random.randint(50, 150)
    h_guess = 0
    s_guess = 100
    b_guess = 100
    if 'username' in session:
        return render_template('random.html', logged_in = True, link = 'url(' + globals()['image_url'] + ')', 
                           hue = globals()['hue_str'], sat = globals()['saturation'], bri = globals()['brightness'],
                           h_g = h_guess, s_g = s_guess, b_g = b_guess)
    return render_template('random.html', link = 'url(' + globals()['image_url'] + ')', 
                           hue = globals()['hue_str'], sat = globals()['saturation'], bri = globals()['brightness'],
                           h_g = h_guess, s_g = s_guess, b_g = b_guess)

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    session.pop('username', None)
    session.pop('password', None)
    return redirect("/home")

if __name__ == "__main__":
    app.debug = True
    app.run()
    #app.run(host='0.0.0.0')
