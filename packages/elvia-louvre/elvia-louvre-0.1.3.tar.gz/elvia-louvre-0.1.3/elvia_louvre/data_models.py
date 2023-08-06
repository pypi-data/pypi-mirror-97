from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union


@dataclass
class ImageFile:
    """Represent image files from ImageAPI."""

    image_variant: str
    size: int
    sasuri: str
    height: float
    width: float


@dataclass
class ImageData:
    """Represent image data from ImageAPI."""

    image_id: str
    etag: str
    metadata: List[dict]
    image_files: List[ImageFile]

    @property
    def image_variants(self) -> List[str]:
        """
        Return a list with the imageVariants present.
        """
        return [image_file.image_variant for image_file in self.image_files]

    def get_variant(self, variant: str) -> Union[ImageFile, None]:
        """
        Given an image variant, return its corresponding ImageFile if it exits in the ImageData 
        instance.

        Parameters
        ----------
        variant : str
            Name of the desired image variant.

        Returns
        -------
        ImageFile, None
        """
        for image_file in self.image_files:
            if variant == image_file.image_variant:
                return image_file
        return None


@dataclass
class UpdateMetadataRequest:
    """Represent a metadata update request to be sent to ImageEnhanceAPI."""

    image_id: str
    additional_metadata: Dict[str, str] = field(default_factory=dict)
    plugin_id: Optional[str] = None
    e_tag: Optional[str] = None
    skip_e_tag_validation: bool = True
    client_name: str = 'python-client'
