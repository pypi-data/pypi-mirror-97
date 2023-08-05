from typing import Tuple, Optional, Union, Any

from pandas import DataFrame

from pypsql_api.config.types import Session
from pypsql_api.wire.extended.types import PreparedStatement, Portal
from pypsql_api.wire.front import ParseMessage, BindMessage


class AuthHandler:

    def handle(self, session: Session) -> Tuple[bool, Optional[str]]:
        """
        :param session:
        :return: Tuple[bool, Optional[str]] if (true, any) then AuthOK, otherwise AuthFail, and the message in the str
        contains any error message
        """
        raise Exception("Not implemented")


class QueryHandler:

    def handle(self, session: Session, sql) -> Tuple[Optional[Union[Any, Optional[DataFrame]]], Optional[Any]]:
        """
        :param session:
        :param sql: any sql statement passed by the client,
         this can be multiple statements and being-commit statements.
        :return: None -> No result
                 (Any, Msg)  -> Msg for future use to return notification messages.
                 (DataFrame, Any) -> The DataFrame the contains the data and schema returned
        """
        raise Exception("Not implemented")


class ExtendedQueryHandler:
    """
    Parse prepared statement queries
    """

    def parse(self, session: Session, msg: ParseMessage) -> Tuple[
        Optional[Union[Any, Optional[PreparedStatement]]], Optional[Any]]:
        """
        :param session:
        :param msg: ParseMessage
         this can be multiple statements and being-commit statements.
        :return: None -> No result
                 (Any, Msg)  -> Msg for future use to return notification messages.
                 (PreparedStatement, Any) -> The DataFrame the contains the data and schema returned
        """
        raise Exception("Not implemented")

    def bind(self, session: Session, prepared_statement: PreparedStatement, bind: BindMessage) -> Tuple[
        Optional[Union[Any, Optional[Portal]]], Optional[Any]]:
        """
        :param session:
        :param prepared_statement: PreparedStatement
        :param bind: BindMessage
         this can be multiple statements and being-commit statements.
        :return: None -> No result
                 (Any, Msg)  -> Msg for future use to return notification messages.
                 (Portal, Any) -> The DataFrame the contains the data and schema returned
        """
        raise Exception("Not implemented")

    def execute(self, session: Session, portal: Portal, max_rows: int) -> Tuple[Optional[Union[Any, Optional[DataFrame]]], Optional[Any]]:
        """
        Any exception throws an error
        :param session:
        :param portal: Portal
        :param max_rows: int
        :return: None -> No result
                 (Any, Msg)  -> Msg for future use to return notification messages.
                 (PreparedStatement, Any) -> The DataFrame the contains the data and schema returned
        """
        raise Exception("Not implemented")
