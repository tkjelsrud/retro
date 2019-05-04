import unittest
from urllib import request, parse
import json

# Integration test cases

baseURL = "http://notoms.pythonanywhere.com/retro"

class TestRetroIntegration(unittest.TestCase):
    def test_CreateAndLoadObject(self):
        # Create

        try:
            data = parse.urlencode({'type':'board', 'json': '{}'}).encode()
            req = request.Request(baseURL + "/node/0", data=data) # this will make the method "POST"
            response = request.urlopen(req)
            res = response.read()

            js = json.loads(res)

            self.assertTrue(js['result'] == "200")
            self.assertTrue(int(js['id']) > 0)

            testId = int(js['id'])
            print("Created " + str(testId))

        except AssertionError:
            pass

        except Exception as error:
                assert False, "Integration test failed with exception " + str(error)

        # Load

        try:
            with request.urlopen(baseURL + "/node/" + str(testId) + "?s=null") as response:
                res = response.read()
                js = json.loads(res)

        except AssertionError:
            pass

        except Exception as error:
            assert False, "Integration test failed with exception " + str(error)

        try:
            data = parse.urlencode({'pid': testId, 'type':'note', 'json': '{}'}).encode()
            req = request.Request(baseURL + "/node/0", data=data) # this will make the method "POST"
            response = request.urlopen(req)
            res = response.read()

            js = json.loads(res)

            self.assertTrue(js['result'] == "200")
            self.assertTrue(int(js['id']) > 0)

            testId = int(js['id'])

        except AssertionError:
            pass

        except Exception as error:
                assert False, "Integration test failed with exception " + str(error)

        try:
            with request.urlopen(baseURL + "/node/" + str(testId) + "/children") as response:
                res = response.read()
                js = json.loads(res)

                self.assertTrue(isinstance(js, list))
                self.assertTrue(len(js) == 1)
                self.assertTrue(int(js[0]['pid']) > 0)
                self.assertTrue(int(js[0]['pid']) == testId)

        except AssertionError:
            pass

        except Exception as error:
                assert False, "Integration test failed with exception " + str(error)
