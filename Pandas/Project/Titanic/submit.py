import pandas as pd
from sklearn.ensemble import RandomForestClassifier

train_df = pd.read_csv('train.csv')
test_df = pd.read_csv('test.csv')

def preprocess_data(df):
    data = df.copy()
    data['Age'] = data.groupby(['Pclass', 'Sex'])['Age'].transform(lambda x: x.fillna(x.median()))
    data['Fare'] = data['Fare'].fillna(data['Fare'].median())
    data['FamilySize'] = data['SibSp'] + data['Parch'] + 1
    data['IsAlone'] = (data['FamilySize'] == 1).astype(int)
    data['FarePerPerson'] = data['Fare'] / data['FamilySize']
    data['Title'] = data['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)
    data['Title'] = data['Title'].replace(['Lady', 'Countess','Capt', 'Col',
                                         'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')
    data['Title'] = data['Title'].replace('Mlle', 'Miss')
    data['Title'] = data['Title'].replace('Ms', 'Miss')
    data['Title'] = data['Title'].replace('Mme', 'Mrs')
    data['Sex'] = data['Sex'].map({'female': 1, 'male': 0}).astype(int)
  
    features = ['Pclass', 'Sex', 'Age', 'Fare', 'Title', 'FamilySize', 'IsAlone', 'FarePerPerson']
    data = data[features]
    
    data = pd.get_dummies(data, columns=['Title'], drop_first=False)
    
    return data

X_train = preprocess_data(train_df)
X_test = preprocess_data(test_df)

y_train = train_df['Survived']
X_train, X_test = X_train.align(X_test, join='left', axis=1, fill_value=0)

model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
submission = pd.DataFrame({
    "PassengerId": test_df["PassengerId"],
    "Survived": predictions})

submission.to_csv('my_submission2.csv', index=False)

print("预测完成，文件 my_submission2.csv 已生成在当前目录下！")