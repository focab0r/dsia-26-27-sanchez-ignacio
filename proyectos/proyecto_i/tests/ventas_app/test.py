
import pytest

from ventas_app.loader import load_csv
from ventas_app.contract import VentaModel
from ventas_app.preprocess import clean_data

from pandas import DataFrame


@pytest.fixture
def sample_df():
	return DataFrame({
		"fecha": ["2020-01-01"],
		"region": ["Oeste"],
		"producto": ["A"],
		"unidades":	[33],
		"precio_unitario": [30.5], 
		"cliente_id": ["C001"]
	})

def test_load_csv_no_path():
	df = load_csv(None)
	assert df.any

def test_load_csv_error():
	with pytest.raises(Exception):
		load_csv("this_file_does_not_exists.csv")

def test_contract_invalid_region():
	with pytest.raises(Exception):
		VentaModel("fecha", "invalid_value", "producto", 1, 1, "cliente_id")

def test_contract_invalid_price():
	with pytest.raises(Exception):
		VentaModel("fecha", "Norte", "producto", 1, -1, "cliente_id")

def test_clean_data(sample_df):
	l = clean_data(sample_df)
	assert len(l) == 1

