"""
MySQL DB 연결 관리
"""

import os
import pymysql
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """pymysql 커넥션 생성"""
    return pymysql.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=int(os.environ.get("DB_PORT", 3306)),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", ""),
        database=os.environ.get("DB_NAME", "apt_trade"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )