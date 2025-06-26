# my_project/api-service/api_app.py
from fastapi import FastAPI, HTTPException
import mysql.connector
import os
import time
from mysql.connector import Error

app = FastAPI()

# 從環境變數中獲取資料庫連線資訊
DB_HOST = os.getenv('DB_HOST', 'db')
DB_NAME = os.getenv('DB_NAME', 'titanic_db')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')

def get_db_connection(max_retries=10, retry_delay=5):
    """嘗試連線到 MySQL 資料庫，包含重試邏輯。"""
    conn = None
    for i in range(max_retries):
        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            if conn.is_connected():
                print("API Service: 成功連線到 MySQL 資料庫。")
                return conn
        except Error as e:
            print(f"API Service: 嘗試連線到 MySQL 失敗 (嘗試 {i+1}/{max_retries}): {e}")
            time.sleep(retry_delay)
    print("API Service: 無法連線到 MySQL 資料庫，請檢查資料庫服務。")
    return None

@app.get("/")
async def root():
    """根路徑，提供基本問候。"""
    return {"message": "歡迎來到 Titanic 乘客 API 服務！請訪問 /passengers 以獲取數據。"}

@app.get("/passengers")
async def get_passengers():
    """獲取所有 Titanic 乘客的資料。"""
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            raise HTTPException(status_code=500, detail="無法連線到資料庫。")

        cursor = conn.cursor(dictionary=True) # 以字典形式返回結果
        query = "SELECT * FROM passengers"
        cursor.execute(query)
        passengers = cursor.fetchall()
        return passengers
    except Exception as e:
        print(f"獲取乘客資料時發生錯誤: {e}")
        raise HTTPException(status_code=500, detail=f"內部伺服器錯誤: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
