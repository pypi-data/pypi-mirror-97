from enum import Enum


class CreateDbDataSetRequestDbType(str, Enum):
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    D_B2 = "db2"
    SQLSERVER = "sqlserver"

    def __str__(self) -> str:
        return str(self.value)