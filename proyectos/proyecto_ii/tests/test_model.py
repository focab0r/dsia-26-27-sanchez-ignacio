

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split

from proyecto_ii.model import load_model, train_model, predict_model
from proyecto_ii.cli import DEFAULT_MODEL_PATH, predict



def test_load_model():
	model = load_model(DEFAULT_MODEL_PATH)
	assert str(type(model)) == "<class 'sklearn.linear_model._base.LinearRegression'>"

def test_predict_model():
	df = pd.read_csv("tests/data/prediction.csv")
	model = load_model(DEFAULT_MODEL_PATH)
	result = predict_model(model, df)
	assert str(type(result)) == "<class 'numpy.ndarray'>"

def test_train_model():
	df = pd.read_csv("data/training_data.csv")
	model = train_model(df)
	assert str(type(model)) == "<class 'sklearn.linear_model._base.LinearRegression'>"