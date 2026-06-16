from .auth import auth_bp
from .dashboard import dashboard_bp
from .dataset import dataset_bp
from .ml import ml_bp
from .prediksi import prediksi_bp

__all__ = [
    "auth_bp",
    "dashboard_bp",
    "dataset_bp",
    "ml_bp",
    "prediksi_bp"
]