import io
import logging
from dataclasses import dataclass
from typing import Any, List

from numpy import dtype
from pandas import DataFrame

from pypsql_api.wire.bytes import WritingIO
from pypsql_api.wire.dataframe.types import TYPE_MAP, DataType


@dataclass
class ParameterStatus:
    name: str
    value: str

    def write(self, buff: WritingIO):
        buff.write_byte(ord('S'))
        internal_buff = WritingIO(io.BytesIO())

        internal_buff.write_cstring(self.name)
        internal_buff.write_cstring(self.value)

        bytes = internal_buff.buff.getvalue()

        buff.write_int32(len(bytes) + 4)
        buff.write_bytes(bytes)


@dataclass
class ErrorField:
    type: int  # one of https://www.postgresql.org/docs/current/protocol-error-fields.html
    value: Any


@dataclass
class ErrorResponse:
    fields: List[ErrorField]

    def write(self, buff: WritingIO):
        buff.write_byte(ord('E'))
        internal_buff = WritingIO(io.BytesIO())
        for field in self.fields:
            internal_buff.write_byte(field.type)
            internal_buff.write_cstring(field.value)

        bytes = internal_buff.buff.getvalue()

        buff.write_int32(len(bytes) + 5)
        buff.write_bytes(bytes)

        buff.write_byte(0)

    @staticmethod
    def severe(msg: str):
        """
        Creates a simple string error response
        """
        return ErrorResponse(fields=[ErrorField(type=ord('M'), value=msg)])

    @staticmethod
    def query(msg: str):
        """
        Creates a simple string error response
        """
        return ErrorResponse(fields=[ErrorField(type=ord('W'), value=msg)])


@dataclass
class ReadyForQuery:
    transaction_indicator: int = ord('I')

    def write(self, buff: WritingIO):
        buff.write_byte(ord('Z'))
        buff.write_int32(5)
        buff.write_byte(self.transaction_indicator)


class ParseComplete:

    def write(self, buff: WritingIO):
        buff.write_byte(ord('1'))
        buff.write_int32(4)


class BindComplete:

    def write(self, buff: WritingIO):
        buff.write_byte(ord('2'))
        buff.write_int32(4)


class PortalSuspended:

    def write(self, buff: WritingIO):
        buff.write_byte(ord('s'))
        buff.write_int32(4)


class AuthenticationOk:

    def write(self, buff: WritingIO):
        buff.write_byte(ord('R'))
        buff.write_int32(8)
        buff.write_int32(0)


class AuthenticationCleartextPassword:

    def write(self, buff: WritingIO):
        buff.write_byte(ord('R'))
        buff.write_int32(8)
        buff.write_int32(3)


class SSLYes:
    def write(self, buff: WritingIO):
        buff.write_byte(ord('S'))


class SSLNo:
    def write(self, buff: WritingIO):
        buff.write_byte(ord('N'))


class EmptyQueryResponse:

    def write(self, buff: WritingIO):
        buff.write_byte(ord('I'))
        buff.write_int32(4)


@dataclass
class CommandComplete:
    tag: str

    def write(self, buff: WritingIO):
        buff.write_byte(ord('C'))
        internal_buff = WritingIO(io.BytesIO())
        internal_buff.write_cstring(self.tag)

        bytes = internal_buff.buff.getvalue()

        buff.write_int32(len(bytes) + 4)  # Length of message contents in bytes, including self.
        buff.write_bytes(bytes)
        logging.info("writing COMMAND COMPLETE")
        logging.info(self.tag)


def is_nan(x):
    return x != x


@dataclass
class DataFrameDataRows:
    df: DataFrame
    offset: int
    max_rows: int

    def write_cell(self, buff: WritingIO, row_i: int, col_name, type_map: DataType, df: DataFrame):
        """
        Write out a single column cell value
        """
        v = df.iloc[row_i][col_name]

        if v is None or is_nan(v):
            buff.write_int32(-1)
        else:
            bts = type_map.typsend(v)

            buff.write_int32(len(bts))  # type length in bytes
            buff.write_bytes(bts)

    def write(self, buff: WritingIO):

        df = self.df

        columns = dict(df.dtypes)
        column_names = list(columns.keys())
        row_count = len(df.index)

        column_types = [TYPE_MAP[dt.type] for _, dt in columns.items()]

        offset = self.offset
        if offset < row_count:
            for row_i in range(row_count):
                # for each row
                # write a DataRow
                buff.write_byte(ord('D'))  # Identifies the message as a data row.

                internal_buff = WritingIO(io.BytesIO())
                internal_buff.write_int16(len(column_types))

                for i, type_map in enumerate(column_types):
                    self.write_cell(internal_buff, row_i + offset, column_names[i], type_map, df)

                data_row_bts = internal_buff.buff.getvalue()

                buff.write_int32(len(data_row_bts) + 4)  # Length of message contents in bytes, including self.
                buff.write_bytes(data_row_bts)

            logging.info(f"done writing datarows {row_count}")
            return row_count

        return 0


@dataclass
class DataFrameRowDescription:
    df: DataFrame

    def write_field_desc(self, buff: WritingIO, n: Any, dt: dtype):
        # see https://github.com/postgres/postgres/blob/master/src/include/catalog/pg_type.dat
        logging.info(f"write field {n} = [{dt}, {dt.type}]")

        type_map: DataType = TYPE_MAP[dt.type]

        buff.write_int32(
            0)  # If the field can be identified as a column of a specific table, the object ID of the table; otherwise zero.
        buff.write_int16(
            0)  # If the field can be identified as a column of a specific table, the attribute number of the column; otherwise zero.
        buff.write_int32(int(type_map.oid))  # The object ID of the field's data type.

        buff.write_int16(int(type_map.typlen))  # The data type size (see pg_type.typlen)
        buff.write_int32(-1)  # The type modifier
        # zero is text format for all
        buff.write_int16(0)  # keep always as text, only binary for FETCH commands

    def write(self, buff: WritingIO):
        buff.write_byte(ord('T'))  # Identifies the message as a row description.

        internal_buff = WritingIO(io.BytesIO())

        df = self.df

        columns = dict(df.dtypes)

        internal_buff.write_int16(len(columns))  # Specifies the number of fields in a row (can be zero)

        for n, dt in columns.items():
            internal_buff.write_cstring(n)  # The field name.
            self.write_field_desc(internal_buff, n, dt)

        bytes = internal_buff.buff.getvalue()

        buff.write_int32(len(bytes) + 4)  # Length of message contents in bytes, including self.
        buff.write_bytes(bytes)
