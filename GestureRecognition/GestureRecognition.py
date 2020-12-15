# Last update: 2020-12-15
# Imports:
import glob  # To loop through files
import os  # To find the current working directory
import pandas as pd  # For DataFrame
import numpy as np  # For its arrays
from sklearn import svm, metrics  # To train a simple SVM for testing
from joblib import dump

# Read in data and convert labels to vector:
path = os.path.join(os.getcwd(), "TrainingData")
all_files = glob.glob(os.path.join(path, "*.txt"))
df = pd.concat((pd.read_csv(f, index_col=0) for f in all_files))
df.reset_index(drop=True, inplace=True)
print(df.head())
print("Input data shape:", df.shape)

# Swap the bad cols:
cols = list(df)
cols[75], cols[73], cols[74] = cols[73], cols[74], cols[75]
df = df.loc[:, cols]

# Only take x and y, not visibility (v), and drop the kiss gesture:
df = df.filter(regex='^Label|^[0-9]{1,2}_[^v]', axis=1)
df = df[df.Label != "Kiss"]

# Extract all labels:
labels = df['Label'].unique()
print("All labels:", labels)

# Factorise the categories:
df["label_int"] = pd.factorize(df.Label)[0]
print(df.tail())

# Split in training and testing data:
train_share = 0.8
msk = np.random.rand(len(df)) < train_share
train = df[msk]
test = df[~msk]

# # Convert into binary array, that can be used as target array:
# one_target = np.array((labels[:] == "Clap")).astype(int)
# print("Example of target vector:", one_target)
#
# # Get the binary array for the entire training set (to be used later):
# train_target = pd.get_dummies(train.Label).to_numpy()
# print(train_target)

# Confirm the split:
print("Total nr. of samples:", len(df))
print("Training sampels:", len(train))
print("Testing samples:", len(test))

# Test a simple SVM:
y_train = train.label_int.to_numpy()
X_train = train.loc[:, "0_x":"24_y"].to_numpy()  # or until v
y_test = test.label_int.to_numpy()
X_test = test.loc[:, "0_x":"24_y"].to_numpy()  # or until v

# clf = make_pipeline(StandardScaler(), svm.SVC())
clf = svm.SVC()
clf.fit(X_train, y_train)

predictions = clf.predict(X_test)
print(predictions)
print(y_test)
accuracy = metrics.accuracy_score(y_test, predictions)
print(accuracy)
print(labels)

# Save the SVM:
dump(clf, 'SVM_six_gestures.joblib')
