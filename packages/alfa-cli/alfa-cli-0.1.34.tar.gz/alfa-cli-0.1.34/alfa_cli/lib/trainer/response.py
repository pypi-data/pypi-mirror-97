from datetime import datetime
import os
import pickle

def handle_build_response(body, instance):
    properties = {}
    if isinstance(instance, tuple):
        properties = instance[1]
        instance = instance[0]

    if isinstance(instance, dict) and "file" in instance:
        return instance

    location = store_instance(body.get("algorithmEnvironmentId"), body.get("tag"), instance)
    return prepare_train_response(body, properties, location)


def store_instance(algorithm_environment_id, tag, instance):
    path = os.path.join("build", ".instances", *algorithm_environment_id.split(":"), tag)
    file_name = "{}.pkl".format(int(datetime.utcnow().timestamp()))

    if not os.path.isdir(path):
        os.makedirs(path)
    with open(os.path.join(path, file_name), "wb") as instance_file:
        pickle.dump(instance, instance_file)

    return {"key": os.path.join(path, file_name)}


def prepare_train_response(body, properties, location):
    res = {"file": location["key"], "properties": properties}
    if "method" in body:
        res["method"] = body.get("method")
    if "score" in body:
        res["score"] = body.get("score")
    return res
