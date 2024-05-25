import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

def testing(a,b,c,d):

    df = pd.read_csv("Test_data.csv")
    Y = df.loc[:,["Target"]]
    X = df.drop(columns=["Target"])
    X_train,X_test,Y_train,Y_test = train_test_split(X,Y)
    model = DecisionTreeClassifier()
    model.fit(X_train, Y_train)
    pred = model.predict([[a,b,c,d]])
    return pred[0]

