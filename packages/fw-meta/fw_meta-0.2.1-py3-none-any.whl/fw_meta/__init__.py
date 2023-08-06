"""Flywheel meta extractor."""
import importlib.metadata as importlib_metadata

from .extract import MetaData, MetaExtractor, extract_meta

__all__ = ["MetaData", "MetaExtractor", "extract_meta"]
__version__ = importlib_metadata.version(__name__)
