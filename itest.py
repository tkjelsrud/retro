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

            print(js)

            self.assertTrue(js['result'] == "200")
            self.assertTrue(int(js['id']) > 0)

            self.testId = int(js['id'])

        except AssertionError:
            pass

        except Exception as error:
                assert False, "Integration test failed with exception " + str(error)


    def testLoadObject(self):
        try:
            with request.urlopen(baseURL + "/node/" + str(self.testId)) as response:
                res = response.read()
                js = json.loads(res)

        except AssertionError:
            pass

        except Exception as error:
            assert False, "Integration test failed with exception " + str(error)



    def testLoadObjectList(self):
        #
        with request.urlopen(baseURL + "/node/12/children") as response:
            res = response.read()
            print(res)

    #def
