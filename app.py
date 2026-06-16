from flask import Flask, render_template
from config import Config
from extensions import mail

from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.dataset import dataset_bp
from routes.ml import ml_bp
from routes.prediksi import prediksi_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mail.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(dataset_bp, url_prefix="/dataset")
    app.register_blueprint(ml_bp)
    app.register_blueprint(prediksi_bp)

    return app

app = create_app()

@app.route("/")
def landing():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)