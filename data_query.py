from __future__ import print_function
from db_util import Symptom, RelatedSymptom, Disease, RelatedDisease


def select_related_symptoms(symptom_id):
    query_related_symptoms = Symptom\
        .select(Symptom, RelatedSymptom.rank) \
        .join(RelatedSymptom, on=(RelatedSymptom.related_symptom_id == Symptom.id)) \
        .where(RelatedSymptom.main_symptom_id == symptom_id) \
        .order_by(RelatedSymptom.rank.desc())

    related_symptoms = []
    for r in query_related_symptoms:
        # related_symptoms.append((r.name, r.related_symptom[0].rank))
        related_symptoms.append(r.name)
    return related_symptoms


def select_related_diseases(symptom_id):
    query_related_diseases = Disease\
        .select(Disease, RelatedDisease) \
        .join(RelatedDisease, on=(RelatedDisease.related_disease_id == Disease.id)) \
        .where(RelatedDisease.main_symptom_id == symptom_id)

    related_diseases = []
    for r in query_related_diseases:
        related_diseases.append(r.title)
    return related_diseases


def select(symptom_names=['Dizziness']):
    query_symptom_ids = Symptom.select().where(Symptom.name << symptom_names)
    symptom_ids = [s.id for s in query_symptom_ids]

    all_related_symptoms = []
    for symptom_id in symptom_ids:
        related_symptoms = select_related_symptoms(symptom_id)
        all_related_symptoms.append(related_symptoms)

    # get the intersection of given symptoms
    ret_symptoms = set(all_related_symptoms[0])
    for s in all_related_symptoms[1:]:
        ret_symptoms = ret_symptoms.intersection(s)

    all_related_diseases = []
    for symptom_id in symptom_ids:
        related_diseases = select_related_diseases(symptom_id)
        all_related_diseases.append(related_diseases)

    # get the intersection of given diseases
    ret_diseases = set(all_related_diseases[0])
    for s in all_related_diseases[1:]:
        ret_diseases = ret_diseases.intersection(s)
    return ret_symptoms, ret_diseases


def main():
    symptom_names = ['Dizziness', 'Shortness of Breath']
    # symptom_names = ['Dizziness']
    ret = select(symptom_names)
    print('related_symptoms:', len(ret[0]))
    print(ret[0])
    print('\n----------------------------\n')
    print('related_diseases:', len(ret[1]))
    print(ret[1])
    return


if __name__ == '__main__':
    main()
