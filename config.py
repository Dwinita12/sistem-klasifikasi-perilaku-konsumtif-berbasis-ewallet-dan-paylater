import os

class Config:
    SECRET_KEY = "secret123"

    # ================= DATABASE =================
    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASSWORD = ""
    DB_NAME = "konsumtif_db"

    # ================= EMAIL =================
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "perilakukonsumtifewalletpaylat@gmail.com"
    MAIL_PASSWORD = "ebgjkhlssxdizhkp"