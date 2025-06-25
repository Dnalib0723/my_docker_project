# my_project/data-importer-service/Dockerfile
# 使用官方 Python 映像檔作為基礎映像檔
FROM python:3.9-slim-buster

# 設定工作目錄
WORKDIR /app

# 將 requirements.txt 複製到容器中
COPY requirements.txt .

# 安裝所有依賴
RUN pip install --no-cache-dir -r requirements.txt

# 將 importer.py 和 CSV 檔案複製到容器中
COPY importer.py .
COPY titanic passengers.csv .

# 定義當容器啟動時執行的命令
CMD ["python", "importer.py"]