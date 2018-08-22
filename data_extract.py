from bs4 import BeautifulSoup
import json

def test1():
    with open('data_raw/dizziness.html', 'r') as f:
        html_obj = BeautifulSoup(f.read(), 'lxml')
        print(html_obj.get_text())
    return


def test2():
    with open('data_raw/dizziness|shor.json', 'r') as f:
        json_obj = json.load(f)
        # print(json_obj)
        related_symptoms = json_obj['relatedSymptoms']
        print(related_symptoms)

        diseases = json_obj['items']
        print(diseases)
    return


def main():
    test2()
    return


if __name__ == '__main__':
    main()
