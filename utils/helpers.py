import numpy as np

def map_kategori(val):
    if not val:
        return 0
    val = str(val).lower()
    if val == "rendah":
        return 0
    elif val == "sedang":
        return 1
    else:
        return 2


def generate_insight(hasil, model=None):
    if model:
        fitur = ['pengeluaran','frekuensi','kontrol_keuangan','lingkungan']
        importance = model.feature_importances_
        idx = np.argmax(importance)
        return f"Perilaku dipengaruhi oleh faktor {fitur[idx]}"

    if hasil == "Rendah":
        return "Pengeluaran masih terkontrol dengan baik"
    elif hasil == "Sedang":
        return "Mulai ada kecenderungan konsumtif"
    else:
        return "Perilaku konsumtif tinggi, perlu kontrol lebih"