from P2MT_App.models import InterventionType


def getInterventionTypes():
    interventionTypes = InterventionType.query.all()
    interventionValueLabelTupleList = []
    for interventionType in interventionTypes:
        value = str(interventionType.id)
        label = interventionType.interventionType
        interventionValueLabelTupleList.append((value, label))
    return interventionValueLabelTupleList
