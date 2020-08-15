from P2MT_App import db
from P2MT_App.models import InterventionType
from P2MT_App.main.utilityfunctions import printLogEntry


def addInterventionType(interventionType, maxLevel):
    printLogEntry("Running addInterventionType()")
    interventionTypeExists = InterventionType.query.filter(
        InterventionType.interventionType == interventionType
    ).first()
    if interventionTypeExists == None:
        interventionType = InterventionType(
            interventionType=interventionType, maxLevel=maxLevel
        )
        db.session.add(interventionType)
        print("Intervention type", interventionType, "added to the database.")
    else:
        print(
            "Intervention type",
            interventionType,
            "not added to the database (already exists).",
        )
    return


def initializeInterventionTypes():
    addInterventionType("Conduct Behavior", 6)
    addInterventionType("Academic Behavior", 4)
    addInterventionType("Attendance", 3)
    addInterventionType("Dress Code", 6)
    addInterventionType("Bullying / Harassment", 4)
    addInterventionType("Extended Remediation", 1)
    db.session.commit()
    return
