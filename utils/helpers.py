import numpy as np

def map_kategori(val):
    if not val:
        return 0

    val = str(val).lower().strip()

    if val == "rendah":
        return 0
    elif val == "sedang":
        return 1
    else:
        return 2


def generate_insight_rekomendasi(hasil, model=None):

    insight_model = ""

    if model is not None:
        fitur = [
            'Intensitas E-Wallet',
            'Aktivitas E-Wallet',
            'Intensitas Paylater',
            'Dampak Paylater',
            'Pengaruh Promo',
            'Sosial Lingkungan',
            'Media Gaya Hidup',
            'Kontrol Pengeluaran',
            'Kontrol Literasi'
        ]

        importance = model.feature_importances_
        idx = np.argmax(importance)

        insight_model = (
            f" Faktor yang paling berpengaruh terhadap hasil klasifikasi adalah "
            f"{fitur[idx]}."
        )

    if hasil == "Rendah":

        insight = (
            "Hasil prediksi menunjukkan bahwa tingkat perilaku konsumtif pengguna "
            "berada pada kategori rendah. Pengguna cenderung mampu mengontrol "
            "pengeluaran dan tidak mudah terpengaruh oleh promo maupun lingkungan."
            + insight_model
        )

        rekomendasi = (
            "Pertahankan kebiasaan keuangan yang sudah baik dengan tetap membuat "
            "anggaran bulanan, membedakan kebutuhan dan keinginan, serta "
            "menggunakan E-Wallet dan Paylater secara bijak."
        )

    elif hasil == "Sedang":

        insight = (
            "Hasil prediksi menunjukkan bahwa tingkat perilaku konsumtif pengguna "
            "berada pada kategori sedang. Pengguna mulai menunjukkan kecenderungan "
            "perilaku konsumtif sehingga perlu meningkatkan pengelolaan keuangan."
            + insight_model
        )

        rekomendasi = (
            "Mulailah menyusun prioritas pengeluaran, membatasi penggunaan "
            "Paylater, dan mengurangi pembelian yang dipengaruhi promo agar "
            "kondisi keuangan tetap stabil."
        )

    else:

        insight = (
            "Hasil prediksi menunjukkan bahwa tingkat perilaku konsumtif pengguna "
            "berada pada kategori tinggi. Pengguna memiliki kecenderungan kuat "
            "untuk melakukan pembelian berlebihan dan lebih mudah dipengaruhi "
            "oleh promo, lingkungan, maupun gaya hidup."
            + insight_model
        )

        rekomendasi = (
            "Lakukan evaluasi terhadap pola pengeluaran, batasi penggunaan "
            "Paylater, buat anggaran yang lebih ketat, dan fokus pada kebutuhan "
            "utama untuk mengurangi tingkat perilaku konsumtif."
        )

    return insight, rekomendasi
