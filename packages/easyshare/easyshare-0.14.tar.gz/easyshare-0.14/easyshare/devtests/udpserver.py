from easyshare.sockets import SocketUdpIn
from easyshare.utils.types import btos, stob

s = SocketUdpIn(port=6666)

while True:
    print("Waiting messages....")

    inmsgraw, endpoint = s.recv()

    if not inmsgraw:
        print("Nothing received")
        continue

    inmsg = btos(inmsgraw)
    print("<< {} {}".format(inmsg, endpoint))

    if inmsg == "who":
        outmsg = __name__
        print(">> " + outmsg)
        s.send(stob(outmsg), endpoint[0], endpoint[1])
