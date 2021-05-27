from pytorreq import PyTorReq
from datetime import datetime

treq = PyTorReq(torPath='''Q:\\tor Browser\\Browser\\TorBrowser\\Tor\\tor.exe''', debug=True)

treq.launchTorSession()

for i in range(10):
    print(f'''  | {datetime.now().time()} : TOR IP : {treq.getMyIp()} | ''')
    treq.getNewTorIdentity()
