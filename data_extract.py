from bs4 import BeautifulSoup
import json
import os

from db_util import Symptom, RelatedSymptom, Disease, RelatedDisease


def extract(json_obj):
    main_symptom_names = json_obj['symptomNames']
    related_symptoms = json_obj['relatedSymptoms']
    related_diseases = json_obj['items']

    # print(related_symptoms)
    for name in main_symptom_names:
        if len(Symptom.select().where(Symptom.name == name)) == 0:
            Symptom.create(name=name)

    main_symptoms = Symptom.select().where(Symptom.name << main_symptom_names)
    for main_symptom in main_symptoms:
        # print(main_symptom.id, main_symptom.name)

        for item in related_symptoms:
            if len(Symptom.select().where(Symptom.name == item['cfn'])) == 0:
                Symptom.create(name=item['cfn'])

            related_symptom = Symptom.get(Symptom.name == item['cfn'])
            related_ret = RelatedSymptom.select()\
                .where(RelatedSymptom.related_symptom_id == related_symptom.id) \
                .where(RelatedSymptom.main_symptom_id == main_symptom.id)
            if len(related_ret) == 0:
                d = {
                    'main_symptom_id': main_symptom.id,
                    'related_symptom_id': related_symptom.id,
                    'rank': item['rank']
                }
                RelatedSymptom.create(**d)
            # break

        for item in related_diseases:
            title = item['title'][0]
            if len(Disease.select().where(Disease.title == title)) == 0:
                Disease.create(title=title)
            disease = Disease.get(Disease.title == title)

            related_disease = Disease.get(Disease.title == title)

            print(related_disease)
            related_ret = RelatedDisease.select()\
                .where(RelatedDisease.main_symptom_id == main_symptom.id) \
                .where(RelatedDisease.related_disease_id == disease.id)
            if len(related_ret) == 0:
                d = {
                    'main_symptom_id': main_symptom.id,
                    'related_disease_id': related_disease.id,
                }
                RelatedDisease.create(**d)

    return


def main():
    base_dir = 'data_raw'
    filenames = os.listdir(base_dir)
    for filename in filenames:
        with open(base_dir + '/' + filename, 'r') as f:
            json_obj = json.load(f)
            extract(json_obj)
    return


if __name__ == '__main__':
    main()
