from flask import Flask
from flask_cors import CORS

from api.endpoints import api_bp

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

app.register_blueprint(api_bp, url_prefix="/api")


@app.route("/")
def hello():
    return "Hello, world!"


if __name__ == "__main__":
    app.run(debug=True, port=4001)
