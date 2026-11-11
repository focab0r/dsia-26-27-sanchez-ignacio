

import argparse
import pandas as pd

from proyecto_ii.loader import load_data
from proyecto_ii.preprocess import preprocess_data, correct_values
from proyecto_ii.model import train_model, save_model, load_model, predict_model


DEFAULT_LOAD_PATH = "/home/focab0r/Downloads/DSIA"
DEFAULT_TRAINING_PATH = "data/training_data.csv"
DEFAULT_MODEL_PATH = "data/model.joblib"
DEFAULT_PREDICTION_PATH = "data/prediction.csv"



if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Predict the weather')
	parser.add_argument('-l', '--load', action="store_true", help='Load and parse data from folders to CSV')
	parser.add_argument('-t', '--train', action="store_true", help='Train model')
	parser.add_argument('-p', '--predict', help='Make a prediction from a CSV file')
	args = parser.parse_args()

	if args.load:

		df_calidad, df_metereologia = load_data(DEFAULT_LOAD_PATH)
		df = preprocess_data(df_calidad, df_metereologia)
		df = correct_values(df)
		df.to_csv(DEFAULT_TRAINING_PATH, index=False)
	
	elif args.train:

		df = pd.read_csv(DEFAULT_TRAINING_PATH)
		model = train_model(df)
		save_model(model, DEFAULT_MODEL_PATH)
	
	elif args.predict:

		df = pd.read_csv(args.predict)
		model = load_model(DEFAULT_MODEL_PATH)
		results = predict_model(model, df)
		save_results(df, results)