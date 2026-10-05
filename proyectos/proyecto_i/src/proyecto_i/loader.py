



import requests
import json

DEFAULT_LATITUDE = "40.42"		# Madrid
DEFAULT_LONGITUDE = "-3.70"		# Madrid
DEFAULT_START_DATE = "2015-10-05"

def download_json(latitude, longitude, start_date, end_date):
	print("[*] Downloading content...")
	r = requests.get(f'https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&daily=precipitation_sum&timezone=Europe/Madrid')
	if r.status_code != 200:
		raise Exception("[CRITICAL] ERROR: Unable to get data")
	d = r.content
	print("[+] Content downloaded")
	return json.loads(d)