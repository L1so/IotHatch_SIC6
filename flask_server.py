from flask import Flask, request, jsonify
from pymongo import MongoClient
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# MongoDB konfigurasi
MONGO_URI = "mongodb+srv://IotHatch:password_disembunyikan@iothatch.5kday.mongodb.net/?appName=IotHatch"
DB_NAME = "IotHatch"
COLLECTION_NAME = "sensor"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

@app.route('/data', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()

        # Validasi data
        if not data or 'suhu' not in data or 'jarak' not in data:
            return jsonify({"error": "Invalid data format"}), 400

        try:
            suhu = float(data['suhu'])
            jarak = float(data['jarak'])
        except ValueError:
            return jsonify({"error": "Invalid data type"}), 400

        # Simpan data di mongodb
        result = collection.insert_one({"suhu": suhu, "jarak": jarak})

        logging.debug(f"Inserted data: {result.inserted_id}")

        return jsonify({"message": "Data received and stored successfully", "id": str(result.inserted_id)}), 201

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
