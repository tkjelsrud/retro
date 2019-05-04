from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class JsonModel(object):
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# Generic DB storable object for different app purposes (dynamic variables)
class DbObject(db.Model, JsonModel):
    __tablename__ = "jsonobjects"
    #
    #
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)
    type = db.Column(db.String(16))
    json = db.Column(db.String(2048))
    ts = db.Column(db.DateTime(), server_onupdate=FetchedValue())
    skey = db.Column(db.String(16))
