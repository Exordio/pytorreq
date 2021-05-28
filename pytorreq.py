from stem.process import launch_tor_with_config
from stem.control import Controller
from stem import Signal, connection, socket

import requests
import time


class PyTorReq(object):
    def __init__(self, proxy_port=9050, ctrl_port=9051, password=None, torPath='tor', debug=False):
        self.proxyPort = proxy_port
        self.ctrlPort = ctrl_port
        self.torPath = torPath
        self.password = password
        self._tor_proc = None
        self.ctrl = None
        self.session = None
        self.debug = debug

    def launchTorSession(self):
        if self.debug:
            print(f'Launch new tor session on {self.proxyPort} proxy port, {self.ctrlPort} ctrl port.')
        if not self._torProcessExists():
            self._tor_proc = self._launchTor()
        self.ctrl = Controller.from_port(port=self.ctrlPort)
        self.ctrl.authenticate(password=self.password)
        self.session = requests.Session()
        self.session.proxies.update({
            'http': f'socks5://localhost:{self.proxyPort}',
            'https': f'socks5h://localhost:{self.proxyPort}',
        })

    def _torProcessExists(self):
        try:
            ctrl = Controller.from_port(port=self.ctrlPort)
            ctrl.close()
            return True
        except:
            return False

    def _launchTor(self):
        return launch_tor_with_config(config={'SocksPort': str(self.proxyPort), 'ControlPort': str(self.ctrlPort)},
                                      take_ownership=True, tor_cmd=self.torPath)

    def close(self):
        try:
            self.session.close()
        except:
            pass
        try:
            self.ctrl.close()
        except:
            pass
        if self._tor_proc:
            self._tor_proc.terminate()

    def getNewTorIdentity(self):
        try:
            if self.debug:
                print('Send signal to tor process, NEWNYM, closing session.')
            self.ctrl.signal(Signal.NEWNYM)
            self.ctrl.close()
            self.launchTorSession()
        except:
            print(
                'TOR : The connection is not established. the destination computer rejected the connection request.'
                ' Trying to reconnect.')
            self.ctrl.close()
            self.launchTorSession()
            self.getNewTorIdentity()
        time.sleep(self.ctrl.get_newnym_wait())

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
