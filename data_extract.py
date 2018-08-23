from __future__ import print_function
import json
import os

from db_util import Symptom, RelatedSymptom, Disease, RelatedDisease


def parse_article_body(article_body):
    ''' dfs to parse all the text in article_body
    '''
    waiting_list = []
    for obj in reversed(article_body):
        waiting_list.append(obj)

    results = []
    while len(waiting_list) > 0:
        item = waiting_list.pop()
        if not isinstance(item, dict):
            results.append(item.encode('utf-8'))
        else:
            for sub_item in reversed(item['children']):
                waiting_list.append(sub_item)
    return ''.join(results)


def extract(json_obj):
    ''' extract related symtoms and related diseases
    '''
    main_symptom_names = json_obj['symptomNames']
    related_symptoms = json_obj['relatedSymptoms']
    related_diseases = json_obj['items']

    # 1.save the current querying symptoms
    if 'article' in json_obj:
        name = main_symptom_names[0]
        try:
            data = {
                'name': name,
                'summary': json_obj['article']['summary'],
                'article': parse_article_body(json_obj['article']['body'])
            }
            item = Symptom.get(Symptom.name == name)
        except Exception as e:
            Symptom.create(**data)
        else:
            item.article = parse_article_body(json_obj['article']['body'])
            item.save()

    main_symptoms = Symptom.select().where(Symptom.name << main_symptom_names)
    main_symptom_ids = [str(s.id) for s in main_symptoms]
    main_symptom_ids = sorted(main_symptom_ids)
    main_symptom_ids_key = '|'.join(main_symptom_ids)

    # 2.save the related symtoms:
    # map: dizziness -> (short of breath, 191)
    # map: dizziness|short of breath -> (vomiting, 88)
    for item in related_symptoms:
        if len(Symptom.select().where(Symptom.name == item['cfn'])) == 0:
            Symptom.create(name=item['cfn'], summary='', article='')

        related_symptom = Symptom.get(Symptom.name == item['cfn'])
        related_ret = RelatedSymptom.select()\
            .where(RelatedSymptom.related_symptom_id == related_symptom.id) \
            .where(RelatedSymptom.main_symptom_id == main_symptom_ids_key)
        if len(related_ret) == 0:
            d = {
                'main_symptom_id': main_symptom_ids_key,
                'related_symptom_id': related_symptom.id,
                'rank': item['rank']
            }
            RelatedSymptom.create(**d)
        # break

    # 3.save the related diseases
    for main_symptom in main_symptoms:
        # print(main_symptom.id, main_symptom.name)

        for item in related_diseases:
            title = item['title'][0]
            if len(Disease.select().where(Disease.title == title)) == 0:
                data = {
                    'title': title,
                    'text': item['text'][0],
                    'link': item['link'],
                    'is_emergency': item.get('isEmergency', 0),
                    'thumbnail': item.get('thumbnail', '')
                }
                Disease.create(**data)
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
