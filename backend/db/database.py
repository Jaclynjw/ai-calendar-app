import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import current_app, g
from dotenv import load_dotenv

load_dotenv()

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            dbname=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASS'],
            host=os.environ['DB_HOST'],
            port=os.environ['DB_PORT'],
            cursor_factory=RealDictCursor
        )
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None and not db.closed:
        db.close()


def init_db():
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            start_time TIMESTAMP NOT NULL,
            end_time TIMESTAMP NOT NULL,
            location VARCHAR(255) DEFAULT NULL,
            description TEXT DEFAULT NULL,
            category VARCHAR(255) DEFAULT NULL,
            user_id INTEGER NOT NULL
        );
    """)
    db.commit()
    cursor.close()

def init_app(app):
    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()
