from dataclasses import dataclass
from typing import Dict, Any, Optional

from pypsql_api.config.types import Session
from pypsql_api.ext.handlers import AuthHandler, QueryHandler, ExtendedQueryHandler
from pypsql_api.wire.bytes import ReadingIO, WritingIO
from pypsql_api.wire.extended.types import PreparedStatement, Portal


@dataclass
class Context:
    input: ReadingIO
    output: WritingIO

    session: Session

    auth_handler: AuthHandler
    query_handler: QueryHandler
    extended_query_handler: ExtendedQueryHandler

    mem: Dict[str, Any]  # keep memory between tasks

    # The extended query protocol
    prepared_statements: Dict[str, PreparedStatement]
    portals: Dict[str, Portal]

    key_file: Optional[str]
    cert_file: Optional[str]

    socket: Optional[Any]

    def update_mem(self, k, v):
        return Context(input=self.input, output=self.output,
                       session=self.session,
                       auth_handler=self.auth_handler,
                       query_handler=self.query_handler,
                       extended_query_handler=self.extended_query_handler,
                       mem={**self.mem, **{k: v}},
                       prepared_statements=self.prepared_statements,
                       portals=self.portals,
                       key_file=self.key_file,
                       cert_file=self.cert_file,
                       socket=self.socket)
