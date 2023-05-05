import logging

import hvac

from griffin.decorators import singleton
from griffin.choices import EntityType
from griffin.config import ENTITY_NAME, SERVICE_NAME, VAULT_TOKEN, MOUNT_POINT, KEY
from griffin.exceptions import VaultAuthenticationException, SecretNotFoundException, ValidationFailedException, \
    VaultConnectivityException
from griffin.utils import get_keypath_from_input, get_hashicorp_url_based_on_env

LOGGER = logging.getLogger("secret_management_util")


@singleton
class SecretManagementUtil:
    """
    This util is responsible for making connection with HashiCorp Vault service and to fetch the secrets
    from the Vault
    """

    @staticmethod
    def _validate_values_from_input():
        if not (ENTITY_NAME and SERVICE_NAME):
            raise ValidationFailedException("Validation failed. Entity Name or Service Name not present. Please pass required values")
        if ENTITY_NAME not in (EntityType.PAYUFIN.value, EntityType.PAYSENSE.value, EntityType.PAYSENSE_PTE.value, EntityType.LAZYPAY.value, EntityType.LAZYCARD.value):
            raise ValidationFailedException("Validation failed. Entity Name does not belongs to valid Enum. Please pass correct value.")

    @staticmethod
    def vault_client():
        try:
            hashicorp_url = get_hashicorp_url_based_on_env()
            vault_client = hvac.Client(
                url=hashicorp_url,
                token=VAULT_TOKEN,
            )

            if vault_client.is_authenticated():
                LOGGER.info("Vault authentication successful for service:{}".format(SERVICE_NAME))
                return vault_client
            else:
                raise VaultAuthenticationException("Vault authentication failed.")
        except Exception as e:
            msg = "Failed to connect to vault for service: {service} with error:{e}".format(
                service=SERVICE_NAME, e=str(e)
            )
            LOGGER.exception(msg)
            raise VaultConnectivityException(e)

    def get_secret_from_vault(self, secret_key):
        self._validate_values_from_input()
        vault_client = self.vault_client()
        keypath = get_keypath_from_input(secret_key)
        try:
            secret_response = (vault_client.secrets.kv.v2.read_secret_version(path=keypath, mount_point=MOUNT_POINT))
            return secret_response["data"]["data"][KEY]
        except Exception as e:
            msg = "Failed to fetch secret for service: {service} having secret_key: {secret_key} with error:{e}".format(
                service=SERVICE_NAME, secret_key=secret_key, e=str(e)
            )
            LOGGER.exception(msg)
            raise SecretNotFoundException(msg)
