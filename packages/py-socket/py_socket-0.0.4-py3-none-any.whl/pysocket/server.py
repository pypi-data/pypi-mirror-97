#
#  Pysocket Template
#  Template classes for Python socket applications.
#  Copyright Patrick Huang 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import threading
import socket
import ctypes
from typing import Any, Callable, List, Tuple
from cryptography.fernet import Fernet
from bcon import loads, dumps


class Client:
    """
    An instance of this is created every time a client connects.
    Meant for communication with that client only.
    Also meant to be used by the Server class only.
    """

    conn: socket.socket
    addr: Tuple
    start_func: Callable
    cipher: Fernet

    verbose: bool
    active: bool

    header: int
    padding: str
    packet_size: int

    def __init__(self, conn: socket.socket, addr: Tuple, start_func: Callable, verbose: bool, cipher: Fernet):
        self.conn = conn
        self.addr = addr
        self.start_func = start_func
        self.cipher = cipher

        self.verbose = verbose
        self.active = True

        self.header = 64
        self.padding = " " * self.header
        self.packet_size = 8192

    def alert(self, msg):
        print(f"[{self.addr}] {msg}")

    def start(self, *args):
        self.start_func(self, *args)

    def quit(self):
        if self.active:
            self.conn.close()
            self.active = False

    def send(self, obj):
        data = self.cipher.encrypt(dumps(obj))
        len_msg = (str(len(data)) + self.padding)[:self.header].encode()

        packets = []
        while data:
            curr_len = min(len(data), self.packet_size)
            packets.append(data[:curr_len])
            data = data[curr_len:]

        self.conn.send(len_msg)
        for packet in packets:
            self.conn.send(packet)

    def recv(self):
        len_msg = b""
        while len(len_msg) < self.header:
            len_msg += self.conn.recv(self.header-len(len_msg))

        length = int(len_msg)
        data = b""
        while len(data) < length:
            curr_len = min(self.packet_size, length-len(data))
            data += self.conn.recv(curr_len)

        return loads(self.cipher.decrypt(data))


class Server:
    """
    Server class.
    Handles client accepting.
    """

    ip: str
    port: int
    client_start: Callable
    cipher_key: bytes
    cipher: Fernet

    verbose: bool
    args: Tuple[Any]
    active: bool
    clients: List[Client]

    server: socket.socket

    def __init__(self, ip: str, port: int, client_start: Callable, cipher_key: bytes, verbose: bool = True, args: Tuple = ()):
        """
        Initializes server.
        :param ip: IP address to bind to.
        :param port: Port to bind to.
        :param client_start: Start function of clients.
        :param cipher_key: Key used to encrypt messages. Auto-generated if set to None.
        :param verbose: Whether to print information to the console.
        :param args: Arguments to pass to Client start.
        """
        self.ip = ip
        self.port = port
        self.client_start = client_start
        self.cipher_key = cipher_key
        self.cipher = Fernet(self.cipher_key)

        self.verbose = verbose
        self.args = args
        self.active = True
        self.clients = []

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))

    def start(self):
        self.server.listen()
        if self.verbose:
            print(f"[SERVER] Started. IP={self.ip}, PORT={self.port}")

        while self.active:
            try:
                conn, addr = self.server.accept()
            except KeyboardInterrupt:
                self.quit(True)
                return
            client = Client(conn, addr, self.client_start, self.verbose, self.cipher)
            self.clients.append(client)
            threading.Thread(target=client.start, args=self.args).start()

    def quit(self, force: bool = False):
        """
        Quits the server and all connected clients.
        :param force: Whether to force quit Python.
        """
        self.active = False
        self.server.close()
        for c in self.clients:
            c.quit()

        if force:
            ctypes.pointer(ctypes.c_char.from_address(5))[0]
