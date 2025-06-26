# my_project/data-importer-service/importer.py
import mysql.connector
import pandas as pd
import os
import time
from mysql.connector import Error

# 從環境變數中獲取資料庫連線資訊
DB_HOST = os.getenv('DB_HOST', 'db')
DB_NAME = os.getenv('DB_NAME', 'titanic_db')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
CSV_FILE = 'titanic_passengers.csv'

def connect_to_db(max_retries=10, retry_delay=5):
    """嘗試連線到 MySQL 資料庫，包含重試邏輯。"""
    conn = None
    for i in range(max_retries):
        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME # 這裡嘗試連線到已存在的資料庫，如果不存在會在後面創建
            )
            if conn.is_connected():
                print(f"成功連線到 MySQL 資料庫: {DB_NAME}")
                return conn
        except Error as e:
            print(f"嘗試連線到 MySQL 失敗 (嘗試 {i+1}/{max_retries}): {e}")
            time.sleep(retry_delay)
    print("無法連線到 MySQL 資料庫，請檢查資料庫服務。")
    return None

def create_database_and_table():
    """創建資料庫和 titanic 表格。"""
    conn = None
    try:
        # 連線到 MySQL 但不指定資料庫，以便創建資料庫
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        if conn.is_connected():
            cursor = conn.cursor()

            # 創建資料庫
            try:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
                print(f"資料庫 '{DB_NAME}' 已準備好或已存在。")
            except Error as e:
                print(f"創建資料庫失敗: {e}")
                return False

            # 切換到新創建的資料庫
            cursor.execute(f"USE {DB_NAME}")

            # 創建表格
            create_table_query = """
            CREATE TABLE IF NOT EXISTS passengers (
                PassengerId INT PRIMARY KEY AUTO_INCREMENT,
                Survived INT,
                Pclass INT,
                Name VARCHAR(255),
                Sex VARCHAR(10),
                Age FLOAT,
                SibSp INT,
                Parch INT,
                Ticket VARCHAR(255),
                Fare FLOAT,
                Cabin VARCHAR(255),
                Embarked VARCHAR(10)
            )
            """
            cursor.execute(create_table_query)
            print("表格 'passengers' 已準備好或已存在。")
            conn.commit()
            return True
    except Error as e:
        print(f"資料庫或表格創建過程中發生錯誤: {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()
    return False

def import_data():
    """從 CSV 檔案匯入資料到資料庫。"""
    if not create_database_and_table():
        print("無法準備資料庫和表格，停止匯入。")
        return

    conn = connect_to_db()
    if conn is None:
        return

    try:
        df = pd.read_csv(CSV_FILE)
        cursor = conn.cursor()

        # 刪除所有現有資料以避免重複匯入
        cursor.execute("DELETE FROM passengers")
        conn.commit()
        print("已清除 'passengers' 表格中的現有資料。")

        # 插入資料
        for index, row in df.iterrows():
            # 處理可能為 NaN 的值
            age = None if pd.isna(row['Age']) else float(row['Age'])
            fare = None if pd.isna(row['Fare']) else float(row['Fare'])
            cabin = None if pd.isna(row['Cabin']) else str(row['Cabin'])
            embarked = None if pd.isna(row['Embarked']) else str(row['Embarked'])

            insert_query = """
            INSERT INTO passengers (Survived, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            data = (
                int(row['Survived']),
                int(row['Pclass']),
                str(row['Name']),
                str(row['Sex']),
                age,
                int(row['SibSp']),
                int(row['Parch']),
                str(row['Ticket']),
                fare,
                cabin,
                embarked
            )
            cursor.execute(insert_query, data)
        conn.commit()
        print(f"成功匯入 {len(df)} 筆資料到 'passengers' 表格。")

    except FileNotFoundError:
        print(f"錯誤: 找不到 CSV 檔案 '{CSV_FILE}'。請確保檔案存在於正確路徑。")
    except Error as e:
        print(f"資料匯入過程中發生錯誤: {e}")
        conn.rollback() # 發生錯誤時回滾
    except Exception as e:
        print(f"發生未預期的錯誤: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("資料庫連線已關閉。")

if __name__ == "__main__":
    print("啟動資料匯入服務...")
    import_data()
