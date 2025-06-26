# my_project/web-frontend/Dockerfile
# 使用官方 Nginx 映像檔作為基礎映像檔
FROM nginx:alpine

# 將自定義的 Nginx 設定檔複製到容器中
COPY nginx.conf /etc/nginx/nginx.conf

# 將靜態網頁檔案複製到 Nginx 的預設靜態檔案目錄
COPY html/ /usr/share/nginx/html/

# 暴露 Nginx 預設埠
EXPOSE 80

# Nginx 預設的 CMD 會啟動 Nginx 服務，因此無需額外指定
CMD ["nginx", "-g", "daemon off;"]
