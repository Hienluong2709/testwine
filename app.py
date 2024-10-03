from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import csv

app = FastAPI()

# Mount thư mục static để phục vụ CSS và JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Sử dụng Jinja2 template cho HTML
templates = Jinja2Templates(directory="templates")

# Đọc dữ liệu CSV
def read_csv():
    with open('data.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
    return data

# Route chính để hiển thị trang web
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    data = read_csv()  # Lấy dữ liệu từ CSV
    return templates.TemplateResponse("index.html", {"request": request, "data": data})

# Khởi động server
# Chạy ứng dụng bằng lệnh: uvicorn app:app --reload
