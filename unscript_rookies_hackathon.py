# -*- coding: utf-8 -*-
"""Unscript Rookies hackathon.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14S8Wk0wYyZDTIakCdSZ0Bjj8qyv6rPkQ

# Summary from Research paper and our manual data analysis

Manual Data Research:
1. all frauds are of type 'CASH_OUT' and 'TRANSFER'. Get rid of all other transactions in dataset.
2. while making transfer, old balance cannot be 0. Anomaly
3. Final amt and initial amt must differ by transaction amount.
4. Same applies for sender.
5. Create new col which have the error value of (transfer) - (mod(send amt - rec amt))

# Importing Libraries
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold, train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from sklearn.metrics import accuracy_score, confusion_matrix
from xgboost import XGBClassifier
import seaborn as sns
import pickle
# for plotting graph in jupyter cell
# %matplotlib inline

df = pd.read_csv("/content/drive/MyDrive/AIML_Unscript/AIML Dataset.csv")

"""# Data Preprocessing"""

df.describe()

df.isnull().sum()

"""#### We will now create 4 lists of the given data namely:

L1) The hour when fraud happened

L2) total trnascations then 

L3) fraud transactions

L4) valid transactions
 
"""

def fraud_per_hour(df):
    l1=[]
    l2=[]
    l3=[]
    l4=[]
    
    for h in df["step"].unique():
        t_df = df.loc[df["step"] == h]
        l1.append(h)
        l2.append(t_df.shape[0])
        l3.append(t_df.loc[t_df["isFraud"] == 1].shape[0])
        l4.append(t_df.loc[t_df["isFraud"] == 0].shape[0]) # shape[0] -> the no of rows is the number of records 
        
    return (l1, l2, l3, l4)


l1, l2, l3, l4 = fraud_per_hour(df)

# Create a new DataFrame
fraud_tx_per_hour = pd.DataFrame()

# Add new Columns to the DataFrame
fraud_tx_per_hour["houre"] = l1
fraud_tx_per_hour["total_tx"] = l2
fraud_tx_per_hour["fraud_tx"] = l3
fraud_tx_per_hour["valid_tx"] = l4
fraud_tx_per_hour.head(5)

len(l1)
#-

"""we have 743 hours' data

### Plots of the above data
"""

# plt.figure(figsize=(20, 50))
# these
plt.plot(l2,)

plt.plot(l3)

plt.plot(l4)

"""Day wise seperation of data"""

def get_day_data(df):
    day = []
    val = 1
    for i in df["houre"]:
        day.append(val)
        if i % 24 == 0:
            val += 1
    return day

day = get_day_data(fraud_tx_per_houre)

fraud_tx_per_houre["day"] = day
fraud_tx_per_houre

def plot_tx_per_day(df, day_num):
    fig, axes = plt.subplots(3, 1, figsize=(10, 20))
    axes[0].set_title(f"day - {day_num}")
    sns.barplot(x="houre", y="total_tx", data=df, ax=axes[0])
    sns.barplot(x="houre", y="fraud_tx", data=df, ax=axes[1])
    sns.barplot(x="houre", y="valid_tx", data=df, ax=axes[2])
    
d1 = fraud_tx_per_houre.loc[fraud_tx_per_houre["day"] == 1]
plot_tx_per_day(d1, 1)


#for all days
for day in range(1, 32):
  day_df = fraud_tx_per_houre.loc[fraud_tx_per_houre["day"] == day]
  plot_tx_per_day(day_df, day)

"""## Day wise insight - 

For Fraud transaction

Day 1+3+6+7+8+9+10:

most frauds were high during early and late hours (while mid day fraudulent transactions happened the least)

Day 2+5: 

compratively more during mid day hours

For valid transactions:

15 days:

mid day to late hours maximum valid transaction takes place so a constant pattern is observed  [ between 11- 21 hours]

## Hour wise plot
"""

plt.figure(figsize=(12, 150))
sns.barplot(y="houre", x="fraud_tx", orient="h", data=fraud_tx_per_houre)

"""# **Final Breakdown- data preprocessing:**

### Preprocesssing & Feature Engeenering



---



---


"""

fraudTransactions = df.loc[df.isFraud == 1].type.drop_duplicates().values 
print(list(fraudTransactions))

dfTransactions = df.loc[(df.type == 'TRANSFER') | (df.type == 'CASH_OUT')] 
dfFraud = dfTransactions['isFraud']
del dfTransactions['isFraud']

dfFraud.head()

dfTransactions.loc[dfTransactions.type == 'TRANSFER', 'type'] = 0 
dfTransactions.loc[dfTransactions.type == 'CASH_OUT', 'type'] = 1 
dfTransactions.type = dfTransactions.type.astype(int)

dfTransactions.head()

dfTransactionsFraud = dfTransactions.loc[dfFraud == 1] 
dfTransactionsNonFraud = dfTransactions.loc[dfFraud == 0] 
fractionAnomalyTransactionsInFraud = len(dfTransactionsFraud.loc[
                                                                (dfTransactionsFraud.oldbalanceDest == 0)
                                                                & (dfTransactionsFraud.newbalanceDest == 0) 
                                                                & (dfTransactionsFraud.amount)
                                                                ]) / (1.0 * len(dfTransactionsFraud)) 
print("Part of anomaly transactions among fraudulent: ",fractionAnomalyTransactionsInFraud )
fractionAnomalyTransactionsInNonFraud = len(dfTransactionsNonFraud.loc[ (dfTransactionsNonFraud.oldbalanceDest == 0) & (dfTransactionsNonFraud.newbalanceDest == 0) & (dfTransactionsNonFraud.amount) ]) / (1.0 * len(dfTransactionsNonFraud)) 
print("Part of anomaly transactions among regular (non-fraudulent): ",fractionAnomalyTransactionsInNonFraud )

dfTransactions.loc[
                   (dfTransactions.oldbalanceDest == 0) 
                   & (dfTransactions.newbalanceDest == 0) 
                   & (dfTransactions.amount != 0),  
                   ['oldbalanceDest', 'newbalanceDest']] = - 1

dfTransactions.tail()

dfTransactions.loc[ 
                   (dfTransactions.oldbalanceOrg == 0)
                   & (dfTransactions.newbalanceOrig == 0) & (dfTransactions.amount != 0), 
                   ['oldbalanceOrg', 'newbalanceOrig']] = np.nan

dfTransactions.head()

dfTransactions['errorbalanceDest'] = dfTransactions.oldbalanceDest + dfTransactions.amount - dfTransactions.newbalanceDest
dfTransactions['errorbalanceOrig'] = dfTransactions.newbalanceOrig + dfTransactions.amount - dfTransactions.oldbalanceOrg

dfTransactions.head()

dfTransactions = dfTransactions.drop( ['nameOrig', 'nameDest', 'isFlaggedFraud'], axis = 1)

dfTransactions.head()

list(dfTransactions)

randomState = 5
np.random.seed(randomState)
trainX, testX, trainY, testY = train_test_split(dfTransactions, dfFraud, test_size = 0.2, random_state = randomState )

weights = (dfFraud == 0).sum() / (1.0 * (dfFraud == 1).sum()) 
classifier = XGBClassifier(max_depth = 3, scale_pos_weight = weights, n_jobs = 4)
predictions = classifier.fit(trainX, trainY).predict_proba(testX)

from sklearn.metrics import average_precision_score
AURPC = average_precision_score(testY, predictions[:, 1])
AURPC

preddf=classifier.predict(testX)

preddf

from sklearn.metrics import classification_report 

print(classification_report(testY,preddf))

onerow = pd.DataFrame({'step': [459], 'type': [0], 'amount': [1153156], 'oldbalanceOrg': [1153156]
                       , 'newbalanceOrig': [0], 'oldbalanceDest': [-1], 'newbalanceDest': [-1], 'errorbalanceDest': [1153156]
                       , 'errorbalanceOrig': [0]})

onerow.head()

classifier.predict(onerow)

predictions

testX[testX.index==6020168]

testY[testY==1]

testX.shape

print(testX.iloc[0])

testX.isnull().sum()

classifier.save_model('5bajekamodel.bin')

from sklearn.metrics import accuracy_score, confusion_matrix,plot_confusion_matrix



matrix= plot_confusion_matrix( classifier,testX,testY)
matrix.ax_.set_title('Confusion Matrix',color='white')
plt.xlabel('Predicted label',color='white')
plt.ylabel('True label',color='white')
plt.gcf().axes[0].tick_params(color='white')
plt.gcf().axes[1].tick_params(color='white')
plt.gcf().set_size_inches(10,6)
plt.show()



"""### **Model Charecteristics**"""



"""### Model training"""



"""### Model Validation"""



"""# References:

1. Fraud Detection Technology in Payment Systems

Iulia Khlevna, Bohdan Koval

Taras Shevchenko National University of Kyiv, Volodymyrska str., 60, Kyiv, 01033, Ukraine

2. Financial Fraud Detection using Machine Learning Techniques

Matar Al Marri
mka8033@rit.edu

Ahmad AlAli
aaa4476@rit.edu
"""