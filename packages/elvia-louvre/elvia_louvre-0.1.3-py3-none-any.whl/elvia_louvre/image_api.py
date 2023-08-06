"""
API wrapper for talking to the ImageAPI to fetch images based on IDs.

Authors: Rafael Sanchez & Sindre Eik de Lange
Date: 26.08.20
"""

from http import HTTPStatus
import requests
from typing import Any, Dict, Union, List

from .config import Config
from .data_models import ImageData, ImageFile
from .enums import ImageVariants, SecretPaths
from .errors import LouvreImageNotFound, LouvreQueryError, LouvreKeyError, \
    LouvreInvalidImageVariant
from .token import Token


class ImageAPI():
    """Wrapper class for communicating with ImageAPI."""
    @staticmethod
    def get_image_data(img_id: str,
                       using_production_images: bool = False) -> ImageData:
        """
        Return image data for a given image ID: parsed additionalMetadata, _etag, imageFiles.

        Parameters
        ----------
        img_id : str
            ID of the image.
        using_production_images : bool
            Whether to search in production.

        Returns
        -------
        ImageData

        Raises
        ------      
        LouvreImageNotFound,
        LouvreKeyError,
        LouvreQueryError,
        RequestException,
        """

        query = \
            f'''query GetImage {{
                    getImage(id: "{img_id}")
                    {{
                        _etag
                        additionalMetadata {{
                            key
                            value          
                        }}
                        imageFiles {{
                            imageVariant
                            sasUri
                            size
                            height
                            width
                        }}                        
                    }}
                }}'''

        response = requests.post(
            url=Config.get_secret(
                SecretPaths.LOUVRE_DOMAIN_TRAINING
                if using_production_images else SecretPaths.LOUVRE_DOMAIN) +
            Config.image_api_relative_url,
            json={'query': query},
            headers=Token.get_headers(
                using_production_images=using_production_images))

        if response.status_code == HTTPStatus.OK:
            try:
                return ImageData(
                    image_id=img_id,
                    etag=response.json()['data']['getImage']['_etag'],
                    image_files=ImageAPI._extract_image_files(
                        image_files=response.json()['data']['getImage']
                        ['imageFiles']),
                    metadata=ImageAPI._extract_additional_metadata(
                        metadata=response.json()['data']['getImage']
                        ['additionalMetadata']))
            except KeyError as key_error:
                raise LouvreKeyError(str(key_error))
        elif response.status_code == HTTPStatus.BAD_REQUEST and 'No image with id' in str(
                response.content):
            raise LouvreImageNotFound()
        raise LouvreQueryError()

    @staticmethod
    def get_image_sasuri(img_id: str,
                         image_variant: Union[str, None] = None,
                         using_production_images: bool = False) -> str:
        """
        Given image ID and image variant, return the corresponding sasuri.

        Parameters
        ----------
        img_id : str
            ID of the image.
        image_variant : str, optional
            Image size. Valid choices are thumbnail, standard and original.
        using_production_images : bool
            Whether to search in production.
            
        Returns
        -------
        sasuri : str
            Link to the desired image file with a built-in access token.

        Raises
        ------
        LouvreImageNotFound,
        LouvreKeyError,
        LouvreQueryError,
        LouvreInvalidImageVariant,
        RequestException,
        """

        if image_variant is None:
            image_variant = ImageVariants.DEFAULT
        if image_variant not in [
                ImageVariants.THUMBNAIL, ImageVariants.STANDARD,
                ImageVariants.ORIGINAL
        ]:
            raise LouvreInvalidImageVariant()

        query = \
            f'''query GetImage {{
                    getImage(id: "{img_id}", imageVariants: ["{image_variant}"]) {{
                        imageFiles {{
                            sasUri
                        }}
                    }}
                }}'''

        response = requests.post(
            url=Config.get_secret(
                SecretPaths.LOUVRE_DOMAIN_TRAINING
                if using_production_images else SecretPaths.LOUVRE_DOMAIN) +
            Config.image_api_relative_url,
            json={'query': query},
            headers=Token.get_headers(
                using_production_images=using_production_images))

        if response.status_code == 200:
            try:
                return response.json(
                )['data']['getImage']['imageFiles'][0]['sasUri']
            except KeyError as key_error:
                raise LouvreKeyError(str(key_error))
        elif response.status_code == HTTPStatus.BAD_REQUEST and 'No image with id' in str(
                response.content):
            raise LouvreImageNotFound()
        else:
            raise LouvreQueryError()

    @staticmethod
    def _extract_image_files(image_files: list) -> List[ImageFile]:
        result = []
        if isinstance(image_files, list):
            for image_file in image_files:
                if isinstance(image_file, dict) and all([
                        key in image_file.keys() for key in
                    ['imageVariant', 'size', 'sasUri', 'height', 'width']
                ]):
                    result.append(
                        ImageFile(image_variant=str(
                            image_file['imageVariant']),
                                  size=int(image_file['size']),
                                  sasuri=str(image_file['sasUri']),
                                  height=float(image_file['height']),
                                  width=float(image_file['width'])))
        return result

    @staticmethod
    def _extract_additional_metadata(metadata: List[Dict[str, Any]]) -> list:
        """Return a list of dictionaries, each with the original key name and their corresponding values, 
        without deserialising."""
        result: List[Dict[str, Any]] = []
        if isinstance(metadata, list):
            for item in metadata:
                print(item)
                if isinstance(item, dict) and all(_key in ['key', 'value']
                                                  for _key in item.keys()):
                    result.extend({item['key']: item['value']})
        return result
