import logging
import sys

from satella.os import hang_until_sig

from modbus_tcp_server.network import ModbusTCPServer


def run():
    """Entry point for the MODBUS TCP server"""
    if len(sys.argv) < 2 or '-h' in sys.argv or '--help' in sys.argv or 'help' in sys.argv:
        print('''Usage:
        
modbus-tcp-server <name of interface to bind to> <optional port to bind to>

    Extra allowed arguments (after the name of interface and optional port)
        -v : display inbound traffic
        -vv : display inbound and outbound traffic

    0.0.0.0 will bind to all interfaces
    127.0.0.1 will bind to localhost only, which means that modbus-tcp-server will be
    reachable only from this machine
    
    Default port is 502
''')
        sys.exit(0)

    if len(sys.argv) < 3:
        port = 502
    else:
        port = int(sys.argv[2])

    host = sys.argv[1]

    l_level = logging.WARNING
    if '-vv' in sys.argv:
        l_level = logging.DEBUG
    elif '-v' in sys.argv:
        l_level = logging.INFO

    logging.basicConfig(level=l_level)

    at = ModbusTCPServer(host, port).start()
    hang_until_sig()
    at.terminate().join()
    sys.exit(0)
