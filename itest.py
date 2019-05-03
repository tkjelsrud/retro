import unittest
from urllib import request, parse
#data = parse.urlencode(<your data dict>).encode()

# Integration test cases

baseURL = "http://notoms.pythonanywhere.com/retro"

class TestRetroIntegration(unittest.TestCase):

    def testLoadObject(self):
        #
        with request.urlopen(baseURL + "/board/12") as response:
            res = response.read()
            print(res)

    def testLoadObjectList(self):
        #
        with request.urlopen(baseURL + "/board/12/notes") as response:
            res = response.read()
            print(res)

    #def 
