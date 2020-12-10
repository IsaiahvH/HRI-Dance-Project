# Last update: 2020-12-10
# Imports:
import pandas as pd  # For DataFrame
import numpy as np  # For its arrays
from sklearn import svm  # To train a simple SVM for testing

# Read in data and convert labels to vector:
df = pd.read_csv(r"TrainingData/TestResults_Emma1.txt", index_col=0)
print(df.head())

# Extract all labels:
labels = df['Label'].unique()
print("All labels:", labels)

# Convert into binary array, that can be used as target array:
test = np.array((labels[:] == "Clap")).astype(int)
print("Example of target vector:", test)

# Split in training and testing data:
train_share = 0.8
msk = np.random.rand(len(df)) < train_share
train = df[msk]
test = df[~msk]

# Confirm the split:
print("Total nr. of samples:", len(df))
print("Training sampels:", len(train))
print("Testing samples:", len(test))

# Test a simple SVM:
y_train = pd.get_dummies(train.Label).to_numpy()
print(y_train)

# TODO: Pick the corresponding X data and train the very simple SVM:
# https://scikit-learn.org/stable/modules/svm.html
