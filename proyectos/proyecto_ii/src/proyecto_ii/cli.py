

import argparse
from pathlib import Path
import pandas as pd

from proyecto_ii.loader import load_data
from proyecto_ii.preprocess import preprocess_data, correct_values
from proyecto_ii.model import train_model


DEFAULT_LOAD_PATH = "/home/focab0r/Downloads/DSIA"

# def save_data(file_name, l):
# 	with open(file_name, "w") as f:
# 		f.write("year,month,day,precipitation\n")
# 		for elem in l:
# 			f.write(f'{elem.year},{elem.month},{elem.day},{elem.precipitation}\n')


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Predict the weather')
	parser.add_argument('-o', '--output', help='Output file where the data will be stored', required=True)
	parser.add_argument('-i', '--input', help='Input file where the data is stored')
	parser.add_argument('-l', '--load', action="store_true", help='Load data to CSV')
	parser.add_argument('-t', '--train', action="store_true", help='Train model')
	args = parser.parse_args()

	if args.load:
		df_calidad, df_metereologia = load_data(Path(DEFAULT_LOAD_PATH))
		df = preprocess_data(df_calidad, df_metereologia)
		df = correct_values(df)
		df.to_csv("final2.csv", index=False)
		print("[*] Null values in each column:")
		print(df.isnull().sum())
	
	elif args.train:
		df = pd.read_csv("final2.csv")
		train_model(df)

	# if not args.train:

	# 	d = download_json(DEFAULT_LATITUDE, DEFAULT_LONGITUDE, DEFAULT_START_DATE, "2026-11-05")
	# 	l = preprocessDict(d)
	# 	save_data(args.output, l)
	# 	print(f'[+] Data saved to file {args.output}')

	# elif args.train:

	# 	if not args.input:
	# 		print("[X] ERROR: Received --train without a --input")
	# 		exit(1)
	# 	print("[*] Training model...")
	# 	model = train_model(args.input)
	# 	print("[+] Trained")

	# print("[+++] Finished")