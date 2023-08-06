import struct
import io
import time
from typing import Callable, Any, List, Union, Optional, Tuple

from pypsql_api.wire.errors.core import NoData

packer_s1 = struct.Struct('b')
packer_s2be = struct.Struct('>h')
packer_s4be = struct.Struct('>i')
packer_s8be = struct.Struct('>q')

MAX_SIZE = 1024 * 1024 * 1024


def check_max_size(l):
    if l > MAX_SIZE:
        raise Exception(f"The message cannot be larger than {MAX_SIZE} bytes")


class ReadingIO:

    def __init__(self, buff: io.BufferedIOBase):
        self.buff = buff

    def read_bytes(self, n=0) -> bytes:
        data = self.buff.read(n) if n > 0 else self.buff.read()
        if not data:
            raise NoData(n, 0, f"No data. Expected {n} bytes")
        if len(data) < n:
            raise NoData(n, len(data), f"Not enough data. Expected {n} bytes got {len(data)}")

        return data

    def read_byte(self) -> bytes:
        return self.buff.read(1)

    def read_int32(self) -> int:
        data = self.read_bytes(4)
        return packer_s4be.unpack(data)[0]

    def read_int16(self) -> int:
        data = self.read_bytes(2)
        return packer_s2be.unpack(data)[0]

    def read_array_int16_head(self, fn: Callable[[int, Any], Any]) -> List[Any]:
        l = self.read_int16()
        return [fn(i, self) for i in range(l)]

    def read_array_int32_head(self, fn: Callable[[int, Any], Any]) -> List[Any]:
        l = self.read_int32()
        return [fn(i, self) for i in range(l)]

    def read_cstring(self, encoding='UTF-8'):
        s = io.BytesIO()
        b = self.read_byte()

        while b != b'\x00' and b != b'':
            s.write(b)

            b = self.read_byte()

        return s.getvalue().decode(encoding)

    def read_int32_delim_message(self, timeout=5) -> Tuple[Optional[Any], int]:
        """
        Reads the len = int32,
        then a bytes message of message_len = len - 4
        :return: a ReadingIO object or None
        """
        l = self.read_int32()
        msg_len = l - 4

        if msg_len <= 0:
            return None, 0

        check_max_size(msg_len)

        msg = self.read_bytes(msg_len)
        return ReadingIO(io.BytesIO(msg)), msg_len


class WritingIO:

    def __init__(self, buff: io.BufferedIOBase):
        self.buff = buff

    def write_bytes(self, bts: Union[bytes, bytearray]):
        # BufferedIOBase will throw an exception if the bts cannot be written
        self.buff.write(bts)

    def write_byte(self, b: int):
        # BufferedIOBase will throw an exception if the bts cannot be written
        self.write_bytes(packer_s1.pack(b)[0:1])

    def write_int32(self, i: int):
        self.write_bytes(packer_s4be.pack(i))

    def write_int64(self, i: int):
        self.write_bytes(packer_s8be.pack(i))

    def write_int16(self, i: int):
        self.write_bytes(packer_s2be.pack(i))

    def write_array_int16_head(self, n: int, fn: Callable[[int, Any], Any]) -> List[Any]:
        self.write_int16(n)
        if n > 0:
            for i in range(n):
                fn(i, self)

    def write_array_int32_head(self, n: int, fn: Callable[[int, Any], Any]) -> List[Any]:
        self.write_int32(n)
        if n > 0:
            for i in range(n):
                fn(i, self)

    def write_cstring(self, v: str, encoding='UTF-8'):
        if v:
            self.write_bytes(
                v.encode(encoding)
            )
        self.write_bytes(b'\x00')

    def flush(self):
        if hasattr(self.buff, 'flush'):
            self.buff.flush()

    def close(self):
        self.buff.close()
