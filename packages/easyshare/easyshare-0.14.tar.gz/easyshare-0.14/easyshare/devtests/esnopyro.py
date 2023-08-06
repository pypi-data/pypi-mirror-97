from easyshare.es.connections.connection import ConnectionMinimal
from easyshare.logging import init_logging
from easyshare.protocol.requests import create_request
from easyshare.utils.json import jtob
from easyshare.utils.net import get_primary_ip

init_logging(5)

endpoint = (get_primary_ip(), 12022)

print(f"Connecting to...{endpoint}")
conn = ConnectionMinimal(endpoint[0], endpoint[1], False)
print(f"Connection created - established = {conn.is_connected_to_server()}")


while True:
    cmd = input(">> ")
    parts = cmd.split(" ")
    api = parts[0]
    params = {p.split(":")[0]: p.split(":")[1] for p in parts[1:]} if len(parts) > 1 else None

    # Send
    req = create_request(parts[0], params)
    req_b = jtob(req)
    print(f">> {repr(req_b)}")
    conn.write(req_b)

    # Recv
    resp = conn.read()
    print(f"<< {repr(resp)}")