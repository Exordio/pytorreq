from stem.process import launch_tor_with_config
from stem.control import Controller
from stem import Signal, connection, socket

import requests
import time


class PyTorReq(object):
    def __init__(self, proxy_port=9050, ctrl_port=9051, password=None, torPath='tor', debug=False):
        self.__proxyPort = proxy_port
        self.__ctrlPort = ctrl_port
        self.__torPath = torPath
        self.__password = password
        self._tor_proc = None
        self.__ctrl = None
        self.session = None
        self.__debug = debug

    def launchTorSession(self):
        if self.__debug:
            print(f'Launch new tor session on {self.__proxyPort} proxy port, {self.__ctrlPort} ctrl port.')
        if not self._torProcessExists():
            self._tor_proc = self._launchTor()
        self.__ctrl = Controller.from_port(port=self.__ctrlPort)
        self.__ctrl.authenticate(password=self.__password)
        self.session = requests.Session()
        self.session.proxies.update({
            'http': f'socks5://localhost:{self.__proxyPort}',
            'https': f'socks5h://localhost:{self.__proxyPort}',
        })

    def _torProcessExists(self):
        try:
            ctrl = Controller.from_port(port=self.__ctrlPort)
            ctrl.close()
            return True
        except:
            return False

    def _launchTor(self):
        return launch_tor_with_config(config={'SocksPort': str(self.__proxyPort), 'ControlPort': str(self.__ctrlPort)},
                                      take_ownership=True, tor_cmd=self.__torPath)

    def close(self):
        try:
            self.session.close()
        except:
            pass
        try:
            self.__ctrl.close()
        except:
            pass
        if self._tor_proc:
            self._tor_proc.terminate()

    def getNewTorIdentity(self):
        try:
            if self.__debug:
                print('Send signal to tor process, NEWNYM, closing session.')
            self.__ctrl.signal(Signal.NEWNYM)
            self.__ctrl.close()
            self.launchTorSession()
        except:
            print(
                'TOR : The connection is not established. the destination computer rejected the connection request.'
                ' Trying to reconnect.')
            self.__ctrl.close()
            self.launchTorSession()
            self.getNewTorIdentity()
        time.sleep(self.__ctrl.get_newnym_wait())

    def get(self, *args, **kwargs):
        return self.session.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.session.post(*args, **kwargs)

    def put(self, *args, **kwargs):
        return self.session.put(*args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.session.patch(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.session.delete(*args, **kwargs)

    def getCookieObj(self):
        return self.session.cookies

    def getCookieDict(self):
        return requests.utils.dict_from_cookiejar(self.session.cookies)

    def updateTorSessionCookie(self, cookie):
        self.session.cookies.update(requests.utils.dict_from_cookiejar(cookie))

    def getMyIp(self):
        return self.get('http://ipecho.net/plain').text

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
