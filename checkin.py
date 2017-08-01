import api
import json
import threading

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
                except api.UN_Exception as e:
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
                except api.UN_Exception as e:
                    print('fail', e)
            else:
                print("Plz set you " + CONF_NAME  + " cookies first.")
    else:
        print("start engin failed")

if __name__ == "__main__":
    try:
        with open('config.json', 'r') as json_privates:
            privates = json.load(json_privates)

            threading.Thread(target=start, args=('smzdm', 'username', api.SMZDM,)).start()
            threading.Thread(target=start, args=('nemusic', 'username', api.NEMUSIC,)).start()
            #  threading.Thread(target=start, args=('refreshss', 'username', api.REFRESHSS,)).start()
            threading.Thread(target=start, args=('tsdm', 'cookies', api.TSDM,)).start()
            threading.Thread(target=start, args=('rainkmc', 'username', api.RAINKMC,)).start()
            threading.Thread(target=start, args=('readfree','cookies',api.READFREE,)).start()
    except:
        print("error")
