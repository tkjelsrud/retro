from flask import Flask, render_template, request, url_for, redirect, make_response, jsonify
import json, datetime, hashlib
from DbSetup import DbSetup
from DbObject import DbObject
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = DbSetup.getUri()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

appRoot = "/retro"
requireKey = True

# Always returning OK 200 to avoid default sever error pages

@app.route(appRoot + "/node/<int:n_id>", methods=["GET", "POST", "PUT", "DELETE"])
def node(n_id):
    if request.method == "POST":
        # We don't care about n_id, probably should be posted on n_id=0
        try:
            pid = None
            type = request.form['type']
            json = request.form['json']

            if 'pid' in request.form:
                pid = int(request.form['pid'])

            skey = hashlib.md5(str(datetime.datetime.now()).encode("utf-8")).hexdigest()[16:32]
            if 'skey' in request.form:
                skey = request.form['skey']

            n = DbObject(pid=pid, type=type, json=json, skey=skey)

            db.session.add(n)
            db.session.commit()
            #db.session.close()

            return make_response(jsonify({'result': 200, 'id': n.id, 'json': json.loads(n.json), 'skey':n.skey, 'ts': n.ts}), 200)
        except Exception as error:
            db.session.rollback()
            db.session.close()
            return make_response(jsonify({'result': 500, 'message': 'Error or missing one of required input pid, type, json. ' + str(error)}), 200)

    if request.method == "PUT":
        try:
            n = DbObject.query.filter_by(id=n_id).one()

            if requireKey:
                if 's' not in request.args or request.args['s'] != n.skey:
                    return make_response(jsonify({'result': 403, 'message': 'Key did not match'}), 200)

            if 'json' in request.form:
                n.json = request.form['json']

            if 'pid' in request.form:
                n.pid = int(request.form['pid'])

            db.session.commit()

            n = DbObject.query.filter_by(id=n_id).one() # Get again to get new timestamp (?)

            db.session.close()

            return make_response(jsonify({'result': 200, 'id': n.id, 'json': n.json, 'skey':n.skey, 'ts': n.ts}), 200)

        except Exception as error:
            db.session.rollback()
            db.session.close()
            return make_response(jsonify({'result': 500, 'message': 'Error or missing one of required input pid, type, json. ' + str(error)}), 200)


    if request.method == "GET":
        try:
            n = DbObject.query.filter_by(id=n_id).one()
            db.session.close()

            if requireKey:
                if 's' not in request.args or request.args['s'] != n.skey:
                    return make_response(jsonify({'result': 403, 'message': 'Key did not match'}), 200)
            if n:
                return make_response(jsonify({'result': 200, 'id': n.id, 'json': json.loads(n.json), 'skey':n.skey, 'ts': n.ts}), 200)

            return make_response(jsonify({'result': 404, 'id': n_id}), 200)

        except Exception as error:
            db.session.rollback()
            db.session.close()
            return make_response(jsonify({'result': 500, 'message': 'Unable to get node ' + str(error)}), 200)

    if request.method == "DELETE":
        try:
            db.session.query(DbObject).filter(DbObject.id == n_id).delete()
            db.session.commit()
            #db.session.close()

            return make_response(jsonify({'result': 200, 'id': n_id}), 200)
        except Exception as error:
            db.session.rollback()
            db.session.close()
            return make_response(jsonify({'result': 500, 'message': 'Unable to delete node' + str(error)}), 200)

@app.route(appRoot + "/node/<int:n_id>/children", methods=["GET"])
def children(n_id):
    if request.method == "GET":
        try:
            cList = DbObject.query.filter_by(pid=n_id)
            db.session.close()

            if cList:
                dList = []
                for b in cList:
                    dList.append({'id': b.id, 'pid': b.pid, 'type': b.type, 'json':b.json, 'skey': b.skey, 'ts': b.ts})

                return make_response(jsonify({'result': 200, 'id': n_id, 'json': dList}), 200)

            return make_response(jsonify({'result': 500, 'id': n_id}), 200)

        except Exception as error:
            db.session.rollback()
            db.session.close()
            return make_response(jsonify({'result': 500, 'message': 'Error in loading children. ' + str(error)}), 200)

@app.route("/retro", methods=["GET"])
@app.route("/retro/", methods=["GET"])
def index():
    if request.method == "GET":
        return render_template("index.html")

@app.route("/", methods=["GET"])
def root():
    if request.method == "GET":
        return make_response(jsonify({'result': 'Hello world'}), 200)
