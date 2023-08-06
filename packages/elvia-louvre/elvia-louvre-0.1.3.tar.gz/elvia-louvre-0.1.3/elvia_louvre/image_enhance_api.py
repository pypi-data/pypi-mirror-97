"""
Module with methods to facilitate communication with ImageEnhanceAPI.
"""

from http import HTTPStatus
import json
import requests

from .data_models import UpdateMetadataRequest
from .enums import SecretPaths
from .errors import LouvreQueryError
from .config import Config
from .token import Token


class ImageEnhanceAPI():
    """
    ImageEnhanceAPI wrapper.
    """
    @staticmethod
    def update_metadata(update_request: UpdateMetadataRequest) -> None:
        """
        Update image metadata. Existing metadata entries with the same keys will get overwritten.

        Parameters
        ----------
        update_request: UpdateMetadataRequest

        Raises
        ------
        RequestException
        LouvreQueryError
        """
        payload = {
            "imageID": update_request.image_id,
            "additionalMetadata": update_request.additional_metadata,
            "skipValidationOfProvidedETag":
            update_request.skip_e_tag_validation,
            "clientName": update_request.client_name
        }

        if update_request.e_tag:
            payload["eTag"] = update_request.e_tag

        if update_request.plugin_id:
            payload["pluginId"] = update_request.plugin_id

        query = json.dumps(payload)

        response = requests.put(
            url=Config.get_secret(SecretPaths.LOUVRE_DOMAIN) +
            Config.image_enhance_api_relative_url,
            headers=Token.get_headers(),
            data=query)

        if not response.status_code == HTTPStatus.OK:
            raise LouvreQueryError(response.content)
