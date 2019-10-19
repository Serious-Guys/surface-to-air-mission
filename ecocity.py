import requests as req


def get_spots():
	link = 	'https://eco-city.org.ua/public.json'
	r = req.get(link)
	spots = r.json()
	return spots


def form_empty_data(keys):
	data = dict()
	data['id'] = None
	data['latitude'] = None
	data['longitude'] = None
	data['time'] = None
	for key in keys:
		data[key] = None

	return data



def get_data_from_spot(spot, time_shift, keys):
	template = 'https://eco-city.org.ua/public.json?id={}&timeShift={}'
	
	data = form_empty_data(keys)

	spot_id = spot['id']
	spot_lat = spot['latitude']
	spot_long = spot['longitude']

	detectors = req.get(template.format(spot_id, time_shift)).json() 
	
	for detector in detectors:
		if 'name' in detector:
#			print(detector)
			if detector['name'] in keys:
				data[detector['name']] = detector['value']
				data['time'] = detector['time']

	data['id'] = spot_id
	data['latitude'] = spot_lat
	data['longitude'] = spot_long

	return data


def get_data(num=-1):
	time_shift = 0
	data = []
	spots = get_spots()
	if num==-1:
		num = len(spots)
	for idx, spot in enumerate(spots):
		if idx >= num:
			break
		spot_data = get_data_from_spot(spot, time_shift, keys=['PM2.5', 'PM10', 'PM1.0'])
		data.append(spot_data)

	return data


def main():
	data = get_data(-1)
	print(data)


if __name__ == '__main__':
	main()
