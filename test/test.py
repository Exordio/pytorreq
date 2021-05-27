from pytorreq import PyTorReq
from datetime import datetime

treq = PyTorReq(torPath='''Q:\\tor Browser\\Browser\\TorBrowser\\Tor\\tor.exe''')

treq.launchTorSession()

for i in range(5):
    print(f'''  | {datetime.now().time()} : TOR IP : {treq.get('http://ipecho.net/plain').text} | ''')
    treq.resetTorIdentity()
