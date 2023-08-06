import logging
import traceback

import ssl
from io import BytesIO
from typing import Optional

from pypsql_api.config.types import Session
from pypsql_api.wire.actions_types import Names
from pypsql_api.context import Context
from pypsql_api.wire.back import SSLNo, AuthenticationCleartextPassword, ReadyForQuery, AuthenticationOk, \
    EmptyQueryResponse, DataFrameRowDescription, DataFrameDataRows, CommandComplete, SSLYes, ErrorResponse, \
    ParameterStatus
from pypsql_api.wire.bytes import ReadingIO, WritingIO
from pypsql_api.wire.errors.core import log_exception, NoData
from pypsql_api.wire.front import SSLRequest, StartupMessage, Message, PasswordMessage

cipher_list = "ECDH+ECDSA+AESGCM:" \
 \
              "ECDH+ECDSA+AES:" \
              "ECDH+AESGCM:" \
              "ECDH+AES:" \
 \
              "DH+ECDSA+AESGCM:" \
              "DH+ECDSA+AES:" \
              "DH+AESGCM:" \
              "DH+AES:" \
 \
              "RSA+AESGCM:" \
              "RSA+AESCBC:" \
 \
              "!aNULL:!MD5:!DSS:"


def reset(rio: ReadingIO) -> ReadingIO:
    rio.buff.seek(0)
    return rio


def prefix_len(rio: ReadingIO) -> ReadingIO:
    bts = rio.read_bytes()
    wio = WritingIO(BytesIO())
    wio.write_int32(len(bts))
    wio.write_bytes(bts)

    buff = wio.buff
    buff.seek(0)

    return ReadingIO(buff)


def read_ssl_request(context: Context):
    logging.error("read_ssl_requst")
    try:
        # Add support for ancient ssl protocol
        # New protocol SSLReq, SSLAns, StartupMsg
        # Ancient: StartupMsg

        ssl_request = SSLRequest.read(context.input)
        logging.error(f"read ssl request {ssl_request}")

        if ssl_request.request_code == 196608:
            # ancient mode
            logging.error("reading startup message from ancient")
            return read_startup_message(context, inner_buff=prefix_len(reset(ssl_request.inner_buff)))
        else:

            if context.key_file and context.cert_file:
                return context.update_mem('ssl_request', ssl_request), Names.WRITE_SSL_YES
            else:
                return context.update_mem('ssl_request', ssl_request), Names.WRITE_SSL_NO

    except Exception as e:
        log_exception(e)
        logging.error("Error while processing ssl request, downgrading to SSL_NO")
        return context, Names.CLOSE


def write_ssl_resp_no(context: Context):
    SSLNo().write(context.output)

    return context, Names.READ_STARTUP_MESSAGE


def write_ssl_resp_yes(context: Context):
    SSLYes().write(context.output)

    # we need wrap the connection in a SSL connection
    ssl_obj: ssl.SSLSocket = ssl.wrap_socket(sock=context.socket,
                                             do_handshake_on_connect=False,
                                             server_side=True,
                                             certfile=context.cert_file,
                                             keyfile=context.key_file,
                                             ciphers=cipher_list)

    ssl_obj.do_handshake()

    context.mem['ssl_obj'] = ssl_obj

    context.input = ReadingIO(ssl_obj)
    context.output = WritingIO(ssl_obj)

    return context, Names.READ_STARTUP_MESSAGE


def read_startup_message(context: Context, inner_buff: Optional[ReadingIO] = None):
    try:

        if inner_buff is None:
            io = context.input
        else:
            logging.error("Using inner buffer to read the startup message")
            io = inner_buff

        startup_front = StartupMessage.read(io)

        logging.error(f"Got startup message: {startup_front}")

        session = Session(
            user=startup_front.user, database=startup_front.database, password=''
        )

        context.session = session
        return context.update_mem('session', session), Names.WRITE_PLAIN_TEXT_PASSWORD_REQUEST
    except NoData as e:
        log_exception(e)
        return context, Names.CLOSE
    except Exception as e:
        log_exception(e)
        raise


def write_plain_text_password_request(context: Context):
    AuthenticationCleartextPassword().write(context.output)
    context.output.flush()

    return context, Names.READ_PLAIN_TEXT_PASSWORD


def read_plain_text_password_request(context: Context):
    m, t = Message.read(context.input)

    if not (m and t):
        return context, None

    if not isinstance(m, PasswordMessage):
        raise Exception(f"UnExpected message {m}")

    session = context.session
    session.password = m.password
    auth_ok, msg = context.auth_handler.handle(session=session)

    if auth_ok:
        return context, Names.WRITE_AUTH_OK
    else:
        ErrorResponse.severe("Password not correct").write(context.output)
        return context, Names.CLOSE


def write_ready_for_query(context: Context):
    ReadyForQuery().write(context.output)
    context.output.flush()

    return context, Names.RECEIVE_COMMAND


def write_auth_ok(context: Context):
    AuthenticationOk().write(context.output)

    # write out the parameters for the server
    for k,v in context.parameters.items():
        ParameterStatus(name=k, value=v).write(context.output)

    context.output.flush()

    return context, Names.READY_FOR_QUERY


def read_receive_command(context: Context):
    m, t = Message.read(context.input)

    logging.info(f">>read_receive_command msg {m}, {t}")
    if not (m and t):
        return context, None

    return context.update_mem('message', m), m.process_name


def read_receive_extended_command(context: Context):
    m, t = Message.read(context.input)

    logging.info(f">>read_receive_extended_command msg {m}, {t}")
    if m is None and t is None:
        logging.info(f"Not m,t  {m}, {t}")
        return context, None

    if m and m.process_name in {Names.EXECUTE, Names.BIND, Names.SYNC, Names.DESCRIBE}:
        return context.update_mem('message', m), m.process_name

    logging.info(f"Expected an extended protocol query message but got {m}, {t}")
    return context, Names.ERROR


def write_empty_response(context: Context):
    EmptyQueryResponse().write(context.output)

    return context, Names.READY_FOR_QUERY


def write_data_frame_response(context: Context):
    df = context.mem['data']
    if df is None:
        raise Exception("We expect a data frame instance here")

    DataFrameRowDescription(df=df).write(context.output)
    rows = DataFrameDataRows(df=df, offset=0, max_rows=1000000).write(context.output)

    CommandComplete(tag=f"SELECT {rows}").write(context.output)

    context.output.flush()

    return context, Names.READY_FOR_QUERY


def read_parse_command(context: Context):
    m, t = Message.read(context.input)
