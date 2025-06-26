# my_project/api-service/Dockerfile
# 使用官方 Python 映像檔作為基礎映像檔
FROM python:3.9-slim-buster

# 設定工作目錄
WORKDIR /app

# 將 requirements.txt 複製到容器中
COPY requirements.txt .

# 安裝所有依賴
RUN pip install --no-cache-dir -r requirements.txt

# 將 api-app.py 複製到容器中
COPY api_app.py .

# 暴露 FastAPI 預設埠
EXPOSE 8000

# 定義當容器啟動時執行的命令
# 使用 uvicorn 啟動 FastAPI 應用程式，並監聽所有網路介面
CMD ["uvicorn", "api_app:app", "--host", "0.0.0.0", "--port", "8000"]
