import pandas as pd
import csv as csv
from sklearn.ensemble import RandomForestClassifier
from statistics import median

#   name
def get_title(name):
    title = str(name).split(",")
    if(len(title)>1):
        title = title[1].split(".")[0]
    return title

def convert_title(title):
    title_dic = {
        "Capt":          6,   # "Officer",
        "Col":           6,   # "Officer",
        "Major":         6,   # "Officer",
        "Jonkheer":      5,   # "Royalty",
        "Don":           5,   # "Royalty",
        "Sir" :          5,   # "Royalty",
        "Dr":            6,   # "Officer",
        "Rev":           6,   # "Officer",
        "the Countess":  5,   # "Royalty",
        "Dona":          5,   # "Royalty",
        "Mme":           3,   # "Mrs",
        "Mlle":          2,   # "Miss",
        "Ms":            3,   # "Mrs",
        "Mr" :           1,   # "Mr",
        "Mrs" :          3,   # "Mrs",
        "Miss" :         2,   # "Miss",
        "Master" :       4,   # "Master",
        "Lady" :         5,   # "Royalty"
    }
    if title in title_dic == True:
        return title_dic[title]
    else:
        return 0

# Cabin
def get_kind_of_cabin(name):
    if(name!=None):
        title = str(name)[0]
    return title

def convert_Cabin(embarked):
    if not embarked in (A, B, C, D, E, F, G):
        return 7 
    if embarked == A:
        return 0
    elif embarked == B:
        return 1
    elif embarked == C:
        return 2
    elif embark3d == D:
        return 3
    elif embarked == E:
        return 4
    elif embarked == F:
        return 5
    elif embarked == G:
        return 6

# Embarked
def MarkEmbarked(embarked):
    if not embarked in ('S', 'C', 'Q'):
        return None
    if embarked == 'S':
        return 0
    elif embarked == 'C':
        return 1
    elif embarked == 'Q':
        return 2

# person
def male_feamale_child(passenger):
    age,sex = passenger
    if age < 16:
        return 3
    else:
        return sex

# Load training data
train_df = pd.read_csv("train.csv", header=0)
test_df  = pd.read_csv("test.csv" , header=0)

# Convert "Sex" to be a dummy variable (female = 0, Male = 1)
train_df["Gender"] = train_df["Sex"].map({"female": 0, "male": 1}).astype(int)
test_df["Gender"]  =  test_df["Sex"].map({"female": 0, "male": 1}).astype(int)

# Complement the missing values of "Age" column with average of "Age"
train_age_comverted = train_df["Age"].dropna().mean()
test_age_comverted =  test_df["Age"].dropna().mean()

if len(train_df.Age[train_df.Age.isnull()]) > 0:
  train_df.loc[(train_df.Age.isnull()), "Age"] = train_age_comverted
if len(test_df.Age[test_df.Age.isnull()]) > 0:
  test_df.loc[(test_df.Age.isnull()), "Age"] = test_age_comverted

#Name
train_df['Title'] = train_df['Name'].apply(lambda x: get_title(x))
test_df['Title']  =  test_df['Name'].apply(lambda x: get_title(x))
train_df['Title'] = train_df['Title'].apply(lambda x: convert_title(x))
test_df['Title']  =  test_df['Title'].apply(lambda x: convert_title(x))

#Cabin
train_df['KindOfCabin'] = train_df['Cabin'].apply(lambda x: get_kind_of_cabin(x))
test_df['KindOfCabin']  =  test_df['Cabin'].apply(lambda x: get_kind_of_cabin(x))
train_df['KindOfCabin'] = train_df['KindOfCabin'].apply(lambda x: convert_title(x))
test_df['KindOfCabin']  =  test_df['KindOfCabin'].apply(lambda x: convert_title(x))

#Embarked
train_df["Embarked"]\
= train_df.apply(lambda row: MarkEmbarked(row["Embarked"]),axis=1)
test_df["Embarked"]\
= test_df.apply(lambda row: MarkEmbarked(row["Embarked"]),axis=1)

train_embarked_comverted = train_df["Embarked"].dropna().median()
test_embarked_comverted = test_df["Embarked"].dropna().median()

if len(train_df.Embarked[train_df.Embarked.isnull()]) > 0:
  train_df.loc[(train_df.Embarked.isnull()), "Embarked"] = train_embarked_comverted
if len(test_df.Embarked[test_df.Embarked.isnull()]) > 0:
    test_df.loc[(test_df.Embarked.isnull()), "Embarked"] = test_embarked_comverted

# FamilySize
train_df["FamilySize"] = train_df["SibSp"] + train_df["Parch"] + 1
test_df["FamilySize"] = test_df["SibSp"] + test_df["Parch"] + 1

train_df["person"] =\
train_df[["Age", "Gender"]].apply(male_feamale_child,axis=1)
test_df["person"] =\
test_df[["Age", "Gender"]].apply(male_feamale_child,axis=1)

# Fare
train_fare_converted = train_df["Fare"].dropna().median()
test_fare_converted = test_df["Fare"].dropna().median()

if len(train_df.Fare[train_df.Fare.isnull()]) > 0:
  train_df.loc[(train_df.Fare.isnull()), "Fare"] = train_fare_converted 
if len(test_df.Fare[test_df.Fare.isnull()]) > 0:
  test_df.loc[(test_df.Fare.isnull()), "Fare"] = test_fare_converted

# Copy test data's "PassengerId" column, and remove un-used columns
ids = test_df["PassengerId"].values

# remove un-used columns
train_df = train_df.drop(["KindOfCabin", "Gender", "Age","Cabin", "Name", "Embarked", "Sex", "SibSp", "Parch", "Ticket", "PassengerId"], axis=1)
test_df = test_df.drop(["KindOfCabin", "Gender", "Age", "Cabin", "Name", "Embarked", "Sex", "SibSp", "Parch", "Ticket",  "PassengerId"], axis=1)

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
