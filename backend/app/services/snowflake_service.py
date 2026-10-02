import snowflake.connector
from contextlib import contextmanager
from app.core.config import get_settings
import logging
import os
import threading

logger = logging.getLogger(__name__)

_global_conn = None
_conn_lock = threading.Lock()


def _is_spcs() -> bool:
    return os.path.exists("/snowflake/session/token")


def _get_spcs_token() -> str:
    with open("/snowflake/session/token", "r") as f:
        return f.read().strip()


def get_connection():
    global _global_conn

    with _conn_lock:
        try:
            if _global_conn is not None and not _global_conn.is_closed():
                return _global_conn

            settings = get_settings()

            if _is_spcs():
                # SPCS-native connection using injected OAuth token
                host = os.environ.get("SNOWFLAKE_HOST", f"{settings.snowflake_account}.snowflakecomputing.com")
                logger.info(f"Connecting via SPCS OAuth token to {host}")
                _global_conn = snowflake.connector.connect(
                    host=host,
                    account=settings.snowflake_account,
                    authenticator="oauth",
                    token=_get_spcs_token(),
                    role=settings.snowflake_role,
                    warehouse=settings.snowflake_warehouse,
                    database=settings.snowflake_database,
                    schema=settings.snowflake_schema,
                    client_session_keep_alive=True,
                    network_timeout=60,
                    login_timeout=30,
                )
                _global_conn.cursor().execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 120")
            else:
                # Local development connection using password
                logger.info("Connecting via username/password (local dev)")
                _global_conn = snowflake.connector.connect(
                    account=settings.snowflake_account,
                    user=settings.snowflake_user,
                    password=settings.snowflake_password,
                    role=settings.snowflake_role,
                    warehouse=settings.snowflake_warehouse,
                    database=settings.snowflake_database,
                    schema=settings.snowflake_schema,
                    client_session_keep_alive=True,
                    network_timeout=60,
                    login_timeout=30,
                )

            logger.info("Snowflake connection established successfully")
            return _global_conn
        except Exception as e:
            logger.error(f"Snowflake connection failed: {e}")
            _global_conn = None
            raise


@contextmanager
def snowflake_cursor():
    conn = get_connection()
    try:
        cur = conn.cursor()
        yield cur
    finally:
        cur.close()


def execute_query(query: str) -> list[dict]:
    with snowflake_cursor() as cur:
        cur.execute(query)
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        return [dict(zip(columns, row)) for row in rows]


def execute_scalar(query: str):
    with snowflake_cursor() as cur:
        cur.execute(query)
        row = cur.fetchone()
        return row[0] if row else None
