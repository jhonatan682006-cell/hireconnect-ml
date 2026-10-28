import os
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Cadena de conexión a MongoDB Atlas
MONGO_URI = "mongodb://hireconnect_app:EBF5Hn0cXcnG1Ug9@ac-b4477to-shard-00-00.idmluya.mongodb.net:27017,ac-b4477to-shard-00-01.idmluya.mongodb.net:27017,ac-b4477to-shard-00-02.idmluya.mongodb.net:27017/?ssl=true&replicaSet=atlas-76e1b6-shard-0&authSource=admin"
client = MongoClient(MONGO_URI)
db = client['hireconnect']

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json() or {}
    
    # Extraer variables predictoras recibidas desde Java
    edad = data.get('edad', 25)
    experiencia = data.get('experienciaAnos', 0)
    match_habilidades = data.get('coincidenciaHabilidades', 50)
    modalidad = data.get('modalidad', '')
    
    # Cálculo inicial de compatibilidad[cite: 8]
    bonus_modalidad = 15 if modalidad == 'Remoto' else (10 if modalidad == 'Hibrido' else 5)
    score = (match_habilidades * 0.5) + (min(experiencia * 10, 30)) + bonus_modalidad
    probabilidad = min(max(score, 10.0), 98.0)

    # Clasificación[cite: 8]
    if probabilidad >= 70:
        compatibilidad = "Alta"
    elif probabilidad >= 45:
        compatibilidad = "Media"
    else:
        compatibilidad = "Baja"

    return jsonify({
        "probabilidad": round(probabilidad, 1),
        "compatibilidad": compatibilidad
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)