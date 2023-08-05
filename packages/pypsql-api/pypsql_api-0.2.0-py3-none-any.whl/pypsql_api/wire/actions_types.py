import enum


class Names(enum.Enum):
    ERROR = 0
    READ_SSL_REQUEST = 1
    WRITE_SSL_YES = 2
    WRITE_SSL_NO = 3

    WRITE_PLAIN_TEXT_PASSWORD_REQUEST = 4
    READ_PLAIN_TEXT_PASSWORD = 5

    READ_STARTUP_MESSAGE = 6

    CLOSE = 7

    READY_FOR_QUERY = 8
    WRITE_AUTH_OK = 9
    RECEIVE_COMMAND = 10  # after ready for query we wait for the next command
    SIMPLE_QUERY = 11

    WRITE_EMPTY_RESPONSE = 12
    WRITE_DATA_FRAME = 13

    PARSE = 14
    BIND = 15
    EXECUTE = 16
    SYNC = 17
    FLUSH = 18
    RECEIVE_EXTENDED_QUERY_COMMAND = 19  # after ready for query we wait for the next command
    WRITE_EXTENDED_EMPTY_RESPONSE = 20
    WRITE_EXTENDED_DATA_FRAME = 21

    DESCRIBE = 22