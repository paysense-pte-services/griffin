from griffin.griffin.config import AWS_INSTANCE, ENTITY_NAME, ENV, REGION, SERVICE_NAME


def get_keypath_from_input(secret_key):
    return str(AWS_INSTANCE + "/" + ENTITY_NAME + "/" + ENV + "/" + REGION + "/" + SERVICE_NAME + "/" + secret_key)

def get_hashicorp_url_based_on_env():
    if ENV == "prod":
        hashicorp_url = "https://hvault-common-cluster.payufin.io"  # todo: prod url to be provided by devops
    else:
        hashicorp_url = "https://hvault-common-cluster.payufin.io"
    return hashicorp_url