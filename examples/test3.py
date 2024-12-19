import pandas as pd

data = {'valor': [1, 2, 0, -3, -1, -2, 3, -9]}
df = pd.DataFrame(data)

df['antes_max'] = (df['valor']>0).astype(int)

print(df)