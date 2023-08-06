"""

Read: https://www.pgcon.org/2014/schedule/attachments/330_postgres-for-the-wire.pdf
"""
import logging
from dataclasses import dataclass
from typing import Callable, Set, Tuple, Any

from pypsql_api.wire.actions import write_ssl_resp_no, read_startup_message, read_plain_text_password_request, \
    write_plain_text_password_request, read_ssl_request, write_ready_for_query, write_auth_ok, read_receive_command, \
    write_empty_response, write_data_frame_response, read_receive_extended_command, write_ssl_resp_yes
from pypsql_api.wire.actions_types import Names
from pypsql_api.wire.errors.core import log_exception
from pypsql_api.wire.query.extended_query import process_parse_command, process_bind_command, process_execute_command, \
    read_till_sync, write_extended_data_frame_response, write_extended_empty_response, describe_statement_or_portal
from pypsql_api.wire.query.simple_query import process_simple_query


@dataclass
class State:
    allowed: Set[str]
    name: str
    fn: Callable[[Any], Tuple[Any, str]]

    def move_next(self, context: Any):
        return self.fn(context)


def move_state(context: Any, state: State) -> Tuple[Any, str]:
    ctx_new, new_state = state.move_next(context)

    if not new_state:
        return ctx_new, Names.CLOSE

    if not new_state in state.allowed:
        raise Exception(f"Invalid state {new_state} from {state.name}, allowed states are {state.allowed}")

    return ctx_new, new_state


processes = {
    Names.READ_SSL_REQUEST: State(name=Names.READ_SSL_REQUEST,
                                  allowed={Names.WRITE_SSL_NO, Names.WRITE_SSL_YES,
                                           Names.WRITE_PLAIN_TEXT_PASSWORD_REQUEST, Names.CLOSE}, fn=read_ssl_request),
    Names.WRITE_SSL_NO: State(name=Names.READ_SSL_REQUEST, allowed={Names.READ_STARTUP_MESSAGE, Names.CLOSE},
                              fn=write_ssl_resp_no),
    Names.WRITE_SSL_YES: State(name=Names.READ_SSL_REQUEST, allowed={Names.READ_STARTUP_MESSAGE, Names.CLOSE},
                               fn=write_ssl_resp_yes),

    Names.READ_STARTUP_MESSAGE: State(name=Names.READ_STARTUP_MESSAGE,
                                      allowed={Names.WRITE_PLAIN_TEXT_PASSWORD_REQUEST, Names.CLOSE,
                                               Names.READ_STARTUP_MESSAGE}, fn=read_startup_message),

    Names.WRITE_PLAIN_TEXT_PASSWORD_REQUEST: State(name=Names.WRITE_PLAIN_TEXT_PASSWORD_REQUEST,
                                                   allowed={Names.READ_PLAIN_TEXT_PASSWORD, Names.CLOSE},
                                                   fn=write_plain_text_password_request),

    Names.READ_PLAIN_TEXT_PASSWORD: State(name=Names.READ_PLAIN_TEXT_PASSWORD,
                                          allowed={Names.CLOSE, Names.WRITE_AUTH_OK},
                                          fn=read_plain_text_password_request),

    Names.WRITE_AUTH_OK: State(name=Names.READ_PLAIN_TEXT_PASSWORD,
                               allowed={Names.READY_FOR_QUERY, Names.CLOSE},
                               fn=write_auth_ok),

    Names.READY_FOR_QUERY: State(name=Names.READY_FOR_QUERY,
                                 allowed={Names.CLOSE, Names.RECEIVE_COMMAND}, fn=write_ready_for_query),

    Names.RECEIVE_COMMAND: State(name=Names.RECEIVE_COMMAND,
                                 allowed={Names.CLOSE, Names.READY_FOR_QUERY, Names.SIMPLE_QUERY,
                                          Names.PARSE},
                                 fn=read_receive_command),

    Names.SIMPLE_QUERY: State(name=Names.SIMPLE_QUERY,
                              allowed={Names.CLOSE, Names.READY_FOR_QUERY, Names.WRITE_EMPTY_RESPONSE,
                                       Names.WRITE_DATA_FRAME},
                              fn=process_simple_query),

    Names.WRITE_EMPTY_RESPONSE: State(name=Names.WRITE_EMPTY_RESPONSE,
                                      allowed={Names.CLOSE, Names.READY_FOR_QUERY},
                                      fn=write_empty_response),

    Names.WRITE_DATA_FRAME: State(name=Names.WRITE_DATA_FRAME,
                                  allowed={Names.CLOSE, Names.READY_FOR_QUERY},
                                  fn=write_data_frame_response),

    Names.PARSE: State(name=Names.PARSE,
                       allowed={Names.CLOSE, Names.ERROR, Names.SYNC, Names.RECEIVE_EXTENDED_QUERY_COMMAND},
                       fn=process_parse_command),

    Names.BIND: State(name=Names.BIND,
                      allowed={Names.CLOSE, Names.ERROR,
                               Names.EXECUTE, Names.SYNC,
                               Names.RECEIVE_EXTENDED_QUERY_COMMAND},
                      fn=process_bind_command),

    Names.EXECUTE: State(name=Names.EXECUTE,
                         allowed={Names.CLOSE, Names.ERROR,
                                  Names.SYNC,
                                  Names.WRITE_EXTENDED_EMPTY_RESPONSE,
                                  Names.WRITE_EXTENDED_DATA_FRAME,
                                  Names.RECEIVE_EXTENDED_QUERY_COMMAND},
                         fn=process_execute_command),

    Names.SYNC: State(name=Names.SYNC,
                      allowed={Names.CLOSE, Names.READY_FOR_QUERY, Names.SYNC,
                               Names.RECEIVE_EXTENDED_QUERY_COMMAND},
                      fn=read_till_sync),

    Names.WRITE_EXTENDED_EMPTY_RESPONSE: State(name=Names.WRITE_EXTENDED_EMPTY_RESPONSE,
                                               allowed={Names.CLOSE, Names.SYNC,
                                                        Names.RECEIVE_EXTENDED_QUERY_COMMAND},
                                               fn=write_extended_empty_response),

    Names.WRITE_EXTENDED_DATA_FRAME: State(name=Names.WRITE_EXTENDED_DATA_FRAME,
                                           allowed={Names.CLOSE, Names.SYNC,
                                                    Names.RECEIVE_EXTENDED_QUERY_COMMAND},
                                           fn=write_extended_data_frame_response),

    Names.DESCRIBE: State(name=Names.DESCRIBE,
                          allowed={Names.CLOSE, Names.SYNC,
                                   Names.WRITE_EXTENDED_DATA_FRAME, Names.WRITE_EXTENDED_EMPTY_RESPONSE,
                                   Names.RECEIVE_EXTENDED_QUERY_COMMAND},
                          fn=describe_statement_or_portal),

    Names.RECEIVE_EXTENDED_QUERY_COMMAND: State(name=Names.RECEIVE_EXTENDED_QUERY_COMMAND,
                                                allowed={Names.CLOSE, Names.EXECUTE, Names.BIND, Names.SYNC,
                                                         Names.PARSE, Names.DESCRIBE},
                                                fn=read_receive_extended_command),

}


def run_states(context, state_name):
    while state_name != Names.CLOSE:
        context, state_name = run_state(context, state_name)

    logging.error("End run states")

    return context, state_name


def run_state(context, state_name):
    logging.error(f"Running state {state_name}")
    state = processes.get(state_name)

    if hasattr(context.output, 'flush'):
        try:
            context.output.flush()
        except Exception as e:
            log_exception(e)

    context, state_name = move_state(context, state)

    if not state_name:
        state_name = Names.CLOSE

    return context, state_name
