import matplotlib
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
matplotlib.use('Agg')

df = pd.read_csv('./pca.csv')
features = ['y', 'x']
result = ['result']
# Separating out the features
x = df.loc[:, features].values
# Separating out the target
y = df.loc[:, result].values
# Standardizing the features
x = MinMaxScaler().fit_transform(x)
y = MinMaxScaler().fit_transform(y)
print("RAW:")
print(x)
print(y)

pca = PCA(n_components=1)
principalComponents = pca.fit_transform(x)
print("RESULT:")
print(principalComponents)
print("COMP:")
print(pca.components_)
print("SINGULAR:")
print(pca.singular_values_)
print("VAR:")
print(pca.explained_variance_)
print("RATIO:")
print(pca.explained_variance_ratio_)  