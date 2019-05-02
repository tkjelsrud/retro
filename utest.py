import unittest

class TestRetro(unittest.TestCase):
    def testDBconfig(self):
        try:
            self.assertEqual(DbSetup, None)
        except NameError:
            None
        from DbSetup import DbSetup
        self.assertTrue(DbSetup.getUri() is not None)
        self.assertTrue(DbSetup.getUri() is not "")
        #self.assertTrue

    def testCreateObject(self):
        from flask import Flask
        from DbObject import DbObject
        from DbSetup import DbSetup

        o = DbObject(type="Test", json="{}")

        from flask_sqlalchemy import SQLAlchemy

        app = Flask(__name__)

        app.config["SQLALCHEMY_DATABASE_URI"] = DbSetup.getUri()

        db = SQLAlchemy(app)

        #db.session.add(note)
        #db.session.commit()

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

if __name__ == '__main__':
    unittest.main()
