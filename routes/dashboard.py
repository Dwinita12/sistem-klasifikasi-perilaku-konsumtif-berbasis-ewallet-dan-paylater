from flask import Blueprint, render_template, session
from utils.db import get_db

# IMPORT DARI ML
from routes.ml import train_c45

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/home")
def home():

    # ==========================
    # TOTAL DATA
    # ==========================
    total_user = 0
    total_training = 0
    total_pengguna = 0
    total_prediksi = 0

    try:

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM users"
        )
        total_user = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM dataset_training"
        )
        total_training = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM dataset_pengguna"
        )
        total_pengguna = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM hasil_prediksi"
        )
        total_prediksi = cursor.fetchone()[0]

        cursor.close()
        db.close()

    except Exception as e:

        print(
            "ERROR TOTAL DASHBOARD:",
            e
        )

    # ==========================
    # STATISTIK HASIL PREDIKSI
    # ==========================
    rendah = 0
    sedang = 0
    tinggi = 0

    try:

        db = get_db()

        cursor = db.cursor(
            dictionary=True
        )

        cursor.execute("""
            SELECT
                SUM(
                    CASE
                    WHEN hasil='Rendah'
                    THEN 1
                    ELSE 0
                    END
                ) AS rendah,

                SUM(
                    CASE
                    WHEN hasil='Sedang'
                    THEN 1
                    ELSE 0
                    END
                ) AS sedang,

                SUM(
                    CASE
                    WHEN hasil='Tinggi'
                    THEN 1
                    ELSE 0
                    END
                ) AS tinggi

            FROM hasil_prediksi
        """)

        hasil = cursor.fetchone()

        if hasil:

            rendah = (
                hasil["rendah"] or 0
            )

            sedang = (
                hasil["sedang"] or 0
            )

            tinggi = (
                hasil["tinggi"] or 0
            )

        cursor.close()
        db.close()

    except Exception as e:

        print(
            "ERROR HITUNG HASIL:",
            e
        )

    # ==========================
    # AKURASI C4.5
    # ==========================
    akurasi_test = "0%"

    try:

        hasil_model = train_c45()

        if hasil_model:

            acc_test = hasil_model.get(
                "acc_test",
                0
            )

            akurasi_test = (
                f"{acc_test:.2f}%"
            )

            print(
                "ACC TEST =",
                acc_test
            )

    except Exception as e:

        print(
            "ERROR AKURASI DASHBOARD:",
            e
        )

    print(
        "AKURASI TEST DASHBOARD =",
        akurasi_test
    )

    # ==========================
    # RENDER
    # ==========================
    return render_template(
        "home.html",

        username=session.get(
            "username"
        ),

        total_user=total_user,

        total_training=total_training,

        total_pengguna=total_pengguna,

        total_prediksi=total_prediksi,

        rendah=rendah,

        sedang=sedang,

        tinggi=tinggi,

        akurasi_test=akurasi_test
    )