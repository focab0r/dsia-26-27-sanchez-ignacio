

import argparse
import pandas as pd
from dotenv import load_dotenv

from proyecto_ii.loader import load_data
from proyecto_ii.preprocess import preprocess_data, correct_values
from proyecto_ii.model import train_model, save_model, load_model, predict_model
from proyecto_ii.agent import call_agent


DEFAULT_LOAD_PATH = "/home/focab0r/Downloads/DSIA"
DEFAULT_TRAINING_PATH = "data/training_data.csv"
DEFAULT_MODEL_PATH = "data/model.joblib"
DEFAULT_PREDICTION_PATH = "data/prediction.csv"


def load():
	df_calidad, df_metereologia = load_data(DEFAULT_LOAD_PATH)
	df = preprocess_data(df_calidad, df_metereologia)
	df = correct_values(df)
	df.to_csv(DEFAULT_TRAINING_PATH, index=False)

def train():
	df = pd.read_csv(DEFAULT_TRAINING_PATH)
	model = train_model(df)
	save_model(model, DEFAULT_MODEL_PATH)

def predict(df):
	model = load_model(DEFAULT_MODEL_PATH)
	results = predict_model(model, df)
	print(f"Result: {results}")

def ask_agent(data):
	load_dotenv()
	print("[*] Calling agent...")
	if "[mock]" in data:
		print("[*] Mock mode activated")
		result =  {'81': 1.0, '82': 45.0, '83': 27.0, '86': 35.0, '87': 942.0, '88': 300.0, '89': 0.0}
		print(f"[+] Get response from agent: {result}")
		return result

	result = call_agent(data)
	if result["status"] == "error":
		print(f"[X] ERROR: {result["error"]}")
		return None
	else:
		print(f"[+] Get response from agent: {result["data"]}")
		return result[data]


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Predict the weather')
	parser.add_argument('-l', '--load', action="store_true", help='Load and parse data from folders to CSV')
	parser.add_argument('-t', '--train', action="store_true", help='Train model')
	parser.add_argument('-p', '--predict', help='Make a prediction from a CSV file')
	parser.add_argument('-a', '--ask-agent', help='Ask an agent to create the CSV values and predictions')
	args = parser.parse_args()

	if args.load:
		load()
	
	elif args.train:
		train()
	
	elif args.predict:
		df = pd.read_csv(args.predict)
		predict(df)

	elif args.ask_agent:
		result = ask_agent(args.ask_agent)
		if result != None:
			df = pd.DataFrame([result])
			predict(df)
