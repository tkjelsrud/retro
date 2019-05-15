from flask import Flask, render_template, request, url_for, redirect, make_response, jsonify
import json, datetime, hashlib
from DbSetup import DbSetup
from DbObject import DbObject
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = DbSetup.getUri()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_POOL_SIZE'] = 100
app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
#app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {autoflush:False}

from sqlalchemy import create_engine
engine = create_engine(DbSetup.getUri())

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine, autoflush=False)
session = Session()

#db = SQLAlchemy(app)

#autoflush=False

appRoot = "/retro"
requireKey = True

# Always returning OK 200 to avoid default sever error pages

def recodeJson(jStr):
    return json.loads(jStr)
    #return str(json.loads(jStr))[1:-1]

@app.route(appRoot + "/node/<int:n_id>", methods=["GET", "POST", "PUT", "DELETE"])
def node(n_id):
    if request.method == "POST":
        try:
            #
            # TODO migrate to json
            reqJson = request.get_json()
            #
            #print(request.__dict__)
            pid = None
            typ = None
            upd = False

            if 'type' in reqJson:
                typ = reqJson['type']

            # Inner JSON
            jso = reqJson['json']

            if 'pid' in reqJson:
                pid = int(reqJson['pid'])

            skey = hashlib.md5(str(datetime.datetime.now()).encode("utf-8")).hexdigest()[16:32]
            if 's' in request.args:
                skey = request.args['s']
            if 'skey' in reqJson:
                skey = reqJson['skey']

            if isinstance(jso, dict):
                jso = json.dumps(jso)

            if n_id > 0:
                # Probable update
                n = session.query(DbObject).filter(DbObject.id==n_id, DbObject.skey==skey).first()
                #n = DbObject.query.filter_by(id=n_id, skey=skey).one()

                if n is not None:
                    # Update, only support changing the json for now?
                    n.json = jso
                    session.commit()

                    upd = True
                else:
                    return make_response(jsonify({'result': 404, 'message': 'Got node to update but not found'}), 200)
            else:
                # New
                n = DbObject(pid=pid, type=typ, json=jso, skey=skey)
                session.add(n)
                session.commit()

            return make_response(jsonify({'result': 200, 'update': str(upd), 'id': n.id, 'json': recodeJson(n.json), 'skey':n.skey, 'ts': n.ts}), 200)
        except Exception as error:
            #db.session.rollback()
            return make_response(jsonify({'result': 500, 'message': 'Error on create or update. ' + str(error)}), 200)
        finally:
            session.close()

    if request.method == "GET":
        try:
            n = session.query(DbObject).filter(DbObject.id==n_id).first()
            #n = DbObject.query.filter_by(id=n_id).one()

            if requireKey:
                if 's' not in request.args or request.args['s'] != n.skey:
                    return make_response(jsonify({'result': 403, 'message': 'Key did not match'}), 200)
            if n is not None:
                return make_response(jsonify({'result': 200, 'id': n.id, 'json': recodeJson(n.json), 'skey':n.skey, 'ts': n.ts}), 200)

            return make_response(jsonify({'result': 404, 'id': n_id}), 200)

        except Exception as error:
            #db.session.rollback()
            return make_response(jsonify({'result': 500, 'message': 'Unable to get node ' + str(error)}), 200)
        finally:
            session.close()

    if request.method == "DELETE":
        try:
            session.query(DbObject).filter(DbObject.id==n_id).delete()
            session.commit()
            #db.session.close()

            return make_response(jsonify({'result': 200, 'id': n_id}), 200)
        except Exception as error:
            session.rollback()
            return make_response(jsonify({'result': 500, 'message': 'Unable to delete node' + str(error)}), 200)
        finally:
            session.close()

@app.route(appRoot + "/node/<int:n_id>/children", methods=["GET"])
def children(n_id):
    if request.method == "GET":
        try:
            cList = []
            if requireKey:
                if 's' not in request.args:
                    return make_response(jsonify({'result': 403, 'message': 'Key required'}), 200)

                key = request.args['s']

                cList = session.query(DbObject).filter(DbObject.pid==n_id, DbObject.skey==key)
            else:
                cList = session.query(DbObject).filter(DbObject.pid==n_id)

            if cList:
                dList = []
                for b in cList:
                    dList.append({'id': b.id, 'pid': b.pid, 'type': b.type, 'json': recodeJson(b.json), 'skey': b.skey, 'ts': b.ts})

                return make_response(jsonify({'result': 200, 'id': n_id, 'json': dList}), 200)

            return make_response(jsonify({'result': 500, 'id': n_id}), 200)

        except Exception as error:
            #db.session.rollback()
            return make_response(jsonify({'result': 500, 'message': 'Error in loading children for ' + str(n_id) + ": " + str(error)}), 200)
        finally:
            session.close()

@app.route("/retro", methods=["GET"])
@app.route("/retro/", methods=["GET"])
def index():
    if request.method == "GET":
        return render_template("index.html")

@app.route("/", methods=["GET"])
def root():
    if request.method == "GET":
        return make_response(jsonify({'result': 'Hello world'}), 200)
