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
        b = DbObject(type="board", json="{'title':'Test Board'}")
        db.session.add(b)
        db.session.commit()

        return make_response(jsonify({'result': 200, 'id': b.id, 'json': b.json}), 200)

    if request.method == "GET":
        # Load object which is the board
        # TODO: create a more private way to separate boards (need key to get it)
        b = DbObject.query.filter_by(id=board_id, type="board").one()

        if b:
            return make_response(jsonify({'result': 200, 'id': b.id, 'json':b.json}), 200)
        else:
            make_response(jsonify({'result': 404, 'id': board_id}), 200)
            # return
        return make_response(jsonify({'result': 500, 'id': board_id}), 200)

@app.route("/retro/board/<int:board_id>/notes", methods=["GET"])
def boardNotes(board_id):
    if request.method == "GET":
        bList = DbObject.query.filter_by(pid=board_id)

        if bList:
            dList = []
            for b in bList:
                dList.add(jsonify({'id': b.id, 'json':b.json}))

            return make_response(jsonify({'result': 200, 'id': board_id, 'json': json.dumps(dList)}), 200)

        return make_response(jsonify({'result': 500, 'id': board_id}), 200)

@app.route("/retro", methods=["GET"])
@app.route("/retro/", methods=["GET"])
def index():
    if request.method == "GET":
        return render_template("index.html")

@app.route("/", methods=["GET"])
def root():
    if request.method == "GET":
        return make_response(jsonify({'result': 'Hello world'}), 200)
