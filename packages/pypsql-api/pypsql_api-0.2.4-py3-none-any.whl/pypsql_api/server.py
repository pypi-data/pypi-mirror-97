# see: https://docs.python.org/3/library/socketserver.html
import logging
import socket
import socketserver
import traceback
from abc import abstractmethod, ABC
from decimal import Decimal
from typing import Tuple, Optional, Union, Any, Dict

from pandas import DataFrame

from pypsql_api.config.types import Session
from pypsql_api.ext.handlers import AuthHandler, QueryHandler, ExtendedQueryHandler
from pypsql_api.wire.actions_types import Names
from pypsql_api.context import Context
from pypsql_api.wire.back import ErrorResponse
from pypsql_api.wire.bytes import ReadingIO, WritingIO
from pypsql_api.wire.errors.core import log_exception
from pypsql_api.wire.extended.types import Portal, PreparedStatement, Param
from pypsql_api.wire.front import BindMessage, ParseMessage
from pypsql_api.wire.protocol import run_states


def state_runner(existing_state, message_processor):
    state = message_processor.next(existing_state)
    message_processor.is_allowed(state)

    return state


class PsqlHandler(ABC, socketserver.StreamRequestHandler, socketserver.ThreadingMixIn):

    @property
    @abstractmethod
    def parameters(self) -> Dict[str, str]:
        raise Exception("Not implemented")

    @property
    @abstractmethod
    def auth_handler_cls(self):
        raise Exception("Not implemented")

    @property
    @abstractmethod
    def socket_timeout(self):
        raise Exception("Not implemented")

    @property
    @abstractmethod
    def query_handler_cls(self):
        raise Exception("Not implemented")

    @abstractmethod
    def init_ssl(self, context: Context):
        raise Exception("Not implemented")

    def handle(self):

        logging.info(f"First Connect")
        logging.info(f"First connect")

        # timeout causes the socket to become non blockgin
        # self.request.settimeout(self.socket_timeout())

        input = ReadingIO(self.rfile)
        output = WritingIO(self.wfile)

        try:
            context = Context(
                input=input,
                output=output,
                mem={},

                auth_handler=self.auth_handler_cls(),
                query_handler=self.query_handler_cls(),
                extended_query_handler=self.extended_query_handler_cls(),
                session=None,
                portals={},
                prepared_statements={},
                key_file=None,
                cert_file=None,
                socket=self.connection,
                parameters=self.parameters
            )

            self.init_ssl(context=context)

            state_name = Names.READ_SSL_REQUEST

            context, state_name = run_states(context, state_name)

        except socket.timeout as  e:
            log_exception(e)
        except Exception as e:
            log_exception(e)
            try:
                ErrorResponse.severe(str(e)).write(output)
            except Exception as e2:
                log_exception(e2)
        finally:
            ssl_obj = context.mem.get('ssl_obj', None)
            if ssl_obj is None:
                output.close()
            else:
                ssl_obj.close()

        logging.info("End")


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


default_parameters = {
    'client_encoding': 'UTF8',
    'application_name': 'psql',
    'server_encidong': 'UTF8',
    'TimeZone': 'UTC',
    'DateSTyle': 'ISO',
    'statement_timeout': '120000',
    'default_tablespace': 'public',
    'default_transaction_isolation': 'read committed'
}


def run(auth_handler_cls, query_handler_cls, extended_query_handler_cls, handler=None, host="", port=55432,
        cert_file=None, key_file=None, socket_timeout=240, parameters=default_parameters):
    auth_1 = auth_handler_cls
    query_1 = query_handler_cls
    query_2 = extended_query_handler_cls
    socket_timeout_1 = socket_timeout
    parameters_1 = parameters

    if not handler:
        class Handler(PsqlHandler):
            auth_handler_cls = auth_1
            query_handler_cls = query_1
            extended_query_handler_cls = query_2
            socket_timeout = socket_timeout_1

            parameters = parameters_1

            def init_ssl(self, context: Context):
                context.key_file = key_file
                context.cert_file = cert_file

        handler = Handler

    with ThreadedTCPServer((host, port), handler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        logging.info(f"Running postgresql server on {host}:{port}")
        server.serve_forever()


def main():
    class TestAuth(AuthHandler):

        def handle(self, session: Session) -> Tuple[bool, Optional[str]]:
            if session.password == "test":
                return True, None

            return False, None

    class TestQueryHandler(QueryHandler):



        def handle_begin(self, session: Session, sql):
            pass

        def handle_end(self, session: Session, sql):
            pass

        def handle_set(self, session: Session, sql):
            pass

        def handle(self, session: Session, sql) -> Tuple[Optional[Union[Any, Optional[DataFrame]]], Optional[Any]]:
            import pandas as pd
            import numpy as np
            from decimal import Decimal
            logging.info(f"Handling query {sql}")
            return pd.DataFrame({'id': [1.232323, 2.1233, np.nan], 'name': [1, 2, 3],
                                 'p': [Decimal(1212323213123), Decimal(121312312321321323121321312321312323213),
                                       Decimal(123123213213213213213)]}), None

    import pandas as pd
    import numpy as np
    data_frame = pd.DataFrame({'id': [1.232323, 2.1233, np.nan], 'name': [1, 2, 3],
                               'p': [Decimal(1212323213123), Decimal(121312312321321323121321312321312323213),
                                     Decimal(123123213213213213213)]})

    class TestExtendedQueryHandler(ExtendedQueryHandler):

        def parse(self, session: Session, msg: ParseMessage) -> Tuple[
            Optional[Union[Any, Optional[PreparedStatement]]], Optional[Any]]:
            return PreparedStatement(
                name="test",
                sql=msg.query,
                parameters=[Param(oid_type=1, index=0, type=None), Param(oid_type=1, index=1, type=None)]
            ), None

        def bind(self, session: Session, prepared_statement: PreparedStatement, bind: BindMessage) -> Tuple[
            Optional[Union[Any, Optional[Portal]]], Optional[Any]]:
            return Portal(
                name=bind.portal_name,
                prepared_statement=prepared_statement,
                execution=None,
                row_description=data_frame,
            ), None

        def execute(self, session: Session, portal: Portal, max_rows: int) -> Tuple[
            Optional[Union[Any, Optional[DataFrame]]], Optional[Any]]:
            return data_frame, None

    FORMAT = '%(levelname)s: %(asctime)-15s: %(filename)s: %(funcName)s: %(module)s: %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT)

    run(auth_handler_cls=TestAuth, query_handler_cls=TestQueryHandler,
        extended_query_handler_cls=TestExtendedQueryHandler)


if __name__ == "__main__":
    main()
