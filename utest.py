import unittest

class TestRetro(unittest.TestCase):
    def testDBconfig(self):
        try:
            self.assertEqual(DbSetup, None)
        except NameError:
            None
        from DbSetup import DbSetup
        self.assertTrue(DbSetup.getUri() is not None)

    def testCreateObject(self):
        from flask import Flask
        from DbObject import DbObject
        from DbSetup import DbSetup

        from flask_sqlalchemy import SQLAlchemy

        app = Flask(__name__)
        app.config["SQLALCHEMY_DATABASE_URI"] = DbSetup.getUri()
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        db = SQLAlchemy(app)

        o = DbObject(type="Test", json="{}")
        db.session.add(o)
        db.session.commit()

        self.assertTrue(o.id > 0)

    def testLoadObject(self):
        from flask import Flask
        from DbObject import DbObject
        from DbSetup import DbSetup
        from flask_sqlalchemy import SQLAlchemy

        app = Flask(__name__)
        app.config["SQLALCHEMY_DATABASE_URI"] = DbSetup.getUri()
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        db = SQLAlchemy(app)
        db.init_app(app)

        o = DbObject.query.filter_by(id=1).one()

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

if __name__ == '__main__':
    unittest.main()
