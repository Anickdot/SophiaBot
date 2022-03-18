import json
import os


def get_local_data(currency: str) -> str | None:
    if not os.path.exists('local_db.json'):
        with open('local_db.json', 'w+') as file:
            json.dump([], file)

    with open('local_db.json', 'r') as file:
        data = json.load(file)
    
    for pair in data:
        if pair['currency'] == currency:
            return pair['version']
    
    return None

def update_local_data(currency: str, version: str) -> bool:
    if not os.path.exists('local_db.json'):
        with open('local_db.json', 'w+') as file:
            json.dump([], file)
    
    with open('local_db.json', 'r') as file:
        data = json.load(file)
    
    result = False

    for pair in data:
        if pair['currency'] == currency:
            result = pair['version'] != version
            pair['version'] = version
            break
    else:
        data.append({'currency': currency, 'version': version})

    with open('local_db.json', 'w+') as file:
        json.dump(data, file)
    
    return result
