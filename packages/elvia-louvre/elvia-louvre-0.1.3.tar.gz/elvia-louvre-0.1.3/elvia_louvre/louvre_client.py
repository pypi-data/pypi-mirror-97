from elvia_louvre.data_models import UpdateMetadataRequest
from io import BytesIO
from PIL import Image
import requests

from .config import Config
from .enums import ImageVariants
from .image_api import ImageAPI
from .image_enhance_api import ImageEnhanceAPI


class LouvreClient:
    """Python client to interact with APIs in the Louvre system."""
    def __init__(self):
        Config.connect()

    def get_image_data(self,
                       image_id: str,
                       using_production_images: bool = False):
        """
        Return an object with image metadata retrieved from ImageAPI.
        
        Parameters
        ----------
        image_id : str
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
        return ImageAPI.get_image_data(
            img_id=image_id, using_production_images=using_production_images)

    def get_image_url(self,
                      image_id: str,
                      image_variant: str = ImageVariants.DEFAULT,
                      using_production_images: bool = False) -> str:
        """
        Return the URL of an image variant.

        Parameters
        ----------
        image_id : str
        image_variant : str
            Accepted values can be found in the ImageVariants class.
        using_production_images : bool
            Whether to search in production.        

        Returns
        -------
        str

        Raises
        ------
        LouvreImageNotFound,
        LouvreKeyError,
        LouvreQueryError,
        LouvreInvalidImageVariant,
        RequestException,
        """
        return ImageAPI.get_image_sasuri(
            img_id=image_id,
            image_variant=image_variant,
            using_production_images=using_production_images)

    def get_image(self,
                  image_id: str,
                  image_variant: str = ImageVariants.DEFAULT,
                  using_production_images: bool = False) -> Image:
        """
        Return the image, as a PIL object.

        Parameters
        ----------
        image_id : str
        image_variant : str
            Accepted values can be found in the ImageVariants class.
        using_production_images : bool
            Whether to search in production.  

        Returns
        -------
        PIL.Image

        Raises
        ------
        LouvreImageNotFound,
        LouvreInvalidImageVariant,
        LouvreKeyError,
        LouvreQueryError,
        RequestException
        """
        file_url = self.get_image_url(
            image_id=image_id,
            image_variant=image_variant,
            using_production_images=using_production_images)
        _response = requests.get(url=file_url)
        _file_bytes = BytesIO(_response.content)
        return Image.open(_file_bytes)

    def update_image_metadata(self,
                              update_request: UpdateMetadataRequest) -> None:
        """
        Update the metadata for an image.

        Parameters
        ----------
        update_request : UpdateMetadataRequest

        Raises
        ------
        RequestException
        LouvreQueryError
        """
        ImageEnhanceAPI.update_metadata(update_request=update_request)
