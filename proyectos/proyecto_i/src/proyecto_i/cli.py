

import argparse

from proyecto_i.loader import download_json, DEFAULT_LATITUDE, DEFAULT_LONGITUDE, DEFAULT_START_DATE
from proyecto_i.preprocess import preprocessDict



if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Predict the weather')
	parser.add_argument('--output', help='Output file where the data will be stored')
	args = parser.parse_args()

	d = download_json(DEFAULT_LATITUDE, DEFAULT_LONGITUDE, DEFAULT_START_DATE, "2026-10-05")
	l = preprocessDict(d)