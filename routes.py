from app import app
from flask import render_template, request, redirect
import users
import topics


@app.route("/")
def index():
    if users.is_logged():
        sectionlist = topics.get_sections()
        return render_template("index.html", sections=sectionlist)
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

@app.route("/new-section", methods=["GET", "POST"])
def new_section():
    if not users.is_admin():
        return redirect("/")
    if request.method == "GET":
        return render_template("new-section.html")
    if request.method == "POST":
        section_name = request.form["section-name"]
        if topics.new_section(section_name):
            return redirect("/")
        else:
            return render_template("error.html", message="Uuden aihealueen luominen ei onnistunut")
