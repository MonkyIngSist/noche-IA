from flask import Flask, request, render_template
import joblib
import config
import numpy as np
from database import load_data
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def load_model():
    try:
        return joblib.load(config.MODEL_PATH)
    except FileNotFoundError:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    investment_recommendation = ""
    plot_url = ""
    
    if request.method == "POST":
        symbol = request.form["symbol"]
        model = load_model()
        
        if model:
            data = load_data()
            prices = [float(entry["1. open"]) for record in data if record["symbol"] == symbol for entry in record["Time Series (Daily)"].values()]
            
            if prices:
                # Usamos el último precio para predecir la tendencia futura
                current_price = np.array(prices[-1]).reshape(1, -1)
                predicted_price = model.predict(current_price)[0]

                # Evaluación de recomendación: Si el precio proyectado es mayor al actual, es una buena inversión
                investment_recommendation = "Buena inversión" if predicted_price > current_price else "No se recomienda invertir ahora"
                
                # Generación del gráfico
                plt.figure(figsize=(10, 5))
                plt.plot(prices, label="Precio Actual")
                plt.axhline(y=predicted_price, color='r', linestyle='--', label="Precio Predicho")
                plt.legend()
                plt.xlabel("Días")
                plt.ylabel("Precio")
                plt.title(f"Predicción de Precio para {symbol} - {investment_recommendation}")
                
                img = io.BytesIO()
                plt.savefig(img, format="png")
                img.seek(0)
                plot_url = base64.b64encode(img.getvalue()).decode()
            else:
                investment_recommendation = "No hay suficientes datos para esta empresa."
        else:
            investment_recommendation = "Modelo no disponible. Entrénelo primero."
    
    return render_template("index.html", plot_url=plot_url, recommendation=investment_recommendation)

if __name__ == "__main__":
    app.run(debug=True)
