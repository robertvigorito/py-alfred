"""This module creates the asset model for the structured data stored in the pymongo
asset collection.
"""
from dataclasses import (
    MISSING,
    dataclass as _dataclass,
    field as _field,
)
import os as _os
from typing import List, Optional, Union

# Wgid Modules
from alfred.models.abstract_model import AbstractAsset
from alfred.models.contexts import Context


@_dataclass
class Asset(AbstractAsset):
    """The asset model for the structured data stored in the pymongo asset collection."""

    def __post_init__(self):
        if not isinstance(self.context, Context):
            raise TypeError(f"Expected context to be of type context, got {type(self.context)}")
        if not isinstance(self.type_, str) or not self.type_:
            raise TypeError(f"Expected type_ to be of type str, got {type(self.type_)}")
        if not isinstance(self.name, str) or not self.name:
            raise TypeError(f"Expected name to be of type str, got {type(self.name)}")
    
    def validate(self):
        return super().validate()

    def fullname(self):
        """Return the full name of the _Asset, which is composed of the context fullname
        and the asset name plus version.
        """
        return f"{self.context.fullname()}_{self.type_}_{self.name}_v{self.version:03d}"
    
    def inject(self, content: str, key: Optional[str] = None, overwrite: bool = False):
        """Inject the data source into the content files.
        
        Args:
            key (str): The key to inject into the content files.
            value (str): The value to inject into the content files.
            overwrite (bool, optional): Whether to overwrite the key if it already exists. Defaults to False.
        
        Raises:
            ValueError: If the key already exists in the content files and overwrite is False.
        
        Returns:
            bool: Whether the injection was successful.
        """
        key = key or "*"
        if not overwrite and key in self.content_files:
            raise ValueError(f"Key {key} already exists in content files.")
        self.content_files[key] = content
        return True
    
    def inject_many(self, data: dict, overwrite: bool = False):
        """Inject many data sources into the content files.
        
        Args:
            data (dict): The data to inject into the content files.
            overwrite (bool, optional): Whether to overwrite the key if it already exists. Defaults to False.
        
        Raises:
            ValueError: If the key already exists in the content files and overwrite is False.
        
        Returns:
            bool: Whether the injection was successful.
        """
        for key, value in data.items():
            self.inject(key, value, overwrite)
        return True

        
