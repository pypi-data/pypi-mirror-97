from schema import Schema, And, Or, Use, Optional
from typing import Any, Dict, List
from datetime import datetime
from dateutil import parser

is_datetime_string = lambda date: isinstance(parser.parse(date), datetime)

datapackage_optional_schema = {
    Optional("title"): str,
    Optional("type"): str,
    Optional("format"): str,
    Optional("space"): str,
    Optional("theme"): str,
    Optional("identifier"): str,
    Optional("landingPage"): str,
    Optional("team"): str,
    Optional("bucket"): str,
    Optional("store"): str,
    Optional("repo"): str,
    Optional("temporal"): str,
}

def validate_datapackage_minimal(package: Dict):

    package_schema = {
        'name': And(str, len),
        Optional('license'): And(str, len),
        Optional('description'): And(str, len),
        Optional('author'): And(str, len),
        Optional('issued'): And(Use(is_datetime_string)),
        Optional("modified"): And(Use(is_datetime_string)),
        Optional("language"): Or(str,[str]),
        Optional('keywords'): Or(str,[str]),
        Optional("keyword"): Or(str,[str]),
        Optional("publisher"): object,
        Optional("distribution"): [object],
        Optional("spatial"): str,
        }

    package_schema.update(datapackage_optional_schema)

    return   Schema(package_schema).validate(package)

def validate_datapackage_dcat2(package: Dict):

    package_schema = {
        'title': And(str, len),
        'description': And(str, len),
        'issued': And(Use(is_datetime_string)),
        "modified": And(Use(is_datetime_string)),
        "language": Or(str,[str]),
        "keyword": Or(str,[str]),
        "publisher": object,
        "distribution": [object]
        }

    package_schema.update(datapackage_optional_schema)
    package_schema.update({Optional("name"): str})

    return   Schema(package_schema).validate(package)