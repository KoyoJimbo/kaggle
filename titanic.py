import pandas as pd
import csv as csv
from sklearn.ensemble import RandomForestClassifier

# Load training data
train_df = pd.read_csv("train.csv", header=0)

# Convert "Sex" to be a dummy variable (female = 0, Male = 1)
train_df["Gender"] = train_df["Sex"].map({"female": 0, "male": 1}).astype(int)

# not move ###########
"""
train_df.Embarked[ train_df.Embarked.isnull() ]\
= train_df.Embarked.dropna().mode().values

train_df["Embarke"]\
= train_df["Embarked"].map({"C": 0, "Q": 1, "S": 2,NA:3}).astype(int)
"""
######################


######################
train_df["FamilySize"] = train_df["SibSp"] + train_df["Parch"] + 1
######################


train_df.head(6)

######################
def male_feamale_child(passenger):
    age,sex = passenger
    if age < 16:
        return 3
    else:
        return sex

train_df["person"] =\
train_df[["Age", "Gender"]].apply(male_feamale_child,axis=1)
######################

# Complement the missing values of "Age" column with average of "Age"
median_age = train_df["Age"].dropna().mean()
if len(train_df.Age[train_df.Age.isnull()]) > 0:
  train_df.loc[(train_df.Age.isnull()), "Age"] = median_age

######################
median_fare = train_df["Fare"].dropna().mean()
if len(train_df.Fare[train_df.Fare.isnull()]) > 0:
  train_df.loc[(train_df.Fare.isnull()), "Fare"] = median_fare
######################


# remove un-used columns
train_df = train_df.drop(["Name", "Sex", "SibSp", "Parch", "Ticket", "Embarked", "Cabin", "PassengerId"], axis=1)
train_df.head(6)

# Load test data, Convert "Sex" to be a dummy variable
test_df = pd.read_csv("test.csv", header=0)
test_df["Gender"] = test_df["Sex"].map({"female": 0, "male": 1}).astype(int)


# not move ###########
"""
test_df.Embarked[ test_df.Embarked.isnull() ]\
= test_df.Embarked.dropna().mode().values

test_df["Embarke"]\
= test_df["Embarked"].map({"C": 0, "Q": 1, "S": 2,NA:3}).astype(int)
"""
######################


######################
test_df["FamilySize"] = test_df["SibSp"] + test_df["Parch"] + 1
######################


######################
test_df["person"] =\
test_df[["Age", "Gender"]].apply(male_feamale_child,axis=1)
######################

# Complement the missing values of "Age" column with average of "Age"
median_age = test_df["Age"].dropna().mean()
if len(test_df.Age[test_df.Age.isnull()]) > 0:
  test_df.loc[(test_df.Age.isnull()), "Age"] = median_age

######################
median_fare = test_df["Fare"].dropna().mean()
if len(test_df.Fare[test_df.Fare.isnull()]) > 0:
  test_df.loc[(test_df.Fare.isnull()), "Fare"] = median_fare

######################


# Copy test data's "PassengerId" column, and remove un-used columns
ids = test_df["PassengerId"].values
test_df = test_df.drop(["Name", "Sex", "SibSp", "Parch", "Ticket", "Embarked", "Cabin",  "PassengerId"], axis=1)
test_df.head(3)

# Predict with "Random Forest"
train_data = train_df.values
test_data = test_df.values
model = RandomForestClassifier(n_estimators=100)
output = model.fit(train_data[0::, 1::], train_data[0::, 0]).predict(test_data).astype(int)

# export result to be "titanic_submit.csv"
submit_file = open("titanic_submit.csv", "w")
file_object = csv.writer(submit_file)
file_object.writerow(["PassengerId", "Survived"])

file_object.writerows(zip(ids, output))
submit_file.close()
