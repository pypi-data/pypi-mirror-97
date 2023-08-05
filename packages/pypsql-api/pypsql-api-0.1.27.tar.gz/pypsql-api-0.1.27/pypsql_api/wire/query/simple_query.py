from pandas import DataFrame

from pypsql_api.wire.actions_types import Names
from pypsql_api.context import Context


def process_simple_query(context: Context):
    msg = context.mem.get('message', None)

    if msg.query:
        msg.query = msg.query.replace('OPERATOR(pg_catalog.~)', '=') \
            .replace('~', '=')

        query_handler = context.query_handler
        resp, _ = query_handler.handle(session=context.session, sql=msg.query)

        if isinstance(resp, DataFrame):
            return context.update_mem('data', resp), Names.WRITE_DATA_FRAME

    return context, Names.WRITE_EMPTY_RESPONSE
