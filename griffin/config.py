import os

# entity name can be payufin/paysense/lazypay/lazycard
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
