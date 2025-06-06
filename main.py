import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import joblib
import tensorflow as tf

app = FastAPI(
    title="API",
    description="API para prever preço de fechamento de ações usando modelo LSTM",
    version="1.0.0"
)

class PredictRequest(BaseModel):
    sequence: list[float]  # lista de preços de fechamento (length = sequence_length)

class PredictResponse(BaseModel):
    predicted_price: float  # preço previsto (desescalonado)

@app.on_event("startup")
def load_model_and_scaler():
    global model, scaler
    try:
        model = tf.keras.models.load_model("model.keras")
        scaler = joblib.load("scaler.pkl")
    except Exception as e:
        print("Erro ao carregar modelo/scaler:", e)

# 3. Endpoint de previsão
@app.post("/predict", response_model=PredictResponse)
def predict_stock_price(request: PredictRequest):
    sequence = request.sequence
    
    if not isinstance(sequence, list):
        raise HTTPException(status_code=400, detail="O campo 'sequence' deve ser uma lista de floats.")
    if len(sequence) != 30:
        raise HTTPException(
            status_code=400,
            detail=f"Tamanho da sequência inválido. Deve ser exatamente 30, mas recebeu {len(sequence)}."
        )
    
    seq_arr = np.array(sequence).reshape(-1, 1)  # shape = (30, 1)
    try:
        seq_scaled = scaler.transform(seq_arr)   # forma (30, 1)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no escalonamento: {e}")
    
    X_input = seq_scaled.reshape((1, seq_scaled.shape[0], 1))
    
    try:
        pred_scaled = model.predict(X_input)  # shape (1, 1)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na predição: {e}")
    
    pred_price = scaler.inverse_transform(pred_scaled)[0][0]
    

    return PredictResponse(predicted_price=float(pred_price))


@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
