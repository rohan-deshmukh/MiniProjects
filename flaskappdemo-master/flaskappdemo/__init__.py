from flask import Flask, render_template, flash, request, url_for, redirect, session
from content_management import Content

from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

from dbconnect import connection
import gc

import os

app = Flask(__name__)

TOPIC_DICT = Content()


class User:
    def username(self):
        try:
            return str(session['username'])
        except:
            return ("guest")


user = User()


def userinformation():
    try:
        client_name = (session['username'])
        guest = False
    except:
        guest = True
        client_name = "Guest"

    if not guest:
        try:
            c, conn = connection()
            c.execute("SELECT * FROM users WHERE username = (%s)",
                      (thwart(client_name)))
            data = c.fetchone()
            settings = data[4]
            tracking = data[5]
        except Exception, e:
            pass

    else:
        settings = [0, 0]
        tracking = [0, 0]

    return client_name, settings, tracking


def update_user_tracking():
    try:
        completed = str(request.args['completed'])
        if completed in str(TOPIC_DICT.values()):
            client_name, settings, tracking = userinformation()
            if tracking == None:
                tracking = completed
            else:
                if completed not in tracking:
                    tracking = tracking + "," + completed

            c, conn = connection()
            c.execute("UPDATE users SET tracking = %s WHERE username = %s",
                      (thwart(tracking), thwart(client_name)))
            conn.commit()
            c.close()
            conn.close()
            client_name, settings, tracking = userinformation()

        else:
            pass

    except Exception, e:
        pass


@app.route('/')
def homepage():
    return render_template("main.html")


def topic_completion_percent():
    try:
        client_name, settings, tracking = userinformation()

        try:
            tracking = tracking.split(",")
        except:
            pass

        if tracking == None:
            tracking = []

        completed_percentages = {}

        for each_topic in TOPIC_DICT:
            total = 0
            total_complete = 0

            for each in TOPIC_DICT[each_topic]:
                total += 1
                for done in tracking:
                    if done == each[1]:
                        total_complete += 1

            percent_complete = int(((total_complete * 100) / total))
            completed_percentages[each_topic] = percent_complete

        return completed_percentages
    except:
        for each_topic in TOPIC_DICT:
            total = 0
            total_complete = 0

            completed_percentages[each_topic] = 0.0

        return completed_percentages

    pass


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@app.errorhandler(405)
def method_not_found(e):
    return render_template("405.html")


# This is handling 500 errors
# @app.route('/slashboard/')
# def slashboard():
# 	try:
# 		return render_template("dashboard.html", TOPIC_DICT = TOPIC_DICT)
# 	except Exception as e:
# 		return render_template("500.html", error=e)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login_page'))

    return wrap


@app.route("/logout/")
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('dashboard'))


@app.route('/login/', methods=['GET', 'POST'])
def login_page():
    error = ''
    try:
        c, conn = connection()
        if request.method == "POST":

            data = c.execute("SELECT * FROM users WHERE username = (%s)",
                             thwart(request.form['username']))
            data = c.fetchone()[2]

            if sha256_crypt.verify(request.form['password'], data):
                session['logged_in'] = True
                session['username'] = request.form['username']

                flash("You are now logged in")
                return redirect(url_for("dashboard"))

            else:
                error = "Invalid credentials, try again."

        gc.collect()

        return render_template("login.html", error=error)

    except Exception as e:
        # flash(e)
        error = "Invalid credentials, try again."
        return render_template("login.html", error=error)


class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [validators.Required(),
                                          validators.EqualTo('confirm', message="Passwords must match.")])
    confirm = PasswordField('Repeat Password')

    accept_tos = BooleanField(
        'I accept the <a href="/tos/">Terms of Service</a> and the <a href="/privacy/">Privacy Notice</a> (Last '
        'updated Oct 7, 2015)',
        [validators.Required()])


@app.route('/register/', methods=['GET', 'POST'])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()

            x = c.execute("SELECT * FROM users WHERE username = (%s)",
                          (thwart(username)))

            if int(x) > 0:
                flash("That username is already taken, please choose another")
                return render_template('register.html', form=form)

            else:
                c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",
                          (thwart(username), thwart(password), thwart(email),
                           thwart("/introduction-to-python-programming/")))
                conn.commit()
                flash("Thanks for registering!")
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('dashboard'))

        return render_template("register.html", form=form)

    except Exception as e:
        return str(e)


# Basics
@app.route(TOPIC_DICT["Basics"][0][1], methods=['GET', 'POST'])
def Introduction_to_Python():
    update_user_tracking()
    completed_percentages = topic_completion_percent()
    # print ("\n" * 10 + os.path.realpath(".") + "\n" * 10)
    print ("\n" * 10 + app.root_path + "\n" * 10)
    return render_template("tutorials/Basics/introduction-to-python-programming.html",
                           completed_percentages=completed_percentages,
                           curLink=TOPIC_DICT["Basics"][0][1], curTitle=TOPIC_DICT["Basics"][0][0],
                           nextLink=TOPIC_DICT["Basics"][1][1], nextTitle=TOPIC_DICT["Basics"][1][0])


@app.route(TOPIC_DICT["Basics"][1][1], methods=['GET', 'POST'])
def Print_functions_and_Strings():
    update_user_tracking()
    completed_percentages = topic_completion_percent()
    print ("\n" * 10 + app.root_path + "\n" * 10)
    return render_template("tutorials/Basics/python-tutorial-print-function-strings.html",
                           completed_percentages=completed_percentages,
                           curLink=TOPIC_DICT["Basics"][1][1], curTitle=TOPIC_DICT["Basics"][1][0],
                           nextLink=TOPIC_DICT["Basics"][2][1], nextTitle=TOPIC_DICT["Basics"][2][0])


@app.route(TOPIC_DICT["Basics"][2][1], methods=['GET', 'POST'])
def Math_basics_with_Python_3():
    update_user_tracking()
    completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/math-basics-python-3-beginner-tutorial.html",
                           completed_percentages=completed_percentages,
                           curLink=TOPIC_DICT["Basics"][2][1], curTitle=TOPIC_DICT["Basics"][2][0],
                           nextLink=TOPIC_DICT["Basics"][3][1], nextTitle=TOPIC_DICT["Basics"][3][0])


@app.route(TOPIC_DICT["Basics"][3][1], methods=['GET', 'POST'])
def Varaibles():
    update_user_tracking()
    completed_percentages = topic_completion_percent()
    return render_template("tutorials/Basics/python-3-variables-tutorial.html",
                           completed_percentages=completed_percentages,
                           curLink=TOPIC_DICT["Basics"][3][1], curTitle=TOPIC_DICT["Basics"][3][0])


@app.route('/dashboard/')
def dashboard():
    try:
        try:
            client_name, settings, tracking = userinformation()
            gc.collect()
            if client_name == "Guest":
                flash("Welcome Guest! Progress tracking is available for logged-in users.")
                tracking = ['None']

            update_user_tracking()

            completed_percentages = topic_completion_percent()
            # flash("flash test!!!")
            # flash("Add another Flash message if you want to!!")
            return render_template("dashboard.html", TOPIC_DICT=TOPIC_DICT, tracking=tracking,
                                   completed_percentages=completed_percentages)
        except Exception, e:
            return str(e), "please report errors to abc@gmail.com"
    except Exception, e:
        return str(e), "please report errors to abc@gmail.com"


if __name__ == "__main__":
    app.run()
