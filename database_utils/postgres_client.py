import os
import psycopg
from psycopg.rows import dict_row


def create_postgres_client():
    return psycopg.connect(os.getenv("DATABASE_URL"), row_factory=dict_row)
