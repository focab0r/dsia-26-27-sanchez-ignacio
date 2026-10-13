

from ventas_app.contract import VentaModel

import pandas as pd


def clean_data(df):
	d = df.to_dict(orient="index")
	l = []
	for id_row, value in d.items():
		try:
			l.append(VentaModel(**value))
		except:
			print(f'[-] Unable to process row {id_row}')

	return l