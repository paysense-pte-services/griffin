import os

#Vault
# entity name can be payufin/paysense/paysense-pte/lazypay/lazycard
ENTITY_NAME = os.environ.get("ENTITY_NAME")
# env can be prod/sbox
ENV = os.environ.get("ENV", "sbox")
REGION = os.environ.get("REGION", "ap-south-1")
SERVICE_NAME = os.environ.get("SERVICE_NAME")
KEY = "current"
MOUNT_POINT = "payu"
# aws instance ec2
AWS_INSTANCE = "ec2"
# vault token
VAULT_TOKEN = os.environ.get("VAULT_TOKEN")
HASHICORP_URL_SBOX = "https://hvault-common-cluster.payufin.io"
HASHICORP_URL_PROD = "https://hvault-common-cluster.payufin.io"


# Redis
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
REDIS_DB = os.environ.get("REDIS_DB", 0)

# Griffin
GRIFFIN_CACHE_TTL = os.environ.get("GRIFFIN_CACHE_TTL", 94608000)
GRIFFIN_CACHE_NAMESPACE = "griffin"
