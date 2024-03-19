from app import app
from flask import render_template, request, redirect, url_for
import users
import topics


@app.route("/")
def index():
    if users.is_logged():
        topiclist = topics.get_topics()
        return render_template("index.html", topics=topiclist)
    else:
        return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        return redirect("/")
    else:
        return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")
        
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/new-topic", methods=["GET", "POST"])
def new_topic():
    if not users.is_admin():
        return redirect("/")
    if request.method == "GET":
        return render_template("new-topic.html")
    if request.method == "POST":
        topic_name = request.form["topic-name"]
        if topics.new_topic(topic_name):
            return redirect("/")
        else:
            return render_template("error.html", message="Uuden aihealueen luominen ei onnistunut")
        
@app.route("/topic/<name>")
def topic(name):
    if users.is_logged():
        return render_template("topic.html", topicname=name)
    else:
        return redirect("/")
