import json
import requests
import os
#  import base64
#  import binascii
#  from Crypto.Cipher import AES

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
                headers = headers, verify = False)
        r = self.session.get(self.CHECKIN_URL, headers = headers,
                verify = False)
        if r.status_code != 200:
            raise UN_Exception(r)
        json_out = r.text
        out = json.loads(json_out)
        return out

class NEMUSIC_Checkin(object):
    BASE_URL = 'http://music.163.com'
    #  LOGIN_URL = BASE_URL + '/weapi/login/'
    #  PHONE_LOGIN_URL = BASE_URL + '/weapi/login/cellphone/'
    #  CHECKIN_URL = BASE_URL + '/weapi/point/dailyTask/'
    CHECKIN_URL = BASE_URL + "/api/point/dailyTask?type="
    WEB_CHECKIN_URL = CHECKIN_URL + "0"
    PHONE_CHECKIN_URL = CHECKIN_URL + "1"

    #  modulus = ('00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7'
    #      'b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280'
    #      '104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932'
    #      '575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b'
    #      '3ece0462db0a22b8e7')
    #  nonce = '0CoJUm6Qyw8W8jud'
    #  pubKey = '010001'

    #  def __init__(self, username, password):
        #  self.username = username
        #  self.password = password
    #      self.session = requests.Session()
    def __init__(self, cookies):
        self.cookies = cookies
        self.session = requests.Session()

    #  def encrypted_request(self, text):
    #      text = json.dumps(text)
    #      secKey = self.createSecretKey(16)
    #      encText = self.aesEncrypt(self.aesEncrypt(text, self.nonce), secKey)
    #      encSecKey = self.rsaEncrypt(secKey, self.pubKey, self.modulus)
    #      data = {'params': encText, 'encSecKey': encSecKey}
    #      return data
    #
    #  def aesEncrypt(self, text, secKey):
    #      pad = 16 - len(text) % 16
    #      text = text + chr(pad) * pad
    #      encryptor = AES.new(secKey, 2, '0102030405060708')
    #      ciphertext = encryptor.encrypt(text)
    #      ciphertext = base64.b64encode(ciphertext).decode('utf-8')
    #      return ciphertext
    #
    #  def rsaEncrypt(self, text, pubKey, modulus):
    #      text = text[::-1]
    #      rs = pow(int(binascii.hexlify(text), 16),
    #              int(pubKey, 16), int(modulus, 16))
    #      return format(rs, 'x').zfill(256)
    #
    #  def createSecretKey(self, size):
    #      return binascii.hexlify(os.urandom(size))[:16]

    #  def checkin(self):
        #  headers = {
        #      'Accept': '*/*',
        #      'Accept-Encoding': 'gzip,deflate,sdch',
        #      'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
        #      'Connection': 'keep-alive',
        #      'Content-Type': 'application/x-www-form-urlencoded',
        #      'Host': 'music.163.com',
        #      'Referer': 'http://music.163.com/search/',
        #      'User-Agent' : ('Mozilla/5.0 (X11; Linux x86_64) '
        #                      'AppleWebKit/537.36 (KHTML, like Gecko) '
        #                      'Chrome/56.0.2924.87 Safari/537.36')
        #  }
        #  text = {
        #      'username' : self.username,
        #      'password' : self.password,
        #      'remerberLogin' : 'true'
        #  }
        #  data = self.encrypted_request(text)
        #  r = self.session.post(self.LOGIN_URL, data = data,
        #      headers = headers)
        #  if r.status_code != 200:
        #      raise UN_Exception(r)
        #  text = {'type' : 0}
        #  data = encrypted_request(text)
        #  r = self.session.post(self.CHECKIN_URL, data = data,
        #          headers = headers)
        #  text = {'type' : 1}
        #  data = encrypted_request(text)
        #  r = self.session.post(self.CHECKIN_URL, data = data,
        #          headers = headers)
        #  out = json.loads(r.text)
    #      return out
    def checkin(self):
        headers = {'Referer' : 'http://music.163.com/'}
        cookies = { 'MUSIC_U' : self.cookies }
        r = self.session.post(self.WEB_CHECKIN_URL, cookies = cookies,
                headers = headers)
        r = self.session.post(self.PHONE_CHECKIN_URL, cookies = cookies,
                headers = headers)
        out = json.loads(r.text)
        return out

class UN_Exception(Exception):
    def __init__(self, req):
        self._req = req

    def __str__(self):
        return str(self._req)

with open('config.json', 'r') as json_privates:
    privates = json.load(json_privates)
    for private in privates['smzdm']:
        if (private['username'] != 'username'
                or private['password'] != 'password'):
            try:
                SMZDM_USERNAME = private['username']
                SMZDM_PASSWORD = private['password']
                smzdm = SMZDM_Checkin(SMZDM_USERNAME, SMZDM_PASSWORD)
                result = smzdm.checkin()
            except UN_Exception as e:
                print('fail', e)
            except Exception as e:
                print('fail', e)
            print('success', result)
        else:
            print("Plz set you smzdm username and password first.")
    for private in privates['nemusic']:
        #  if (private['username'] != 'username'
        #          or private['password'] != 'password'):
        if private['cookies'] != 'cookies':
            try:
                #  NEMUSIC_USERNAME = private['username']
                #  NEMUSIC_PASSWORD = private['password']
                NEMUSIC_COOKIES = private['cookies']
                #  nemusic = NEMUSIC_Checkin(NEMUSIC_USERNAME, NEMUSIC_PASSWORD)
                nemusic = NEMUSIC_Checkin(NEMUSIC_COOKIES)
                result = nemusic.checkin()
                print('success', result)
            except UN_Exception as e:
                print('fail', e)
            except Exception as e:
                print('fail', e)
        else:
            print("Plz set you netease music username and password first.")

