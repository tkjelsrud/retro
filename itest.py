import unittest
from urllib import request, parse
#data = parse.urlencode(<your data dict>).encode()

# Integration test cases

baseURL = "http://notoms.pythonanywhere.com/retro"

class TestRetroIntegration(unittest.TestCase):
    def testCreateObject(self):
        data = parse.urlencode({'type':'board', 'json': '{}'}).encode()
        req = request.Request(aseURL + "/node/0", data=data) # this will make the method "POST"
        resp = request.urlopen(req)
        print(resp)

    def testLoadObject(self):
        #
        with request.urlopen(baseURL + "/node/12") as response:
            res = response.read()
            print(res)

    def testLoadObjectList(self):
        #
        with request.urlopen(baseURL + "/node/12/children") as response:
            res = response.read()
            print(res)

    #def
