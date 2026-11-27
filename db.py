import os
import psycopg2#this acts as a bridge between our RAG and psql database
from dotenv import load_dotenv

load_dotenv()  # reads the .env file in the project folder


def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "5433")),
        dbname=os.getenv("DB_NAME", "rag"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.environ["DB_PASSWORD"],
    )