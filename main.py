from flask import Flask

from api.endpoints import api_bp

app = Flask(__name__)

app.register_blueprint(api_bp, url_prefix="/api")

@app.route("/")
def hello():
    return "Hello, world!"
    
if __name__ == "__main__":
    app.run(debug=True, port=4001)
