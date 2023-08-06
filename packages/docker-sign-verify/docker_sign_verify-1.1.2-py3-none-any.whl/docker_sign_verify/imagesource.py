#!/usr/bin/env python

# pylint: disable=too-many-arguments

"""Classes that provide a source of docker images."""

import abc
import logging

from functools import wraps
from typing import Any, Dict, List, Optional, NamedTuple

from aiofiles.base import AiofilesContextManager
from docker_registry_client_async import FormattedSHA256, ImageName
from docker_registry_client_async.utils import must_be_equal

from .exceptions import SignatureMismatchError, UnsupportedSignatureTypeError
from .imageconfig import ImageConfig, SignatureTypes
from .manifest import Manifest
from .signer import Signer
from .utils import xellipsis

LOGGER = logging.getLogger(__name__)


class ImageSourceVerifyImageIntegrity(NamedTuple):
    # pylint: disable=missing-class-docstring
    compressed_layer_files: Optional[List[AiofilesContextManager]]
    image_config: ImageConfig
    manifest: Manifest
    uncompressed_layer_files: List[AiofilesContextManager]

    def close(self):
        """Cleanup temporary files."""
        for file in self.compressed_layer_files + self.uncompressed_layer_files:
            file.close()


class ImageSourceSignImageConfig(NamedTuple):
    # pylint: disable=missing-class-docstring
    image_config: ImageConfig
    signature_value: str
    verify_image_data: ImageSourceVerifyImageIntegrity


class ImageSourceVerifyImageConfig(NamedTuple):
    # pylint: disable=missing-class-docstring
    image_config: ImageConfig
    image_layers: List[FormattedSHA256]
    manifest: Manifest
    manifest_layers: List[FormattedSHA256]


class ImageSourceGetImageLayerToDisk(NamedTuple):
    # pylint: disable=missing-class-docstring
    digest: FormattedSHA256
    size: int


class ImageSourceSignImage(NamedTuple):
    # pylint: disable=missing-class-docstring
    image_config: ImageConfig
    manifest_signed: Manifest
    signature_value: str
    verify_image_data: ImageSourceVerifyImageIntegrity


class ImageSourceVerifyImageSignatures(NamedTuple):
    # pylint: disable=missing-class-docstring
    compressed_layer_files: Optional[List[AiofilesContextManager]]
    image_config: ImageConfig
    manifest: Manifest
    signatures: Any
    uncompressed_layer_files: List[AiofilesContextManager]

    def close(self):
        """Cleanup temporary files."""
        for file in self.compressed_layer_files + self.uncompressed_layer_files:
            file.close()


class ImageSource(abc.ABC):
    """
    Abstract source of docker images.
    """

    def __init__(
        self,
        *,
        dry_run: bool = False,
        signer_kwargs: Dict[str, Dict] = None,
        **kwargs,
    ):
        # pylint: disable=unused-argument
        """
        Args:
            dry_run: If true, destination image sources will not be changed.
            signer_kwargs: Parameters to be passed to the Signer instances when the are initialized.
            image_source_params: Extra parameters for image source processing.
        """
        self.dry_run = dry_run
        self.signer_kwargs = signer_kwargs
        if self.signer_kwargs is None:
            self.signer_kwargs = {}

    @staticmethod
    def check_dry_run(func):
        """Validates the state of ImageSource.dry_run before invoking the wrapped method."""

        @wraps(func)
        async def wrapper(*args, **kwargs):
            if args[0].dry_run:
                LOGGER.debug("Dry Run: skipping %s", func)
            else:
                return await func(*args, **kwargs)

        return wrapper

    async def _sign_image_config(
        self,
        signer: Signer,
        image_name: ImageName,
        signature_type: SignatureTypes,
        **kwargs,
    ) -> ImageSourceSignImageConfig:
        """
        Verifies an image, then signs it without storing it in the image source.

        Args:
            signer: The signer used to create the signature value.
            image_name: The image name.
            signature_type: Specifies what type of signature action to perform.

        Returns:
            NamedTuple:
                image_config: The ImageConfig object corresponding to the signed image.
                signature_value: as defined by :func:~docker_sign_verify.ImageConfig.sign.
                verify_image_data: as defined by :func:~docker_sign_verify.ImageSource.verify_image_integrity.
        """
        # Verify image integrity (we use the verified values from this point on)
        data = await self.verify_image_integrity(image_name, **kwargs)

        # Perform the desired signing operation
        try:
            signature_value = await data.image_config.sign(signer, signature_type)
        except Exception:
            for file in data.compressed_layer_files + data.uncompressed_layer_files:
                file.close()
            raise

        return ImageSourceSignImageConfig(
            image_config=data.image_config,
            signature_value=signature_value,
            verify_image_data=data,
        )

    async def _verify_image_config(
        self, image_name: ImageName, **kwargs
    ) -> ImageSourceVerifyImageConfig:
        """
        Verifies the integration of an image configuration against metadata contained within a manifest.

        Args:
            image_name: The image name for which to retrieve the configuration.

        Returns:
            NamedTuple:
                image_config: The image configuration.
                image_layers: The listing of image layer identifiers.
                manifest: The image-source specific manifest.
                manifest_layers: The listing of manifest layer identifiers.
        """

        # Retrieve the image configuration digest and layers identifiers from the manifest ...
        LOGGER.debug("Verifying Integrity: %s ...", image_name.resolve_name())
        manifest = await self.get_manifest(image_name, **kwargs)
        LOGGER.debug("    manifest digest: %s", xellipsis(manifest.get_digest()))
        config_digest = manifest.get_config_digest(image_name)
        LOGGER.debug("    config digest: %s", xellipsis(config_digest))
        manifest_layers = manifest.get_layers(image_name)
        LOGGER.debug("    manifest layers:")
        for layer in manifest_layers:
            LOGGER.debug("        %s", xellipsis(layer))

        # Retrieve the image configuration ...
        image_config = await self.get_image_config(image_name, **kwargs)
        config_digest_canonical = image_config.get_digest_canonical()
        LOGGER.debug(
            "    config digest (canonical): %s", xellipsis(config_digest_canonical)
        )
        must_be_equal(
            config_digest,
            image_config.get_digest(),
            "Image config digest mismatch",
        )

        # Retrieve the image layers from the image configuration ...
        image_layers = image_config.get_image_layers()
        LOGGER.debug("    image layers:")
        for layer in image_layers:
            LOGGER.debug("        %s", xellipsis(layer))

        # Quick check: Ensure that the layer counts are consistent
        must_be_equal(len(manifest_layers), len(image_layers), "Layer count mismatch")

        return ImageSourceVerifyImageConfig(
            image_config=image_config,
            image_layers=image_layers,
            manifest=manifest,
            manifest_layers=manifest_layers,
        )

    @abc.abstractmethod
    async def get_image_config(self, image_name: ImageName, **kwargs) -> ImageConfig:
        """
        Retrieves an image configuration (config.json).

        Args:
            image_name: The image name.

        Returns:
            The image configuration.
        """

    @abc.abstractmethod
    async def get_image_layer_to_disk(
        self, image_name: ImageName, layer: FormattedSHA256, file, **kwargs
    ) -> ImageSourceGetImageLayerToDisk:
        """
        Retrieves a single image layer stored to disk.

        Args:
            image_name: The image name.
            layer: The layer identifier in the form: <hash type>:<digest value>.
            file: File in which to store the image layer.
        """

    @abc.abstractmethod
    async def get_manifest(self, image_name: ImageName = None, **kwargs) -> Manifest:
        """
        Retrieves the manifest for a given image.

        Args:
            image_name: The name image for which to retrieve the manifest.

        Returns:
            The image source-specific manifest.
        """

    @abc.abstractmethod
    async def layer_exists(
        self, image_name: ImageName, layer: FormattedSHA256, **kwargs
    ) -> bool:
        """
        Checks if a given image layer exists.

        Args:
            image_name: The image name.
            layer: The layer identifier in the form: <hash type>:<digest value>.

        Returns:
            bool: True if the layer exists, False otherwise.
        """

    @abc.abstractmethod
    async def put_image(
        self,
        image_source,
        image_name: ImageName,
        manifest: Manifest,
        image_config: ImageConfig,
        layer_files: List,
        **kwargs,
    ):
        """
        Stores a given image (manifest, image_config, and layers) from another image source.

        Args:
            image_source: The source image source.
            image_name: The name of the image being stored.
            manifest: The image source-specific manifest to be stored, in source image source format.
            image_config: The image configuration to be stored.
            layer_files: List of files from which to read the layer content, in source image source format.
        """

    @abc.abstractmethod
    async def put_image_config(
        self, image_name: ImageName, image_config: ImageConfig, **kwargs
    ):
        """
        Assigns an image configuration (config.json).

        Args:
            image_name: The image name.
            image_config: The image configuration to be assigned.
        """

    @abc.abstractmethod
    async def put_image_layer(self, image_name: ImageName, content, **kwargs):
        """
        Assigns a single image layer.

        Args:
            image_name: The image name.
            content: The layer content.
        """

    @abc.abstractmethod
    async def put_image_layer_from_disk(self, image_name: ImageName, file, **kwargs):
        """
        Assigns a single image layer read from disk.

        Args:
            image_name: The image name.
            file: File from which to read the layer content.
        """

    @abc.abstractmethod
    async def put_manifest(
        self, manifest: Manifest, image_name: ImageName = None, **kwargs
    ):
        """
        Assigns the manifest for a given image.

        Args:
            manifest: The image source-specific manifest to be assigned.
            image_name: The name of the image for which to assign the manifest.
        """

    @abc.abstractmethod
    async def sign_image(
        self,
        signer: Signer,
        src_image_name: ImageName,
        dest_image_source,
        dest_image_name: ImageName,
        signature_type: SignatureTypes = SignatureTypes.SIGN,
        **kwargs,
    ) -> ImageSourceSignImage:
        """
        Retrieves, verifies and signs the image, storing it in the destination image source.

        Args:
            signer: The signer used to create the signature value.
            src_image_name: The source image name.
            dest_image_source: The destination image source into which to store the signed image.
            dest_image_name: The description image name.
            signature_type: Specifies what type of signature action to perform.

        Returns:
            NamedTuple:
                image_config: The ImageConfig object corresponding to the signed image.
                signature_value: as defined by :func:~docker_sign_verify.ImageConfig.sign.
                verify_image_data: as defined by :func:~docker_sign_verify.ImageSource.verify_image_integrity.
                manifest_signed: The signed image source-specific manifest.
        """

    @abc.abstractmethod
    async def verify_image_integrity(
        self, image_name: ImageName, **kwargs
    ) -> ImageSourceVerifyImageIntegrity:
        """
        Verifies that the image source data format is consistent with respect to the image configuration and image
        layers, and that the image configuration and image layers are internally consistent (the digest values match).

        Args:
            image_name: The image name.

        Returns:
            NamedTuple:
                compressed_layer_files: The list of compressed layer files on disk (optional).
                image config: The image configuration.
                manifest: The image source-specific manifest file (archive, registry, repository).
                uncompressed_layer_files: The list of uncompressed layer files on disk.
        """

    async def verify_image_signatures(
        self, image_name: ImageName, **kwargs
    ) -> ImageSourceVerifyImageSignatures:
        """
        Verifies that signatures contained within the image source data format are valid (that the image has not been
        modified since they were created)

        Args:
            image_name: The image name.

        Returns:
            NamedTuple:
                compressed_layer_files: The list of compressed layer files on disk (optional).
                image config: The image configuration.
                manifest: The image source-specific manifest file (archive, registry, repository).
                signatures: as defined by :func:~docker_sign_verify.ImageConfig.verify_signatures.
                uncompressed_layer_files: The list of uncompressed layer files on disk.
        """

        # Verify image integrity (we use the verified values from this point on)
        data = await self.verify_image_integrity(image_name, **kwargs)

        # Verify image signatures ...
        try:
            LOGGER.debug("Verifying Signature(s): %s ...", image_name.resolve_name())
            LOGGER.debug(
                "    config digest (signed): %s",
                xellipsis(data.image_config.get_digest()),
            )
            signatures = await data.image_config.verify_signatures(
                signer_kwargs=self.signer_kwargs
            )
            data = ImageSourceVerifyImageSignatures(
                compressed_layer_files=data.compressed_layer_files,
                image_config=data.image_config,
                manifest=data.manifest,
                signatures=signatures,
                uncompressed_layer_files=data.uncompressed_layer_files,
            )

            # List the image signatures ...
            LOGGER.debug("    signatures:")
            for result in data.signatures.results:
                if not hasattr(result, "valid"):
                    raise UnsupportedSignatureTypeError(
                        f"Unsupported signature type: {type(result)}!"
                    )

                if hasattr(result, "signer_short") and hasattr(result, "signer_long"):
                    if not result.valid:
                        raise SignatureMismatchError(
                            f"Verification failed for signature; {result.signer_short}"
                        )

                    for line in result.signer_long.splitlines():
                        LOGGER.debug(line)
                # Try to be friendly ...
                else:
                    if not result.valid:
                        raise SignatureMismatchError(
                            f"Verification failed for signature; unknown type: {type(result)}!"
                        )
                    LOGGER.debug("        Signature of unknown type: %s", type(result))
        except Exception:
            for file in data.compressed_layer_files + data.uncompressed_layer_files:
                file.close()
            raise

        LOGGER.debug("Signature check passed.")

        return data
