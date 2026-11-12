

import pandas as pd
import pytest

from proyecto_ii.preprocess import correct_values, preprocess_calidad, preprocess_metereologia


@pytest.fixture
def sample_preprocessed_dict():
	d = {
		"year": [2023, 2023, 2023],
		"month": [5, 5, 5],
		"day": [3, 3, 3],
		"81": [5, None, 4],
		"82": [8, 9, 15],
		"83": [8, 3, 1],
		"86": [4, None, None],
		"87": [8, 10, None],
		"88": [7, 8, 9],
		"89": [1, 2, 3]
	}
	return d


def test_correct_values(sample_preprocessed_dict):
	df = pd.DataFrame(sample_preprocessed_dict)
	new_df = correct_values(df)
	assert new_df.isnull().sum().sum() == 0

def test_preprocess_calidad():
	df = pd.read_csv("tests/data/calidad.csv")
	new_df = preprocess_calidad(df)
	assert "D01" not in  new_df.columns
	assert "target" in  new_df.columns
	assert new_df.shape[0] == 174
