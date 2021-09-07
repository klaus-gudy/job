from flask import Flask, render_template, url_for, redirect, request, session, flash
from datetime import timedelta 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "mysecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

class users(db.Model):
    user_id = db.Column("id", db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/view')
def view():
    return render_template('view.html', values = users.query.all())   

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["username"]
        # user = {
        #     "name":name
        # }
        session["user"] = user

        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()

        flash("login succesfully")
        return redirect(url_for("welcome"))
    else:
        if "user" in session:
            flash("already logged in")
            return redirect(url_for("welcome"))
        return render_template('login.html')


@app.route('/welcome', methods=["POST", "GET"])
def welcome():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("email was saved")
        else:
            if "email" in session:
                email = session["email"]

        return render_template('welcome.html', email=email)
    else:
        flash("you are not logged in")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash("you have been log out","info")
    session.pop("user", None ) 
    session.pop("email", None )
    return redirect(url_for("login"))

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)
