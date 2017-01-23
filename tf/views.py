from flask import render_template
from . import app
from .controller import get_items

@app.route("/")
def front_page():
    return render_template("index.html")

@app.route("/list/<id>")
def item_list(id):
    return render_template("itemlist.html", items=get_items(id))