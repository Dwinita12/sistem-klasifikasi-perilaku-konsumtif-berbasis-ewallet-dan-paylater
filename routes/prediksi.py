from flask import (
    Blueprint,
    render_template,
    redirect,
    flash,
    url_for,
    session
)

from utils.db import get_db

import os
import pickle

from .C45 import predict

prediksi_bp = Blueprint(
    "prediksi",
    __name__
)


# =========================================================
# HELPER KONVERSI KATEGORI
# =========================================================
def map_kategori_ke_angka(val):

    if not val:
        return None

    val = str(val).strip().lower()

    if val in [
        "rendah",
        "jarang",
        "lemah",
        "baik",
        "kecil"
    ]:
        return 0

    elif val in [
        "sedang",
        "cukup"
    ]:
        return 1

    elif val in [
        "tinggi",
        "sering",
        "kuat",
        "buruk",
        "besar"
    ]:
        return 2

    return None


# =========================================================
# ANGKA KE LABEL
# =========================================================
def angka_ke_label(val):

    try:
        val = int(val)

    except:

        return "Tidak diketahui"

    if val == 0:
        return "Rendah"

    elif val == 1:
        return "Sedang"

    elif val == 2:
        return "Tinggi"

    return "Tidak diketahui"


# =========================================================
# REKOMENDASI DAN INSIGHT
# =========================================================
def get_rekomendasi_dan_insight(hasil):

    if hasil == "Rendah":

        rekomendasi = (
            "Pertahankan kebiasaan keuangan yang sudah baik dengan "
            "tetap membuat anggaran bulanan, membedakan kebutuhan "
            "dan keinginan, serta menggunakan e-wallet dan paylater "
            "secara bijak."
        )

        insight = (
            "Hasil prediksi menunjukkan bahwa tingkat perilaku "
            "konsumtif pengguna berada pada kategori rendah. "
            "Pengguna cenderung mampu mengontrol pengeluaran "
            "dan tidak mudah terpengaruh promo maupun lingkungan."
        )

    elif hasil == "Sedang":

        rekomendasi = (
            "Mulailah lebih disiplin dalam mengatur pengeluaran "
            "dan mengurangi transaksi impulsif akibat promo, "
            "media sosial, maupun penggunaan paylater."
        )

        insight = (
            "Hasil prediksi menunjukkan bahwa tingkat perilaku "
            "konsumtif pengguna berada pada kategori sedang. "
            "Pengguna sudah memiliki kesadaran dalam mengatur "
            "keuangan, namun masih terdapat kecenderungan "
            "berbelanja di luar kebutuhan utama."
        )

    else:

        rekomendasi = (
            "Pengguna perlu meningkatkan kontrol keuangan dengan "
            "membatasi penggunaan e-wallet dan paylater, membuat "
            "catatan pengeluaran rutin, mengurangi pembelian "
            "berdasarkan keinginan sesaat, serta menghindari "
            "pengaruh lingkungan dan media sosial."
        )

        insight = (
            "Hasil prediksi menunjukkan bahwa tingkat perilaku "
            "konsumtif pengguna berada pada kategori tinggi. "
            "Pengguna cenderung sering melakukan pengeluaran "
            "berlebih dan masih kurang dalam pengendalian keuangan."
        )

    return rekomendasi, insight

    # =========================================================
# LIST DATA PREDIKSI
# =========================================================
@prediksi_bp.route("/prediksi")
def prediksi():

    if "user_id" not in session:

        flash(
            "Silakan login terlebih dahulu"
        )

        return redirect(
            url_for("auth.login")
        )

    db = get_db()

    cursor = db.cursor(
        dictionary=True
    )

    # =====================================================
    # DATA PENGGUNA
    # =====================================================
    cursor.execute("""
        SELECT *
        FROM dataset_pengguna
        WHERE user_id = %s
        ORDER BY id DESC
    """, (session["user_id"],))

    data = cursor.fetchall()

    # =====================================================
    # HASIL PREDIKSI
    # =====================================================
    cursor.execute("""
        SELECT *
        FROM hasil_prediksi
        WHERE user_id = %s
    """, (session["user_id"],))

    hasil_data = cursor.fetchall()

    hasil_dict = {

        h["id"]: h

        for h in hasil_data
    }

    # =====================================================
    # KONVERSI DATA
    # =====================================================
    for d in data:

        d["intensitas_ewallet_num"] = (
            map_kategori_ke_angka(
                d.get(
                    "intensitas_ewallet"
                )
            )
        )

        d["aktivitas_ewallet_num"] = (
            map_kategori_ke_angka(
                d.get(
                    "aktivitas_ewallet"
                )
            )
        )

        d["intensitas_paylater_num"] = (
            map_kategori_ke_angka(
                d.get(
                    "intensitas_paylater"
                )
            )
        )

        d["dampak_paylater_num"] = (
            map_kategori_ke_angka(
                d.get(
                    "dampak_paylater"
                )
            )
        )

        d["pengaruh_promo_num"] = (
            map_kategori_ke_angka(
                d.get(
                    "pengaruh_promo"
                )
            )
        )

        d["sosial_lingkungan_num"] = (
            map_kategori_ke_angka(
                d.get(
                    "sosial_lingkungan"
                )
            )
        )

        d["media_gayahidup_num"] = (
            map_kategori_ke_angka(
                d.get(
                    "media_gayahidup"
                )
            )
        )

        d["kontrol_pengeluaran_num"] = (
            map_kategori_ke_angka(
                d.get(
                    "kontrol_pengeluaran"
                )
            )
        )

        d["kontrol_literasi_num"] = (
            map_kategori_ke_angka(
                d.get(
                    "kontrol_literasi"
                )
            )
        )

        d["hasil"] = hasil_dict.get(
            d["id"]
        )

    cursor.close()
    db.close()

    return render_template(

        "prediksi.html",

        data=data
    )

    # =========================================================
# PROSES PREDIKSI
# =========================================================
@prediksi_bp.route("/proses_prediksi/<int:id>")
def proses_prediksi(id):

    if "user_id" not in session:

        flash(
            "Silakan login terlebih dahulu"
        )

        return redirect(
            url_for("auth.login")
        )

    db = get_db()

    cursor = db.cursor(
        dictionary=True
    )

    # =====================================================
    # AMBIL DATA PENGGUNA
    # =====================================================
    cursor.execute("""
        SELECT *
        FROM dataset_pengguna
        WHERE id = %s
        AND user_id = %s
    """, (

        id,
        session["user_id"]

    ))

    data = cursor.fetchone()

    if not data:

        cursor.close()
        db.close()

        flash(
            "Data tidak ditemukan"
        )

        return redirect(
            url_for("prediksi.prediksi")
        )

    # =====================================================
    # KONVERSI KE ANGKA
    # =====================================================
    sample = {

        "intensitas_ewallet":
            map_kategori_ke_angka(
                data["intensitas_ewallet"]
            ),

        "aktivitas_ewallet":
            map_kategori_ke_angka(
                data["aktivitas_ewallet"]
            ),

        "intensitas_paylater":
            map_kategori_ke_angka(
                data["intensitas_paylater"]
            ),

        "dampak_paylater":
            map_kategori_ke_angka(
                data["dampak_paylater"]
            ),

        "pengaruh_promo":
            map_kategori_ke_angka(
                data["pengaruh_promo"]
            ),

        "sosial_lingkungan":
            map_kategori_ke_angka(
                data["sosial_lingkungan"]
            ),

        "media_gayahidup":
            map_kategori_ke_angka(
                data["media_gayahidup"]
            ),

        "kontrol_pengeluaran":
            map_kategori_ke_angka(
                data["kontrol_pengeluaran"]
            ),

        "kontrol_literasi":
            map_kategori_ke_angka(
                data["kontrol_literasi"]
            )
    }

    # =====================================================
    # VALIDASI
    # =====================================================
    if None in sample.values():

        cursor.close()
        db.close()

        flash(
            "Data tidak valid."
        )

        return redirect(
            url_for("prediksi.prediksi")
        )

    # =====================================================
    # LOAD MODEL C4.5
    # =====================================================
    model_path = os.path.join(

        os.getcwd(),

        "model_c45.pkl"
    )

    if not os.path.exists(
        model_path
    ):

        cursor.close()
        db.close()

        flash(
            "Model C4.5 belum tersedia. "
            "Silakan buka menu Decision Tree terlebih dahulu."
        )

        return redirect(
            url_for("prediksi.prediksi")
        )

    with open(

        model_path,

        "rb"

    ) as f:

        model = pickle.load(f)

    # =====================================================
    # PREDIKSI
    # =====================================================
    hasil_prediksi = predict(

        model,

        sample
    )

    hasil_label = angka_ke_label(
        hasil_prediksi
    )

    # =====================================================
    # REKOMENDASI
    # =====================================================
    rekomendasi, insight = (
        get_rekomendasi_dan_insight(
            hasil_label
        )
    )

    # =====================================================
    # CEK DATA HASIL
    # =====================================================
   # =====================================================
# CEK DATA HASIL
# =====================================================
    cursor.execute("""
        SELECT *
        FROM hasil_prediksi
        WHERE id = %s
        AND user_id = %s
    """, (

        id,
        session["user_id"]

    ))

    cek = cursor.fetchone()

    # =====================================================
    # INSERT
    # =====================================================
    if not cek:

        cursor.execute("""
            INSERT INTO hasil_prediksi (

                id,
                nama,
                hasil,
                rekomendasi,
                insight,
                user_id

            )

            VALUES (

                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """, (

            id,
            data["nama"],
            hasil_label,
            rekomendasi,
            insight,
            session["user_id"]

        ))

    # =====================================================
    # UPDATE
    # =====================================================
    else:

        cursor.execute("""
            UPDATE hasil_prediksi

            SET

                nama = %s,
                hasil = %s,
                rekomendasi = %s,
                insight = %s

            WHERE id = %s
            AND user_id = %s
        """, (

            data["nama"],
            hasil_label,
            rekomendasi,
            insight,
            id,
            session["user_id"]

        ))

    db.commit()

    cursor.close()
    db.close()

    flash(
        "Prediksi berhasil menggunakan Decision Tree C4.5"
    )

    return redirect(
        url_for("prediksi.hasil")
    )
    # =========================================================
# HALAMAN HASIL PREDIKSI
# =========================================================
@prediksi_bp.route("/hasil")
def hasil():

    if "user_id" not in session:

        flash(
            "Silakan login terlebih dahulu"
        )

        return redirect(
            url_for("auth.login")
        )

    db = get_db()

    cursor = db.cursor(
        dictionary=True
    )

    cursor.execute("""
        SELECT

            hp.id,

            dp.nama,

            dp.intensitas_ewallet,
            dp.aktivitas_ewallet,
            dp.intensitas_paylater,
            dp.dampak_paylater,
            dp.pengaruh_promo,
            dp.sosial_lingkungan,
            dp.media_gayahidup,
            dp.kontrol_pengeluaran,
            dp.kontrol_literasi,
            
            dp.tanggal_input,
            
            hp.hasil,
            hp.rekomendasi,
            hp.insight

        FROM hasil_prediksi hp

        JOIN dataset_pengguna dp
            ON hp.id = dp.id

        WHERE hp.user_id = %s

        ORDER BY hp.id DESC
    """, (
        session["user_id"],
    ))

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(

        "hasil.html",

        data=data
    )