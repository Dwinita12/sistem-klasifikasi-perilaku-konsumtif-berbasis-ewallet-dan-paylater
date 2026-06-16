from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    session
)

from utils.db import get_db
import csv

dataset_bp = Blueprint("dataset", __name__)


# =========================================================
# DATASET TRAINING
# =========================================================
@dataset_bp.route("/dataset-training")
def dataset_training():

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM dataset_training
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "dataset_training.html",
        data=data
    )


# =========================================================
# IMPORT TRAINING CSV
# =========================================================
@dataset_bp.route("/import-training", methods=["POST"])
def import_training():

    file = request.files.get("file")

    if not file or file.filename == "":
        flash("File tidak ditemukan")
        return redirect(url_for("dataset.dataset_training"))

    try:

        stream = file.stream.read().decode("UTF8").splitlines()

        reader = csv.reader(stream)

        # SKIP HEADER
        next(reader, None)

        db = get_db()
        cursor = db.cursor()

        total_import = 0

        for row in reader:

            if not row:
                continue

            if len(row) < 11:
                continue

            nama = row[0].strip()

            # LEWATI HEADER YANG IKUT KEIMPORT
            if nama.lower() == "nama":
                continue

            cursor.execute(
                """
                INSERT INTO dataset_training (

                    nama,
                    intensitas_ewallet,
                    aktivitas_ewallet,
                    intensitas_paylater,
                    dampak_paylater,
                    pengaruh_promo,
                    sosial_lingkungan,
                    media_gayahidup,
                    kontrol_pengeluaran,
                    kontrol_literasi,
                    status

                )

                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s
                )
                """,
                (
                    row[0].strip(),
                    row[1].strip(),
                    row[2].strip(),
                    row[3].strip(),
                    row[4].strip(),
                    row[5].strip(),
                    row[6].strip(),
                    row[7].strip(),
                    row[8].strip(),
                    row[9].strip(),
                    row[10].strip()
                )
            )

            total_import += 1

        db.commit()

        cursor.close()
        db.close()

        flash(f"Import CSV berhasil ({total_import} data masuk)")

    except Exception as e:

        flash(f"Gagal import CSV: {str(e)}")

    return redirect(url_for("dataset.dataset_training"))


# =========================================================
# DATASET PENGGUNA
# =========================================================
@dataset_bp.route("/dataset-pengguna", methods=["GET", "POST"])
def dataset_pengguna():

    if "user_id" not in session:

        flash("Silakan login terlebih dahulu")
        return redirect(url_for("auth.login"))

    db = get_db()
    cursor = db.cursor(dictionary=True)

    # =====================================================
    # FUNGSI KATEGORI
    # =====================================================
    def kategori_3(nilai):

        if nilai < 2:
            return "Rendah"

        elif nilai < 3.5:
            return "Sedang"

        else:
            return "Tinggi"

    def kategori_ewallet(nilai):

        if nilai < 2:
            return "Jarang"

        elif nilai < 3.5:
            return "Cukup"

        else:
            return "Sering"

    def kategori_paylater(nilai):

        if nilai < 2:
            return "Jarang"

        elif nilai < 3.5:
            return "Cukup"

        else:
            return "Sering"

    def kategori_dampak(nilai):

        if nilai < 2:
            return "Kecil"

        elif nilai < 3.5:
            return "Sedang"

        else:
            return "Besar"

    def kategori_promo(nilai):

        if nilai < 2:
            return "Lemah"

        elif nilai < 3.5:
            return "Sedang"

        else:
            return "Kuat"

    def kategori_kontrol(nilai):

        if nilai < 2:
            return "Baik"

        elif nilai < 3.5:
            return "Cukup"

        else:
            return "Buruk"

    def kategori_literasi(nilai):

        if nilai < 2:
            return "Baik"

        elif nilai < 3.5:
            return "Sedang"

        else:
            return "Rendah"

    # =====================================================
    # AMBIL ANGKA
    # =====================================================
    def ambil_angka(field):

        val = request.form.get(field)

        try:
            return int(val)

        except:
            return 0

    # =====================================================
    # POST
    # =====================================================
    if request.method == "POST":

        nama = request.form.get("nama")
        jk = request.form.get("jk")
        usia = request.form.get("usia")
        pekerjaan = request.form.get("pekerjaan")
        pendapatan = request.form.get("pendapatan")

        # =================================================
        # AMBIL DATA X01 - X28
        # =================================================
        x01 = ambil_angka("x01")
        x02 = ambil_angka("x02")
        x03 = ambil_angka("x03")
        x04 = ambil_angka("x04")
        x05 = ambil_angka("x05")

        x06 = ambil_angka("x06")
        x07 = ambil_angka("x07")
        x08 = ambil_angka("x08")
        x09 = ambil_angka("x09")
        x10 = ambil_angka("x10")

        x11 = ambil_angka("x11")
        x12 = ambil_angka("x12")

        x13 = ambil_angka("x13")
        x14 = ambil_angka("x14")

        x15 = ambil_angka("x15")
        x16 = ambil_angka("x16")
        x17 = ambil_angka("x17")

        x18 = ambil_angka("x18")
        x19 = ambil_angka("x19")

        x20 = ambil_angka("x20")
        x21 = ambil_angka("x21")
        x22 = ambil_angka("x22")

        # REVERSE SCORING
        x23_asli = ambil_angka("x23")
        x23 = 6 - x23_asli

        x24 = ambil_angka("x24")
        x25 = ambil_angka("x25")
        x26 = ambil_angka("x26")
        x27 = ambil_angka("x27")
        x28 = ambil_angka("x28")

        # =================================================
        # DEBUG
        # =================================================
        print("x01 =", x01)
        print("x02 =", x02)
        print("x03 =", x03)
        print("x04 =", x04)
        print("x05 =", x05)

        # =================================================
        # KATEGORI
        # =================================================
        intensitas_ewallet = kategori_ewallet(
            (x01 + x02) / 2
        )

        aktivitas_ewallet = kategori_3(
            (x03 + x04 + x05) / 3
        )

        intensitas_paylater = kategori_paylater(
            (x06 + x07) / 2
        )

        dampak_paylater = kategori_dampak(
            (x08 + x09 + x10) / 3
        )

        pengaruh_promo = kategori_promo(
            (x11 + x12) / 2
        )

        sosial_lingkungan = kategori_3(
            (x13 + x14) / 2
        )

        media_gayahidup = kategori_3(
            (x15 + x16 + x17) / 3
        )

        kontrol_pengeluaran = kategori_kontrol(
            (x18 + x19) / 2
        )

        kontrol_literasi = kategori_literasi(
            (x20 + x21 + x22 + x23) / 4
        )

        # =================================================
        # TARGET
        # =================================================
        rata_target = (
            x24 + x25 + x26 + x27 + x28
        ) / 5

        status = kategori_3(rata_target)

        # =================================================
        # INSERT DATABASE
        # =================================================
        cursor.execute(
            """
            INSERT INTO dataset_pengguna (

                nama,
                jk,
                usia,
                pekerjaan,
                pendapatan,

                x01, x02, x03, x04, x05,
                x06, x07, x08, x09, x10,
                x11, x12, x13, x14,
                x15, x16, x17,
                x18, x19,
                x20, x21, x22, x23,
                x24, x25, x26, x27, x28,

                intensitas_ewallet,
                aktivitas_ewallet,
                intensitas_paylater,
                dampak_paylater,
                pengaruh_promo,
                sosial_lingkungan,
                media_gayahidup,
                kontrol_pengeluaran,
                kontrol_literasi,

                status,
                user_id

            )

            VALUES (

                %s, %s, %s, %s, %s,

                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s, %s,

                %s, %s, %s, %s, %s,
                %s, %s, %s, %s,

                %s,
                %s
            )
            """,
            (
                nama,
                jk,
                usia,
                pekerjaan,
                pendapatan,

                x01, x02, x03, x04, x05,
                x06, x07, x08, x09, x10,
                x11, x12, x13, x14,
                x15, x16, x17,
                x18, x19,
                x20, x21, x22, x23,
                x24, x25, x26, x27, x28,

                intensitas_ewallet,
                aktivitas_ewallet,
                intensitas_paylater,
                dampak_paylater,
                pengaruh_promo,
                sosial_lingkungan,
                media_gayahidup,
                kontrol_pengeluaran,
                kontrol_literasi,

                status,
                session["user_id"]
            )
        )

        db.commit()

        flash("Data pengguna berhasil disimpan")

        cursor.close()
        db.close()

        return redirect(url_for("prediksi.prediksi"))

    # =====================================================
    # GET DATA
    # =====================================================
    cursor.execute(
        """
        SELECT *
        FROM dataset_pengguna
        WHERE user_id = %s
        ORDER BY id DESC
        """,
        (session["user_id"],)
    )

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "dataset_pengguna.html",
        data=data
    )