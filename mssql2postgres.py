import asyncio

import asyncodbc
import asyncpg
from tqdm import tqdm

from config import settings

loop = asyncio.get_event_loop()


async def get_pg():
    """Get connection to PostgreSQL.

    :return: connection
    """

    url = "postgresql://{}:{}@{}/{}".format(
        settings.postgres_user,
        settings.postgres_password,
        settings.postgres_server,
        settings.postgres_db,
    )
    conn = await asyncpg.connect(url)
    return conn


async def get_mssql():
    """Get connection to MS SQL.

    :return: connection
    """

    dsn = (
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + settings.mssql_server
        + ";DATABASE="
        + settings.mssql_db
        + ";UID="
        + settings.mssql_username
        + ";PWD="
        + settings.mssql_password
    )
    conn = await asyncodbc.connect(
        dsn=dsn,
        loop=loop,
    )
    return conn


async def create_table_in_pg(conn):
    """Create new table in PostgreSQL.

    :param conn: connection to db
    """

    await conn.execute(
        """
            CREATE TABLE gga(
            id serial PRIMARY KEY,
            time timestamp,
            name varchar(50) NOT NULL,
            session varchar(50) NOT NULL,
            state integer NOT NULL,
            h float NOT NULL,
            b float NOT NULL,
            l float NOT NULL,
            satellite integer NOT NULL,
            dop float NOT NULL,
            delay integer NOT NULL
        )
                              """
    )


async def main():
    """Entry point."""

    mssql_conn = await get_mssql()
    pg_conn = await get_pg()

    mssql_cur = await mssql_conn.cursor()

    try:

        await create_table_in_pg(pg_conn)

        await mssql_cur.execute(
            """SELECT COUNT(*)
        FROM [CRNetProject].[dbo].[UserGGA]"""
        )
        row = await mssql_cur.fetchone()
        rows_count = row[0]
        for n in tqdm(range(24409798, 24409798 + rows_count + 1)):
            await mssql_cur.execute(
                """SELECT [ID]
            ,[onLineTime]
            ,[AccountName]
            ,[differentialState]
            ,[cur_H]
            ,[cur_B]
            ,[cur_L]
            ,[satelliteNumber]
            ,[dopValue]
            ,[delay]
        FROM [CRNetProject].[dbo].[UserGGA]
        WHERE [ID] = ?""",
                n,
            )
            row = await mssql_cur.fetchone()
            if not row:
                continue
            name, session = row[2].split("_")

            await pg_conn.execute(
                """
        INSERT INTO gga(
            time,
            name,
            session,
            state,
            h,
            b,
            l,
            satellite,
            dop,
            delay) VALUES(
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
    """,
                row[1],
                name,
                session,
                row[3],
                row[4],
                row[5],
                row[6],
                row[7],
                row[8],
                row[9],
            )

    except Exception as ex:
        raise ex
    finally:
        await mssql_cur.close()
        await mssql_conn.close()
        await pg_conn.close()


loop.run_until_complete(main())
