from pandas import DataFrame

from pypsql_api.wire.actions_types import Names
from pypsql_api.context import Context
from pypsql_api.wire.back import CommandComplete


def process_simple_query(context: Context):
    msg = context.mem.get('message', None)

    if msg.query:
        msg.query = msg.query.replace('OPERATOR(pg_catalog.~)', '=') \
            .replace('~', '=')

        query_handler = context.query_handler

        query = msg.query.lower()

        if query.startswith("set"):
            query_handler.handle_set(session=context.session, sql=msg.query)
            CommandComplete(tag="SET").write(context.output)
            return context, Names.READY_FOR_QUERY
        elif query == 'begin':
            query_handler.handle_begin(session=context.session, sql=msg.query)
            CommandComplete(tag="BEGIN").write(context.output)
            return context, Names.READY_FOR_QUERY
        elif query == 'end':
            query_handler.handle_end(session=context.session, sql=msg.query)
            CommandComplete(tag="END").write(context.output)
            return context, Names.READY_FOR_QUERY
        elif query == 'rollback':
            query_handler.handle_rollback(session=context.session, sql=msg.query)
            CommandComplete(tag="ROLLBACK").write(context.output)
            return context, Names.READY_FOR_QUERY
        else:
            resp, _ = query_handler.handle(session=context.session, sql=msg.query)

            if isinstance(resp, DataFrame):
                return context.update_mem('data', resp), Names.WRITE_DATA_FRAME

            return context, Names.WRITE_EMPTY_RESPONSE
