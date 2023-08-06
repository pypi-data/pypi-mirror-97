from abc import ABC, abstractmethod
from io import BytesIO
from pathlib import Path
from typing import Dict, Union

import frictionless


class ValidataResource(ABC):
    """A resource to validate: url or uploaded file"""

    @abstractmethod
    def build_table_args(self):
        """return (source, option_dict)"""
        pass

    @abstractmethod
    def get_source(self):
        """return filename or URL"""
        pass

    def extract_tabular_data(self):
        """Extract header and data rows from source."""
        table_source, table_options = self.build_table_args()
        return _extract_header_and_rows_from_frictionless_source(
            table_source, **table_options
        )

    @classmethod
    def detect_encoding(cls, bytes_data):
        """Try to decode using utf-8 first, fallback on frictionless helper function."""
        try:
            bytes_data.decode("utf-8")
            return "utf-8"
        except UnicodeDecodeError:
            encoding = frictionless.Detector().detect_encoding(bytes_data)
            return encoding.lower() if encoding else None


class URLValidataResource(ValidataResource):
    """URL resource"""

    def __init__(self, url):
        """Built from URL"""
        self.url = url

    def get_source(self):
        return self.url

    def build_table_args(self):
        """URL implementation"""
        return (
            self.url,
            {
                "detector": frictionless.Detector(
                    encoding_function=ValidataResource.detect_encoding
                )
            },
        )


class FileContentValidataResource(ValidataResource):
    """Uploaded file resource"""

    def __init__(self, filename: str, content: bytes):
        """Built from filename and bytes content"""
        self.filename = filename
        self.file_ext = Path(filename).suffix.lower()
        self.content = content

    def get_source(self):
        return self.filename

    def build_table_args(self):
        """Uploaded file implementation"""

        def detect_format_from_file_extension(file_ext: str):
            if file_ext in (".csv", ".tsv", ".ods", ".xls", ".xlsx"):
                return file_ext[1:]
            return None

        format = detect_format_from_file_extension(self.file_ext)
        options = {
            "format": format,
            "detector": frictionless.Detector(
                encoding_function=ValidataResource.detect_encoding
            ),
        }
        if format in {"csv", "tsv"}:
            options["encoding"] = ValidataResource.detect_encoding(self.content)
        source = self.content

        return (source, options)


def _extract_header_and_rows_from_frictionless_source(source, **source_options):
    """Extract header and data rows from frictionless source and options."""
    with frictionless.Resource(source, **source_options) as res:
        rows = list(res.read_lists())
        if not rows:
            raise ValueError("Empty source")
        return rows[0], rows[1:]


def is_body_error(err: Union[frictionless.errors.Error, Dict]) -> bool:
    """Classify the given error as 'body error' according to its tags."""
    tags = err.tags if isinstance(err, frictionless.errors.Error) else err["tags"]
    return "#body" in tags or "#content" in tags


def is_structure_error(err: Union[frictionless.errors.Error, Dict]) -> bool:
    """Classify the given error as 'structure error' according to its tags."""
    tags = err.tags if isinstance(err, frictionless.errors.Error) else err["tags"]
    return "#head" in tags or "#structure" in tags
