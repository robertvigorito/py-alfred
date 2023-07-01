"""This module creates the asset model for the structured data stored in the pymongo
asset collection.
"""
from dataclasses import (
    dataclass as _dataclass,
    field as _field,
)
from distutils import extension
import os as _os
from typing import (
    List,
    Dict,
    Optional,
    Type,
    Union
)

# Wgid Modules
from alfred.models.abstract_model import AbstractAsset
from alfred.models.contexts import context


@_dataclass(slots=True)
class _Asset(AbstractAsset):
    context: Type[context] = _field(default_factory=context, repr=False) # type: ignore
    type_: str = _field(default_factory=str)
    
    def __post_init__(self):
        #self.root = self.context.root / f"{self.type_}_{self.name}_{self.version:03d}"
        # Validate the context and the type_ is set
        if not isinstance(self.context, context):
            raise TypeError(f"Expected context to be of type context, got {type(self.context)}")
        if not isinstance(self.type_, str) or not self.type_:
            raise TypeError(f"Expected type_ to be of type str, got {type(self.type_)}")

    def  validate(self):
        return super().validate()
    
    def fullname(self):
        """Return the full name of the _Asset, which is composed of the context fullname and the asset name plus version."""
        return f"{self.context.fullname()}_{self.type_}_{self.name}_v{self.version:03d}"

    def registry(self, contents: Union[List[str], str], symlink: bool = False, rename: bool = False):
        """Register the asset in the database and copy or symlink the contents to the
        asset root directory.
        """
        if isinstance(contents, str):
            contents = [contents]
        fullname = self.fullname()

        for content in contents:
            print(content)
            # Create the asset file path
            extension = _os.path.splitext(content)[-1]
            asset_file_path = f"{fullname}/{fullname}{extension}"
            
            self.content_files.append(asset_file_path)

            
# /assets/{type}_{name}_{version:%03d}/{name}_{version:%03d}.{extension}
    
asset = _Asset # pylint: disable=invalid-name



job_context = context(job="alfred")
sequence_context = context(job=job_context.job, sequence="playground")
shot_context = context(job=job_context.job, sequence=sequence_context.sequence, shot="deleteme")


plate_job_asset = asset(
    context=job_context,
    name="mp01",
    comment="This is the plate asset",
    type_="plate",
    version=1,
)
print(plate_job_asset)
plate_job_asset = asset(
    context=job_context,
    name="mp01",
    comment="This is the plate asset",
    type_="plate",
    version=3,
)

path = "/d/dh5/PANA5668_prores.mov"

plate_job_asset.registry(contents=path, symlink=True)
print(plate_job_asset)

