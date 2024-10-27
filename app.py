import numpy as np
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sklearn.preprocessing import StandardScaler
from pydantic import BaseModel
import joblib

app = FastAPI()

# Mount thư mục static để phục vụ CSS và JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Sử dụng Jinja2 template cho HTML
templates = Jinja2Templates(directory="templates")

# Định nghĩa cấu trúc dữ liệu đầu vào
class PredictionInput(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float

def predict_all_models(input_data):
    # Chuyển đổi dữ liệu người dùng nhập vào thành mảng numpy
    input_array = np.array(list(input_data.dict().values())).reshape(1, -1)
    
    scaler = StandardScaler()
    # Chuẩn hóa dữ liệu người dùng nhập vào
    input_scaled = scaler.fit_transform(input_array)
    
    # Dự đoán với mô hình Perceptron
    pred_perceptron = joblib.load('models/perceptron.pkl').predict(input_scaled)
    
    # Dự đoán với mô hình Logistic Regression
    pred_logistic = joblib.load('models/logistic_regression.pkl').predict(input_scaled)
    
    # Dự đoán với mô hình MLPClassifier
    pred_mlp = joblib.load('models/mlp.pkl').predict(input_scaled)
    
    return {
        'Perceptron': int(pred_perceptron[0]),
        'Logistic Regression': int(pred_logistic[0]),
        'MLPClassifier': int(pred_mlp[0])
    }

# Route chính để hiển thị trang web
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict/perceptron")
async def predict_perceptron(input_data: PredictionInput):
    try:
        predictions = predict_all_models(input_data)
        return JSONResponse(content={"prediction": predictions['Perceptron']})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/logistic_regression")
async def predict_logistic_regression(input_data: PredictionInput):
    try:
        predictions = predict_all_models(input_data)
        return JSONResponse(content={"prediction": predictions['Logistic Regression']})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/mlp")
async def predict_mlp(input_data: PredictionInput):
    try:
        predictions = predict_all_models(input_data)
        return JSONResponse(content={"prediction": predictions['MLPClassifier']})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Khởi động server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
