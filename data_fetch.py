import requests
import json
import os


def fetch_conditions(symptoms=['Dizziness'], replace=False):
    url = 'https://www.healthline.com/api/symptom-checker/conditions'

    def func(s):
        return s.lower().replace(' ', '-')
    form_data = map(func, symptoms)
    filename = 'data_raw/{}.json'.format('|'.join(form_data))
    if not replace and os.path.exists(filename):
        return json.load(open(filename, 'r'))
    data = {"rows": 1000, "start": 0, "symptoms": form_data}
    rep = requests.post(url, json=data)
    result = rep.json()
    with open(filename, 'w') as f:
        json.dump(result, f, indent=2)
    return result


def main():
    fetch_conditions(['Dizziness'])
    fetch_conditions(['Dizziness', 'Shortness of Breath'])
    return


if __name__ == '__main__':
    main()
