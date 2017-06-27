import requests
import time
import logging

logging.basicConfig(level=logging.DEBUG)


class dcs5020l:
    def __init__(self):
        self.url = ""
        self.user = ""
        self.password = ""
        self.connectedState = 0
        logging.debug('Creating instance')

    def connect(self, URL, user, password):
        self.url = URL
        self.user = user
        self.password = password
        self.connectedState = 1
        logging.debug('URL: %s user: %s password: %s' % (URL, user, password))

    def disconnect(self):
        self.connectedState = 0

    def up(self, degrees=1):
        delay = degrees / 20
        logging.debug('up by ' + str(degrees))
        sData = {'TiltSingleMoveDegree': str(degrees),
                 'PanTiltSingleMove': '1'}
        r = requests.post(self.url+'/pantiltcontrol.cgi',
                          data=sData, auth=(self.user, self.password),
                          verify=False)
        time.sleep(delay + 1)
        return r

    def down(self, degrees=1):
        delay = degrees / 20
        logging.debug('down by ' + str(degrees))
        sData = {'TiltSingleMoveDegree': str(degrees),
                 'PanTiltSingleMove': '7'}
        r = requests.post(self.url+'/pantiltcontrol.cgi',
                          data=sData, auth=(self.user, self.password),
                          verify=False)
        time.sleep(delay + 1)
        return r

    def left(self, degrees=1):
        delay = degrees / 15
        logging.debug('left by ' + str(degrees))
        sData = {'PanSingleMoveDegree': str(degrees), 'PanTiltSingleMove': '3'}
        r = requests.post(self.url+'/pantiltcontrol.cgi',
                          data=sData, auth=(self.user, self.password))
        time.sleep(delay+1)
        return r

    def right(self, degrees=1):
        delay = degrees / 15
        logging.debug('right by ' + str(degrees))
        sData = {'PanSingleMoveDegree': str(degrees), 'PanTiltSingleMove': '5'}
        r = requests.post(self.url+'/pantiltcontrol.cgi',
                          data=sData, auth=(self.user, self.password),
                          verify=False)
        time.sleep(delay+1)
        return r

    def home(self):
        logging.debug('return ptz to home')
        p, t = self.getPosition()
        logging.debug('before moving home: ' + str(p) + ' ' + str(t))

        sData = {'PanTiltSingleMove': '4'}
        r = requests.post(self.url+'/pantiltcontrol.cgi', data=sData,
                          auth=(self.user, self.password), verify=False)
        time.sleep(15)
        return r

    def getImage(self, fileName):
        """
        in: fileName
        return: r - results of requests.get

        note: will potentially write a file 
        """
        r = requests.get(self.url+'/image.jpg',
                         auth=(self.user, self.password),
                         stream=True, verify=False)
        if r.status_code == 200:
            with open(fileName, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
        return r

    def getPosition(self):
        """
        return: pan position, tilt position
        """

        r = requests.get(self.url+'/config/ptz_pos.cgi',
                         auth=(self.user, self.password), verify=False)
        for x in r.text.split("\n"):
            if x.startswith('p'):
                pan = int(x.split('=')[1])
            if x.startswith('t'):
                tilt = int(x.split('=')[1])
        return pan, tilt

    def daynight(self, mode):
        """
        return r - result of requests post
        """
        r = requests.post(self.url+'/nightmodecontrol.cgi?IRLed=' + str(mode),
                          auth=(self.user, self.password))
        return r
