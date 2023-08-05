import io
import logging
from dataclasses import dataclass
from typing import Any, Optional, Tuple, List

from pypsql_api.wire.actions_types import Names
from pypsql_api.wire.bytes import ReadingIO


def parse_portal_name(portal_name: str) -> str:
    if not portal_name:
        return "UNNAMED"

    return portal_name.lower().strip()


@dataclass
class SSLRequest:
    request_code: int
    inner_buff: Optional[ReadingIO]

    @staticmethod
    def read(buff: ReadingIO):
        inner_buff, message_len = buff.read_int32_delim_message()
        return SSLRequest(request_code=inner_buff.read_int32(), inner_buff=inner_buff)


@dataclass
class StartupMessage:
    protocol_version: int
    user: str
    database: str
    options: str

    @staticmethod
    def read(buff: ReadingIO):
        logging.error(f"Reading startup message using {buff}")

        inner_buff, message_len = buff.read_int32_delim_message()

        if not inner_buff:
            raise Exception("Invalid startup message, the length must be > 4 bytes")

        protocol_version = inner_buff.read_int32()
        message_len -= 4
        d = {}

        if message_len > 0:
            while True:
                n = inner_buff.read_cstring()
                if not n:
                    break
                v = inner_buff.read_cstring()
                if not v:
                    break

                d[n] = v

        return StartupMessage(
            protocol_version=protocol_version, user=d.get('user', ''), database=d.get('database', ''),
            options=d.get('options', '')
        )


@dataclass
class PasswordMessage:
    password: str

    @staticmethod
    def read_body(buff: ReadingIO):
        return PasswordMessage(password=buff.read_cstring())


@dataclass
class QueryMessage:
    query: str

    process_name: Any = Names.SIMPLE_QUERY

    @staticmethod
    def read_body(buff: ReadingIO):
        return QueryMessage(query=buff.read_cstring())


@dataclass
class BindMessage:
    portal_name: str
    prepared_statement_name: str

    # If empty the default text parameter format code is applied
    # The parameter format codes. Each must presently be zero (text) or one (binary).
    format_codes: List[int]

    parameter_values: List[Optional[bytes]]

    # The result-column format codes. Each must presently be zero (text) or one (binary).
    result_format_codes: List[int]

    process_name: Any = Names.BIND

    @staticmethod
    def read_body(buff: ReadingIO):
        portal_name = parse_portal_name(buff.read_cstring())

        prepared_statement_name = parse_portal_name(buff.read_cstring())

        # read the parameter format codes
        number_of_format_codes = buff.read_int16()
        format_codes = [buff.read_int16() for _ in range(number_of_format_codes)]

        # read the parameter values
        number_of_params = buff.read_int16()
        parameter_values = []
        for _ in range(number_of_params):
            param_len = buff.read_int32()
            if param_len == 0 or param_len == -1:
                parameter_values.append(None)
            else:
                parameter_values.append(buff.read_bytes(param_len))

        number_of_result_format_codes = buff.read_int16()
        result_format_codes = [buff.read_int16() for _ in range(number_of_result_format_codes)]

        return BindMessage(
            portal_name=portal_name,
            prepared_statement_name=prepared_statement_name,
            format_codes=format_codes,
            parameter_values=parameter_values,
            result_format_codes=result_format_codes
        )


@dataclass
class ParseMessage:
    name: str
    query: str

    # zero is unspecified
    oid_types: List[int]

    process_name: Any = Names.PARSE

    @staticmethod
    def read_body(buff: ReadingIO):
        assert isinstance(buff, ReadingIO), f"got {buff}"
        name = parse_portal_name(buff.read_cstring())

        query = buff.read_cstring()

        parameter_data_types_len = buff.read_int16()

        oid_types = [buff.read_int32() for _ in range(parameter_data_types_len)]

        logging.info(f"Parse : name {name}, {query}, {oid_types}")

        return ParseMessage(
            name=name,
            query=query,
            oid_types=oid_types
        )


@dataclass
class ExecuteMessage:
    portal_name: str
    max_rows: int

    process_name: Any = Names.EXECUTE

    def unlimited(self):
        return self.max_rows == 0

    @staticmethod
    def read_body(buff: ReadingIO):
        return ExecuteMessage(portal_name=parse_portal_name(buff.read_cstring()),
                              max_rows=buff.read_int32())


@dataclass
class Terminate:
    process_name: Any = Names.CLOSE

    @staticmethod
    def read_body(_: ReadingIO):
        return Terminate()


@dataclass
class Flush:
    process_name: Any = Names.FLUSH

    @staticmethod
    def read_body(_: ReadingIO):
        return Flush()


@dataclass
class Sync:
    process_name: Any = Names.SYNC

    @staticmethod
    def read_body(_: ReadingIO):
        return Sync()


@dataclass
class Describe:
    t: str  # 'S == describe prepared statement, P == describe portal
    name: str

    process_name: Any = Names.DESCRIBE

    @staticmethod
    def read_body(buff: ReadingIO):
        t = buff.read_byte()
        name = buff.read_cstring()
        if not name:
            name = 'UNNAMED'

        return Describe(t=t, name=name)


message_type_map = {
    ord('p'): PasswordMessage.read_body,
    ord('Q'): QueryMessage.read_body,
    ord('X'): Terminate.read_body,
    ord('P'): ParseMessage.read_body,
    ord('B'): BindMessage.read_body,
    ord('E'): ExecuteMessage.read_body,
    ord('H'): Flush.read_body,
    ord('S'): Sync.read_body,
    ord('D'): Describe.read_body,
}


class Message:

    @staticmethod
    def read(buff: ReadingIO) -> Tuple[Optional[Any], Optional[bytes]]:
        """
        Returns [Optional[Message], type:bytes
        If The message and Type are None, we've reached the end of stream
        """

        t = buff.read_byte()

        if not t:
            return None, None

        fn = message_type_map.get(ord(t), None)
        logging.info(f"Read message type {t} using fn {fn}")
        if fn:
            try:
                inner_buff, _ = buff.read_int32_delim_message()
                return fn(inner_buff), t
            except Exception as e:
                logging.error(e)
                return fn(ReadingIO(io.BytesIO())), t

        return None, t
