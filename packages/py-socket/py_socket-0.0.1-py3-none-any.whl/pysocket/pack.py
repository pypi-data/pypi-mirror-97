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

# Similar to pickle but doesn't execute any code.
# Safe to use.

import struct
import io
from typing import Any, Dict, List, Tuple

ALLOWED_TYPES = (
    bool,
    int,
    float,
    str,
    bytes,
    Tuple,
    List,
    Dict,
)


def pack_num(i):
    packed = struct.pack("f", float(i))
    if len(packed) != 4:
        raise ValueError(f"Float {i} too large to pack as 32 bits.")
    cls = b"\x00" if isinstance(i, int) else b"\x01"
    return cls + packed


def unpack_num(data):
    if isinstance(data, bytes):
        data = io.BytesIO(data)
    cls = data.read(1)
    num = struct.unpack("f", data.read(4))[0]
    if cls == b"\x00":
        num = int(num)
    return num


def dumps(obj: Any):
    """
    Saves obj as a byte string.
    :param obj: Any object in ALLOWED_TYPES.
    """
    if isinstance(obj, bool):
        data = b"\x00"
        data += b"\x01" if obj else b"\x00"
    elif isinstance(obj, int):
        data = b"\x01" + pack_num(obj)
    elif isinstance(obj, float):
        data = b"\x02" + pack_num(obj)
    elif isinstance(obj, str):
        data = b"\x03" + pack_num(len(obj))
        data += obj.encode()
    elif isinstance(obj, bytes):
        data = b"\x04" + pack_num(len(obj))
        data += obj
    elif isinstance(obj, tuple):
        data = b"\x05"
        data += pack_num(len(obj))
        for o in obj:
            data += dumps(o)
    elif isinstance(obj, list):
        data = b"\x06"
        data += pack_num(len(obj))
        for o in obj:
            data += dumps(o)
    elif isinstance(obj, dict):
        data = b"\x07"
        data += pack_num(len(obj))
        for key, o in obj.items():
            data += dumps(key)
            data += dumps(o)
    else:
        raise NotImplementedError(f"Type {type(obj)} not allowed.")

    return data


def loads(data):
    """
    Loads byte string as an object.
    :param data: String of bytes to load.
    """
    if isinstance(data, bytes):
        data = io.BytesIO(data)
    cls = data.read(1)

    if cls == b"\x00":
        obj = True if data.read(1) == b"\x01" else False
    elif cls in (b"\x01", b"\x02"):
        obj = unpack_num(data)
    elif cls == b"\x03":
        length = unpack_num(data)
        obj = data.read(length).decode()
    elif cls == b"\x04":
        length = unpack_num(data)
        obj = data.read(length)
    elif cls in (b"\x05", b"\x06"):
        length = unpack_num(data)
        obj = []
        for _ in range(length):
            obj.append(loads(data))
        if cls == b"\x05":
            obj = tuple(obj)
    elif cls == b"\x07":
        length = unpack_num(data)
        obj = {}
        for _ in range(length):
            key = loads(data)
            o = loads(data)
            obj[key] = o

    return obj
