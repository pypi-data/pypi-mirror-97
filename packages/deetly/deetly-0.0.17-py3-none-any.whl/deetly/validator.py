from schema import Schema, And, Or, Use, Optional
from typing import Any, Dict, List
from datetime import datetime
from dateutil import parser

is_datetime_string = lambda date: isinstance(parser.parse(date), datetime)

datapackage_optional_schema = {
    Optional("id"): str,
    Optional("author"): str,
    Optional("accrualPeriodicity"): Or(str,object),
    Optional("accessRights"): Or(str,[str]),
    Optional("accessRightsComments"): Or(str,[str]),
    Optional("bucket"): str,
    Optional("byteSize"): Or(str,int),
    Optional("category"): str,
    Optional("creator"): Or(str,{
         "name" : str,
         "email" : str,
     }),
    Optional("contactpoint"): [],
    Optional("code"): str,
    Optional("description"): str,
    Optional("distribution"): [],
    Optional("format"): str,
    Optional("identifier"): str,
    Optional("issued"): And(Use(is_datetime_string)),
    Optional("keyword"): Or(str,[str]),
    Optional("keywords"): Or(str,[str]),
    Optional("landingPage"): str,
    Optional("language"): str,
    Optional("license"): Or(str,{
         "name" : str,
         "url" : str,
     }),
    Optional("modified"): And(Use(is_datetime_string)),
    Optional("notebook"): str,
    Optional("provenance"): Or(str,object),
    Optional("publisher"): str,
    Optional("repo"): str,
    Optional("rights"): str,
    Optional("sample"): [str],
    Optional("suggest"): str,
    Optional("space"): str,
    Optional("source"): str,
    Optional("spatial"): [str],
    Optional("status"): str,
    Optional("store"): str,
    Optional("url"): str,
    Optional("team"): str,
    Optional("term"): str,
    Optional("temporal"): str,
    Optional("theme"): str,
    Optional("title"): str,
    Optional("type"): str,
    Optional("versionInfo"): str,
    Optional("versionNotes"): str,

}

def validate_datapackage_minimal(package: Dict):

    package_schema = {
        Or("title", "name", only_one=False):  And(str, len),
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