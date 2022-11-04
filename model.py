import pandas as pd
import pickle
df=pd.read_csv('ready_to_model.csv')
df=df.drop(['Unnamed: 0'], axis=1)
#Separating X and y
X=df.drop(['Churn'], axis=1)
y=df['Churn']
from xgboost import XGBClassifier
XGB = XGBClassifier()
XGB.fit(X, y)
pickle.dump(XGB,open('model.pkl','wb') )
