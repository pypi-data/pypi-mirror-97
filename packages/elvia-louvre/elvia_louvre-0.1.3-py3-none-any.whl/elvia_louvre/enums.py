"""Store various application values."""


class AppKeys:
    """Store application keys in one place."""

    GITHUB_TOKEN = 'GITHUB_TOKEN'
    VAULT_ADDR = 'VAULT_ADDR'

    IMAGE_API_RELATIVE_URL = 'image_api_relative_url'
    IMAGE_ENHANCE_API_RELATIVE_URL = 'image_enhance_api_relative_url'


class SecretPaths:
    """Store secret paths used against the vault service."""

    TOKEN_ENDPOINT = 'louvre/kv/elvid/louvre-power-pole-vision-api/tokenendpoint'
    CLIENT_ID_API = 'louvre/kv/elvid/louvre-power-pole-vision-api/clientid'
    CLIENT_SECRET_API = 'louvre/kv/elvid/louvre-power-pole-vision-api/clientsecret'
    LOUVRE_DOMAIN = 'louvre/kv/louvre/generic/domain'

    # Against PROD
    TOKEN_ENDPOINT_TRAINING = 'louvre/kv/manual/louvre-vision-training-prod/tokenendpoint'
    CLIENT_ID_API_TRAINING = 'louvre/kv/manual/louvre-vision-training-prod/clientid'
    CLIENT_SECRET_API_TRAINING = 'louvre/kv/manual/louvre-vision-training-prod/clientsecret'
    LOUVRE_DOMAIN_TRAINING = 'louvre/kv/manual/louvre-vision-training-prod/domain'

    ISSUER = 'louvre/kv/elvid/generic/authority'


class ImageVariants:
    """Allowed values for the image variant parameter."""

    STANDARD = 'standard'
    THUMBNAIL = 'thumbnail'
    ORIGINAL = 'original'
    DEFAULT = STANDARD
