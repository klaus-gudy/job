from flask import Flask, render_template, url_for, redirect, request, session

app = Flask(__name__)
app.secret_key = "mysecretkey"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        return redirect(url_for("welcome", usr=user))
    else:
        return render_template('login.html')


@app.route('/welcome/<usr>')
def welcome(usr):
    return render_template('welcome.html', usr=usr)

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug = True)
