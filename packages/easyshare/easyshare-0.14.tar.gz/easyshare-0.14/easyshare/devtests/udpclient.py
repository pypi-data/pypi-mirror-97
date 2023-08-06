from easyshare.sockets import SocketUdpOut
from easyshare.utils.net import get_primary_ip
from easyshare.utils.types import stob, btos

TO = (get_primary_ip(), 6666)
s = SocketUdpOut()

while True:
    outmsg = input(">> ")

    if outmsg == "recv":
        inmsgraw, endpoint = s.recv()
        inmsg = btos(inmsgraw)
        print("<< {} {}".format(inmsg, endpoint))

    s.send(stob(outmsg), TO[0], TO[1])
