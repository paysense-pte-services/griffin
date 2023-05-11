import logging
import hvac
from griffin.decorators import singleton
from griffin.choices import EntityType
from griffin.config import ENTITY_NAME, SERVICE_NAME, VAULT_TOKEN, MOUNT_POINT, KEY, HASHICORP_URL
from griffin.exceptions import VaultAuthenticationException, SecretNotFoundException, ValidationFailedException, \
    VaultConnectivityException, CacheWarmUpFailedException
from griffin.utils import get_keypath_from_input, construct_cache_key



LOGGER = logging.getLogger("secret_management_util")


@singleton
class SecretManagementUtil:
    """
    This util is responsible for making connection with HashiCorp Vault service and to fetch the secrets
    from the Vault
    """

    def __init__(self):
        self.cache = {}

    def _validate_values_from_input(self):
        if not (ENTITY_NAME and SERVICE_NAME):
            raise ValidationFailedException("Validation failed. Entity Name or Service Name not present. Please pass required values")
        if ENTITY_NAME not in (EntityType.PAYUFIN.value, EntityType.PAYSENSE.value, EntityType.PAYSENSE_PTE.value, EntityType.LAZYPAY.value, EntityType.LAZYCARD.value):
            raise ValidationFailedException("Validation failed. Entity Name does not belongs to valid Enum. Please pass correct value.")

    def vault_client(self):
        try:
            vault_client = hvac.Client(
                url=HASHICORP_URL,
                token=VAULT_TOKEN,
            )
            if vault_client.is_authenticated():
                LOGGER.info(f"Vault authentication successful for service:{SERVICE_NAME}")
                return vault_client
            else:
                pass
                # raise VaultAuthenticationException("Vault authentication failed")
        except Exception as e:
            msg = f"Failed to connect to vault for service: {SERVICE_NAME} with url: {HASHICORP_URL} and token: {VAULT_TOKEN} with error: {str(e)}"
            LOGGER.exception(msg)
            # raise VaultConnectivityException(msg)

    def get_secret_value(self, secret_key):
        #self._validate_values_from_input()
        try:
            secret = self.get_secret_from_cache(secret_key)
            return secret
        except SecretNotFoundException:
            pass
        except Exception as e:
            LOGGER.error(f"Exception occurred while getting secret from cache - {str(e)}")
            LOGGER.exception(e)

        try:
            secret = self.get_secret_from_vault(secret_key)
            LOGGER.info(f'Secret Value fetched from vault for secret key {secret_key}')
            self.set_secret_to_cache(secret_key, secret)
            return secret
        except Exception as e:
            msg = f"Failed to fetch secret for service: {SERVICE_NAME} having secret_key: {secret_key} with error:{str(e)}"
            LOGGER.exception(msg)
            raise SecretNotFoundException(msg)

    def get_secret_from_vault(self, secret_key):
        vault_client = self.vault_client()
        #keypath = get_keypath_from_input(secret_key)
        return "ok"
        # secret_response = (vault_client.secrets.kv.v2.read_secret_version(path=keypath, mount_point=MOUNT_POINT))
        # return secret_response["data"]["data"][KEY]

    def get_secret_from_cache(self, secret_key):
        cache_key = construct_cache_key(secret_key)
        cache_value = self.cache.get(cache_key)
        if cache_value is None:
            raise SecretNotFoundException(f"Secret Unavailable in cache for secret key - {secret_key}")
        LOGGER.info(f'Secret Value fetched from cache for secret key {secret_key}')
        return cache_value

    def set_secret_to_cache(self, key, value):
        cache_key = construct_cache_key(key)
        try:
            self.cache[cache_key] = value
        except Exception as e:
            LOGGER.error(f"Failed to set cache value for cache key {cache_key} - {str(e)}")
        LOGGER.info(f"Successfully set cache for secret key {key}")

    def delete_secret_from_cache(self, key):
        cache_key = construct_cache_key(key)
        try:
            self.cache.pop(cache_key)
        except Exception as e:
            LOGGER.error(f"Failed to delete cache key {cache_key} - {str(e)}")

    def warm_up_cache(self, secret_keys):
        try:
            for secret_key in secret_keys:
                cache_key = construct_cache_key(secret_key)
                if cache_key not in self.cache.keys():
                    self.cache[cache_key] = self.get_secret_from_vault(secret_key)
        except Exception as e:
            msg = f"Cache warm up failed for service {SERVICE_NAME} with exception {str(e)}"
            LOGGER.error(msg)
            raise CacheWarmUpFailedException(msg)
        LOGGER.info(f'Successfully warmed up cache for service {SERVICE_NAME}')

