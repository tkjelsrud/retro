import unittest
from urllib import request, parse
import json
#data = parse.urlencode(<your data dict>).encode()

# Integration test cases

baseURL = "http://notoms.pythonanywhere.com/retro"

class TestRetroIntegration(unittest.TestCase):
    testId = 0

    def testCreateObject(self):
        try:
            data = parse.urlencode({'type':'board', 'json': '{}'}).encode()
            req = request.Request(baseURL + "/node/0", data=data) # this will make the method "POST"
            response = request.urlopen(req)
            res = response.read()

            js = json.loads(res)

            self.assertTrue(js.result == "200")
            self.assertTrue(js.id > 0)

            self.testId = js.id

        except Exception as error:
                assert False, "Integration test failed with exception " + str(error)


    def testLoadObject(self):
        try:
            with request.urlopen(baseURL + "/node/" + str(self.testId)) as response:
                res = response.read()
                js = json.loads(res)
        except Exception as error:
            assert False, "Integration test failed with exception " + str(error)



    def testLoadObjectList(self):
        #
        with request.urlopen(baseURL + "/node/12/children") as response:
            res = response.read()
            print(res)

    #def
