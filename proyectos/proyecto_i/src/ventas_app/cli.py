

import argparse

from ventas_app.loader import load_csv
from ventas_app.preprocess import clean_data




if __name__ == "__main__":

	# Just in case we need args
	parser = argparse.ArgumentParser(description='Ventas')
	parser.add_argument('--input', help='Input CSV file', required=True)
	parser.add_argument('--output', help='Output cleaned CSV file')
	args = parser.parse_args()

	df = load_csv(args.input)
	df_cleaned = clean_data(df)

	if args.output:
		with open(args.output, "w") as f:
			for elem in df_cleaned:
				f.write(f'{elem.fecha},{elem.region},{elem.producto},{elem.unidades},{elem.precio_unitario},{elem.cliente_id}\n')
	