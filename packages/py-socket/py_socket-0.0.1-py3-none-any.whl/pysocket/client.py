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

import socket
from typing import Tuple, Callable
from cryptography.fernet import Fernet
from .pack import loads, dumps


class Client:
    """
    A class which can be used by the client to communicate to the server.
    """

    ip: str
    port: int
    conn: socket.socket
    cipher_key: bytes
    cipher: Fernet

    verbose: bool
    active: bool

    header: int
    padding: str
    packet_size: int

    def __init__(self, ip: str, port: int, cipher_key: bytes):
        self.ip = ip
        self.port = port
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((ip, port))

        self.cipher_key = cipher_key
        self.cipher = Fernet(self.cipher_key)

        self.header = 64
        self.padding = " " * self.header
        self.packet_size = 8192

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
