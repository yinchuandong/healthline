from db_util import Symptom, RelatedSymptom, Disease, RelatedDisease


def select_related_symtoms(symptom_id):
    query_related_symtoms = Symptom\
        .select(Symptom, RelatedSymptom.rank) \
        .join(RelatedSymptom, on=(RelatedSymptom.related_symptom_id == Symptom.id)) \
        .where(RelatedSymptom.main_symptom_id == symptom_id) \
        .order_by(RelatedSymptom.rank.desc())

    related_symtoms = []
    for r in query_related_symtoms:
        # related_symtoms.append((r.name, r.related_symptom[0].rank))
        related_symtoms.append(r.name)
    return related_symtoms


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

    all_related_symtoms = []
    for symptom_id in symptom_ids:
        related_symtoms = select_related_symtoms(symptom_id)
        all_related_symtoms.append(related_symtoms)

    # get the intersection of given symtoms
    ret_symptoms = set(all_related_symtoms[0])
    for s in all_related_symtoms[1:]:
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
    print(len(ret[0]), len(ret[1]))
    return


if __name__ == '__main__':
    main()
