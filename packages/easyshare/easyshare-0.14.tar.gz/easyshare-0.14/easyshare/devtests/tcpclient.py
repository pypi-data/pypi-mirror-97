import time

from easyshare.logging import init_logging
from easyshare.sockets import SocketTcpOut
from easyshare.utils.net import get_primary_ip
from easyshare.utils.rand import randstring
from easyshare.utils.types import stob, itob


init_logging(5)

s = SocketTcpOut(get_primary_ip(), 5555)
print("Connected")

while True:
    msg = input(">> ")

    payload = stob(msg)

    payload_1st_half = stob(msg[0:len(msg) // 2])
    payload_2st_half = stob(msg[len(msg) // 2:])

    data = bytearray()
    data += itob(len(payload), 2)
    data += payload_1st_half

    s.send(data)
    print("... sent header + 1 half payload")

    time.sleep(0.14)

    data = bytearray()
    data += payload_2st_half
    data += stob(randstring(4))    # eve
    s.send(data)
    print("... sent 2 half payload")