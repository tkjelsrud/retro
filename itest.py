import urllib.request

# Integration test cases

baseURL = "http://notoms.pythonanywhere.com/retro"

class TestRetroIntegration(unittest.TestCase):

    def testLoadObject(self):
        #
        with urllib.request.urlopen(baseURL + "/board/12") as response:
            res = response.read()
            print(res)

    def testLoadObjectList(self):
        #
        with urllib.request.urlopen(baseURL + "/board/12/notes") as response:
            res = response.read()
            print(res)
