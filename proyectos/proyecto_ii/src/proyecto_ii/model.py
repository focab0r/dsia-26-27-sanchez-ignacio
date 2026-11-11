

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import joblib


X_VALUES = [
	"81",
	"82",
	"83",
	"86",
	"87",
	"88",
	"89"
]

TARGET = "target"



def train_model(df):

	X = df[X_VALUES]
	y = df[TARGET]
	scaler = StandardScaler()
	model = LinearRegression()

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
	scaled_numeric = scaler.fit_transform(X_train)
	scaled_numeric_df = pd.DataFrame(scaled_numeric, columns=X_VALUES)

	model.fit(scaled_numeric_df, y_train)

	scaled_numeric = scaler.transform(X_test)
	scaled_numeric_df = pd.DataFrame(scaled_numeric, columns=X_VALUES)

	print(f"[*] R2 score: {model.score(scaled_numeric_df, y_test)}")

	print("[*] Correlation matrix:")
	matrix = X.corr()
	print(matrix)

	return model


def save_model(model, path):
	joblib.dump(model, path)


def load_model(path):
	model = joblib.load(path)
	return model

def predict_model(model, df):
	result = model.predict(df)
	return result