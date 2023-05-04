import logging

import hvac

from griffin.griffin.decorators import singleton
from .config import ENTITY_NAME, ENV, REGION, SERVICE_NAME, HASHICORP_URL, AWS_INSTANCE, VAULT_TOKEN, MOUNT_POINT, KEY
from .exceptions import VaultAuthenticationException, SecretNotFoundException, ValidationFailedException

LOGGER = logging.getLogger("secret_exception_util")


@singleton
class SecretManagementUtil:
    """
    This util is responsible for making connection with HashiCorp Vault service and to fetch the secrets
    from the Vault
    """

    @staticmethod
    def _validate_values_from_input(entity_name, service_name):
        if not (entity_name or service_name):
            raise ValidationFailedException("Validation failed.")

    @staticmethod
    def _get_keypath_from_input(secret_key):
        return str(AWS_INSTANCE+"/"+ENTITY_NAME+"/"+ENV+"/"+REGION+"/"+SERVICE_NAME+"/"+secret_key)

    @staticmethod
    def vault_client():
        try:
            vault_client = hvac.Client(
                url=HASHICORP_URL,
                token=VAULT_TOKEN,
            )

            if vault_client.is_authenticated():
                LOGGER.info("Vault authentication successful for service:{}".format(SERVICE_NAME))
                return vault_client
            else:
                LOGGER.error("Vault authentication failed for service:{}".format(SERVICE_NAME))
                raise VaultAuthenticationException("Vault authentication failed.")
        except Exception as e:
            LOGGER.error("Failed to authenticate for service:{} with error:{}".format(SERVICE_NAME, e))
            raise VaultAuthenticationException(e)

    def get_secret_from_vault(self, secret_key):
        self._validate_values_from_input(ENTITY_NAME, SERVICE_NAME)
        vault_client = self.vault_client()
        keypath = self._get_keypath_from_input(secret_key)
        try:
            secret_response = (vault_client.secrets.kv.v2.read_secret_version(path=keypath, mount_point=MOUNT_POINT))
            return secret_response["data"]["data"][KEY]
        except Exception as e:
            LOGGER.error("Failed to fetch secret for service:{} having secret_key:{} with error:{}".format(SERVICE_NAME, secret_key, e))
            raise SecretNotFoundException(e)


