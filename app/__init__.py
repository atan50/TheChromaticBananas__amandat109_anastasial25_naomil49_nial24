"""
The Chromatic BaNANAs: Amanda Tan, Anastasia Lee, Naomi Lai, and Nia Lam
SoftDev
P05: Color Theory for Dummies
2025-06-11
"""

from flask import Flask, render_template, request, redirect, session, flash
import db

app = Flask(__name__)
app.secret_key = 'your_secret_key'
# HOME PAGE, SHOULD PROMPT REGISTER OR LOGIN
db.resetDB()

@app.route('/', methods=['GET', 'POST'])
def homeBase():
    if('username' in session):
        return render_template('home.html', logged_in = True)
    return render_template('home.html', logged_in = False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if 'login' in request.form:
            user = user_collection.find_one({'username': username})
            if user and verify_user_login(username, password):
                session['username'] = username
                flash('Login successful.')
                return redirect('/')
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
                    insert_user_data(username, password)
                    flash('Registration successful.')

    return render_template('login.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if ('username' in session):
        return render_template("profile.html", logged_in=True, username = session['username'])
    else:
        return redirect('/login')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    session.pop('password', None)
    return redirect("/")

if __name__ == "__main__":
    app.debug = True
    app.run()
>>>>>>> 9c80b8d5adeb6210febc1181818f746d75fd06fd
