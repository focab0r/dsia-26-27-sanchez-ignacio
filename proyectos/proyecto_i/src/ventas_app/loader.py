

import os
import pandas as pd

DEFAULT_INPUT_PATH = "proyectos/proyecto_i/data/ventas.csv"


def load_csv(path):
	if not path:
		path  = DEFAULT_INPUT_PATH
	if os.path.exists(path) == False:
		raise Exception("[CRITICAL]: Path does not exists")
	df = pd.read_csv(path)
	return df
