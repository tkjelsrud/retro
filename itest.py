import unittest
from urllib import request, parse
import json

# Integration test cases

baseURL = "http://notoms.pythonanywhere.com/retro"

class TestRetroIntegration(unittest.TestCase):
    testId = -1

    def test_a_CreateObject(self):
        try:
            data = parse.urlencode({'type':'board', 'json': '{}'}).encode()
            req = request.Request(baseURL + "/node/0", data=data) # this will make the method "POST"
            response = request.urlopen(req)
            res = response.read()

            js = json.loads(res)

            self.assertTrue(js['result'] == "200")
            self.assertTrue(int(js['id']) > 0)

            self.testId = int(js['id'])

        except AssertionError:
            pass

        except Exception as error:
                assert False, "Integration test failed with exception " + str(error)

    def test_b_LoadObject(self):
        try:
            with request.urlopen(baseURL + "/node/" + str(self.testId)) as response:
                res = response.read()
                js = json.loads(res)

        except AssertionError:
            pass

        except Exception as error:
            assert False, "Integration test failed with exception " + str(error)

    def test_c_CreateChild(self):
        try:
            data = parse.urlencode({'pid': self.testId, 'type':'note', 'json': '{}'}).encode()
            req = request.Request(baseURL + "/node/0", data=data) # this will make the method "POST"
            response = request.urlopen(req)
            res = response.read()

            js = json.loads(res)

            self.assertTrue(js['result'] == "200")
            self.assertTrue(int(js['id']) > 0)

            self.testId = int(js['id'])

        except AssertionError:
            pass

        except Exception as error:
                assert False, "Integration test failed with exception " + str(error)

    def test_d_LoadObjectList(self):
        try:
            with request.urlopen(baseURL + "/node/" + str(self.testId) + "/children") as response:
                res = response.read()
                js = json.loads(res)

                self.assertTrue(isinstance(js, list))
                self.assertTrue(len(js) == 1)
                self.assertTrue(int(js[0]['pid']) > 0)
                self.assertTrue(int(js[0]['pid']) == self.testId)

        except AssertionError:
            pass

        except Exception as error:
                assert False, "Integration test failed with exception " + str(error)
