import unittest
from urllib import request, parse
import json

# Integration test cases

baseURL = "http://notoms.pythonanywhere.com/retro"

class TestRetroIntegration(unittest.TestCase):
    def test_CreateAndLoadObject(self):
        # Create
        testId = 0

        try:
            data = parse.urlencode({'type':'board', 'json': '{"content":"v1"}'}).encode()
            req = request.Request(baseURL + "/node/0", data=data, method='POST')
            response = request.urlopen(req)
            res = response.read()

            js = json.loads(res)

            self.assertTrue(js['result'] == "200")
            self.assertTrue(int(js['id']) > 0)

            testId = int(js['id'])
            print("Created " + str(testId))

        except Exception as error:
                print(js)
                assert False, "Integration test POST/CREATE failed with exception " + str(error)

        #
        # Update
        try:
            data = parse.urlencode({'type':'board', 'json': '{"content":"v2"}'}).encode()
            req = request.Request(baseURL + "/node/" + str(testId), data=data, method='PUT')
            response = request.urlopen(req)
            res = response.read()

            js = json.loads(res)

            self.assertTrue(js['result'] == "200")

        except Exception as error:
            assert False, "Integration test UPDATE failed with exception " + str(error)
        #
        # Load
        try:
            with request.urlopen(baseURL + "/node/" + str(testId) + "?s=null") as response:
                res = response.read()
                js = json.loads(res)

                self.assertTrue(js['result'] == "200")
                self.assertTrue(js['json']['content'] == "v2") # Check that update was done

        except Exception as error:
            assert False, "Integration test LOAD failed with exception " + str(error)

        try:
            data = parse.urlencode({'pid': testId, 'type':'note', 'json': '{}'}).encode()
            req = request.Request(baseURL + "/node/0", data=data) # this will make the method "POST"
            response = request.urlopen(req)
            res = response.read()

            js = json.loads(res)

            self.assertTrue(js['result'] == "200")
            self.assertTrue(int(js['id']) > 0)

            testId = int(js['id'])

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

        except Exception as error:
                assert False, "Integration test failed with exception " + str(error)
