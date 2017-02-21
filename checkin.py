import json
import requests
import sys

SMZDM_USERNAME = "" # username or email
SMZDM_PASSWORD = "" # password

class SMZDM_Checkin(object):
    BASE_URL = 'http://zhiyou.smzdm.com'
    LOGIN_URL = BASE_URL + '/user/login/ajax_check'
    CHECKIN_URL = BASE_URL + '/user/checkin/jsonp_checkin'

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()

    def checkin(self):
        headers = {
                'Host' : 'zhiyou.smzdm.com',
                'Referer' : 'http://www.smzdm.com/',
                'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) '
                    + 'AppleWebKit/537.36 (KHTML, like Gecko) '
                    + 'Chrome/56.0.2924.87 Safari/537.36'
        }
        data = {
                'username' : self.username,
                'password' : self.password
        }
        r = self.session.get(self.BASE_URL, headers = headers, verify=False)
        r = self.session.post(self.LOGIN_URL, data = data, 
                headers = headers, verify = False)
        r = self.session.get(self.CHECKIN_URL, headers = headers, verify = False)
        if r.status_code != 200:
            raise SMZDMException(r)
        json_out = r.text
        out = json.loads(json_out)

        return json_out

class SMZDM_Exception(Exception):
    def __init__(self, req):
        self._req = req

    def __str__(self):
        return str(self.req)

with open('config.json', 'r') as json_privates:
    privates = json.load(json_privates)
    for private in privates['smzdm']:
        if private['username'] == 'username' or private['password'] == 'password':
            print("Plz set you username and password first.")
            sys.exit()
        try:
            SMZDM_USERNAME = private['username']
            SMZDM_PASSWORD = private['password']
            smzdm = SMZDM_Checkin(SMZDM_USERNAME, SMZDM_PASSWORD)
            result = smzdm.checkin()
        except SMZDM_Exception as e:
            print('fail', e)
        except Exception as e:
            print('fail', e)
        else:
            print('success', result)
