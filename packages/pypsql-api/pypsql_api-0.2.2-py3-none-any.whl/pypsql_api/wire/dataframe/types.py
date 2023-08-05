from dataclasses import dataclass
from typing import Callable, Any

import numpy as np
import pandas

from pypsql_api.wire.bytes import WritingIO


@dataclass
class DataType:
    oid: str
    typlen: int

    typsend: Callable[[WritingIO, Any], bytes]


def send_as_str(v: Any, encoding='UTF-8') -> bytes:
    return str(v).encode(encoding)


def boolsend(v: Any, encoding="UTF-8") -> bytes:
    return b't' if v else b'f'


def date_out(v, encoding="UTF-8") -> bytes:
    return v.isoformat().encode(encoding)


INT_MAP = {

    np.char: DataType(oid='25', typlen=1, typsend=send_as_str),
    np.int8: DataType(oid='25', typlen=1, typsend=send_as_str),

    np.int16: DataType(oid='21', typlen=2, typsend=send_as_str),

    np.int32: DataType(oid='23', typlen=4, typsend=send_as_str),

    np.int64: DataType(oid='20', typlen=8, typsend=send_as_str),

}

TYPE_MAP = {
    np.bool: DataType(oid='16', typlen=1, typsend=boolsend),
    np.bool_: DataType(oid='16', typlen=1, typsend=boolsend),

    # char

    np.char: INT_MAP[np.char],

    np.int8: INT_MAP[np.int8],
    np.int16: INT_MAP[np.int16],

    np.int32: INT_MAP[np.int32],

    np.int: INT_MAP[np.int64],
    np.int64: INT_MAP[np.int64],

    np.uint8: INT_MAP[np.int8],
    np.uint16: INT_MAP[np.int16],
    np.uint: INT_MAP[np.int64],

    np.uint32: INT_MAP[np.int32],
    np.uint64: INT_MAP[np.int64],

    np.ubyte: INT_MAP[np.char],
    np.byte: INT_MAP[np.char],

    np.float16: DataType(oid='700', typlen=4, typsend=send_as_str),

    np.float32: DataType(oid='700', typlen=4, typsend=send_as_str),

    np.float64: DataType(oid='701', typlen=8, typsend=send_as_str),

    np.float128: DataType(oid='1700', typlen=-1, typsend=send_as_str),

    # str
    np.object: DataType(oid='25', typlen=-1, typsend=send_as_str),
    np.object_: DataType(oid='25', typlen=-1, typsend=send_as_str),

    np.datetime64: DataType(oid='1114', typlen=8, typsend=send_as_str),

    pandas._libs.tslibs.timestamps.Timestamp: DataType(oid='25', typlen=-1, typsend=send_as_str)
}
