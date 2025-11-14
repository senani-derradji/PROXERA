from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
import os

max_size = 5_000_000
providers = ['AZURE', 'GCP', 'AWS']
data_types = [".jpg", ".jpeg", ".png", ".gif", ".bmp",".tif", ".tiff", ".webp", ".svg", ".heic", ".heif"]

def is_valid_file_type(path: str) -> bool:
    return path.lower().endswith(tuple(data_types))


class DataPayload(BaseModel):
    data: bytes
    @field_validator("data", mode='before')
    def validate_data(cls, value):
        if not value:
           raise ValueError("Data must not be empty.")
        if not isinstance(value, bytes):
            raise TypeError("Data must be of type bytes.")
        if len(value) > max_size:
            raise ValueError("Data Payload is Too Long")
        return value