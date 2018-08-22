from peewee import *


db = SqliteDatabase('my_database.db')
# db = MySQLDatabase()


class BaseModel(Model):
    class Meta:
        database = db


class Symptom(BaseModel):
    name = CharField(unique=True)


class RelatedSymptom(BaseModel):
    main_symptom_id = ForeignKeyField(Symptom)
    related_symptom_id = ForeignKeyField(Symptom)
    rank = IntegerField()


class Disease(BaseModel):
    title = CharField(unique=True)


class RelatedDisease(BaseModel):
    main_symptom_id = ForeignKeyField(Symptom)
    related_disease_id = ForeignKeyField(Disease)


def create_db():
    db.connect()
    db.create_tables([Symptom, RelatedSymptom, Disease, RelatedDisease])

    return


def insert_db():
    import json
    with open('data_raw/dizziness|shortness-of-breath.json', 'r') as f:
        json_obj = json.load(f)
        # print(json_obj)
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
    # create_db()
    insert_db()
    return


if __name__ == '__main__':
    main()
