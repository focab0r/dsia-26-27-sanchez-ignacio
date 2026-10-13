

import argparse

from proyecto_i.loader import download_json, DEFAULT_LATITUDE, DEFAULT_LONGITUDE, DEFAULT_START_DATE
from proyecto_i.preprocess import preprocessDict



if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Predict the weather')
	parser.add_argument('--output', help='Output file where the data will be stored', required=True)
	args = parser.parse_args()

	d = download_json(DEFAULT_LATITUDE, DEFAULT_LONGITUDE, DEFAULT_START_DATE, "2026-10-05")
	l = preprocessDict(d)
	with open(args.output, "w") as f:
		for elem in l:
			f.write(f'{elem.september},{elem.october},{elem.november},{elem.december},{elem.january},{elem.february},{elem.march},{elem.april},{elem.may},{elem.june},{elem.target}\n')
	print(f'[+] Data saved to file {args.output}')
	print("[+++] Finished")