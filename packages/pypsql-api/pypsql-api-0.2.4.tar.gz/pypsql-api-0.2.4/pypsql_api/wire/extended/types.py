from dataclasses import dataclass
from typing import Optional, List, Any

from pandas import DataFrame


@dataclass
class Param:
    oid_type: Optional[int]
    index: Optional[int]
    type: Optional[Any]

    @staticmethod
    def create_empty():
        return Param(oid_type=0, index=0, type=None)


@dataclass
class PreparedStatement:
    name: str
    sql: str
    parameters: Optional[List[Param]]


@dataclass
class Execution:
    max_rows: int
    offset: int
    df: Optional[DataFrame]


@dataclass
class Portal:
    name: str
    prepared_statement: PreparedStatement

    execution: Optional[Execution]

    # RowDescription message describing the rows that will be returned by executing the portal;
    row_description: Optional[DataFrame]
