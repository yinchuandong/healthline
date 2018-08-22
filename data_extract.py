from __future__ import print_function
import json
import os

from db_util import Symptom, RelatedSymptom, Disease, RelatedDisease


def extract(json_obj):
    ''' extract related symtoms and related diseases
    '''
    main_symptom_names = json_obj['symptomNames']
    related_symptoms = json_obj['relatedSymptoms']
    related_diseases = json_obj['items']

    # print(related_symptoms)
    # save the current querying symptoms
    for name in main_symptom_names:
        if len(Symptom.select().where(Symptom.name == name)) == 0:
            Symptom.create(name=name)

    main_symptoms = Symptom.select().where(Symptom.name << main_symptom_names)
    for main_symptom in main_symptoms:
        # print(main_symptom.id, main_symptom.name)

        # save the related symtoms
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

        # save the related diseases
        for item in related_diseases:
            title = item['title'][0]
            if len(Disease.select().where(Disease.title == title)) == 0:
                Disease.create(title=title)
            disease = Disease.get(Disease.title == title)

            related_disease = Disease.get(Disease.title == title)

            # print(related_disease)
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
    filenames = sorted(filenames)
    for filename in filenames:
        with open(base_dir + '/' + filename, 'r') as f:
            json_obj = json.load(f)
            print(filename)
            if 'symptomNames' not in json_obj:
                continue
            extract(json_obj)
            # break
    return


if __name__ == '__main__':
    main()
