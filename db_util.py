from __future__ import print_function

from peewee import *


db = SqliteDatabase('my_database.db')


class BaseModel(Model):
    class Meta:
        database = db


class Symptom(BaseModel):
    name = CharField(unique=True)
    summary = TextField()
    article = TextField(null=True)


class RelatedSymptom(BaseModel):
    main_symptom_id = CharField()
    related_symptom_id = ForeignKeyField(Symptom, backref='related_symptom')
    rank = IntegerField()

    class Meta:
        indexes = (
            (('main_symptom_id', 'related_symptom_id'), True),
        )


class Disease(BaseModel):
    title = CharField(unique=True)
    text = CharField()
    link = CharField()
    is_emergency = IntegerField()
    thumbnail = CharField()


class RelatedDisease(BaseModel):
    main_symptom_id = ForeignKeyField(Symptom, backref='main_symptom')
    related_disease_id = ForeignKeyField(Disease, backref='related_disease')


def create_db():
    db.connect()
    db.create_tables([Symptom, RelatedSymptom, Disease, RelatedDisease])

    return


def main():
    create_db()
    return


if __name__ == '__main__':
    main()
