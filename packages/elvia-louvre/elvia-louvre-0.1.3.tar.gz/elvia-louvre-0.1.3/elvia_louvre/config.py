from typing import Union

from elvia_vault import VaultClient
from .errors import LouvreVaultConnError, LouvreSecretError


class Config():
    """Configuration values and secrets."""

    vault: VaultClient
    secrets: dict = {}

    # ImageAPI - GraphQL API to fetch images
    image_api_relative_url: str = '/image/graphql'

    # ImageEnhanceAPI - API to update image's metadata
    image_enhance_api_relative_url: str = '/imageenhance/Metadata'

    # Token buffer in seconds
    token_buffer_seconds: int = 60

    @classmethod
    def connect(cls, github_token: Union[str, None] = None):
        """        
        Connects to the vault using VAULT_ADDR from os.environ.
        If cluster, it uses kubernetes auth, else the Github token.

        Raises
        ------
        LouvreVaultConnError
        """
        # Clean up, to avoid mixing secrets from different vaults, in the case
        # VAULT_ADDR changes between calls
        cls.secrets = {}
        # Get a fresh VaultClient instance and connect to the vault service
        try:
            cls.vault = VaultClient(github_token=github_token)
        except Exception as exception:
            raise LouvreVaultConnError(str(exception))

    @classmethod
    def get_secret(cls, secret_path: str) -> str:
        """
        Return a secret value given a secret path.
        Fetch from vault only if not previously fetched.

        Parameters
        ----------
        secret_path : str

        Raises
        ------
        LouvreSecretError
        """
        try:
            if not secret_path in cls.secrets.keys():
                cls.secrets[secret_path] = cls.vault.get_value(secret_path)
            return cls.secrets[secret_path]

        except KeyError as exception:
            raise LouvreSecretError(exception)
