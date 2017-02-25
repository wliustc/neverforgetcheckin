import json
import requests
import os
import base64
import binascii
import hashlib
import time
from Crypto.Cipher import AES
from bs4 import BeautifulSoup

def start(CONF_NAME, MODLE, CHECKIN_ENGINE):
    if MODLE == "username":
        for private in privates[CONF_NAME]:
            if ('username' in private 
                and (private['username'] != 'username' 
                or private['password'] != 'password')):
                try:
                    USERNAME = private['username']
                    PASSWORD = private['password']
                    boot = CHECKIN_ENGINE(USERNAME, PASSWORD)
                    result = boot.checkin()
                    print('success', result)
                except UN_Exception as e:
                    print('fail', e)
                except Exception as e:
                    raise e
            else:
                print("Plz set you " + CONF_NAME  +
                        " username and password first.")
    elif MODLE == "cookies":
        for private in privates[CONF_NAME]:
            if ( private != {} ):
                try:
                    COOKIES = private
                    boot = CHECKIN_ENGINE(COOKIES)
                    result = boot.checkin()
                    print('success', result)
                except UN_Exception as e:
                    print('fail', e)
                except Exception as e:
                    raise e
            else:
                print("Plz set you " + CONF_NAME  + " cookies first.")
    else:
        print("start engin failed")

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
                'User-Agent' : ('Mozilla/5.0 (X11; Linux x86_64) '
                                'AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/56.0.2924.87 Safari/537.36')
        }
        param = {
                'username' : self.username,
                'password' : self.password
        }
        r = self.session.post(self.LOGIN_URL, data = param,
                headers = headers)
        r = self.session.get(self.CHECKIN_URL, headers = headers)
        if r.status_code != 200:
            raise UN_Exception(r)
        result = json.loads(r.text)
        return result

class NEMUSIC_Checkin(object):
    BASE_URL = 'https://music.163.com'
    LOGIN_URL = BASE_URL + '/weapi/login'
    CHECKIN_URL = BASE_URL + "/api/point/dailyTask?type="
    WEB_CHECKIN_URL = CHECKIN_URL + "0"
    PHONE_CHECKIN_URL = CHECKIN_URL + "1"

    modulus = ('00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace61'
               '5bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fc'
               'cf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7'
               'a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d'
               '546b8e289dc6935b3ece0462db0a22b8e7')
    nonce = '0CoJUm6Qyw8W8jud'
    pubKey = '010001'

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()

    def encrypted_request(self, text):
        text = json.dumps(text)
        secKey = self.createSecretKey(16)
        encText = self.aesEncrypt(
                self.aesEncrypt(text, self.nonce), secKey)
        encSecKey = self.rsaEncrypt(secKey, self.pubKey, self.modulus)
        data = {'params': encText, 'encSecKey': encSecKey}
        return data

    def aesEncrypt(self, text, secKey):
        pad = 16 - len(text) % 16
        text = text + chr(pad) * pad
        encryptor = AES.new(secKey, 2, '0102030405060708')
        ciphertext = encryptor.encrypt(text)
        ciphertext = base64.b64encode(ciphertext).decode('utf-8')
        return ciphertext

    def rsaEncrypt(self, text, pubKey, modulus):
        text = text[::-1]
        rs = pow(int(binascii.hexlify(text), 16),
                int(pubKey, 16), int(modulus, 16))
        return format(rs, 'x').zfill(256)

    def createSecretKey(self, size):
        return binascii.hexlify(os.urandom(size))[:16]

    def checkin(self):
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/search',
            'User-Agent' : ('Mozilla/5.0 (X11; Linux x86_64) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/56.0.2924.87 Safari/537.36')
        }
        text = {
            'username' : self.username,
            'password' : hashlib.md5(
                self.password.encode('utf-8')).hexdigest(),
            'rememberLogin' : 'true'
        }
        data = self.encrypted_request(text)
        r = self.session.post(self.LOGIN_URL, data = data,
            headers = headers)
        r = self.session.post(self.WEB_CHECKIN_URL, headers = headers)
        r = self.session.post(self.PHONE_CHECKIN_URL, headers = headers)
        if r.status_code != 200:
            raise UN_Exception(r)
        result = json.loads(r.text)
        return result

class REFRESHSS_Checkin(object):
    BASE_URL = 'https://www.refreshss.ml'
    LOGIN_URL = BASE_URL + '/auth/login'
    CHECKIN_URL = BASE_URL + '/user/checkin'
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()

    def checkin(self):
        headers = {
                'Host' : 'www.refreshss.ml',
                'Referer' : 'https://www.refreshss.ml/user',
                'User-Agent' : ('Mozilla/5.0 (X11; Linux x86_64) '
                                'AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/56.0.2924.87 Safari/537.36'),
        }
        param = {
                'email' : self.username,
                'passwd' : self.password
        }
        r = self.session.post(self.LOGIN_URL, data = param,
                headers = headers)
        r = self.session.post(self.CHECKIN_URL, headers = headers)
        if r.status_code != 200:
           raise UN_Exception(r)
        result = json.loads(r.text)
        return result

class TSDM_Checkin(object):
    BASE_URL = 'http://www.tsdm.me'
    CHECKIN_URL = BASE_URL + ('/plugin.php?id=dsu_paulsign%3Asign'
            '&operation=qiandao&infloat=1&inajax=1')

    def get_formhash(self, target):
        result = BeautifulSoup(target, "html.parser").find('input',
                attrs={'name':'formhash'})
        return result

    def __init__(self, cookies):
        self.cookies = cookies
        self.session = requests.Session()

    def checkin(self):
        headers = {
                'Host' : 'www.tsdm.me',
                'Referer' : 'http://www.tsdm.me/',
                'User-Agent' : ('Mozilla/5.0 (X11; Linux x86_64) '
                                'AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/56.0.2924.87 Safari/537.36'),
                }
        r = self.session.get(self.BASE_URL, cookies = self.cookies,
                headers = headers)
        prama = {
                "formhash" : self.get_formhash(r.text)["value"],
                "qdxq" : "kx",
                "qdmode" : "1",
                "todaysay" : "May the force be with you.",
                "fastreply" : "1"
        }
        r = self.session.post(self.CHECKIN_URL, cookies = self.cookies,
                data = prama, headers = headers)
        result = r.text
        return result

class UN_Exception(Exception):
    def __init__(self, req):
        self._req = req

    def __str__(self):
        return str(self._req)

with open('./config.json', 'r') as json_privates:
    privates = json.load(json_privates)
    start('smzdm', 'username', SMZDM_Checkin)
    start('nemusic', 'username', NEMUSIC_Checkin)
    start('refreshss', 'username', REFRESHSS_Checkin)
    start('tsdm', 'cookies', TSDM_Checkin)
