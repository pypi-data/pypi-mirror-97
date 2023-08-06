"""

Portal

Param:
  oid_type
  index
  type
  is_void?

PreparedStatement
  parameters

Session:
 parepared-statements = {
   'UNNAMED': ...
   'Name': ...
   }

 portals = {
  'UNNAMED': ...
  'Name': ...
 }

Named prepared statements can also be created and accessed at the SQL command level, using PREPARE and EXECUTE.

Destroy any unamed prepared statements

F -> Parse
       query-string
       name optional
        data type
        parameter placeholders

      parameter types acn be 0 or
      shorter than the $1 placeholders

      Note we need to see type void id and ignore

B -> ParseComplete
      create prepared statement
   or ErrorResponse


 DECLARE CURSOR and FETCH

F --> Bind (destroy unnamed portal if any)
     name ==> must exist in the session
     return format
     len(prepared_statement.params) must eq len(bind.params)

     void params must have Null

B --> BindComplete
        create portal

    or ErrorResopnse

F --> Execute
     name ==> portal must exist in the session
     result row count, or zero for all

     No rowdescription, only RowData

     If more rows than result row count
     return PortalSuspend
     and save the result and index to the Portal
     a next execute command should carry on from where
     the portal left off

     CommandComplete on completion
     allowed values:
      CommandComplete, EmptyQueryRespones,
      ErrorResponse, PortalSuspended

F --> Sync
     Reads and closes all portals

Note on any back error
   Do:
     Send ErrorResponse and read till Sync found
     then send ReadyForQuery
"""
import logging
import traceback

from pandas import DataFrame

from pypsql_api.wire.actions_types import Names
from pypsql_api.context import Context
from pypsql_api.wire.back import ParseComplete, BindComplete, ErrorResponse, EmptyQueryResponse, DataFrameDataRows, \
    PortalSuspended, CommandComplete, DataFrameRowDescription
from pypsql_api.wire.errors.core import log_exception
from pypsql_api.wire.extended.types import PreparedStatement, Portal, Execution
from pypsql_api.wire.front import ParseMessage, BindMessage, ExecuteMessage, Sync, Message, Describe


def process_parse_command(context: Context):
    """
     Process the query
     then write  ParseComplete, and  send to bind
     Expects a query_parser
    :param context:
    :return:
    """
    logging.info("#################  Handler Parse  ####################")
    try:
        msg = context.mem.get('message', None)

        if not isinstance(msg, ParseMessage):
            raise Exception(f"ParseMessage expected but got: {msg}")

        if msg.query:
            msg.query = msg.query.replace('OPERATOR(pg_catalog.~)', '=') \
                .replace('~', '=')

            handler = context.extended_query_handler

            try:
                resp, error_msg = handler.parse(session=context.session, msg=msg)

                logging.info(resp)

                if isinstance(resp, PreparedStatement):
                    context.prepared_statements[msg.name] = resp
                    ParseComplete().write(context.output)
                    logging.info(f"Have prepared statement: {context.prepared_statements}")
                    return context, Names.RECEIVE_EXTENDED_QUERY_COMMAND
                else:
                    logging.error(f"Error: {resp} {error_msg}")
                    return context, Names.CLOSE
            except Exception as e:
                log_exception(e)
                return context, Names.CLOSE

        else:
            logging.error("Closing from Parse no query")
            return context, Names.CLOSE
    except Exception as e:
        log_exception(e)
        logging.error(f"Error when parsing {msg}")
        return context, Names.CLOSE
    finally:
        logging.info("######################################################")


def process_bind_command(context: Context):
    msg = context.mem.get('message', None)

    if not isinstance(msg, BindMessage):
        if isinstance(msg, Sync):
            return context, Names.SYNC

        raise Exception(f"Bind expected but got: {msg}")

    handler = context.extended_query_handler
    try:
        prepared_statement = context.prepared_statements[msg.prepared_statement_name]

        resp, _ = handler.bind(session=context.session,
                               prepared_statement=prepared_statement,
                               bind=msg)

        print(f"From BIND got handler response: {resp}")

        if isinstance(resp, Portal):
            context.portals[msg.portal_name] = resp
            logging.info(f"From BIND wrote_portals: {context.portals}")

            BindComplete().write(context.output)

            return context, Names.RECEIVE_EXTENDED_QUERY_COMMAND
    except KeyError as e:
        logging.info(f"No prepared statement was found for {msg.prepared_statement_name} in {context.prepared_statements}")
        try:
            ErrorResponse.query(str(e)).write(context.output)
        except:
            pass
        return context, Names.CLOSE
    except ValueError as e:
        # ValueError("If using all scalar values, you must pass an index")
        if "using all scalar" in str(e):
            logging.info(
                f"Check your pandas dataframe, remember to pass in values as lists e.g DataFrame({'col1': [val]}) and not 'col1': val, do 'col1': [val].")

        return context, Names.CLOSE
    except Exception as e:
        log_exception(e)
        try:
            ErrorResponse.query(str(e)).write(context.output)
        except:
            return context, Names.CLOSE

        return context, Names.RECEIVE_EXTENDED_QUERY_COMMAND

    return context, Names.ERROR


def process_execute_command(context: Context):
    msg = context.mem.get('message', None)

    if not isinstance(msg, ExecuteMessage):
        if isinstance(msg, Sync):
            return context, Names.SYNC

        raise Exception(f"ExecuteMessage expected but got: {msg}")

    handler = context.extended_query_handler
    try:
        portal = context.portals[msg.portal_name]

        resp, _ = handler.execute(session=context.session,
                                  portal=portal,
                                  max_rows=msg.max_rows)

        if isinstance(resp, DataFrame):
            execution = portal.execution
            if not execution:
                execution = Execution(
                    max_rows=msg.max_rows if msg.max_rows else 10000000,
                    offset=0,
                    df=resp
                )
                portal.execution = execution

            context = context.update_mem("execution_portal", portal)

            return context, Names.WRITE_EXTENDED_DATA_FRAME
        else:
            return context, Names.WRITE_EXTENDED_EMPTY_RESPONSE
    except KeyError as e:
        log_exception(e)
        try:
            ErrorResponse.query(f"key error {e}").write(context.output)
        except:
            return context, Names.CLOSE

        return context, Names.SYNC
    except Exception as e:
        log_exception(e)
        try:
            ErrorResponse.query(str(e)).write(context.output)
        except:
            return context, Names.CLOSE

        return context, Names.SYNC


def read_till_sync(context: Context):
    msg = context.mem.get('message', None)

    if not isinstance(msg, Sync):
        m, t = Message.read(context.input)

        if m.process_name not in {Names.SYNC, Names.CLOSE}:
            return context, Names.SYNC

    return context, Names.READY_FOR_QUERY


def write_extended_empty_response(context: Context):
    EmptyQueryResponse().write(context.output)

    return context, Names.RECEIVE_EXTENDED_QUERY_COMMAND


def write_extended_data_frame_response(context: Context):
    portal = context.mem['execution_portal']

    execution = portal.execution

    if not execution:
        raise Exception("We expect a execution_portal instance here")

    try:
        if execution.df is None:
            EmptyQueryResponse().write(context.output)
        else:
            rows = DataFrameDataRows(df=execution.df,
                                     offset=execution.offset,
                                     max_rows=execution.max_rows).write(context.output)
            context.output.flush()

            df_rows = len(execution.df.index)

            read_all_rows = rows + execution.offset >= df_rows

            if rows == 0:
                EmptyQueryResponse().write(context.output)
            elif read_all_rows:
                CommandComplete(f"SELECT {df_rows}").write(context.output)
            elif rows < execution.max_rows:
                PortalSuspended().write(context.output)

        return context, Names.RECEIVE_EXTENDED_QUERY_COMMAND

    finally:
        context.output.flush()


def describe_statement_or_portal(context: Context):
    msg = context.mem.get('message', None)

    if not isinstance(msg, Describe):
        if isinstance(msg, Sync):
            return context, Names.SYNC

        raise Exception(f"Describe expected but got: {msg}")

    try:
        if msg.t == 'S':
            prepared_statement = context.prepared_statements[msg.name]
            logging.info(f"Describe {prepared_statement}")
            logging.error(f"Describe on prepared statement is not implemented yet")
            return context, Names.CLOSE
        else:
            portal = context.portals[msg.name]
            logging.info(f"Describe {portal}")
            logging.info(f"Writing DataFrameRowDescription")
            if portal.row_description is None:
                logging.error(f"Empty row description for portal {portal.row_description}")

                return write_extended_empty_response(context)
            else:
                DataFrameRowDescription(df=portal.row_description).write(context.output)

            context.output.flush()

        return context, Names.RECEIVE_EXTENDED_QUERY_COMMAND
    except KeyError:
        logging.error(
            f"No portal or prepared_statement_found for {msg.name} in {context.portals}, {context.prepared_statements}")
        return context, Names.CLOSE
    except Exception as e:
        log_exception(e)
        try:
            ErrorResponse.query(str(e)).write(context.output)
        except:
            return context, Names.CLOSE

        return context, Names.RECEIVE_EXTENDED_QUERY_COMMAND
