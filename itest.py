import unittest
#from urllib import requests, parse
import requests
import json

# Integration test cases

baseURL = "http://notoms.pythonanywhere.com/retro"

class TestRetroIntegration(unittest.TestCase):
    def test_CreateAndLoadObject(self):
        # Create
        testId = 0
        skey = ''

        try:
            dJson = {'type':'group', 'json': '{"content":"v1"}'}
            #headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            req = requests.post(baseURL + "/node/0", json=dJson)
            #response = request.urlopen(req)
            #res = response.read()
            if req.status_code() != 200:
                assert False, "Integration test POST/CREATE failed response code" + str(req.status_code())

            js = req.json() # json.loads(res)

            self.assertTrue(int(js['result']) == 200)
            self.assertTrue(int(js['id']) > 0)

            skey = js['skey']

            testId = int(js['id'])
            skey = js['skey']
            print("Created " + str(testId))

        except Exception as error:
                if 'js' in locals():
                    print(js)
                assert False, "Integration test POST/CREATE failed with exception " + str(error)

        #
        # Update
        try:
            dJson = {'type':'board', 'json': '{"content":"v2"}'}

            req = requests.post(baseURL + "/node/" + str(testId) + "?s=" + skey, json=dJson)
            if req.status_code != 200:
                assert False, "Integration test POST/CREATE failed response code" + str(req.status_code)

            js = req.json() #json.loads(res)

            self.assertTrue(int(js['result']) == 200)
            self.assertTrue(js['update'] == "True")

        except Exception as error:
            print(js)
            assert False, "Integration test UPDATE failed with exception " + str(error)
        #
        # Load
        try:
            r = requests.get(baseURL + "/node/" + str(testId) + "?s=" + skey)

            if r.status_code != 200:
                assert False, "Integration test LOAD failed response code" + str(r.status_code)

            js = r.json()

            self.assertTrue(int(js['result']) == 200)

            innerjs = js['json']

            self.assertTrue(innerjs['content'] == "v2") # Check that update was done

        except Exception as error:
            print(js)
            assert False, "Integration test LOAD failed with exception " + str(error)

        # Create child
        try:
            dJson = {'pid': testId, 'type':'note', 'json': '{}', 'skey': skey}

            req = requests.post(baseURL + "/node/" + str(testId) + "?s=" + skey, json=dJson)
            if req.status_code != 200:
                assert False, "Integration test POST/CREATE failed response code" + str(req.status_code)

            js = req.json()

            self.assertTrue(int(js['result']) == 200)
            self.assertTrue(int(js['id']) > 0)

        except Exception as error:
                assert False, "Integration test POST CHILD failed with exception " + str(error)

        try:
            r = requests.get(baseURL + "/node/" + str(testId) + "/children?s=" + skey)

            if r.status_code != 200:
                assert False, "Integration test LOAD children failed response code" + str(r.status_code)

            js = r.json()

            self.assertTrue(int(js['result']) == 200)
            self.assertTrue(isinstance(js['json'], list))
            self.assertTrue(len(js['json']) == 1)
            self.assertTrue(int(js['json'][0]['pid']) > 0)
            self.assertTrue(int(js['json'][0]['pid']) == testId)

        except Exception as error:
                print(js)
                assert False, "Integration test failed with exception " + str(error)
