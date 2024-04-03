import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Baca data dari file CSV dengan delimiter koma
flpath = r'D:\data_renang.xlsx'
data = pd.read_excel(flpath)
print(data.shape)

# Definisikan variabel input
kecepatan_per_m = ctrl.Antecedent(np.arange(1, 2.5, 0.1), 'kecepatan_per_m')
jarak_maksimal = ctrl.Antecedent(np.arange(100, 301, 10), 'jarak_maksimal')
jarak_10_menit = ctrl.Antecedent(np.arange(400, 1001, 50), 'jarak_10_menit')

# Definisikan variabel output
tingkat_kehebatan_renang = ctrl.Consequent(np.arange(0, 101, 1), 'tingkat_kehebatan_renang')

# Definisikan fungsi keanggotaan untuk variabel input dan output
kecepatan_per_m.automf(3)
jarak_maksimal.automf(3)
jarak_10_menit.automf(3)

tingkat_kehebatan_renang['rendah'] = fuzz.trimf(tingkat_kehebatan_renang.universe, [0, 0, 40])
tingkat_kehebatan_renang['sedang'] = fuzz.trimf(tingkat_kehebatan_renang.universe, [30, 50, 70])
tingkat_kehebatan_renang['tinggi'] = fuzz.trimf(tingkat_kehebatan_renang.universe, [60, 80, 100])

# Aturan fuzzy
rule1 = ctrl.Rule(kecepatan_per_m['poor'] | jarak_maksimal['poor'] | jarak_10_menit['poor'], tingkat_kehebatan_renang['rendah'])
rule2 = ctrl.Rule(kecepatan_per_m['average'] | jarak_maksimal['average'] | jarak_10_menit['average'], tingkat_kehebatan_renang['sedang'])
rule3 = ctrl.Rule(kecepatan_per_m['good'] | jarak_maksimal['good'] | jarak_10_menit['good'], tingkat_kehebatan_renang['tinggi'])

# Buat sistem kontrol fuzzy
tingkat_kehebatan_renang_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tingkat_kehebatan_renang_sim = ctrl.ControlSystemSimulation(tingkat_kehebatan_renang_ctrl)

# Inisialisasi list untuk menyimpan hasil
hasil_tingkat_kehebatan_renang = []

# Iterasi melalui setiap record dalam data
for index, row in data.iterrows():
    # Masukkan nilai variabel input dari data yang dibaca
    tingkat_kehebatan_renang_sim.input['kecepatan_per_m'] = row['kecepatan_per_m']
    tingkat_kehebatan_renang_sim.input['jarak_maksimal'] = row['jarak_maksimal']
    tingkat_kehebatan_renang_sim.input['jarak_10_menit'] = row['jarak_10_menit']

    # Hitung nilai variabel output
    tingkat_kehebatan_renang_sim.compute()

    # Simpan hasil
    hasil_tingkat_kehebatan_renang.append(tingkat_kehebatan_renang_sim.output['tingkat_kehebatan_renang'])

# Tambahkan hasil ke data frame
data['hasil_tingkat_kehebatan_renang'] = hasil_tingkat_kehebatan_renang

# Buat fungsi untuk mengkategorikan tingkat kehebatan
def kategori_tingkat_kehebatan(nilai):
    if nilai <= 45:
        return 'Rendah'
    elif nilai <= 60:
        return 'Sedang'
    else:
        return 'Tinggi'

# Tambahkan kolom kategori tingkat kehebatan pada DataFrame
data['kategori_tingkat_kehebatan'] = data['hasil_tingkat_kehebatan_renang'].apply(kategori_tingkat_kehebatan)

# Simpan ke file Excel
data.to_excel('D:\hasil_fuzzy_renang.xlsx', index=False)


