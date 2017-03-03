import api
import json

def start(CONF_NAME, MODLE, CHECKIN_ENGINE):
    if MODLE == "username":
        for private in privates[CONF_NAME]:
            if ((private['username'] != 'username' 
                or private['password'] != 'password')):
                try:
                    USERNAME = private['username']
                    PASSWORD = private['password']
                    BOOT = CHECKIN_ENGINE(USERNAME, PASSWORD)
                    result = BOOT.checkin()
                    print('success', result)
                except UN_Exception as e:
                    print('fail', e)
                except Exception as e:
                    print('fail', e)
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

if __name__ == "__main__":
    with open('config.json', 'r') as json_privates:
        privates = json.load(json_privates)
        start('smzdm', 'username', api.SMZDM)
        start('nemusic', 'username', api.NEMUSIC)
        start('refreshss', 'username', api.REFRESHSS)
        start('tsdm', 'cookies', api.TSDM)
        start('rainkmc', 'username', api.RAINKMC)
