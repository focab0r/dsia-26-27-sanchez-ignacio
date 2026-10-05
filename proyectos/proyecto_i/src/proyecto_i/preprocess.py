

from proyecto_i.contract import YearModel

def saveData(l):


	l = []
	for year in l:
		july = year.pop()
		august = year.pop()
		year.append(july+august)
		y = YearModel(year=year[0],
			september=year[1],
			october=year[2],
			november=year[3],
			december=year[4],
			january=year[5],
			february=year[6],
			march=year[7],
			april=year[8],
			may=year[9],
			june=year[10],
			target=year[11])
		l.append(y)
	
	return l

def preprocessDict(d):
	d_time = d["daily"]["time"]
	d_precipitation_sum = list(map(float, d["daily"]["precipitation_sum"]))

	all_list = []
	year_list = []
	selected_month = -1
	selected_year = 0
	month_add = 0

	print("[*] Starting preprocess...")
	for selected_value in range(len(d_time)):
		year, month, day = map(int, d_time[selected_value].split("-"))
		if selected_month != -1:
			if month == selected_month:
				month_add += d_precipitation_sum[selected_value]
			else:
				# print(f'Added month {selected_month} to list')
				year_list.append(int(month_add))
				month_add = 0
				if selected_month == 8:
					print(f'[*] Added year {selected_year} to list')
					all_list.append(year_list)
					year_list = []
					selected_month = -1
				else:
					selected_month = month
					month_add += d_precipitation_sum[selected_value]
		if selected_month == -1:
			if month == 9 and day == 1:
				# print(f'Starting at: Year: {year}, month {month}, day {day}')
				selected_month = 9
				selected_year = year
				year_list.append(selected_year)
	
	l = saveData(all_list)
	print("[+] Finished preprocess")
	return l