import pandas as pd
import numpy as np

# Generate random data for the dataset
np.random.seed(0)  # for reproducibility

# Generate random values for kecepatan_per_m, jarak_maksimal, and jarak_10_menit
kecepatan_per_m = np.random.uniform(1, 2.5, 50)
jarak_maksimal = np.random.uniform(100, 301, 50)
jarak_10_menit = np.random.uniform(400, 1000, 50)

# Create the DataFrame
data = pd.DataFrame({
    'kecepatan_per_m': kecepatan_per_m,
    'jarak_maksimal': jarak_maksimal,
    'jarak_10_menit': jarak_10_menit
})

# Save the dataset to an Excel file
data.to_excel(r'D:\data_renang.xlsx', index=False)

