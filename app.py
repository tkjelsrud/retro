from flask import Flask, render_template, request, url_for, redirect, make_response, jsonify
import json, datetime
from DbSetup import DbSetup
from DbObject import DbObject
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = DbSetup.getUri()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route("/retro/board/<int:board_id>", methods=["GET", "POST", "DELETE"])
def board(board_id):
    if request.method == "POST":
        # Create a board
        # Json properties must be included

        b = DbObject(type="board", json="{'title':'Test Board'}")
        db.session.add(b)
        db.session.commit()

        return make_response(b.json, 200)

    if request.method == "GET":
        # Load object which is the board
        # TODO: create a more private way to separate boards (need key to get it)
        b = DbObject.query.filter(id=board_id, type="board").one()

        if b:
            print("Found board " + b)

            # return
        else:
            None
            # return

        return make_response(jsonify({'result': 'Some text here' + str(board_id)}), 200)

@app.route("/retro", methods=["GET"])
@app.route("/retro/", methods=["GET"])
def index():
    if request.method == "GET":
        #app.config["TEST123"] = app.config["TEST123"] + 1
        return make_response(jsonify({'result': 'Some text here' + str(app.config["TEST123"])}), 200)

#return render_template("index.html")
