from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to CloudKart",
        "status": "running",
        "version": "v1"
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })

@app.route("/products")
def products():
    return jsonify([
        {"id": 1, "name": "Premium Bouquet", "price": 20000},
        {"id": 2, "name": "Luxury Rose Box", "price": 15000},
        {"id": 3, "name": "Wedding Flower Hamper", "price": 30000}
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
