
import os
import pandas as pd
from pathlib import Path

DEFAULT_LATITUDE = "40.42"		# Madrid
DEFAULT_LONGITUDE = "-3.70"		# Madrid
DEFAULT_START_DATE = "1940-01-02"

DEFAULT_DIR_CALIDAD = "calidad_diaria"
DEFAULT_DIR_METEREOLOGIA = "metereologia_diaria"


def load_csvs_from_file(path):

	list_pandas = []
	for filename in os.listdir(path):
		list_pandas.append(pd.read_csv(path / filename, sep=';'))

	new_df = pd.concat(list_pandas)
	
	return new_df


def load_data(dir_str):
	dir = Path(dir_str)
	df_calidad = load_csvs_from_file(dir / DEFAULT_DIR_CALIDAD)
	df_metereologia = load_csvs_from_file(dir / DEFAULT_DIR_METEREOLOGIA)
	return df_calidad, df_metereologia