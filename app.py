from flask import Flask, render_template, url_for, redirect, request, session
from datetime import timedelta 

app = Flask(__name__)
app.secret_key = "mysecretkey"
app.permanent_session_lifetime = timedelta(minutes=5)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        name = request.form["username"]
        user = {
            "name":name
        }
        session["user"] = user
        return redirect(url_for("welcome"))
    else:
        if "user" in session:
            return redirect(url_for("welcome"))
        return render_template('login.html')


@app.route('/welcome')
def welcome():
    if "user" in session:
        user = session["user"]
        return render_template('welcome.html', user=user)
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None )
    return redirect(url_for("login"))

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug = True)
