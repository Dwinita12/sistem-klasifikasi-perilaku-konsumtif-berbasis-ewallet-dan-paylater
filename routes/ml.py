from flask import (
    Blueprint,
    render_template,
    send_file
)

from utils.db import get_db
from .C45 import *

import os
import pickle
import pandas as pd

from io import BytesIO
from sklearn.model_selection import train_test_split

# =====================================================
# BLUEPRINT
# =====================================================
ml_bp = Blueprint(
    "ml",
    __name__
)


# =====================================================
# KONVERSI LABEL KE ANGKA
# =====================================================
def map_kategori(val):

    if val is None:
        return None

    val = str(
        val
    ).strip().lower()

    # angka
    if val == "0":
        return 0

    if val == "1":
        return 1

    if val == "2":
        return 2

    # rendah
    if val in [
        "rendah",
        "jarang",
        "lemah",
        "baik",
        "kecil"
    ]:

        return 0

    # sedang
    if val in [
        "sedang",
        "cukup"
    ]:

        return 1

    # tinggi
    if val in [
        "tinggi",
        "sering",
        "kuat",
        "buruk",
        "besar"
    ]:

        return 2

    return None


# =====================================================
# ANGKA KE LABEL
# =====================================================
def angka_ke_label(val):

    if val is None:
        return "Tidak diketahui"

    mapping = {

        0: "Rendah",

        1: "Sedang",

        2: "Tinggi"
    }

    return mapping.get(
        int(val),
        "Tidak diketahui"
    )

# =====================================================
# FITUR
# =====================================================
def get_fitur():

    return [

        "intensitas_ewallet",

        "aktivitas_ewallet",

        "intensitas_paylater",

        "dampak_paylater",

        "pengaruh_promo",

        "sosial_lingkungan",

        "media_gayahidup",

        "kontrol_pengeluaran",

        "kontrol_literasi"
    ]


# =====================================================
# NAMA FITUR TAMPILAN
# =====================================================
def nama_fitur_tampilan():

    return {

        "intensitas_ewallet":
            "Intensitas E-Wallet",

        "aktivitas_ewallet":
            "Aktivitas E-Wallet",

        "intensitas_paylater":
            "Intensitas Paylater",

        "dampak_paylater":
            "Dampak Paylater",

        "pengaruh_promo":
            "Pengaruh Promo",

        "sosial_lingkungan":
            "Sosial Lingkungan",

        "media_gayahidup":
            "Media Gaya Hidup",

        "kontrol_pengeluaran":
            "Kontrol Pengeluaran",

        "kontrol_literasi":
            "Kontrol Literasi"
    }


# =====================================================
# AMBIL DATASET DATABASE
# =====================================================
def ambil_dataset_training():

    db = get_db()

    cursor = db.cursor(
        dictionary=True
    )

    cursor.execute("""

        SELECT

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

        FROM dataset_training

    """)

    data = cursor.fetchall()

    cursor.close()

    db.close()

    return data


# =====================================================
# PREPROCESSING
# =====================================================
def preprocessing_dataset(
    data
):

    df_asli = pd.DataFrame(
        data
    )

    df_model = (
        df_asli.copy()
    )

    fitur = get_fitur()

    for col in fitur:

        df_model[col] = (
            df_model[col]
            .apply(
                map_kategori
            )
        )

    df_model["status"] = (

        df_model["status"]

        .apply(
            map_kategori
        )
    )

    df_model = (
        df_model
        .dropna()
    )

    df_asli = (
        df_asli.loc[
            df_model.index
        ]
        .copy()
    )

    return (
        df_model,
        df_asli
    )
    # =====================================================
# SPLIT DATASET
# =====================================================
def split_dataset(df_model):

    fitur = get_fitur()

    X = df_model[fitur]

    y = df_model["status"]

    X_train, X_test, y_train, y_test = train_test_split(

        X,

        y,

        test_size=0.2,

        random_state=42,

        stratify=y

    )

    return (

        X_train,

        X_test,

        y_train,

        y_test
    )


# =====================================================
# SIMPAN MODEL
# =====================================================
def simpan_model(
    model
):

    model_path = os.path.join(

        os.getcwd(),

        "model_c45.pkl"
    )

    with open(

        model_path,

        "wb"

    ) as f:

        pickle.dump(
            model,
            f
        )

    return model_path


# =====================================================
# LOAD MODEL
# =====================================================
def load_model():

    model_path = os.path.join(

        os.getcwd(),

        "model_c45.pkl"
    )

    if not os.path.exists(
        model_path
    ):

        return None

    with open(

        model_path,

        "rb"

    ) as f:

        model = pickle.load(
            f
        )

    return model

# =====================================================
# TRAIN MODEL C4.5
# =====================================================
def train_c45():

    data = ambil_dataset_training()

    if not data:
        return None

    df_model, df_asli = preprocessing_dataset(data)

    X_train, X_test, y_train, y_test = split_dataset(
        df_model
    )

    print("\n====================")
    print("DISTRIBUSI TRAIN")
    print(y_train.value_counts())

    print("\nDISTRIBUSI TEST")
    print(y_test.value_counts())
    print("====================")

    fitur = get_fitur()

    df_train = X_train.copy()
    df_train["status"] = y_train

    # =====================
    # BUILD TREE
    # =====================
    tree = build_tree(
        df_train,
        fitur,
        "status"
    )

    simpan_model(tree)

    # =====================
    # PREDIKSI TRAIN
    # =====================
    y_pred_train = predict_batch(
        tree,
        X_train
    )

    # =====================
    # PREDIKSI TEST
    # =====================
   # =====================
# PREDIKSI TEST
# =====================
    y_pred_test = predict_batch(
        tree,
        X_test
    )

    print("Jumlah X_test =", len(X_test))
    print("Jumlah y_test =", len(y_test))
    print("Jumlah y_pred_test =", len(y_pred_test))

    print("ISI y_pred_test =")
    print(y_pred_test)

    print(
        "Jumlah prediksi None =",
        sum(
            1
            for x in y_pred_test
            if x is None
        )
    )

    # =====================
    # AKURASI
    # =====================
    acc_train = accuracy(
        list(y_train),
        y_pred_train
    )

    acc_test = accuracy(
        list(y_test),
        y_pred_test
    )
    # =====================
    # CONFUSION MATRIX
    # =====================
    cm = confusion_matrix_manual(
        list(y_test),
        y_pred_test
    )

    # =====================
    # CLASSIFICATION REPORT
    # =====================
    report = classification_report_manual(
        list(y_test),
        y_pred_test
    )

    return {
        "tree": tree,
        "df_model": df_model,
        "df_asli": df_asli,
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "y_pred_test": y_pred_test,
        "acc_train": acc_train,
        "acc_test": acc_test,
        "cm": cm,
        "report": report
    }
    # =====================================================
# HALAMAN DECISION TREE C4.5
# =====================================================
@ml_bp.route(
    "/decision-tree"
)
def decision_tree():

    hasil = train_c45()

    if hasil is None:

        return render_template(

            "decision_tree.html",

            error="Data training kosong."
        )

    tree = hasil["tree"]

    graph = export_tree_graph(tree)

    graph.render(
        "static/tree",
        cleanup=True
    )

    df_model = hasil["df_model"]

    X_train = hasil["X_train"]

    X_test = hasil["X_test"]

    y_train = hasil["y_train"]

    y_test = hasil["y_test"]

    y_pred_test = hasil[
        "y_pred_test"
    ]

    acc_train = hasil[
        "acc_train"
    ]

    acc_test = hasil[
        "acc_test"
    ]

    cm = hasil[
        "cm"
    ]

    report = hasil[
        "report"
    ]

    fitur = get_fitur()

    fitur_label = (
        nama_fitur_tampilan()
    )

    # =====================================
    # DISTRIBUSI LABEL
    # =====================================
    distribusi_label = {

        "Rendah":

            int(
                (
                    df_model["status"]
                    == 0
                ).sum()
            ),

        "Sedang":

            int(
                (
                    df_model["status"]
                    == 1
                ).sum()
            ),

        "Tinggi":

            int(
                (
                    df_model["status"]
                    == 2
                ).sum()
            )
    }

    # =====================================
    # RULES
    # =====================================
    rules = generate_rules(
        tree
    )

    rule_text = "\n".join(
        rules
    )

    # =====================================
    # VISUALISASI POHON
    # =====================================
    tree_visual = tree_to_text(
        tree
    )

    # =====================================
    # NODE DETAILS
    # =====================================
    df_node = (
        X_train.copy()
    )

    df_node[
        "status"
    ] = y_train

    node_details = (

        collect_node_details(

            df_node,

            fitur,

            "status"
        )
    )

    # =====================================
    # SUMMARY
    # =====================================
    summary = tree_summary(
        tree
    )

    summary["total_data"] = (
        len(df_model)
    )

    summary["total_train"] = (
        len(X_train)
    )

    summary["total_test"] = (
        len(X_test)
    )

    summary["criterion"] = (
        "Gain Ratio (C4.5)"
    )
        # =====================================
    # FEATURE IMPORTANCE C4.5
    # =====================================
    feature_importance = []

    for feature in fitur:

        ratio = gain_ratio(

            df_node,

            feature,

            "status"
        )

        feature_importance.append({

            "feature":

                fitur_label.get(
                    feature,
                    feature
                ),

            "importance":

                round(
                    ratio,
                    6
                )
        })

    feature_importance = sorted(

        feature_importance,

        key=lambda x:

        x["importance"],

        reverse=True
    )

    # =====================================
    # DATA LATIH
    # =====================================
    data_latih = []

    for idx in X_train.index:

        row = df_model.loc[idx]

        data_latih.append({

            "intensitas_ewallet":

                angka_ke_label(
                    row[
                        "intensitas_ewallet"
                    ]
                ),

            "aktivitas_ewallet":

                angka_ke_label(
                    row[
                        "aktivitas_ewallet"
                    ]
                ),

            "intensitas_paylater":

                angka_ke_label(
                    row[
                        "intensitas_paylater"
                    ]
                ),

            "dampak_paylater":

                angka_ke_label(
                    row[
                        "dampak_paylater"
                    ]
                ),

            "pengaruh_promo":

                angka_ke_label(
                    row[
                        "pengaruh_promo"
                    ]
                ),

            "sosial_lingkungan":

                angka_ke_label(
                    row[
                        "sosial_lingkungan"
                    ]
                ),

            "media_gayahidup":

                angka_ke_label(
                    row[
                        "media_gayahidup"
                    ]
                ),

            "kontrol_pengeluaran":

                angka_ke_label(
                    row[
                        "kontrol_pengeluaran"
                    ]
                ),

            "kontrol_literasi":

                angka_ke_label(
                    row[
                        "kontrol_literasi"
                    ]
                ),

            "status":

                angka_ke_label(
                    row["status"]
                )
        })

    # =====================================
    # DATA UJI
    # =====================================
    data_uji = []

    for i, idx in enumerate(

        X_test.index

    ):

        row = df_model.loc[idx]

        data_uji.append({

            "intensitas_ewallet":

                angka_ke_label(
                    row[
                        "intensitas_ewallet"
                    ]
                ),

            "aktivitas_ewallet":

                angka_ke_label(
                    row[
                        "aktivitas_ewallet"
                    ]
                ),

            "intensitas_paylater":

                angka_ke_label(
                    row[
                        "intensitas_paylater"
                    ]
                ),

            "dampak_paylater":

                angka_ke_label(
                    row[
                        "dampak_paylater"
                    ]
                ),

            "pengaruh_promo":

                angka_ke_label(
                    row[
                        "pengaruh_promo"
                    ]
                ),

            "sosial_lingkungan":

                angka_ke_label(
                    row[
                        "sosial_lingkungan"
                    ]
                ),

            "media_gayahidup":

                angka_ke_label(
                    row[
                        "media_gayahidup"
                    ]
                ),

            "kontrol_pengeluaran":

                angka_ke_label(
                    row[
                        "kontrol_pengeluaran"
                    ]
                ),

            "kontrol_literasi":

                angka_ke_label(
                    row[
                        "kontrol_literasi"
                    ]
                ),

            "status":

                angka_ke_label(
                    row["status"]
                ),

            "prediksi":

                angka_ke_label(
                    y_pred_test[i]
                )
        })
            # =====================================
    # RENDER TEMPLATE
    # =====================================
    print("CM =", cm)
    print("REPORT =", report)
    return render_template(

        "decision_tree.html",

        error=None,

        acc_train=acc_train,

        acc_test=acc_test,

        cm=cm,

        report=report,

        summary=summary,

        distribusi_label=distribusi_label,

        feature_importance=feature_importance,

        rule_text=rule_text,

        tree_visual=tree_visual,

        tree_image="tree.png",

        node_details=node_details,

        data_latih=data_latih,

        data_uji=data_uji,

        image=None
    )

# =====================================================
# DOWNLOAD HASIL SPLITTING
# =====================================================
# =====================================================
# DOWNLOAD HASIL SPLITTING
# =====================================================
@ml_bp.route(
    "/decision-tree/download-splitting"
)
def download_splitting():

    hasil = train_c45()

    if hasil is None:

        return (
            "Data training kosong."
        )

    X_train = hasil[
        "X_train"
    ]

    X_test = hasil[
        "X_test"
    ]

    y_pred_test = hasil[
        "y_pred_test"
    ]

    df_asli = hasil[
        "df_asli"
    ]

    # ==========================
    # DATA LATIH
    # ==========================
    data_latih = (
        df_asli.loc[
            X_train.index
        ]
        .copy()
    )

    # ==========================
    # DATA UJI
    # ==========================
    data_uji = (
        df_asli.loc[
            X_test.index
        ]
        .copy()
    )

    # Nomor urut
    data_latih.insert(
        0,
        "No",
        range(
            1,
            len(data_latih) + 1
        )
    )

    data_uji.insert(
        0,
        "No",
        range(
            1,
            len(data_uji) + 1
        )
    )

    # Prediksi label
    data_uji[
        "prediksi"
    ] = [

        angka_ke_label(x)

        for x in y_pred_test
    ]

    output = BytesIO()

    with pd.ExcelWriter(

        output,

        engine="openpyxl"

    ) as writer:

        data_latih.to_excel(

            writer,

            sheet_name="Data Latih",

            index=False
        )

        data_uji.to_excel(

            writer,

            sheet_name="Data Uji",

            index=False
        )

    output.seek(0)

    return send_file(

        output,

        as_attachment=True,

        download_name=
        "hasil_data_splitting_c45.xlsx",

        mimetype=
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )