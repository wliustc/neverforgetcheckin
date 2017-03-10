import json
import requests
import os
import base64
import binascii
import hashlib
import time
from Crypto.Cipher import AES
from bs4 import BeautifulSoup

class SMZDM(object):
    BASE_URL = 'http://zhiyou.smzdm.com'
    LOGIN_URL = BASE_URL + '/user/login/ajax_check'
    CHECKIN_URL = BASE_URL + '/user/checkin/jsonp_checkin'
    HEADERS = {
                'Host' : 'zhiyou.smzdm.com',
                'Referer' : 'http://www.smzdm.com/',
                'User-Agent' : ('Mozilla/5.0 (X11; Linux x86_64) '
                                'AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/56.0.2924.87 Safari/537.36')
    }
    
    def __init__(self, USERNAME, PASSWORD):
        self._USERNAME = USERNAME
        self._PASSWORD = PASSWORD
        self._SESSION = requests.Session()

    def checkin(self):
        param = {
                'username' : self._USERNAME,
                'password' : self._PASSWORD
        }
        try:
            r = self._SESSION.post(self.LOGIN_URL, data = param,
                    headers = self.HEADERS, timeout = 3)
            r = self._SESSION.get(self.CHECKIN_URL,
                    headers = self.HEADERS, timeout = 3)
            if r.status_code != 200:
                result = 'SMZDM checkin failed!'
            else:
                result = json.loads(r.text)
        except Exception as e:
            print("failed", e)
        return result

class NEMUSIC(object):
    BASE_URL = 'https://music.163.com'
    LOGIN_URL = BASE_URL + '/weapi/login'
    CHECKIN_URL = BASE_URL + "/api/point/dailyTask?type="
    WEB_CHECKIN_URL = CHECKIN_URL + "0"
    PHONE_CHECKIN_URL = CHECKIN_URL + "1"
    HEADERS = {
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
    MODULUS = ('00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace61'
               '5bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fc'
               'cf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7'
               'a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d'
               '546b8e289dc6935b3ece0462db0a22b8e7')
    NONCE = '0CoJUm6Qyw8W8jud'
    PUBKEY = '010001'
    
    def __init__(self, USERNAME, PASSWORD):
        self._USERNAME = USERNAME
        self._PASSWORD = PASSWORD
        self._SESSION = requests.Session()

    def encrypted_request(self, text):
        text = json.dumps(text)
        secKey = self.createSecretKey(16)
        encText = self.aesEncrypt(
                self.aesEncrypt(text, self.NONCE), secKey)
        encSecKey = self.rsaEncrypt(secKey, self.PUBKEY, self.MODULUS)
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
        text = {
            'username' : self._USERNAME,
            'password' : 
            	hashlib.md5(self._PASSWORD.encode('utf-8')).hexdigest(),
            'rememberLogin' : 'true'
        }
        param = self.encrypted_request(text)
        try:
            r = self._SESSION.post(self.LOGIN_URL, data = param,
                    headers = self.HEADERS, timeout = 3)
            r = self._SESSION.post(self.WEB_CHECKIN_URL,
        	    headers = self.HEADERS, timeout = 3)
            r = self._SESSION.post(self.PHONE_CHECKIN_URL,
        	    headers = self.HEADERS, timeout = 3)
            if r.status_code != 200:
                result = 'Netease Music checkin failed!'
            else:
                result = json.loads(r.text)
        except Exception as e:
            print("failed", e)
        return result

class REFRESHSS(object):
    BASE_URL = 'https://www.refreshss.ml'
    LOGIN_URL = BASE_URL + '/auth/login'
    CHECKIN_URL = BASE_URL + '/user/checkin'
    HEADERS = {
                'Host' : 'www.refreshss.ml',
                'Referer' : 'https://www.refreshss.ml/user',
                'User-Agent' : ('Mozilla/5.0 (X11; Linux x86_64) '
                                'AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/56.0.2924.87 Safari/537.36'),
    }
    
    def __init__(self, USERNAME, PASSWORD):
        self._USERNAME = USERNAME
        self._PASSWORD = PASSWORD
        self._SESSION = requests.Session()

    def checkin(self):
        param = {
                'email' : self._USERNAME,
                'passwd' : self._PASSWORD
        }
        try:
            r = self._SESSION.post(self.LOGIN_URL, data = param,
                    headers = self.HEADERS, timeout = 3)
            r = self._SESSION.post(self.CHECKIN_URL,
                    headers = self.HEADERS, timeout = 3)
            if r.status_code != 200:
                result = 'Refreshss checkin failed!'
            else:
                result = json.loads(r.text)
        except Exception as e:
            print("failed", e)
        return result

class TSDM(object):
    BASE_URL = 'http://www.tsdm.me'
    CHECKIN_URL = BASE_URL + ('/plugin.php?id=dsu_paulsign%3Asign'
            '&operation=qiandao&infloat=1&inajax=1')
    HEADERS = {
                'Host' : 'www.tsdm.me',
                'Referer' : 'http://www.tsdm.me/',
                'User-Agent' : ('Mozilla/5.0 (X11; Linux x86_64) '
                                'AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/56.0.2924.87 Safari/537.36'),
    }

    def __init__(self, COOKIES):
        self._COOKIES = COOKIES
        self._SESSION = requests.Session()

    def get_formhash(self, target):
        result = BeautifulSoup(target, "html.parser").find('input',
                attrs={'name':'formhash'})
        return result

    def checkin(self):
        try:
            r = self._SESSION.get(self.BASE_URL, cookies = self._COOKIES,
                    headers = self.HEADERS, timeout = 3)
            param = {
                    "formhash" : self.get_formhash(r.text)["value"],
                    "qdxq" : "kx",
                    "qdmode" : "1",
                    "todaysay" : "May the force be with you.",
                    "fastreply" : "1"
            }
            r = self._SESSION.post(self.CHECKIN_URL,cookies = self._COOKIES,
                    data = param, headers = self.HEADERS, timeout = 3)
            if r.status_code != 200:
                result = 'TSDM Checkin failed!'
            else:
                result = r.text
        except Exception as e:
            print("failed", e)
        return result

class RAINKMC(object):
    BASE_URL = 'https://rainkmc.ml'
    LOGIN_URL = BASE_URL + ('/member.php?mod=logging&action=login'
            '&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1')
    CHECKIN_URL = BASE_URL + ('/plugin.php?id=u179_qdgj&action=punch'
            '&inajax=1&ajaxtarget=undefined')
    HEADERS = {
                'Host' : 'rainkmc.ml',
                'Referer' : 'https://rainkmc.ml/forum.php',
                'User-Agent' : ('Mozilla/5.0 (X11; Linux x86_64) '
                                'AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/56.0.2924.87 Safari/537.36'),
    }

    def __init__(self, USERNAME, PASSWORD):
        self._USERNAME = USERNAME
        self._PASSWORD = PASSWORD
        self._SESSION = requests.Session()

    def checkin(self):
        param = {
                'username' : self._USERNAME,
                'password' : self._PASSWORD
        }
        try:
            r = self._SESSION.post(self.LOGIN_URL, data = param,
                    headers = self.HEADERS, timeout = 3)
            r = self._SESSION.get(self.CHECKIN_URL,
                    headers = self.HEADERS, timeout = 3)
            if r.status_code != 200:
                result = 'Rainkmc checkin failed!'
            else:
                result = r.text
        except Exception as e:
            print("failed", e)
        return result

class UN_Exception(Exception):
    def __init__(self, req):
        self._req = req

    def __str__(self):
        return str(self._req)
