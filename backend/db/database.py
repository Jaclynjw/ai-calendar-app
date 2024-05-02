import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import current_app, g
from dotenv import load_dotenv
from dateutil import parser
from datetime import datetime
import pytz

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
            category VARCHAR(255) DEFAULT NULL
        );
    """)
    db.commit()
    cursor.close()

def init_app(app):
    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()

def parse_datetime(iso_string):
    # 解析 ISO 8601 格式字符串，并假定它是 UTC 时间
    return datetime.fromisoformat(iso_string.replace('Z', '+00:00')).astimezone(pytz.utc)


def create_event(event_data):
    db = get_db()
    cursor = db.cursor()
    try:
        # 将日期时间字符串转换为 datetime 对象
        start_time = parse_datetime(event_data['start_time'])
        end_time = parse_datetime(event_data['end_time'])

        cursor.execute("""
            INSERT INTO events (title, start_time, end_time, location, description, category)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
        """, (event_data['title'], start_time, end_time, event_data['location'], event_data['description'], event_data['category']))
        db.commit()
        event_id = cursor.fetchone()  # 获取返回的 ID
        if event_id:
            return {"success": True, "id": event_id['id']}
        else:
            print("No ID returned from the database")
            return None
    except Exception as e:
        print("Database error:", e)
        db.rollback()  # 出现异常时回滚事务
        return None
    finally:
        cursor.close()
