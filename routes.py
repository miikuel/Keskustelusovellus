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
        
@app.route("/new-thread/<topicname>", methods=["GET", "POST"])
def new_thread(topicname):
    if users.is_logged():
        if request.method == "GET":
            return render_template("new-thread.html", topicname=topicname)
        if request.method == "POST":
            threadname = request.form["thread-name"]
            content = request.form["content"]
            topics.new_thread(topicname, threadname, content=content)
            return redirect(url_for("topic", name=topicname))
    else:
        return render_template("error.html", message="Uuden viestiketjun luominen epäonnistui")
    
@app.route("/<topicname>/<threadname>/new-message", methods=["POST"])
def new_message(topicname, threadname):
    if not users.is_logged():
        return redirect("/")
    message = request.form["content"]
    if topics.new_message(threadname, message):
        return redirect(url_for("thread", name=topicname, thread=threadname))
    else:
        return render_template("error.html", message="Viestin lähetys epäonnistui")



@app.route("/topic/<name>")
def topic(name):
    if users.is_logged():
        threads = topics.topic_threads(name)
        return render_template("topic.html", topicname=name, topicthreads=threads)
    else:
        return redirect("/")
    
@app.route("/topic/<name>/<thread>")
def thread(name, thread):
    if users.is_logged():
        messages = topics.get_messages(thread)
        return render_template("thread.html", topicname=name, threadname=thread, messages=messages)
    else:
        return redirect("/")
    
@app.route("/result")
def result():
    if users.is_logged():
        query = request.args["query"]
        messages = topics.search_messages(query)
        return render_template("result.html", messages=messages)
    else:
        return redirect("/")

    
