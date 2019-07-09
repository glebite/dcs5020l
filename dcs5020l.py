"""
dcs5020l
"""
import time
import logging
import requests

logging.basicConfig(level=logging.DEBUG)


class Dcs5020l:
    """ Dcs5020l """
    def __init__(self):
        """ init """
        self.url = ""
        self.user = ""
        self.password = ""
        self.connected_state = 0
        logging.debug('Creating instance')

    def connect(self, url, user, password):
        """ connect """
        self.url = url
        self.user = user
        self.password = password
        self.connected_state = 1
        logging.debug('URL: %s user: %s password: %s', url, user, password)

    def disconnect(self):
        """ disconnect """
        self.connected_state = 0

    def move_up(self, degrees=1):
        """ up """
        delay = degrees / 20
        logging.debug('up by %s', str(degrees))
        string_data = {'TiltSingleMoveDegree': str(degrees),
                       'PanTiltSingleMove': '1'}
        result = requests.post(self.url+'/pantiltcontrol.cgi',
                               data=string_data, auth=(self.user, self.password),
                               verify=False)
        time.sleep(delay + 1)
        return result

    def move_down(self, degrees=1):
        """ down """
        delay = degrees / 20
        logging.debug('down by %s', str(degrees))
        string_data = {'TiltSingleMoveDegree': str(degrees),
                       'PanTiltSingleMove': '7'}
        result = requests.post(self.url+'/pantiltcontrol.cgi',
                               data=string_data, auth=(self.user, self.password),
                               verify=False)
        time.sleep(delay + 1)
        return result

    def move_left(self, degrees=1):
        """ left """
        delay = degrees / 15
        logging.debug('left by %s', str(degrees))
        string_data = {'PanSingleMoveDegree': str(degrees), 'PanTiltSingleMove': '3'}
        result = requests.post(self.url+'/pantiltcontrol.cgi',
                               data=string_data, auth=(self.user, self.password))
        time.sleep(delay+1)
        return result

    def move_right(self, degrees=1):
        """ right """
        delay = degrees / 15
        logging.debug('right by %s', str(degrees))
        string_data = {'PanSingleMoveDegree': str(degrees), 'PanTiltSingleMove': '5'}
        result = requests.post(self.url+'/pantiltcontrol.cgi',
                               data=string_data, auth=(self.user, self.password),
                               verify=False)
        time.sleep(delay+1)
        return result

    def move_home(self):
        """ home """
        logging.debug('return ptz to home')
        pan_pos, tilt_pos = self.get_position()
        logging.debug('before moving home: %s %s', str(pan_pos), str(tilt_pos))

        string_data = {'PanTiltSingleMove': '4'}
        result = requests.post(self.url+'/pantiltcontrol.cgi', data=string_data,
                               auth=(self.user, self.password), verify=False)
        time.sleep(15)
        return result

    def get_image(self, file_name):
        """
        in: fileName
        return: result - results of requests.get

        note: will potentially write a file
        """
        result = requests.get(self.url+'/image.jpg',
                              auth=(self.user, self.password),
                              stream=True, verify=False)
        if result.status_code == 200:
            with open(file_name, 'wb') as file_handle:
                for chunk in result.iter_content(1024):
                    file_handle.write(chunk)
        return result

    def get_position(self):
        """
        return: pan position, tilt position
        """

        result = requests.get(self.url+'/config/ptz_pos.cgi',
                              auth=(self.user, self.password), verify=False)
        for item in result.text.split("\n"):
            if item.startswith('p'):
                pan = int(item.split('=')[1])
            if item.startswith('t'):
                tilt = int(item.split('=')[1])
        return pan, tilt

    def day_night(self, mode):
        """
        return result - result of requests post
        """
        result = requests.post(self.url+'/nightmodecontrol.cgi?IRLed=' + str(mode),
                               auth=(self.user, self.password))
        return result
