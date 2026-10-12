
import pytest


from proyecto_i.loader import download_json, DEFAULT_LATITUDE, DEFAULT_LONGITUDE, DEFAULT_START_DATE
from proyecto_i.preprocess import saveData


@pytest.fixture
def sample_row():
	return [2000,1,2,3,4,5,6,7,8,9,10,11,12]	# This include july and august

def test_download():
	l = download_json(DEFAULT_LATITUDE, DEFAULT_LONGITUDE, DEFAULT_START_DATE, "2000-12-10")
	assert l["timezone"] == "Europe/Madrid"

def test_download_max_year():
	with pytest.raises(Exception):
		download_json(DEFAULT_LATITUDE, DEFAULT_LONGITUDE, "1900-12-10", "2000-12-10")


def test_save_data(sample_row):
	sample_list = [sample_row]
	assert len(saveData(sample_list)) == 1
