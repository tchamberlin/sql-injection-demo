from datetime import datetime
import logging
import os
from typing import List

from bottle import request, jinja2_template
import psycopg2
import psycopg2.extensions
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers.sql import PostgresLexer


class AppState:
    queries: List[str] = []
    errors: List[str] = []
    logged_in = False


appState = AppState()


class CodeHtmlFormatter(HtmlFormatter):
    def wrap(self, source, outfile):
        return self._wrap_code(source)

    def _wrap_code(self, source):
        yield 0, '<div class="highlight">'
        for i, t in source:
            if i == 1:
                # it's a line of formatted code
                t += "<br>"
            yield i, t
        yield 0, "</div>"


class LoggingCursor(psycopg2.extensions.cursor):
    def execute(self, sql, args=None):
        query = self.mogrify(sql, args).decode("utf-8")
        logger = logging.getLogger("sql_debug")
        logger.info(f"Query: '{query}'")

        error_ = None
        try:
            psycopg2.extensions.cursor.execute(self, sql, args)
        except Exception as error:
            logger.error(f"{error.__class__.__name__}: {error}")
            appState.errors = [str(error)]
            error_ = error
            raise
        finally:
            appState.queries = [
                (
                    datetime.now(),
                    highlight((query), PostgresLexer(), CodeHtmlFormatter()),
                    error_,
                ),
                *appState.queries[:9],
            ]


def template(*args, **kwargs):
    """template function that injects context into each call"""
    rendered = jinja2_template(
        *args,
        **kwargs
        | dict(
            queries=appState.queries,
            errors=appState.errors,
            path=request.path,
            logged_in=appState.logged_in,
        ),
    )
    # Clear active errors after every render
    appState.errors = []

    return rendered


_db_info = os.environ.get("DB", None)
if not _db_info:
    raise ValueError(
        "'DB' must be defined in your environment: either populate a .env file, or set it manually!"
    )
conn = psycopg2.connect(_db_info)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor(cursor_factory=LoggingCursor)
