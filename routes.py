from app import app
from flask import render_template, request, redirect, url_for, flash, session, abort
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
        flash("Väärä tunnus tai salasana")
        return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            flash("Salasanat eroavat")
            return redirect("/register")
        if len(password1) < 5 or len(password1) > 20:
            flash("Salasanan tulee olla 5-20 merkkiä pitkä")
            return redirect("/register")
        if len(username) < 2 or len(username) > 15:
            flash("Käyttäjätunnuksen tulee olla 2-15 merkkiä pitkä")
            return redirect("/register")
        if users.register(username, password1):
            flash("success")
            return redirect("/")
        else:
            flash("Valitsemasi käyttäjätunnus on jo käytössä")
            return redirect("/register")
        
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/manage-topics", methods=["GET"])
def manage_topics():
    if not users.is_admin():
        return redirect("/")
    topicnames = topics.get_topics()
    return render_template("manage-topics.html", topicnames=topicnames)

@app.route("/new-topic", methods=["POST"])
def new_topic():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if not users.is_admin():
        return redirect("/")
    topic_name = request.form["topic-name"]
    if len(topic_name) < 3 or len(topic_name) > 25:
        flash("new_topic_len_error")
        return redirect("/manage-topics")
    try:
        secret = request.form["secret"]
        secretmessage = "salainen "
    except:
        secret = False
        secretmessage = ""
    if topics.new_topic(topic_name, secret):
        flash(f"Uusi {secretmessage}alue ({topic_name}) luotu onnistuneesti!")
        return redirect("/manage-topics")
    else:
        flash("new_topic_error")
        return redirect("/manage-topics")
    
@app.route("/delete-topic", methods=["POST"])
def delete_topic():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if not users.is_admin():
        return redirect("/")
    topicname = request.form["topic-name"]
    if topics.delete_topic(topicname):
        flash(f"*Alue {topicname} poistettu pysyvästi")
        return redirect("/manage-topics")
    else:
        flash("delete-error")
        return redirect("/manage-topics")
    
@app.route("/delete-thread", methods=["POST"])
def delete_thread():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    threadname = request.form["threadname"]
    topicname = request.form["topicname"]
    if users.is_admin() or topics.thread_creator(threadname):
        if topics.delete_thread(threadname):
            return redirect(url_for("topic", name=topicname))
        else:
            flash("Ketjun poistaminen epäonnistui")
            return redirect(url_for("edit_thread", topicname=topicname, threadname=threadname))
    else:
        return redirect("/")
        
@app.route("/new-thread/<topicname>", methods=["GET", "POST"])
def new_thread(topicname):
    if not users.is_logged():
        return redirect("/")
    if topics.has_permission(topicname):
        if request.method == "GET":
            return render_template("new-thread.html", topicname=topicname)
        if request.method == "POST":
            if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)
            threadname = request.form["thread-name"]
            content = request.form["content"]
            if len(threadname) < 3 or len(threadname) > 25:
                flash("Ketjun nimen tulee olla 3-25 merkkiä pitkä")
                return redirect(url_for("new_thread", topicname=topicname))
            if len(content) < 1 or len(content) > 500:
                flash("Viestin maksimipituus on 500 merkkiä")
                return redirect(url_for("new_thread", topicname=topicname))
            if topics.new_thread(topicname, threadname, content=content):
                return redirect(url_for("thread", name=topicname, thread=threadname))
            else:
                flash("Uuden viestiketjun luominen epäonnistui")
                return redirect(url_for("new_thread", topicname=topicname))
    else:
        return redirect("/")
    
@app.route("/<topicname>/<threadname>/new-message", methods=["POST"])
def new_message(topicname, threadname):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if not users.is_logged():
        return redirect("/")
    if topics.has_permission(topicname):
        message = request.form["content"]
        if len(message) < 1 or len(message) > 500:
            flash("Viestin maksimipituus on 500 merkkiä")
            return redirect(url_for("thread", name=topicname, thread=threadname))
        if topics.new_message(threadname, message):
            return redirect(url_for("thread", name=topicname, thread=threadname))
        else:
            flash("Viestin lähetys epäonnistui")
            return redirect(url_for("thread", name=topicname, thread=threadname))
    else:
        return redirect("/")

@app.route("/topic/<name>")
def topic(name):
    if not users.is_logged():
        return redirect("/")
    if topics.has_permission(name):
        threads = topics.topic_threads(name)
        secret = topics.is_secret(name)
        return render_template("topic.html", topicname=name, topicthreads=threads, secret=secret)
    else:
        return redirect("/")
    
@app.route("/topic/<name>/permissions", methods=["GET", "POST"])
def topic_permissions(name):
    if not users.is_logged():
        return redirect("/")
    if not users.is_admin():
        return redirect("/")
    if not topics.topic_exists(name):
        return redirect("/")
    if request.method == "GET":
        userlist = topics.no_permissions(name)
        return render_template("topic-permissions.html", userlist=userlist, topicname=name)
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        username = request.form["username"]
        if topics.add_permissions(name, username):
            flash(f"Käyttäjäoikeudet lisätty käyttäjälle {username}")
            return redirect(url_for("topic_permissions", name=name))
        else:
            flash("Käyttäjäoikeuksien lisääminen epäonnistui")
            return redirect(url_for("topic_permissions", name=name))
    
    
@app.route("/topic/<name>/<thread>")
def thread(name, thread):
    if not users.is_logged():
        return redirect("/")
    if topics.has_permission(name):
        messages = topics.get_messages(thread)
        secret = topics.is_secret(name)
        if users.is_admin() or topics.thread_creator(thread):
            can_edit = True
        else:
            can_edit = False
        return render_template("thread.html", topicname=name, threadname=thread, messages=messages, can_edit=can_edit, secret=secret)
    else:
        return redirect("/")

    
@app.route("/edit-message/<id>", methods=["GET", "POST"])
def edit_message(id):
    if users.is_logged:
        if request.method == "GET":
            message = topics.message_for_edit(id)
            if message:
                return render_template("edit-message.html", message=message)
            else:
                return redirect("/")
        if request.method == "POST":
            if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)
            new_message = request.form["content"]
            topicname = request.form["topicname"]
            threadname = request.form["threadname"]
            if len(new_message) < 1 or len(new_message) > 500:
                flash("Viestin maksimipituus on 500 merkkiä")
                return redirect(url_for("edit_message", id=id))
            if topics.edit_message(id, new_message):
                return redirect(url_for("thread", name=topicname, thread=threadname))
            else:
                flash("Viestin muokkaaminen epäonnistui")
                return redirect(url_for("edit_message", id=id))
    else:
        return redirect("/")

@app.route("/delete-message/<id>/<topic>/<thread>")
def delete_message(id, topic, thread):
    if users.is_logged():
        if topics.message_author(id):
            admin = False
        elif users.is_admin():
            admin = True
        if topics.delete_message(id, admin):
            return redirect(url_for("thread", name=topic, thread=thread))
        else:
            return redirect("/")

    
@app.route("/edit-thread/<topicname>/<threadname>", methods=["GET", "POST"])
def edit_thread(topicname, threadname):
    if not users.is_logged():
        return redirect("/")
    if not topics.topic_exists(topicname):
        return redirect("/")
    if users.is_admin() or topics.thread_creator(threadname):
        if request.method == "GET":
            secret = topics.is_secret(topicname)
            return render_template("edit-thread.html", topicname=topicname, threadname=threadname, secret=secret)
        if request.method == "POST":
            if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)
            newname = request.form["newname"]
            if len(newname) < 3 or len(newname) > 25:
                flash("Ketjun nimen tulee olla 3-25 merkkiä pitkä")
                return redirect(url_for("edit_thread", topicname=topicname, threadname=threadname))
            if topics.rename_thread(threadname, newname):
                return redirect(url_for("thread", name=topicname.lower(), thread=newname.lower()))
            else:
                flash("Ketjun nimen muuttaminen epäonnistui")
                return redirect(url_for("edit_thread", topicname=topicname, threadname=threadname))
            
@app.route("/result")
def result():
    if users.is_logged():
        query = request.args["query"]
        messages = topics.search_messages(query)
        return render_template("result.html", messages=messages)
    else:
        return redirect("/")

    
