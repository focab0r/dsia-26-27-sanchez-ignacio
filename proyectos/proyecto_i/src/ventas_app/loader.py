

import os
import pandas as pd

DEFAULT_INPUT_PATH = "../../data/ventas.csv"


def load_csv(path):
	if os.path.exists(path) == False:
		raise Exception("[CRITICAL]: Path does not exists")
	df = pd.read_csv(path)
	return df
