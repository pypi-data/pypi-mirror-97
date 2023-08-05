"""Deetly utils.

Utility functions
"""
import hashlib
import re
import os
from typing import Dict
import uuid

import pandas
import pyarrow
import requests
import mimetypes
import urllib
import urllib3

from deetly.error import DatapackageError

def get_schema(
    df: pandas.DataFrame,
    resource_name: str,
    resource_description: str,
    format: str,
    compress: str,
    dsv_separator: str,
    spec: dict,
) -> dict:
    """Get Schema from Pandas dataframe.

    Args:
        df: pandas dataframe.
        resource_name: resoure name.
        resource_description: resource description.
        format: file format.
        compress: boolean. True for compressed files.
        dsv_separator: dsv/csv separator.
        spec: figure spec.

    Returns:
        dict
    """

    fields = []

    for name, dtype in zip(df.columns, df.dtypes):
        if str(dtype) == "object":
            dtype = "string"
        else:
            dtype = "number"

        description = ""
        if spec and spec.get("fields"):
            spec_fields = spec["fields"]
            for field in spec_fields:
                if field["name"] == name:
                    description = field["description"]

        fields.append({"name": name, "description": description, "type": dtype})

    mediatype = get_media_type(format)

    return {
        "name": resource_name,
        "description": resource_description,
        "format": format,
        "dsv_separator": dsv_separator,
        "compressed": compress,
        "mediatype": mediatype,
        "schema": {"fields": fields},
        "spec": spec,
    }


def get_media_type(fmt: str) -> str:
    """Guess media type from file type.

    Args:
        fmt: file type

    Returns:
        String
    """

    return mimetypes.types_map[fmt]


def get_resource_path(
    path: str, resource_name: str, fmt: str, compress: bool = False
) -> str:
    """Get path of resource file.

    Args:
        path: root path
        resource_name: name of the resource
        fmt: file type
        compress: boolean. True for compressed files

    Returns:
        String
    """
    if compress:
        return f"{path}/resources/{resource_name}.{fmt}.gz"
    else:
        return f"{path}/resources/{resource_name}.{fmt}"


def verify_add_resource_input_types(
    df: pandas.DataFrame, dataset_name: str, dataset_description: str
) -> None:
    if not isinstance(df, pandas.DataFrame):
        raise TypeError(f"df must be of type pandas.Dataframe()")
    if not isinstance(dataset_name, str):
        raise TypeError(f"dataset_name must be of type string")
    if not isinstance(dataset_description, str):
        raise TypeError(f"dataset_description must be of type string")


def get_id_from_metadata(metadata: Dict) -> str:
    """Get id from metadata dict if availble.

    If id not available then a new id is inserted.
    The id is calculated as a hash to metadata dict.

    Args:
        metadata: metadata dict

    Returns:
        String
    """

    name = metadata.get("name", None)
 
    space = None
    try: 
        space = os.environ["DEETLY_SPACE"]
    except:
        pass

    id_string = "-".join(filter(None, (space, name)))
    if id_string:
        hash_object = hashlib.md5(id_string.encode())
        dp_id = hash_object.hexdigest()
        dp_id = re.sub('[^0-9a-z]+', '-', dp_id.lower())
        return dp_id
    else:
        return str(uuid.uuid4())

def get_slug_from_metadata(metadata: Dict) -> str:
    """Get slug from metadata dict if available.

    If slug not available then a new slug is inserted.
    The slug depends on the title, team and space.

    Args:
        metadata: metadata dict

    Returns:
        String
    """

    name = metadata.get("name", None)
    
    space = None
    try: 
        space = os.environ["DEETLY_SPACE"]
    except:
        pass

    id_string = "-".join(filter(None, (space, name)))
    if id_string:
        dp_slug = urllib.parse.quote_plus(id_string)
        dp_slug = re.sub('[^0-9a-z]+', '-', dp_slug.lower())
        return dp_slug
    else:
        return str(uuid.uuid4())


def get_name_and_extension_from_url(resource_url: str) -> [str, str]:
    """Extract name and extension from url.

    Args:
        resource_url: resource URL

    Returns:
        String

    Raises:
        ValueError: If the input string is not a valid url format.
    """

    parsed_url = urllib3.util.parse_url(resource_url)

    if not parsed_url.scheme == "https" and not parsed_url.scheme == "http":
        raise ValueError(
            f"Remote resource needs to be a web address, scheme is {parsed_url.scheme}"
        )

    resource = parsed_url.path.split("/")[-1]

    name = resource.split(".", 1)[0]

    if len(name) == 0:
        raise ValueError(f"Url does not contain a filename")

    mimetype, encoding = mimetypes.guess_type(resource_url)
    extension = mimetypes.guess_extension(mimetype)

    if extension == None:
         raise ValueError(f"Unable to guess extension from mimetype")

    if len(extension) == 0:
        raise ValueError(f"Url does not contain an extension")

    return name, extension


def serialize_table(df: pandas.DataFrame, compress: bool = False) -> bytearray:
    """Serialize pandas dataframe to arrow buffer.

    Args:
        df: pandas dataframe.
        compress: boolean. True for compressed files.

    Returns:
        Bytearray
    """
    ser = pyarrow.serialize(df).to_buffer()
    return ser


def read_file(url: str) -> str:
    """Download file and return contents as a string.

    Args:
        url: File url

    Returns:
        str
    """

    try:
        c = requests.get(url)
        c.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(e)
        return ""

    return c.content


def upload_file(
    space: str,
    token: str,
    package_id: str,
    file_name: str,
    content_type: str,
    content: str,
    api_url: str
) -> str:
    """Upload file to storage.

    Args:
        space: Space Id
        token: Access token
        package_id: Datapackage id
        file_name: Name of the file
        content_type: Content type
        content: File content as string

    Returns:
        str
    """

    res = requests.post(
        f"{api_url}/store",
        json={
            "package_id": package_id,
            "content": content,
            "name": file_name,
            "content_type": content_type,
            "space": space,
            "token": token,
        },
    )

    return res.text

def upload_from_url(
    space: str,
    token: str,
    package_id: str,
    file_name: str,
    content_type: str,
    url: str,
    api_url: str
) -> str:
    """Upload file to storage.

    Args:
        space: Space Id
        token: Access token
        package_id: Datapackage id
        file_name: Name of the file
        content_type: Content type
        url: Source url

    Returns:
        str
    """

    res = requests.post(
        f"{api_url}/upload",
        json={
            "package_id": package_id,
            "url": url,
            "name": file_name,
            "content_type": content_type,
            "space": space,
            "token": token,
        },
    )

    return res.text


def index_document(space: str, token: str, doc: Dict, api_url: str) -> str:
    """Add/update Elastic search item.

    Args:
        token: Access token
        space: Space id
        doc: Document (JSON) to add to index

    Returns:
        str
    """

    res = requests.post(
        f"{api_url}/index", json={"space": space, "token": token, "doc": doc}
    )

    return res.text
