from griffin.config import AWS_INSTANCE, ENTITY_NAME, ENV, REGION, SERVICE_NAME, GRIFFIN_CACHE_NAMESPACE, \
    HASHICORP_URL_SBOX, HASHICORP_URL_PROD


def get_keypath_from_input(secret_key):
    return str(AWS_INSTANCE + "/" + ENTITY_NAME + "/" + ENV + "/" + REGION + "/" + SERVICE_NAME + "/" + secret_key)


def get_hashicorp_url_based_on_env():
    if ENV == "prod":
        return HASHICORP_URL_PROD  # todo: prod url to be provided by devops
    else:
        return HASHICORP_URL_SBOX


def construct_cache_key(secret_key):
    return str(GRIFFIN_CACHE_NAMESPACE + "::" + ENTITY_NAME + "::" + ENV + "::" + REGION + "::" + SERVICE_NAME + "::" + secret_key)