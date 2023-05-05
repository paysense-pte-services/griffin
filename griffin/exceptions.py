class VaultAuthenticationException(Exception):
    pass

class VaultConnectivityException(Exception):
    pass

class SecretNotFoundException(Exception):
    pass

class ValidationFailedException(Exception):
    pass
