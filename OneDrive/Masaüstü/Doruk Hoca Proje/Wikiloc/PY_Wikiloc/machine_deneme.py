import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from scipy.stats import zscore
import matplotlib.pyplot as plt

# Load the Excel file
data_path = r'C:\Users\aylin\OneDrive\Masaüstü\Wikiloc\main_hiking_data.xlsx'
data = pd.read_excel(data_path)

# Step 1: Outlier Removal using Z-score method
def remove_outliers_zscore(df, columns, threshold=3):
    z_scores = df[columns].apply(zscore)
    return df[(z_scores.abs() < threshold).all(axis=1)]

# Apply Z-score based outlier removal
numerical_columns = data.select_dtypes(include=['float64', 'int64']).columns
cleaned_data = remove_outliers_zscore(data, numerical_columns)
print(f"Original data shape: {data.shape}")
print(f"Cleaned data shape: {cleaned_data.shape}")

# Step 2: Encoding
encoded_data = pd.get_dummies(cleaned_data, columns=['Region'], drop_first=True)

# Step 3: Scaling
numerical_columns = [
    'Total Length (km)', 'Highest Point (m)', 'Lowest Point (m)',
    'Elevation Gain', 'Elevation Loss', 'Steep Sections',
    'Longest Gain Section Total Gain', 'Longest Gain Section Distance',
    'Most Gain Section Total Gain', 'Most Gain Section Distance',
    'Direction Changes'
]
scaler = StandardScaler()
encoded_data[numerical_columns] = scaler.fit_transform(encoded_data[numerical_columns])

# Step 4: Elbow Method
X = encoded_data.select_dtypes(include=['float64', 'int64', 'uint8'])
inertia = []
K = range(1, 10)
for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X)
    inertia.append(kmeans.inertia_)
plt.figure(figsize=(8, 4))
plt.plot(K, inertia, 'bo-')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia')
plt.title('Elbow Method for Optimal k')
plt.show()

# Step 5: Apply K-Means with k=3
optimal_k = 3
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
encoded_data['Cluster'] = kmeans.fit_predict(X)

# Step 6: Cluster Summary
numeric_encoded_data = encoded_data.select_dtypes(include=['float64', 'int64', 'uint8'])
numeric_encoded_data['Cluster'] = encoded_data['Cluster']
cluster_summary = numeric_encoded_data.groupby('Cluster').mean()
print(cluster_summary)

# Step 7: Label Clusters
cluster_labels = {0: 'Moderate', 1: 'Difficult', 2: 'Easy'}
encoded_data['Cluster Difficulty'] = encoded_data['Cluster'].map(cluster_labels)

# Step 8: Compare with Technical Difficulty
comparison = encoded_data[['Technical difficulty', 'Cluster Difficulty']]
print(comparison.head())
agreement = (comparison['Technical difficulty'] == comparison['Cluster Difficulty']).mean()
print(f"Agreement between cluster-based and technical difficulty labels: {agreement:.2%}")
