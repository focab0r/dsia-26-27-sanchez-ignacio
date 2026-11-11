

from proyecto_ii.contract import LineModel
import pandas as pd


DEFAULT_TARGET = 14		# Ozono

DF_CALIDAD_COLUMNS = [
	"provincia",
	"municipio",
	"estacion",
	"magnitud",
	"punto_muestreo",
	"year",
	"month",
	"day",
	"target"
]


def convert_serie_to_frame(row):
	d = {}
	for elem in DF_CALIDAD_COLUMNS:
		d[elem] = [row[elem]]
	df = pd.DataFrame(d)
	return df


def preprocess_calidad(df_calidad):
	df_calidad = df_calidad.loc[df_calidad['MAGNITUD'] == 14]
	df_calidad.drop(columns=["D31","V31"], inplace=True)
	new_dict = {
		"provincia": [],
		"municipio": [],
		"estacion": [],
		"magnitud": [],
		"punto_muestreo": [],
		"year": [],
		"month": [],
		"day": [],
		"target": []
	}
	for i, row in df_calidad.iterrows():
		for e in range(1, 30):
			new_dict["provincia"].append(row["PROVINCIA"])
			new_dict["municipio"].append(row["MUNICIPIO"])
			new_dict["estacion"].append(row["ESTACION"])
			new_dict["magnitud"].append(row["MAGNITUD"])
			new_dict["punto_muestreo"].append(row["PUNTO_MUESTREO"])
			new_dict["year"].append(row["ANO"])
			new_dict["month"].append(row["MES"])
			new_dict["day"].append(str(e))
			aux = str(e)
			if e < 10:
				aux = "0"+str(e)
			new_dict["target"].append(row["D"+aux])
	
	return pd.DataFrame(new_dict)


def preprocess_metereologia(df_calidad, df_metereologia):
	df_metereologia.drop(columns=["D31", "V31"], inplace=True)
	stations = df_calidad["estacion"].unique()
	df_metereologia = df_metereologia.loc[df_metereologia["ESTACION"].isin(stations)]

	new_dict = {
		"provincia": [],
		"municipio": [],
		"estacion": [],
		"magnitud": [],
		"punto_muestreo": [],
		"year": [],
		"month": [],
		"day": [],
		"value": []
	}

	for i, row in df_metereologia.iterrows():
		for e in range(1, 30):
			new_dict["provincia"].append(row["PROVINCIA"])
			new_dict["municipio"].append(row["MUNICIPIO"])
			new_dict["estacion"].append(row["ESTACION"])
			new_dict["magnitud"].append(row["MAGNITUD"])
			new_dict["punto_muestreo"].append(row["PUNTO_MUESTREO"])
			new_dict["year"].append(row["ANO"])
			new_dict["month"].append(row["MES"])
			new_dict["day"].append(str(e))
			aux = str(e)
			if e < 10:
				aux = "0"+str(e)
			new_dict["value"].append(row["D"+aux])

	df_metereologia_new = pd.DataFrame(new_dict)

	df_calidad["81"] = ''
	df_calidad["82"] = ''
	df_calidad["83"] = ''
	df_calidad["86"] = ''
	df_calidad["87"] = ''
	df_calidad["88"] = ''
	df_calidad["89"] = ''

	df_calidad_new = pd.DataFrame({
		"provincia": [],
		"municipio": [],
		"estacion": [],
		"magnitud": [],
		"punto_muestreo": [],
		"year": [],
		"month": [],
		"day": [],
		"81": [],
		"82": [],
		"83": [],
		"86": [],
		"87": [],
		"88": [],
		"89": []

	})

	df_metereologia_size = df_metereologia.size
	for i, row in df_calidad.iterrows():
		print(f"[*] Processing {i} of {df_metereologia_size} possible values...")
		aux_station = df_metereologia_new.loc[df_metereologia_new["estacion"] == row["estacion"]]
		aux_y = aux_station.loc[aux_station["year"] == row["year"]]
		aux_m = aux_y.loc[aux_y["month"] == row["month"]]
		aux_d = aux_m.loc[aux_m["day"] == row["day"]]

		df_row = convert_serie_to_frame(row)

		for e, row2 in aux_d.iterrows():
			df_row[str(row2["magnitud"])] = row2["value"]
		
		df_calidad_new = pd.concat([df_calidad_new, df_row])
	
	df_calidad_new.drop(columns=["80"], inplace=True)

	return df_calidad_new



def preprocess_data(df_calidad, df_metereologia):
	
	print("[*] Processing calidad...")
	df_calidad = preprocess_calidad(df_calidad)
	print("[+] Processed")
	print("[*] Processing metereologia...")
	df_total = preprocess_metereologia(df_calidad, df_metereologia)
	print("[+] Processed")

	return df_total


def correct_values(df):
	print("[*] Correcting values...")
	keys = ["year", "month", "day"]
	cols = ["81", "82", "83", "86", "87", "88", "89"]
	df[cols] = df[cols].fillna(df.groupby(keys)[cols].transform('mean'))
	print("[+] Corrected")
	print("[*] Null values in each column:")
	print(df.isnull().sum())
	return df