import requests
import json


def fetch_conditions(symptoms=['Dizziness']):
    url = 'https://www.healthline.com/api/symptom-checker/conditions'

    def func(s):
        return s.lower().replace(' ', '-')
    form_data = map(func, symptoms)
    data = {"rows": 1000, "start": 0, "symptoms": form_data}
    rep = requests.post(url, json=data)
    result = rep.json()
    filename = '|'.join(form_data)
    with open('data_raw/{}.json'.format(filename), 'w') as f:
        json.dump(result, f, indent=2)
    return


def main():
    fetch_conditions(['Dizziness'])
    fetch_conditions(['Dizziness', 'Shortness of Breath'])
    return


if __name__ == '__main__':
    main()
