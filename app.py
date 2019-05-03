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

appRoot = "/retro"


# new layout
# node = Load
# LoadChildren
# Store

# Always returning OK 200 to avoid default sever error pages

@app.route(appRoot + "/node/<int:n_id>", methods=["GET", "POST", "DELETE"])
def node(n_id):
    if request.method == "POST":
        # We don't care about n_id, probably should be posted on n_id=0
        try:
            pid = int(request.form['pid'])
            type = request.form['type']
            json = request.form['json']

            n = DbObject(pid=pid, type=type, json=json)
            db.session.add(b)
            db.session.commit()

            return make_response(jsonify({'result': 200, 'id': n.id, 'json': n.json}), 200)
        except:
            return make_response(jsonify({'result': 500, 'message': 'Missing one of required input pid, type, json'}), 200)

    if request.method == "GET":
        # Load object which is the board
        # TODO: create a more private way to separate boards (need key to get it)
        #request.args.get("type")
        try:
            b = DbObject.query.filter_by(id=n_id).one()

            if b:
                return make_response(jsonify({'result': 200, 'id': b.id, 'json':b.json}), 200)

            return make_response(jsonify({'result': 404, 'id': n_id}), 200)
        except:
            return make_response(jsonify({'result': 500, 'message': 'Unable to get node'}), 200)

    if request.method == "DELETE":
        try:
            db.session.query(DbObject).filter(DbObject.id == n_id).delete()
            db.session.commit()

            return make_response(jsonify({'result': 200, 'id': n_id}), 200)
        except:
            return make_response(jsonify({'result': 500, 'message': 'Unable to delete node'}), 200)

@app.route(appRoot + "/node/<int:n_id>/children", methods=["GET"])
def children(n_id):
    if request.method == "GET":
        bList = DbObject.query.filter_by(pid=n_id)

        if bList:
            dList = []
            for b in bList:
                dList.append({'id': b.id, 'type': b.type, 'json':b.json})

            return make_response(jsonify({'result': 200, 'id': n_id, 'json': dList}), 200)

        return make_response(jsonify({'result': 500, 'id': n_id}), 200)

@app.route("/retro", methods=["GET"])
@app.route("/retro/", methods=["GET"])
def index():
    if request.method == "GET":
        return render_template("index.html")

@app.route("/", methods=["GET"])
def root():
    if request.method == "GET":
        return make_response(jsonify({'result': 'Hello world'}), 200)
