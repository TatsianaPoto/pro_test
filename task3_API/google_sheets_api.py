import requests

def get_location_by_address(api_key, address):
    url = f'https://maps.googleapis.com/maps/api/geocode/json'
    params = {
        'address': address,
        'key': api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
        return latitude, longitude
    else:
        print(f"Ошибка при запросе: {data['status']}")
        return None, None

if __name__ == '__main__':
    # Вставьте ваш ключ API Google Maps
    api_key = 'AIzaSyAnO3Rc04Q5KVMLXiFR2ySb9_uYmTRh3sU'

    address = '1600 Amphitheatre Parkway, Mountain View, CA'
    latitude, longitude = get_location_by_address(api_key, address)

    if latitude is not None and longitude is not None:
        print(f"Широта: {latitude}, Долгота: {longitude}")
    else:
        print("Не удалось получить информацию о местоположении.")
