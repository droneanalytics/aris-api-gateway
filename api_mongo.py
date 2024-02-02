from bson import ObjectId

def get_model_arn(client, org_id):
    print("Getting model ARN")
    try:
        db = client["droneanalytics"]
        print("db:", db)
        collection = db["org"]
        print("collection:", collection)
        # print everything in org collection
        for org in collection.find({}):
            print("asdfasd", org)
    except Exception as e:
        print("Error initializing MongoDB client:", e)
    # get org specified by org_id
    org_id = ObjectId(org_id)
    org = collection.find_one({"_id": org_id})
    print("org:", org)
    # get modelArn from org
    model_arn = org["modelArn"]
    print("model_arn:", model_arn)
    return model_arn


def get_project_name(client, org_id):
    db = client["droneanalytics"]
    collection = db["org"]
    # get org specified by org_id
    org_id = ObjectId(org_id)
    org = collection.find_one({"_id": org_id})

    # get modelArn from org
    project_name = org["projectName"]
    return project_name


def get_model_name(client, org_id):
    db = client["droneanalytics"]
    collection = db["org"]
    # get org specified by org_id
    org_id = ObjectId(org_id)
    org = collection.find_one({"_id": org_id})

    # get modelArn from org
    model_name = org["modelName"]
    return model_name


def add_class_mappings(client, org_id):
    class_map = {
        "Loose Material": 0,
        "Hail Hit": 1,
        "Soft Metal Damage": 2,
        "Ponding Water": 3,
        "Other": 4,
        "Rust": 5,
        "Flashing Defect": 6,
        "Broken Seal": 7,
        "Improper Installation": 8,
        "Lichen": 9,
        "Material Defect": 10,
        "Prior Repair": 11,
        "Foot Traffic": 12,
        "Chipped Corner": 13,
        "Rotten Fascia": 14,
        "Split Wood": 15,
    }
    db = client[org_id]
    collection = db["damageLabelData"]

    for class_label in class_map:
        class_slug = class_label.lower().replace(" ", "-")
        # look for document with class label and add slug field and class_id field
        existing_doc = collection.find_one({"label": class_label})

        if existing_doc:
            print("updating existing doc")
            collection.update_one(
                {"label": class_label},
                {"$set": {"slug": class_slug, "classId": class_map[class_label]}},
            )


def update_training_flag(client, org_id, property_id):
    db = client[org_id]
    collection = db["properties"]
    # get property specified by property_id
    property_id = ObjectId(property_id)

    # update usedInTraining to True
    collection.update_one({"_id": property_id}, {"$set": {"usedInTraining": True}})


def update_project_name(client, org_id, project_name):
    db = client["droneanalytics"]
    collection = db["org"]
    # get org specified by org_id
    org_id = ObjectId(org_id)

    # update projectName field
    collection.update_one({"_id": org_id}, {"$set": {"projectName": project_name}})
    print("Project Name Updated:", project_name)


def update_model_name(client, org_id, model_name):
    db = client["droneanalytics"]
    collection = db["org"]
    # get org specified by org_id
    org_id = ObjectId(org_id)


    # update projectName field
    collection.update_one({"_id": org_id}, {"$set": {"modelName": model_name}})
    print("Model Name Updated:", model_name)


def update_model_arn(client, org_id, model_arn):
    db = client["droneanalytics"]
    collection = db["org"]
    # get org specified by org_id
    org_id = ObjectId(org_id)


    # update modelArn field
    collection.update_one({"_id": org_id}, {"$set": {"modelArn": model_arn}})
    print("Model ARN Updated:", model_arn)


def get_training_properties(client, org_id):
    db = client[org_id]
    collection = db["properties"]
    # get all properties where usedInTraining is False
    results = collection.find({"usedInTraining": False})

    # convert each result to a string

    properties = [str(result["_id"]) for result in results]
    print("Properties to be used in training:", properties)
    return properties


def get_org_ids(client):
    db = client["droneanalytics"]
    collection = db["org"]
    # get all orgs
    results = collection.find({})

    # convert each result from an ObjectId to a string
    org_ids = [str(result["_id"]) for result in results]
    print("Org IDs:", org_ids)
    return org_ids
