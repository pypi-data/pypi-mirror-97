from easyshare.logging import init_logging
from easyshare.protocol.requests import create_request
from easyshare.protocol.streams import Stream
from easyshare.sockets import SocketTcpOut
from easyshare.utils.json import jtob
from easyshare.utils.net import get_primary_ip
from easyshare.utils.types import btos

init_logging(5)

endpoint = (get_primary_ip(), 12020)

print(f"Connecting to...{endpoint}")
sock = SocketTcpOut(endpoint[0], endpoint[1])
ss = Stream(sock)
print("socket connected")
ss.write(jtob(create_request("connect")))
resp = ss.read()
print(f"connect << {repr(resp)}")

while True:

    cmd = input("rexec >> ")

    # Send
    req = create_request("rexec", {"cmd": cmd})
    ss.write(jtob(req))
    print(f"rexec << {repr(resp)}")

    # Recv
    while True:
        resp = ss.read()
        if not resp:
            break
        print(btos(resp), end="")

    rexec_resp = ss.read()
    print(f"rexec << {repr(rexec_resp)}")
