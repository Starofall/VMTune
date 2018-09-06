import matplotlib
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

matplotlib.use('Agg')
#
df = pd.read_csv('./anova.csv')
features = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
result = ['result']
# Separating out the features
x = df.loc[:, features].values
# Separating out the target
y = df.loc[:, result].values
# # Standardizing the features
x = MinMaxScaler().fit_transform(x)
y = MinMaxScaler().fit_transform(y)
# print("RAW:")
# print(x)
# print(y)

import statsmodels.api as sm

results = sm.OLS(y, x).fit()
print(results.summary())

moore_lm = ols('result ~ C(x, Sum)*C(y, Sum)',data=df).fit()
table = sm.stats.anova_lm(results, typ=2)
print(table)