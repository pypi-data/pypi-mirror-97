import threading

from easyshare.consts.net import ADDR_ANY
from easyshare.logging import init_logging
from easyshare.sockets import SocketTcpAcceptor, SocketTcpIn
from easyshare.utils.types import btos, stob, btoi

init_logging(5)

s = SocketTcpAcceptor(ADDR_ANY, 5555)

def talk(sock: SocketTcpIn):
    print("Connection received from", sock.remote_endpoint())
    print("Server sock: ", sock.endpoint())
    while True:
        print("...")
        header = sock.recv(2)

        if not header:
            print(f"Connection closed ({sock.endpoint()})")
            break

        payload_size = btoi(header)
        print(f"... next payload size = {payload_size}")

        payload = sock.recv(payload_size)

        print(f"received payload size = {len(payload)}")

        msg = btos(payload)
        print("<< " + msg)

while True:
    print("Waiting connections....")
    while True:

        ns = s.accept()
        threading.Thread(target=talk, args=(ns, ), daemon=True).start()
