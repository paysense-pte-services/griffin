from griffin.config import AWS_INSTANCE, ENTITY_NAME, ENV, REGION, SERVICE_NAME, GRIFFIN_CACHE_NAMESPACE

@staticmethod
def get_keypath_from_input(secret_key):
    return str(AWS_INSTANCE + "/" + ENTITY_NAME + "/" + ENV + "/" + REGION + "/" + SERVICE_NAME + "/" + secret_key)

@staticmethod
def construct_cache_key(secret_key):
    return str(GRIFFIN_CACHE_NAMESPACE + "::" + ENTITY_NAME + "::" + ENV + "::" + REGION + "::" + SERVICE_NAME + "::" + secret_key)