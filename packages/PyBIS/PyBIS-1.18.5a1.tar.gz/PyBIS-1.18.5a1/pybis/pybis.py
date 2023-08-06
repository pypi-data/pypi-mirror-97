#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
pybis.py

Work with openBIS from Python.

"""

from __future__ import print_function
import os
import random
import subprocess
import errno

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import time
import json
import re
from urllib.parse import urlparse, urljoin, quote
import zlib
from collections import namedtuple, defaultdict
from texttable import Texttable
from tabulate import tabulate

from . import data_set as pbds
from .utils import parse_jackson, check_datatype, split_identifier, format_timestamp, is_identifier, is_permid, nvl, VERBOSE
from .utils import extract_attr, extract_permid, extract_code,extract_deletion,extract_identifier,extract_nested_identifier,extract_nested_permid, extract_nested_permids, extract_identifiers,extract_property_assignments,extract_role_assignments,extract_person, extract_person_details,extract_id,extract_userId, is_number
from .entity_type import EntityType, SampleType, DataSetType, MaterialType, ExperimentType
from .vocabulary import Vocabulary, VocabularyTerm
from .openbis_object import OpenBisObject, Transaction
from .definitions import openbis_definitions, get_definition_for_entity, fetch_option, get_fetchoption_for_entity, get_type_for_entity, get_method_for_entity, get_fetchoptions


# import the various openBIS entities
from .things import Things
from .space import Space
from .project import Project
from .experiment import Experiment
from .sample import Sample
from .dataset import DataSet
from .person import Person
from .group import Group
from .role_assignment import RoleAssignment
from .tag import Tag
from .semantic_annotation import SemanticAnnotation

from pandas import DataFrame, Series
import pandas as pd

from datetime import datetime

LOG_NONE    = 0
LOG_SEVERE  = 1
LOG_ERROR   = 2
LOG_WARNING = 3
LOG_INFO    = 4
LOG_ENTRY   = 5
LOG_PARM    = 6
LOG_DEBUG   = 7

DEBUG_LEVEL = LOG_NONE


def get_search_type_for_entity(entity, operator=None):
    """ Returns a dictionary containing the correct search criteria type
    for a given entity.

    Example::
        get_search_type_for_entity('space')
        # returns:
        {'@type': 'as.dto.space.search.SpaceSearchCriteria'}
    """
    search_criteria = {
        "space": "as.dto.space.search.SpaceSearchCriteria",
        "userId": "as.dto.person.search.UserIdSearchCriteria",
        "email": "as.dto.person.search.EmailSearchCriteria",
        "firstName": "as.dto.person.search.FirstNameSearchCriteria",
        "lastName": "as.dto.person.search.LastNameSearchCriteria",
        "project": "as.dto.project.search.ProjectSearchCriteria",
        "experiment": "as.dto.experiment.search.ExperimentSearchCriteria",
        "experiment_type": "as.dto.experiment.search.ExperimentTypeSearchCriteria",
        "sample": "as.dto.sample.search.SampleSearchCriteria",
        "sample_type": "as.dto.sample.search.SampleTypeSearchCriteria",
        "dataset": "as.dto.dataset.search.DataSetSearchCriteria",
        "dataset_type": "as.dto.dataset.search.DataSetTypeSearchCriteria",
        "external_dms": "as.dto.externaldms.search.ExternalDmsSearchCriteria",
        "material": "as.dto.material.search.MaterialSearchCriteria",
        "material_type": "as.dto.material.search.MaterialTypeSearchCriteria",
        "vocabulary_term": "as.dto.vocabulary.search.VocabularyTermSearchCriteria",
        "tag": "as.dto.tag.search.TagSearchCriteria",
        "authorizationGroup": "as.dto.authorizationgroup.search.AuthorizationGroupSearchCriteria",
        "person": "as.dto.person.search.PersonSearchCriteria",
        "code": "as.dto.common.search.CodeSearchCriteria",
        "global": "as.dto.global.GlobalSearchObject",
        "plugin": "as.dto.plugin.search.PluginSearchCriteria",
        "propertyType": "as.dto.property.search.PropertyTypeSearchCriteria",
    }

    sc = { "@type": search_criteria[entity] }
    if operator is not None:
        sc["operator"] = operator

    return sc


def _type_for_id(ident, entity):
    ident = ident.strip()
    """Returns the data type for a given identifier/permId for use with the API call, e.g.
    {
        "identifier": "/DEFAULT/SAMPLE_NAME",
        "@type": "as.dto.sample.id.SampleIdentifier"
    }
    or
    {
        "permId": "20160817175233002-331",
        "@type": "as.dto.sample.id.SamplePermId"
    }
    """
    # Tags have strange permIds...
    if entity.lower() == 'tag':
        if '/' in ident:
            if not ident.startswith('/'):
                ident = '/'+ident
            return {
                "permId": ident,
                "@type" : "as.dto.tag.id.TagPermId"
            }
        else:
            return {
                "code": ident,
                "@type": "as.dto.tag.id.TagCode"
            }

    entities = {
        "sample"            : "Sample",
        "dataset"           : "DataSet",
        "experiment"        : "Experiment",
        "plugin"            : "Plugin",
        "space"             : "Space",
        "project"           : "Project",
        "semanticannotation": "SemanticAnnotation",
    }
    search_request = {}
    if entity.lower() in entities:
        entity_capitalize = entities[entity.lower()]
    else:
        entity_capitalize = entity.capitalize()

    if is_identifier(ident):
        # people tend to omit the / prefix of an identifier...
        if not ident.startswith('/'):
            ident = '/'+ident
        # ELN-LIMS style contains also experiment in sample identifer, i.e. /space/project/experiment/sample_code
        # we have to remove the experiment-code
        if ident.count('/') == 4:
            codes = ident.split('/')
            ident = '/'.join([codes[0], codes[1], codes[2], codes[4]])

        search_request = {
            "identifier": ident.upper(),
            "@type": "as.dto.{}.id.{}Identifier".format(entity.lower(), entity_capitalize)
        }
    else:
        search_request = {
            "permId": ident,
            "@type": "as.dto.{}.id.{}PermId".format(entity.lower(), entity_capitalize)
        }
    return search_request

def get_search_criteria(entity, **search_args):
    search_criteria = get_search_type_for_entity(entity)

    criteria = []
    attrs = openbis_definitions(entity)['attrs']
    for attr in attrs:
        if attr in search_args:
            sub_crit = get_search_type_for_entity(attr)
            sub_crit['fieldValue'] = get_field_value_search(attr, search_args[attr])
            criteria.append(sub_crit)

    search_criteria['criteria'] = criteria
    search_criteria['operator'] = "AND"

    return search_criteria

def crc32(fileName):
    """since Python3 the zlib module returns unsigned integers (2.7: signed int)
    """
    prev = 0
    for eachLine in open(fileName, "rb"):
        prev = zlib.crc32(eachLine, prev)
    # return as hex
    return "%x" % (prev & 0xFFFFFFFF)


def _tagIds_for_tags(tags=None, action='Add'):
    """creates an action item to add or remove tags. 
    Action is either 'Add', 'Remove' or 'Set'
    """
    if tags is None:
        return
    if not isinstance(tags, list):
        tags = [tags]

    items = []
    for tag in tags:
        items.append({
            "code": tag,
            "@type": "as.dto.tag.id.TagCode"
        })

    tagIds = {
        "actions": [
            {
                "items": items,
                "@type": "as.dto.common.update.ListUpdateAction{}".format(action.capitalize())
            }
        ],
        "@type": "as.dto.common.update.IdListUpdateValue"
    }
    return tagIds


def _list_update(ids=None, entity=None, action='Add'):
    """creates an action item to add, set or remove ids. 
    """
    if ids is None:
        return
    if not isinstance(ids, list):
        ids = [ids]

    items = []
    for ids in ids:
        items.append({
            "code": ids,
            "@type": "as.dto.{}.id.{}Code".format(entity.lower(), entity)
        })

    list_update = {
        "actions": [
            {
                "items": items,
                "@type": "as.dto.common.update.ListUpdateAction{}".format(action.capitalize())
            }
        ],
        "@type": "as.dto.common.update.IdListUpdateValue"
    }
    return list_update


def get_field_value_search(field, value, comparison="StringEqualToValue"):
    return {
        "value": value,
        "@type": "as.dto.common.search.{}".format(comparison)
    }

def _common_search(search_type, value, comparison="StringEqualToValue"):
    sreq = {
        "@type": search_type,
        "fieldValue": {
            "value": value,
            "@type": "as.dto.common.search.{}".format(comparison)
        }
    }
    return sreq


def _criteria_for_code(code):
    return {
        "fieldValue": {
            "value": code.upper(),
            "@type": "as.dto.common.search.StringEqualToValue"
        },
        "@type": "as.dto.common.search.CodeSearchCriteria"
    }

def _subcriteria_for_userId(userId):
    return {
          "criteria": [
            {
              "fieldName": "userId",
              "fieldType": "ATTRIBUTE",
              "fieldValue": {
                "value": userId,
                "@type": "as.dto.common.search.StringEqualToValue"
              },
              "@type": "as.dto.person.search.UserIdSearchCriteria"
            }
          ],
          "@type": "as.dto.person.search.PersonSearchCriteria",
          "operator": "AND"
        }


def _subcriteria_for_type(code, entity):
    return {
        "@type": "as.dto.{}.search.{}TypeSearchCriteria".format(entity.lower(), entity),
        "criteria": [
            {
                "@type": "as.dto.common.search.CodeSearchCriteria",
                "fieldValue": {
                    "value": code.upper(),
                    "@type": "as.dto.common.search.StringEqualToValue"
                }
            }
        ]
    }


def _subcriteria_for_status(status_value):
    status_value = status_value.upper()
    valid_status = "AVAILABLE LOCKED ARCHIVED UNARCHIVE_PENDING ARCHIVE_PENDING BACKUP_PENDING".split()
    if not status_value in valid_status:
        raise ValueError("status must be one of the following: " + ", ".join(valid_status))

    return {
        "@type": "as.dto.dataset.search.PhysicalDataSearchCriteria",
        "operator": "AND",
        "criteria": [{
            "@type":
                "as.dto.dataset.search.StatusSearchCriteria",
            "fieldName": "status",
            "fieldType": "ATTRIBUTE",
            "fieldValue": status_value
        }]
    }


def _gen_search_criteria(req):
    sreq = {}
    for key, val in req.items():
        if key == "criteria":
            items = []
            for item in req['criteria']:
                items.append(_gen_search_criteria(item))
            sreq['criteria'] = items
        elif key == "code":
            sreq["criteria"] = [_common_search(
                "as.dto.common.search.CodeSearchCriteria", val.upper()
            )]
        elif key == "identifier":
            if is_identifier(val):
                # if we have an identifier, we need to search in Space and Code separately
                si = split_identifier(val)
                sreq["criteria"] = []
                if "space" in si:
                    sreq["criteria"].append(
                        _gen_search_criteria({"space": "Space", "code": si["space"]})
                    )
                if "experiment" in si:
                    pass

                if "code" in si:
                    sreq["criteria"].append(
                        _common_search(
                            "as.dto.common.search.CodeSearchCriteria", si["code"].upper()
                        )
                    )
            elif is_permid(val):
                sreq["criteria"] = [_common_search(
                    "as.dto.common.search.PermIdSearchCriteria", val
                )]
            else:
                # we assume we just got a code
                sreq["criteria"] = [_common_search(
                    "as.dto.common.search.CodeSearchCriteria", val.upper()
                )]

        elif key == "operator":
            sreq["operator"] = val.upper()
        else:
            sreq["@type"] = "as.dto.{}.search.{}SearchCriteria".format(key, val)
    return sreq


def _subcriteria_for_tags(tags):
    if not isinstance(tags, list):
        tags = [tags]

    criteria = []
    for tag in tags:
        criteria.append({
            "fieldName": "code",
            "fieldType": "ATTRIBUTE",
            "fieldValue": {
                "value": tag,
                "@type": "as.dto.common.search.StringEqualToValue"
            },
            "@type": "as.dto.common.search.CodeSearchCriteria"
        })

    return {
        "@type": "as.dto.tag.search.TagSearchCriteria",
        "operator": "AND",
        "criteria": criteria
    }


def _subcriteria_for_is_finished(is_finished):
    return {
        "@type": "as.dto.common.search.StringPropertySearchCriteria",
        "fieldName": "FINISHED_FLAG",
        "fieldType": "PROPERTY",
        "fieldValue": {
            "value": is_finished,
            "@type": "as.dto.common.search.StringEqualToValue"
        }
    }


def _subcriteria_for_properties(prop, value, entity):
    """This internal method creates the JSON RPC criterias for searching
    in properties. It distinguishes between numbers, dates and strings
    and uses the comparative operator (< > >= <=), if available.
    creationDate and modificationDate attributes can be searched as well.
    To search in the properties of parents, children, etc. the user has to
    prefix the propery accordingly:

    - parent_propertyName
    - child_propertyName
    - container_propertyName
    """

    search_types = {
        'sample': {
            'parent'    : "as.dto.sample.search.SampleParentsSearchCriteria",
            'parents'   : "as.dto.sample.search.SampleParentsSearchCriteria",
            'child'     : "as.dto.sample.search.SampleChildrenSearchCriteria",
            'children'  : "as.dto.sample.search.SampleChildrenSearchCriteria",
            'container' : "as.dto.sample.search.SampleContainerSearchCriteria",
        },
        'dataset': {
            'parent'    : "as.dto.dataset.search.DataSetParentsSearchCriteria",
            'parents'   : "as.dto.dataset.search.DataSetParentsSearchCriteria",
            'child'     : "as.dto.dataset.search.DataSetChildrenSearchCriteria",
            'children'  : "as.dto.dataset.search.DataSetChildrenSearchCriteria",
            'container' : "as.dto.dataset.search.DataSetContainerSearchCriteria",
        }
    }

    # default values of fieldType, str_type and eq_type
    fieldType = "PROPERTY"
    eq_type = "as.dto.common.search.StringEqualToValue"
    str_type=  "as.dto.common.search.StringPropertySearchCriteria"

    is_date = False
    if 'date' in prop.lower() and re.search(r'\d{4}\-\d{2}\-\d{2}', value):
        is_date = True
        eq_type = "as.dto.common.search.DateEqualToValue"
        if prop.lower().endswith('registrationdate'):
            str_type = "as.dto.common.search.RegistrationDateSearchCriteria"
            fieldType = "ATTRIBUTE"
        elif prop.lower().endswith('modificationdate'):
            str_type = "as.dto.common.search.ModificationDateSearchCriteria"
            fieldType = "ATTRIBUTE"
        else:
            str_type = "as.dto.common.search.DatePropertySearchCriteria"


    if any(str(value).startswith(operator) for operator in ['>','<','=']):
        match = re.search(r"""
            ^
            (?P<comp_operator>\>\=|\>|\<\=|\<|\=\=|\=)  # extract the comparative operator
            \s*
            (?P<value>.*)                           # extract the value
            """,
            value,
            flags=re.X
        )
        if match:
            comp_operator = match.groupdict()['comp_operator']
            value = match.groupdict()['value']

            # date comparison
            if is_date:
                if comp_operator == '>':
                    eq_type = "as.dto.common.search.DateLaterThanOrEqualToValue"
                elif comp_operator == '>=':
                    eq_type = "as.dto.common.search.DateLaterThanOrEqualToValue"
                elif comp_operator == '<':
                    eq_type = "as.dto.common.search.DateEarlierThanOrEqualToValue"
                elif comp_operator == '<=':
                    eq_type = "as.dto.common.search.DateEarlierThanOrEqualToValue"
                else:
                    eq_type = "as.dto.common.search.DateEqualToValue"

            # numeric comparison
            elif is_number(value):
                str_type = "as.dto.common.search.NumberPropertySearchCriteria"
                if comp_operator == '>':
                    eq_type = "as.dto.common.search.NumberGreaterThanValue"
                elif comp_operator == '>=':
                    eq_type = "as.dto.common.search.NumberGreaterThanOrEqualToValue"
                elif comp_operator == '<':
                    eq_type = "as.dto.common.search.NumberLessThanValue"
                elif comp_operator == '<=':
                    eq_type = "as.dto.common.search.NumberLessThanOrEqualToValue"
                else:
                    eq_type = "as.dto.common.search.NumberEqualToValue"

            # string comparison
            else:
                if comp_operator == '>':
                    eq_type = "as.dto.common.search.StringGreaterThanValue"
                elif comp_operator == '>=':
                    eq_type = "as.dto.common.search.StringGreaterThanOrEqualToValue"
                elif comp_operator == '<':
                    eq_type = "as.dto.common.search.StringLessThanValue"
                elif comp_operator == '<=':
                    eq_type = "as.dto.common.search.StringLessThanOrEqualToValue"
                #elif comp_operator == '=':
                #    eq_type = "as.dto.common.search.StringEqualToValue"
                else:
                    eq_type = "as.dto.common.search.StringEqualToValue"


    # searching for parent/child/container identifier
    if any(relation == prop.lower() for relation in ['parent','child','container','parents','children','containers']):
        relation=prop.lower()
        if is_identifier(value):
            identifier_search_type = "as.dto.common.search.IdentifierSearchCriteria"
        # find any parent, child, container
        elif value == '*':
            return {
                "@type": search_types[entity][relation],
                "criteria": [
                    {
                        "@type": "as.dto.common.search.AnyFieldSearchCriteria",
                        "fieldValue": {
                            "@type": "as.dto.common.search.AnyStringValue",
                        }
                    }
                ]
            }
        elif is_permid(value):
            identifier_search_type = "as.dto.common.search.PermIdSearchCriteria"
        else: 
            identifier_search_type = "as.dto.common.search.CodeSearchCriteria"
        return {
            "@type": search_types[entity][relation],
            "criteria": [
                {
                    "@type": identifier_search_type,
                    "fieldType": "ATTRIBUTE",
                    "fieldValue": {
                        "@type": "as.dto.common.search.StringEqualToValue",
                        "value": value,
                    }
                }
            ]
        }

    # searching for parent/child/container property: 
    elif any(prop.lower().startswith(relation) for relation in ['parent_','child_','container_']):
        match = re.search(r'^(\w+?)_(.*)', prop.lower())
        if match:
            relation, property_name = match.groups()
            return {
                "@type": search_types[entity][relation],
                "criteria": [
                    {
                        "@type": str_type,
                        "fieldName": property_name.upper(),
                        "fieldType": fieldType,
                        "fieldValue": {
                            "@type": eq_type,
                            "value": value,
                        }
                    }
                ]
            }

    # searching for properties
    if prop.startswith('_'):
        fieldName = '$'+prop[1:]
    else:
        fieldName = prop
    return {
        "@type": str_type,
        "fieldName": fieldName.upper(),
        "fieldType": fieldType,
        "fieldValue": {
            "value": value,
            "@type": eq_type
        }
    }

def _subcriteria_for(thing, entity, parents_or_children='', operator='AND'):
    """Returns the sub-search criteria for «thing», which can be either:
    - a python object (sample, dataSet, experiment)
    - a permId
    - an identifier
    - a code
    """

    if isinstance(thing, str):
        if is_permid(thing):
            return _subcriteria_for_permid(
                thing, 
                entity=entity,
                parents_or_children=parents_or_children,
                operator=operator
            )
        elif is_identifier(thing):
            return _subcriteria_for_identifier(
                thing, 
                entity=entity,
                parents_or_children=parents_or_children,
                operator=operator
            )
        else:
            # look for code
            return _subcriteria_for_code_new(
                thing,
                entity=entity,
                parents_or_children=parents_or_children,
                operator=operator
            )

    elif isinstance(thing, list):
        criteria = []
        for element in thing:
            crit = _subcriteria_for(element, entity, parents_or_children, operator)
            criteria += crit["criteria"]

        return {
            "criteria": criteria,
            "@type": crit["@type"],
            "operator": "OR"
        }
    elif thing is None:
        # we just need the type
        search_type = get_type_for_entity(entity, 'search', parents_or_children)
        return {
            "criteria": [],
            **search_type,
            "operator": operator
        }
    else:
        # we passed an object
        return _subcriteria_for_permid(
            thing.permId, 
            entity=entity,
            parents_or_children=parents_or_children,
            operator=operator
        )
        

def _subcriteria_for_identifier(ids, entity, parents_or_children='', operator='AND'):
    if not isinstance(ids, list):
        ids = [ids]

    criteria = []
    for id in ids:
        criteria.append({
            "@type": "as.dto.common.search.IdentifierSearchCriteria",
            "fieldValue": {
                "value": id,
                "@type": "as.dto.common.search.StringEqualToValue"
            },
            "fieldType": "ATTRIBUTE",
            "fieldName": "identifier"
        })

    search_type = get_type_for_entity(entity, 'search', parents_or_children)
    return {
        "criteria": criteria,
        **search_type,
        "operator": operator
    }


def _subcriteria_for_permid(permids, entity, parents_or_children='', operator='AND'):
    if not isinstance(permids, list):
        permids = [permids]

    criteria = []
    for permid in permids:
        criteria.append({
            "@type": "as.dto.common.search.PermIdSearchCriteria",
            "fieldValue": {
                "value": permid,
                "@type": "as.dto.common.search.StringEqualToValue"
            },
            "fieldType": "ATTRIBUTE",
            "fieldName": "code"
        })

    search_type = get_type_for_entity(entity, 'search', parents_or_children)
    return {
        "criteria": criteria,
        **search_type,
        "operator": operator
    }


def _subcriteria_for_code_new(codes, entity, parents_or_children='', operator='AND'):
    if not isinstance(codes, list):
        codes = [codes]

    criteria = []
    for code in codes:
        criteria.append({
            "@type": "as.dto.common.search.CodeSearchCriteria",
            "fieldValue": {
                "value": code,
                "@type": "as.dto.common.search.StringEqualToValue"
            },
            "fieldType": "ATTRIBUTE",
            "fieldName": "code"
        })

    search_type = get_type_for_entity(entity, 'search', parents_or_children)
    return {
        "criteria": criteria,
        **search_type,
        "operator": operator
    }


def _subcriteria_for_code(code, entity):
    """ Creates the often used search criteria for code values. Returns a dictionary.

    Example::
        _subcriteria_for_code("username", "space")

    {
        "criteria": [
            {
                "fieldType": "ATTRIBUTE",
                "@type": "as.dto.common.search.CodeSearchCriteria",
                "fieldName": "code",
                "fieldValue": {
                    "@type": "as.dto.common.search.StringEqualToValue",
                    "value": "USERNAME"
                }
            }
        ],
        "operator": "AND",
        "@type": "as.dto.space.search.SpaceSearchCriteria"
    }
    """
    if code is not None:
        if is_permid(code):
            fieldname = "permId"
            fieldtype = "as.dto.common.search.PermIdSearchCriteria"
        else:
            fieldname = "code"
            fieldtype = "as.dto.common.search.CodeSearchCriteria"

         
        #search_criteria = get_search_type_for_entity(entity.lower())
        search_criteria = get_type_for_entity(entity, 'search')
        search_criteria['criteria'] = [{
            "fieldName": fieldname,
            "fieldType": "ATTRIBUTE",
            "fieldValue": {
                "value": code.upper(),
                "@type": "as.dto.common.search.StringEqualToValue"
            },
            "@type": fieldtype
        }]
        
        search_criteria["operator"] = "AND"
        return search_criteria
    else:
        return get_type_for_entity(entity, 'search')
        #return get_search_type_for_entity(entity.lower())


class Openbis:
    """Interface for communicating with openBIS. 

    Note:
        * A recent version of openBIS is required (minimum 16.05.2).
        * For creation of datasets, the dataset-uploader-api ingestion plugin must be present.

    """

    def __init__(self, url=None, verify_certificates=True, token=None,
        use_cache=True,
        allow_http_but_do_not_use_this_in_production_and_only_within_safe_networks=False,
        token_path=None
    ):
        """Initialize a new connection to an openBIS server.

        Examples:
            o = Openbis('https://openbis.example.com')
            o_test = Openbis('https://test_openbis.example.com:8443', verify_certificates=False)

        Args:
            url (str): https://openbis.example.com
            verify_certificates (bool): set to False when you use self-signed certificates
            token (str): a valid openBIS token. If not set, pybis will try to read a valid token from ~/.pybis
            token_path: a path to a file which contains an openBIS token
            use_cache: make openBIS to store spaces, projects, sample types, vocabulary terms and oder more-or-less static objects to optimise speed
            allow_http_but_do_not_use_this_in_production_and_only_within_safe_networks (bool): False
        """

        self.as_v3 = '/openbis/openbis/rmi-application-server-v3.json'
        self.as_v1 = '/openbis/openbis/rmi-general-information-v1.json'
        self.reg_v1 = '/openbis/openbis/rmi-query-v1.json'
        self.verify_certificates = verify_certificates

        if url is None:
            url = os.environ.get("OPENBIS_URL") or os.environ.get('OPENBIS_HOST')
            if url is None:
                raise ValueError("please provide a URL you want to connect to.")

        if not url.startswith('http'):
            url = 'https://'+url

        url_obj = urlparse(url)
        if url_obj.netloc is None or url_obj.netloc == '':
            raise ValueError("please provide the url in this format: https://openbis.host.ch:8443")
        if url_obj.hostname is None:
            raise ValueError("hostname is missing")
        if url_obj.scheme == 'http' and not allow_http_but_do_not_use_this_in_production_and_only_within_safe_networks:
            raise ValueError("always use https!")
            
        self.url = url_obj.geturl()
        self.port = url_obj.port
        self.hostname = url_obj.hostname
        self.download_prefix = os.path.join('data', self.hostname)
        self.use_cache = use_cache
        self.cache = {}
        self.server_information = None

        self.token_path = token_path or self.gen_token_path()
        self.token = token or os.environ.get("OPENBIS_TOKEN") or self._get_saved_token()
        if self.is_token_valid(self.token):
            pass
        else:
            token_path = self._delete_saved_token()
            if token_path and VERBOSE: print("Session is no longer valid. Please log in again.")

    def _get_username(self):
        if self.token:
            match = re.search(r'(?P<username>.*)-.*', self.token)
            username = match.groupdict()['username']
            return username
        return ''


    def __dir__(self):
        return [
            'url', 'port', 'hostname', 'token',
            'login()', 
            'logout()', 
            'is_session_active()', 
            'is_token_valid()',
            "mount()",
            "unmount()",
            "use_cache",
            "clear_cache()",
            "download_prefix",
            "get_mountpoint()",
            "get_server_information()",
            "get_dataset()",
            "get_datasets()",
            "get_dataset_type()",
            "get_dataset_types()",
            "get_datastores()",
            "gen_code()",
            "get_deletions()",
            "get_experiment()",
            "get_experiments()",
            "get_experiment_type()",
            "get_experiment_types()",
            "get_collection()",
            "get_collections()",
            "get_collection_type()",
            "get_collection_types()",
            "get_external_data_management_systems()",
            "get_external_data_management_system()",
            "get_material_type()",
            "get_material_types()",
            "get_project()",
            "get_projects()",
            "get_sample()",
            "get_object()",
            "get_samples()",
            "get_objects()",
            "get_sample_type()",
            "get_object_type()",
            "get_sample_types()",
            "get_object_types()",
            "get_property_types()",
            "get_property_type()",
            "new_property_type()",
            "get_semantic_annotations()",
            "get_semantic_annotation()",
            "get_space()",
            "get_spaces()",
            "get_tags()",
            "get_tag()",
            "new_tag()",
            "get_terms()",
            "get_term()",
            "get_vocabularies()",
            "get_vocabulary()",
            "new_person()",
            "get_persons()",
            "get_person()",
            "get_groups()",
            "get_group()",
            "get_role_assignments()",
            "get_role_assignment()",
            "get_plugins()",
            "get_plugin()",
            "new_plugin()",
            "new_group()",
            'new_space()',
            'new_project()',
            'new_experiment()',
            'new_collection()',
            'new_sample()',
            'new_object()',
            'new_sample_type()',
            'new_object_type()',
            'new_dataset()',
            'new_dataset_type()',
            'new_experiment_type()',
            'new_collection_type()',
            'new_material_type()',
            'new_semantic_annotation()',
            'new_transaction()',
            'update_sample()',
            'update_object()', 
        ]

    def _repr_html_(self):
        html = """
            <table border="1" class="dataframe">
            <thead>
                <tr style="text-align: right;">
                <th>attribute</th>
                <th>value</th>
                </tr>
            </thead>
            <tbody>
        """

        attrs = ['url', 'port', 'hostname', 'verify_certificates', 'as_v3', 'as_v1', 'reg_v1', 'token']
        for attr in attrs:
            html += "<tr> <td>{}</td> <td>{}</td> </tr>".format(
                attr, getattr(self, attr, '')
            )

        html += """
            </tbody>
            </table>
        """
        return html


    @property
    def spaces(self):
        return self.get_spaces()

    @property
    def projects(self):
        return self.get_projects()

    def gen_token_path(self, parent_folder=None):
        """generates a path to the token file.
        The token is usually saved in a file called
        ~/.pybis/hostname.token
        """
        if parent_folder is None:
            # save token under ~/.pybis folder
            parent_folder = os.path.join(
                os.path.expanduser("~"),
                '.pybis'
            )
        path = os.path.join(parent_folder, self.hostname + '.token')
        return path

    def _save_token(self, token=None, parent_folder=None):
        """ saves the session token to the disk, usually here: ~/.pybis/hostname.token. When a new Openbis instance is created, it tries to read this saved token by default.
        """
        if token is None:
            token = self.token

        token_path = None
        if parent_folder is None:
            token_path = self.gen_token_path()
        else:
            token_path = self.gen_token_path(parent_folder)

        # create the necessary directories, if they don't exist yet
        os.makedirs(os.path.dirname(token_path), exist_ok=True)
        with open(token_path, 'w') as f:
            f.write(token)
            self.token_path = token_path
        # prevent other users to be able to read the token
        os.chmod(token_path, 0o600)

    def _get_saved_token(self):
        """Read the token from the .pybis 
        If the token is not valid anymore, delete it. 
        """
        token_path = self.token_path or self.gen_token_path()
        if not os.path.exists(token_path):
            return None
        try:
            with open(token_path) as f:
                token = f.read()
                if token == "":
                    return None
                else:
                    return token
        except FileNotFoundError:
            return None

    def _delete_saved_token(self):
        if self.token_path:
            try:
                os.remove(self.token_path)
                return self.token_path
            except FileNotFoundError:
                return None

    def _post_request(self, resource, request):
        """ internal method, used to handle all post requests and serializing / deserializing
        data
        """
        return self._post_request_full_url(urljoin(self.url,resource), request)

    def _post_request_full_url(self, full_url, request):
        """ internal method, used to handle all post requests and serializing / deserializing
        data
        """
        if "id" not in request:
            request["id"] = "2"
        if "jsonrpc" not in request:
            request["jsonrpc"] = "2.0"
        if request["params"][0] is None:
            raise ValueError("Your session expired, please log in again")

        if DEBUG_LEVEL >=LOG_DEBUG: print(json.dumps(request))

        resp = requests.post(
            full_url,
            json.dumps(request),
            verify=self.verify_certificates
        )

        if resp.ok:
            resp = resp.json()
            if 'error' in resp:
                #print(full_url)
                #print(json.dumps(request))
                raise ValueError(resp['error']['message'])
            elif 'result' in resp:
                return resp['result']
            else:
                raise ValueError('request did not return either result nor error')
        else:
            raise ValueError('general error while performing post request')

    def logout(self):
        """ Log out of openBIS. After logout, the session token is no longer valid.
        """
        if self.token is None:
            return

        logout_request = {
            "method": "logout",
            "params": [self.token],
        }
        resp = self._post_request(self.as_v3, logout_request)
        self.token = None
        self.token_path = None
        return resp

    def login(self, username=None, password=None, save_token=False):
        """Log into openBIS.
        Expects a username and a password and updates the token (session-ID).
        The token is then used for every request.
        Clients may want to store the credentials object in a credentials store after successful login.
        Throw a ValueError with the error message if login failed.
        """

        if password is None:
            import getpass
            password = getpass.getpass()

        login_request = {
            "method": "login",
            "params": [username, password],
        }
        result = self._post_request(self.as_v3, login_request)
        if result is None:
            raise ValueError("login to openBIS failed")
        else:
            self.token = result

            if save_token:
                self._save_token()
                self._password(password)
            # update the OPENBIS_TOKEN environment variable, if OPENBIS_URL is identical to self.url
            if os.environ.get('OPENBIS_URL') == self.url:
                os.environ['OPENBIS_TOKEN'] = self.token
            return self.token

    def _password(self, password=None, pstore={} ):
        """An elegant way to store passwords which are used later
        without giving the user an easy possibility to retrieve it.
        """
        import inspect
        allowed_methods = ['mount']

        if password is not None:
            pstore['password'] = password
        else:
            if inspect.stack()[1][3] in allowed_methods:
                return pstore.get('password')
            else:
                raise Exception("This method can only be called from these internal methods: {}".format(allowed_methods))

    def unmount(self, mountpoint=None):
        """Unmount a given mountpoint or unmount the stored mountpoint.
        If the umount command does not work, try the pkill command.
        If still not successful, throw an error message.
        """

        if mountpoint is None and not getattr(self, 'mountpoint', None):
            raise ValueError("please provide a mountpoint to unmount")

        if mountpoint is None:
            mountpoint = self.mountpoint

        full_mountpoint_path = os.path.abspath(os.path.expanduser(mountpoint))

        if not os.path.exists(full_mountpoint_path):
            return

        # mountpoint is not a mountpoint path
        if not os.path.ismount(full_mountpoint_path):
            return

        status = subprocess.call('umount {}'.format(full_mountpoint_path), shell=True)
        if status == 1:
            status = subprocess.call(
                'pkill -9 sshfs && umount "{}"'.format(full_mountpoint_path),
                shell = True
            )

        if status == 1:
            raise OSError("could not unmount mountpoint: {} Please try to unmount manually".format(full_mountpoint_path))
        else:
           if VERBOSE: print("Successfully unmounted {}".format(full_mountpoint_path))
           self.mountpoint = None


    def is_mounted(self, mountpoint=None):
        if mountpoint is None:
            mountpoint = getattr(self, 'mountpoint', None)

        if mountpoint is None:
            return False

        return os.path.ismount(mountpoint)

    def get_mountpoint(self, search_mountpoint=False):
        """Returns the path to the active mountpoint.
        Returns None if no mountpoint is found or if the mountpoint is not mounted anymore.

        search_mountpoint=True:  Tries to figure out an existing mountpoint for a given hostname 
                                 (experimental, does not work under Windows yet)
        """

        mountpoint = getattr(self, 'mountpoint', None)
        if mountpoint:
            if self.is_mounted(mountpoint):
                return mountpoint
            else:
                return None
        else:
            if not search_mountpoint: return None

        # try to find out the mountpoint
        import subprocess
        p1 = subprocess.Popen(["mount", "-d"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["grep", "--fixed-strings", self.hostname], stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
        output = p2.communicate()[0]
        output = output.decode()
        # output will either be '' (=not mounted) or a string like this:
        # {username}@{hostname}:{path} on {mountpoint} (osxfuse, nodev, nosuid, synchronous, mounted by vermeul)
        try:
            mountpoint = output.split()[2]
            self.mountpoint = mountpoint
            return mountpoint
        except Exception:
            return None


    def mount(self,
        username=None, password=None,
        hostname=None, mountpoint=None,
        volname=None, path='/', port=2222,
        kex_algorithms ='+diffie-hellman-group1-sha1'
    ):

        """Mounts openBIS dataStore without being root, using sshfs and fuse. Both
        SSHFS and FUSE must be installed on the system (see below)

        Params:
        username -- default: the currently used username
        password -- default: the currently used password
        hostname -- default: the current hostname
        mountpoint -- default: ~/hostname


        FUSE / SSHFS Installation (requires root privileges):

        Mac OS X
        ========
        Follow the installation instructions on
        https://osxfuse.github.io

        Unix Cent OS 7
        ==============
        $ sudo yum install epel-release
        $ sudo yum --enablerepo=epel -y install fuse-sshfs
        $ user="$(whoami)"
        $ usermod -a -G fuse "$user"

        """
        if self.is_mounted():
            if VERBOSE: print("openBIS dataStore is already mounted on {}".format(self.mountpoint))
            return

        def check_sshfs_is_installed():
            import subprocess
            import errno
            try:
                subprocess.call('sshfs --help', shell=True)
            except OSError as e:
                if e.errno == errno.ENOENT:
                    raise ValueError('Your system seems not to have SSHFS installed. For Mac OS X, see installation instructions on https://osxfuse.github.io For Unix: $ sudo yum install epel-release && sudo yum --enablerepo=epel -y install fuse-sshfs && user="$(whoami)" && usermod -a -G fuse "$user"')

        check_sshfs_is_installed()

        if username is None: username = self._get_username()
        if not username: raise ValueError("no token available - please provide a username")

        if password is None: password = self._password()
        if not password: raise ValueError("please provide a password")

        if hostname is None: hostname = self.hostname
        if not hostname: raise ValueError("please provide a hostname")

        if mountpoint is None: mountpoint = os.path.join('~', self.hostname)

        # check if mountpoint exists, otherwise create it
        full_mountpoint_path = os.path.abspath(os.path.expanduser(mountpoint))
        if not os.path.exists(full_mountpoint_path):
            os.makedirs(full_mountpoint_path)

        print("full_mountpoint_path: ", full_mountpoint_path)

        from sys import platform
        supported_platforms = ['darwin', 'linux']
        if platform not in supported_platforms:
            raise ValueError("This method is not yet supported on {} plattform".format(platform))


        os_options = {
            "darwin": "-oauto_cache,reconnect,defer_permissions,noappledouble,negative_vncache,volname={} -oStrictHostKeyChecking=no ".format(hostname),
            "linux": "-oauto_cache,reconnect -oStrictHostKeyChecking=no",
        }

        if volname is None:
            volname = hostname

        import subprocess
        args = {
            "username": username,
            "password": password,
            "hostname": hostname,
            "port": port,
            "path": path,
            "mountpoint": mountpoint,
            "volname": volname,
            "os_options": os_options[platform],
            "kex_algorithms": kex_algorithms,
        }

        cmd = 'echo "{password}" | sshfs'\
              ' {username}@{hostname}:{path} {mountpoint}' \
              ' -o port={port} -o ssh_command="ssh -oKexAlgorithms={kex_algorithms}" -o password_stdin'\
              ' {os_options}'.format(**args)

        status = subprocess.call(cmd, shell=True)

        if status == 0:
            if VERBOSE: print("Mounted successfully to {}".format(full_mountpoint_path))
            self.mountpoint = full_mountpoint_path
            return self.mountpoint
        else:
            raise OSError("mount failed, exit status: ", status)


    def get_server_information(self):
        """ Returns a dict containing the following server information:
            api-version, archiving-configured, authentication-service, enabled-technologies, project-samples-enabled
        """
        if self.server_information is not None:
            return self.server_information

        request = {
            "method": "getServerInformation",
            "params": [self.token],
        }
        resp = self._post_request(self.as_v3, request)
        if resp is not None:
            # result is a dict of strings - use more useful types
            keys_boolean = ['archiving-configured', 'project-samples-enabled']
            keys_csv = ['enabled-technologies']
            for key in keys_boolean:
                if key in resp:
                    resp[key] = resp[key] == 'true'
            for key in keys_csv:
                if key in resp:
                    resp[key] = list(map(lambda item: item.strip(), resp[key].split(',')))
            self.server_information = ServerInformation(resp)
            return self.server_information
        else:
            raise ValueError("Could not get the server information")


    def create_permId(self):
        """Have the server generate a new permId"""
        # Request just 1 permId
        request = {
            "method": "createPermIdStrings",
            "params": [self.token, 1],
        }
        resp = self._post_request(self.as_v3, request)
        if resp is not None:
            return resp[0]
        else:
            raise ValueError("Could not create permId")

    def get_datastores(self):
        """ Get a list of all available datastores. Usually there is only one, but in some cases
        there might be multiple servers. If you upload a file, you need to specifiy the datastore you want
        the file uploaded to.
        """
        if hasattr(self, 'datastores'):
            return self.datastores

        request = {
            "method": "searchDataStores",
            "params": [
                self.token,
                {
                    "@type": "as.dto.datastore.search.DataStoreSearchCriteria"
                },
                {
                    "@type": "as.dto.datastore.fetchoptions.DataStoreFetchOptions"
                }
            ]
        }
        resp = self._post_request(self.as_v3, request)
        attrs=['code','downloadUrl','remoteUrl']
        if len(resp['objects']) == 0:
            raise ValueError("No datastore found!")
        else:
            objects = resp['objects']
            parse_jackson(objects)
            datastores = DataFrame(objects)
            self.datastores = datastores[attrs]
            return datastores[attrs]

    def gen_code(self, entity, prefix=""):
        """ Get the next sequence number for a Sample, Experiment, DataSet and Material. Other entities are currently not supported.
        Usage::
            gen_code('SAMPLE', 'SAM-')
            gen_code('EXPERIMENT', 'EXP-')
            gen_code('DATASET', '')
            gen_code('MATERIAL', 'MAT-')
        """

        entity = entity.upper()
        entity2enum = {
            "DATASET" : "DATA_SET",
            "OBJECT"  : "SAMPLE",
            "SAMPLE"  : "SAMPLE",
            "EXPERIMENT" : "EXPERIMENT",
            "COLLECTION" : "EXPERIMENT",
            "MATERIAL" : "MATERIAL",
        }

        if entity not in entity2enum:
            raise ValueError("no such entity: {}. Allowed entities are: DATA_SET, SAMPLE, EXPERIMENT, MATERIAL")

        request = {
            "method": "generateCode",
            "params": [
                self.token,
                prefix,
                entity2enum[entity]
            ]
        }
        try:
            return self._post_request(self.as_v1, request)
        except Exception as e:
            raise ValueError("Could not generate a code for {}: {}".format(entity, e))


    def gen_permId(self, count=1):
        """ Generate a permId (or many permIds) for a dataSet
        """

        request = {
            "method": "createPermIdStrings",
            "params": [
                self.token,
                count
            ]
        }
        try:
            return self._post_request(self.as_v3, request)
        except Exception as exc:
            raise ValueError("Could not generate a code: {}".format(exc))
            

    def new_person(self, userId, space=None):
        """ creates an openBIS person or returns the existing person
        """
        try:
            person = self.get_person(userId=userId)
            return person
        except Exception:
            return Person(self, userId=userId, space=space) 


    def new_group(self, code, description=None, userIds=None):
        """ creates an openBIS group or returns an existing one.
        """
        try:
            group = self.get_group(code=code)
            group.description = description
            return group
        except Exception:
            return Group(self, code=code, description=description, userIds=userIds)


    def get_group(self, code, only_data=False):
        """ Get an openBIS AuthorizationGroup. Returns a Group object.
        """

        ids = [{
            "@type": "as.dto.authorizationgroup.id.AuthorizationGroupPermId",
            "permId": code
        }]

        fetchopts = {
            "@type": "as.dto.authorizationgroup.fetchoptions.AuthorizationGroupFetchOptions"
        }
        for option in ['roleAssignments', 'users', 'registrator']:
            fetchopts[option] = fetch_option[option]

        fetchopts['users']['space'] = fetch_option['space']

        request = {
            "method": "getAuthorizationGroups",
            "params": [
                self.token,
                ids,
                fetchopts
            ]
        }
        resp = self._post_request(self.as_v3, request)
        if len(resp) == 0:
            raise ValueError("No group found!")

        for permid in resp:
            group = resp[permid]
            parse_jackson(group)

            if only_data:
                return group
            else:
                return Group(self, data=group)

    def get_role_assignments(self, start_with=None, count=None, **search_args):
        """ Get the assigned roles for a given group, person or space
        """
        entity = 'roleAssignment'
        search_criteria = get_type_for_entity(entity, 'search')
        allowed_search_attrs = ['role', 'roleLevel', 'user', 'group', 'person', 'space']

        sub_crit = []
        for attr in search_args:
            if attr in allowed_search_attrs:
                if attr == 'space':
                    sub_crit.append(
                        _subcriteria_for_code(search_args[attr], 'space')
                    )
                elif attr in ['user','person']:
                    userId = ''
                    if isinstance(search_args[attr], str):
                        userId = search_args[attr]
                    else:
                        userId = search_args[attr].userId

                    sub_crit.append(
                        _subcriteria_for_userId(userId)    
                    )
                elif attr == 'group':
                    groupId = ''
                    if isinstance(search_args[attr], str):
                        groupId = search_args[attr]
                    else:
                        groupId = search_args[attr].code
                    sub_crit.append(
                        _subcriteria_for_permid(groupId, 'authorizationGroup')
                    )
                elif attr == 'role':
                    # TODO
                    raise ValueError("not yet implemented")
                elif attr == 'roleLevel':
                    # TODO
                    raise ValueError("not yet implemented")
                else:
                    pass
            else:
                raise ValueError("unknown search argument {}".format(attr))

        search_criteria['criteria'] = sub_crit

        method_name = get_method_for_entity(entity, 'search')
        fetchopts = fetch_option[entity]
        fetchopts['from'] = start_with
        fetchopts['count'] = count
        for option in ['space', 'project', 'user', 'authorizationGroup','registrator']:
            fetchopts[option] = fetch_option[option]

        request = {
            "method": method_name,
            "params": [
                self.token,
                search_criteria,
                fetchopts
            ]
        }

        attrs=['techId', 'role', 'roleLevel', 'user', 'group', 'space', 'project']
        resp = self._post_request(self.as_v3, request)
        if len(resp['objects']) == 0:
            roles = DataFrame(columns=attrs)
        else: 
            objects = resp['objects']
            parse_jackson(objects)
            roles = DataFrame(objects)
            roles['techId'] = roles['id'].map(extract_id)
            roles['user'] = roles['user'].map(extract_userId)
            roles['group'] = roles['authorizationGroup'].map(extract_code)
            roles['space'] = roles['space'].map(extract_code)
            roles['project'] = roles['project'].map(extract_code)

        return Things(
            openbis_obj = self,
            entity='role_assignment',
            df=roles[attrs],
            identifier_name='techId',
            start_with = start_with,
            count = count,
            totalCount = resp.get('totalCount'),
        )

    def get_role_assignment(self, techId, only_data=False):
        """ Fetches one assigned role by its techId.
        """

        fetchopts = fetch_option['roleAssignment']
        for option in ['space', 'project', 'user', 'authorizationGroup','registrator']:
            fetchopts[option] = fetch_option[option]

        request = {
            "method": "getRoleAssignments",
            "params": [
                self.token,
                [{
                    "techId": str(techId),
                    "@type": "as.dto.roleassignment.id.RoleAssignmentTechId"
                }],
                fetchopts
            ]
        }

        resp = self._post_request(self.as_v3, request)
        if len(resp) == 0:
            raise ValueError("No assigned role found for techId={}".format(techId))
        
        for permid in resp:
            data = resp[permid]
            parse_jackson(data)

            if only_data:
                return data
            else:
                return RoleAssignment(self, data=data)


    def assign_role(self, role, **args):
        """ general method to assign a role to either
            - a person
            - a group
        The scope is either
            - the whole instance
            - a space
            - a project
        """
        role = role.upper()
        defs = get_definition_for_entity('roleAssignment')
        if role not in defs['role']:
            raise ValueError("Role should be one of these: {}".format(defs['role']))
        userId = None
        groupId = None
        spaceId = None
        projectId = None

        for arg in args:
            if arg in ['person', 'group', 'space', 'project']:
                permId = args[arg] if isinstance(args[arg],str) else args[arg].permId
                if arg == 'person':
                    userId = {
                        "permId": permId,
                        "@type": "as.dto.person.id.PersonPermId"
                    }
                elif arg == 'group':
                    groupId = {
                        "permId": permId,
                        "@type": "as.dto.authorizationgroup.id.AuthorizationGroupPermId"
                    }
                elif arg == 'space':
                    spaceId = {
                        "permId": permId,
                        "@type": "as.dto.space.id.SpacePermId"
                    }
                elif arg == 'project':
                    projectId = {
                        "permId": permId,
                        "@type": "as.dto.project.id.ProjectPermId"
                    }

        request = {
            "method": "createRoleAssignments",
            "params": [
                self.token,
                [ {
                    "role": role,
                    "userId": userId,
                    "authorizationGroupId": groupId,
                    "spaceId": spaceId,
                    "projectId": projectId,
                    "@type": "as.dto.roleassignment.create.RoleAssignmentCreation",
                } ]
            ]
        }
        resp = self._post_request(self.as_v3, request)
        return


    def get_groups(self, start_with=None, count=None, **search_args):
        """ Get openBIS AuthorizationGroups. Returns a «Things» object.

        Usage::
            groups = e.get.groups()
            groups[0]             # select first group
            groups['GROUP_NAME']  # select group with this code
            for group in groups:
                ...               # a Group object
            groups.df             # get a DataFrame object of the group list
            print(groups)         # print a nice ASCII table (eg. in IPython)
            groups                # HTML table (in a Jupyter notebook)

        """

        criteria = []
        for search_arg in ['code']:
            # unfortunately, there aren't many search possibilities yet...
            if search_arg in search_args:
                if search_arg == 'code':
                    criteria.append(_criteria_for_code(search_args[search_arg]))

        search_criteria = get_search_type_for_entity('authorizationGroup')
        search_criteria['criteria'] = criteria
        search_criteria['operator'] = 'AND'
                
        fetchopts = fetch_option['authorizationGroup']
        fetchopts['from'] = start_with
        fetchopts['count'] = count
        for option in ['roleAssignments', 'registrator', 'users']:
            fetchopts[option] = fetch_option[option]
        request = {
            "method": "searchAuthorizationGroups",
            "params": [
                self.token,
                search_criteria,
                fetchopts
            ],
        }
        resp = self._post_request(self.as_v3, request)

        attrs = ['permId', 'code', 'description', 'users', 'registrator', 'registrationDate', 'modificationDate']
        if len(resp['objects']) == 0:
            groups = DataFrame(columns=attrs)
        else:
            objects = resp['objects']
            parse_jackson(objects)
            groups = DataFrame(objects)

            groups['permId'] = groups['permId'].map(extract_permid)
            groups['registrator'] = groups['registrator'].map(extract_person)
            groups['users'] = groups['users'].map(extract_userId)
            groups['registrationDate'] = groups['registrationDate'].map(format_timestamp)
            groups['modificationDate'] = groups['modificationDate'].map(format_timestamp)
        return Things(
            openbis_obj = self,
            entity='group',
            df=groups[attrs],
            identifier_name='permId',
            start_with = start_with,
            count = count,
            totalCount = resp.get('totalCount'),
        )


    def get_persons(self, start_with=None, count=None, **search_args):
        """ Get openBIS users
        """

        search_criteria = get_search_criteria('person', **search_args)
        fetchopts = fetch_option['person']
        fetchopts['from'] = start_with
        fetchopts['count'] = count
        for option in ['space']:
            fetchopts[option] = fetch_option[option]
        request = {
            "method": "searchPersons",
            "params": [
                self.token,
                search_criteria,
                fetchopts
            ],
        }
        resp = self._post_request(self.as_v3, request)

        attrs = ['permId', 'userId', 'firstName', 'lastName', 'email', 'space', 'registrationDate', 'active']
        if len(resp['objects']) == 0:
            persons = DataFrame(columns=attrs)
        else:
            objects = resp['objects']
            parse_jackson(objects)

            persons = DataFrame(resp['objects'])
            persons['permId'] = persons['permId'].map(extract_permid)
            persons['registrationDate'] = persons['registrationDate'].map(format_timestamp)
            persons['space'] = persons['space'].map(extract_nested_permid)

        return Things(
            openbis_obj = self,
            entity='person',
            df=persons[attrs],
            identifier_name='permId',
            start_with = start_with,
            count = count,
            totalCount = resp.get('totalCount'),
        )


    get_users = get_persons # Alias


    def get_person(self, userId, only_data=False):
        """ Get a person (user)
        """
         
        ids = [{
            "@type": "as.dto.person.id.PersonPermId",
            "permId": userId
        }]

        fetchopts = {
            "@type": "as.dto.person.fetchoptions.PersonFetchOptions"
        }
        for option in ['roleAssignments', 'space']:
            fetchopts[option] = fetch_option[option]

        request = {
            "method": "getPersons",
            "params": [
                self.token,
                ids,
                fetchopts,
            ],
        }
        
        resp = self._post_request(self.as_v3, request)
        if len(resp) == 0:
            raise ValueError("No person found!")


        for permid in resp:
            person = resp[permid]
            parse_jackson(person)

            if only_data:
                return person
            else:
                return Person(self, data=person)

    get_user = get_person # Alias


    def get_spaces(self, code=None, start_with=None, count=None):
        """ Get a list of all available spaces (DataFrame object). To create a sample or a
        dataset, you need to specify in which space it should live.
        """

        method = get_method_for_entity('space', 'search')
        search_criteria = _subcriteria_for_code(code, 'space')
        fetchopts = fetch_option['space']
        fetchopts['from'] = start_with
        fetchopts['count'] = count
        request = {
            "method": method,
            "params": [
                self.token,
                search_criteria,
                fetchopts,
            ],
        }
        resp = self._post_request(self.as_v3, request)

        attrs = ['code', 'description', 'registrationDate', 'modificationDate']
        if len(resp['objects']) == 0:
            spaces = DataFrame(columns=attrs)
        else:
            spaces = DataFrame(resp['objects'])
            spaces['registrationDate'] = spaces['registrationDate'].map(format_timestamp)
            spaces['modificationDate'] = spaces['modificationDate'].map(format_timestamp)
        return Things(
            openbis_obj = self,
            entity = 'space',
            df = spaces[attrs],
            start_with = start_with,
            count = count,
            totalCount = resp.get('totalCount'),
        )


    def get_space(self, code, only_data=False):
        """ Returns a Space object for a given identifier.
        """

        code = str(code).upper()
        space = not only_data and self._object_cache(entity='space',code=code)
        if space:
            return space

        fetchopts = {"@type": "as.dto.space.fetchoptions.SpaceFetchOptions"}
        for option in ['registrator']:
            fetchopts[option] = fetch_option[option]

        method = get_method_for_entity('space', 'get')

        request = {
            "method": method,
            "params": [
                self.token,
                [{
                    "permId": code,
                    "@type": "as.dto.space.id.SpacePermId"
                }],
                fetchopts
            ],
        }
        resp = self._post_request(self.as_v3, request)
        if len(resp) == 0:
            raise ValueError("No such space: %s" % code)

        for permid in resp:
            if only_data:
                return resp[permid]
            else:
                space = Space(self, data=resp[permid])
                if self.use_cache:
                    self._object_cache(entity='space',code=code,value=space)
                return space


    def get_samples(
        self, identifier=None, code=None, permId=None,
        space=None, project=None, experiment=None, collection=None, type=None,
        start_with=None, count=None,
        withParents=None, withChildren=None, tags=None, attrs=None, props=None,
        where=None,
        **properties
    ):
        """Returns a DataFrame of all samples for a given space/project/experiment (or any combination)

        Filters
        -------
        type         -- sampleType code or object
        space        -- space code or object
        project      -- project code or object
        experiment   -- experiment code or object
        collection   -- same as above
        tags         -- only return samples with the specified tags
        where        -- key-value pairs of property values to search for

        Paging
        ------
        start_with   -- default=None
        count        -- number of samples that should be fetched. default=None.

        Include in result list
        ----------------------
        withParents  -- the list of parent's permIds in a column 'parents'
        withChildren -- the list of children's permIds in a column 'children'
        attrs        -- list of all desired attributes. Examples:
                        space, project, experiment: just return their identifier
                        parents, children, components: return a list of their identifiers
                        space.code, project.code, experiment.code
                        registrator.email, registrator.firstName
                        type.generatedCodePrefix
        props        -- list of all desired properties. Returns an empty string if
                        a) property is not present
                        b) property is not defined for this sampleType
        """

        if collection is not None:
            experiment = collection

        sub_criteria = []

        if identifier:
            crit = _subcriteria_for(identifier, 'sample')
            sub_criteria += crit['criteria']

        if space:
            sub_criteria.append(_subcriteria_for(space, 'space'))
        if project:
            sub_criteria.append(_subcriteria_for(project, 'project'))
        if experiment:
            sub_criteria.append(_subcriteria_for(experiment, 'experiment'))

        if withParents:
            sub_criteria.append(_subcriteria_for(withParents, 'sample', 'Parents'))
        if withChildren:
            sub_criteria.append(_subcriteria_for(withChildren, 'sample', 'Children'))

        if where:
            if properties is None:
                properties = where
            else:
                properties = {**where, **properties}

        if properties is not None:
            for prop in properties:
                sub_criteria.append(_subcriteria_for_properties(prop, properties[prop], entity='sample'))
        if type:
            sub_criteria.append(_subcriteria_for_code(type, 'sampleType'))
        if tags:
            sub_criteria.append(_subcriteria_for_tags(tags))
        if code:
            sub_criteria.append(_criteria_for_code(code))
        if permId:
            sub_criteria.append(_common_search("as.dto.common.search.PermIdSearchCriteria", permId))


        criteria = {
            "criteria": sub_criteria,
            "@type": "as.dto.sample.search.SampleSearchCriteria",
            "operator": "AND"
        }

        attrs_fetchoptions = self._get_fetchopts_for_attrs(attrs)

        # build the various fetch options
        fetchopts = fetch_option['sample']
        fetchopts['from'] = start_with
        fetchopts['count'] = count

        options = ['tags', 'properties', 'attachments', 'space', 'experiment', 'registrator', 'modifier', 'dataSets']
        if self.get_server_information().project_samples_enabled:
            options.append('project')
        for option in options:
            fetchopts[option] = fetch_option[option]

        for key in ['parents','children','container','components']:
            fetchopts[key] = {"@type": "as.dto.sample.fetchoptions.SampleFetchOptions"}


        if props is not None:
            fetchopts['properties'] = fetch_option['properties']

        request = {
            "method": "searchSamples",
            "params": [
                self.token,
                criteria,
                fetchopts,
            ],
        }
        resp = self._post_request(self.as_v3, request)

        samples = []
        parse_jackson(resp)
        for obj in resp['objects']:
            sample = Sample(
                openbis_obj = self,
                type = self.get_sample_type(obj['type']['code']),
                data = obj
            )
            samples.append(sample)

        return self._sample_list_for_response(
            response=resp['objects'],
            attrs=attrs,
            props=props,
            start_with=start_with,
            count=count,
            totalCount=resp['totalCount'],
            objects=samples
        )

    get_objects = get_samples # Alias


    def _get_fetchopts_for_attrs(self, attrs=None):
        if attrs is None:
            return []

        fetchopts = []
        for attr in attrs:
            if attr.startswith('space'): fetchopts.append('space')
            if attr.startswith('project'): fetchopts.append('project')
            if attr.startswith('experiment'): fetchopts.append('experiment')
            if attr.startswith('sample'): fetchopts.append('sample')
            if attr.startswith('registrator'): fetchopts.append('registrator')
            if attr.startswith('modifier'): fetchopts.append('modifier')

        return fetchopts


    def get_experiments(
        self, code=None, permId=None, type=None, space=None, project=None,
        start_with=None, count=None,
        tags=None, is_finished=None, attrs=None, props=None, where=None, **properties
    ):
        """Returns a DataFrame of all samples for a given space/project (or any combination)

        Filters:
        --------
        space        -- a space code or a space object
        project      -- a project code or a project object
        tags         -- only experiments with the specified tags
        type         -- a experimentType code
        where        -- key-value pairs of property values to search for

        Paging:
        -------
        start_with   -- default=None
        count        -- number of samples that should be fetched. default=None.

        Include:
        --------
        attrs        -- list of all desired attributes. Examples:
                        space, project, experiment: just return their identifier
                        space.code, project.code, experiment.code
                        registrator.email, registrator.firstName
                        type.generatedCodePrefix
        props        -- list of all desired properties. Returns an empty string if
                        a) property is not present
                        b) property is not defined for this sampleType
        """

        def extract_attribute(attribute_to_extract):
            def return_attribute(obj):
                if obj is None: return ''
                return obj.get(attribute_to_extract,'')
            return return_attribute

        def extract_space(obj):
            if isinstance(obj, dict):
                return obj.get('space', {})
            else:
                return ''

        sub_criteria = []
        if space:
            sub_criteria.append(_subcriteria_for_code(space, 'space'))
        if project:
            sub_criteria.append(_subcriteria_for_code(project, 'project'))
        if code:
            sub_criteria.append(_criteria_for_code(code))
        if permId:
            sub_criteria.append(_common_search("as.dto.common.search.PermIdSearchCriteria", permId))
        if type:
            sub_criteria.append(_subcriteria_for_code(type, 'experimentType'))
        if tags:
            sub_criteria.append(_subcriteria_for_tags(tags))
        if is_finished is not None:
            sub_criteria.append(_subcriteria_for_is_finished(is_finished))
        if where:
            if properties is None:
                properties = where
            else:
                properties = {**where, **properties}
        if properties is not None:
            for prop in properties:
                sub_criteria.append(_subcriteria_for_properties(prop, properties[prop], entity='experiment'))

        search_criteria = get_search_type_for_entity('experiment')
        search_criteria['criteria'] = sub_criteria
        search_criteria['operator'] = 'AND'

        fetchopts = fetch_option['experiment']
        fetchopts['from'] = start_with
        fetchopts['count'] = count

        if attrs is None: attrs = []
        options = self._get_fetchopts_for_attrs(attrs)
        for option in ['tags', 'properties', 'registrator', 'modifier']+options:
            fetchopts[option] = fetch_option[option]

        request = {
            "method": "searchExperiments",
            "params": [
                self.token,
                search_criteria,
                fetchopts,
            ],
        }
        resp = self._post_request(self.as_v3, request)
        response = resp['objects']
        parse_jackson(response)

        default_attrs = ['identifier', 'permId', 'type',
                 'registrator', 'registrationDate', 'modifier', 'modificationDate']
        display_attrs = default_attrs + attrs

        if props is None:
            props = []
        else:
            if isinstance(props, str):
                props = [props]

        if len(response) == 0:
            for prop in props:
                if prop == '*': continue
                display_attrs.append(prop)
            experiments = DataFrame(columns=display_attrs)
        else:
            experiments = DataFrame(response)
            experiments['space'] = experiments['project'].map(extract_space)
            for attr in attrs:
                if '.' in attr:
                    entity, attribute_to_extract = attr.split('.')
                    experiments[attr] = experiments[entity].map(extract_attribute(attribute_to_extract))
            for attr in attrs:
                # if no dot supplied, just display the code of the space, project or experiment
                if attr in ['project']:
                    experiments[attr] = experiments[attr].map(extract_nested_identifier)
                if attr in ['space']:
                    experiments[attr] = experiments[attr].map(extract_code)

            experiments['registrationDate'] = experiments['registrationDate'].map(format_timestamp)
            experiments['modificationDate'] = experiments['modificationDate'].map(format_timestamp)
            experiments['project'] = experiments['project'].map(extract_code)
            experiments['registrator'] = experiments['registrator'].map(extract_person)
            experiments['modifier'] = experiments['modifier'].map(extract_person)
            experiments['identifier'] = experiments['identifier'].map(extract_identifier)
            experiments['permId'] = experiments['permId'].map(extract_permid)
            experiments['type'] = experiments['type'].map(extract_code)

            for prop in props:
                if prop == '*':
                    # include all properties in dataFrame.
                    # expand the dataFrame by adding new columns
                    columns = []
                    for i, experiment in enumerate(response):
                        for prop_name, val in experiment.get('properties',{}).items():
                            experiments.loc[i, prop_name.upper()] = val
                            columns.append(prop_name.upper())

                    display_attrs += set(columns)
                    continue

                else:
                    # property name is provided
                    for i, experiment in enumerate(response):
                        val = experiment.get('properties',{}).get(prop,'') or experiment.get('properties',{}).get(prop.upper(),'')
                        experiments.loc[i, prop.upper()] = val
                    display_attrs.append(prop.upper())


        return Things(
            openbis_obj = self,
            entity = 'experiment',
            df = experiments[display_attrs],
            identifier_name ='identifier',
            start_with = start_with,
            count = count,
            totalCount = resp.get('totalCount'),
        )
    get_collections = get_experiments  # Alias


    def get_datasets(
        self, code=None, type=None, withParents=None, withChildren=None,
        start_with=None, count=None, kind=None,
        status=None, sample=None, experiment=None, collection=None, project=None,
        tags=None, attrs=None, props=None, 
        where=None,
        **properties
    ):
        """Returns a DataFrame of all dataSets for a given project/experiment/sample (or any combination)

        Filters
        -------
        project      -- a project code or a project object
        experiment   -- an experiment code or an experiment object
        sample       -- a sample code/permId or a sample/object
        collection   -- same as experiment
        tags         -- only return dataSets with the specified tags
        type         -- a dataSetType code
        where        -- key-value pairs of property values to search for

        Paging
        ------
        start_with   -- default=None
        count        -- number of dataSets that should be fetched. default=None.

        Include in result list
        ----------------------
        withParents  -- the list of parent's permIds in a column 'parents'
        withChildren -- the list of children's permIds in a column 'children'
        attrs        -- list of all desired attributes. Examples:
                        project, experiment, sample: just return their identifier
                        space.code, project.code, experiment.code
                        registrator.email, registrator.firstName
                        type.generatedCodePrefix
        props        -- list of all desired properties. Returns an empty string if
                        a) property is not present
                        b) property is not defined for this dataSetType
        """

        if 'object' in properties:
            sample = properties['object']
        if collection is not None:
            experiment = collection

        sub_criteria = []

        if code:
            sub_criteria.append(_criteria_for_code(code))
        if type:
            sub_criteria.append(_subcriteria_for_code(type, 'dataSetType'))

        if withParents:
            sub_criteria.append(_subcriteria_for(withParents, 'dataSet', 'Parents'))
        if withChildren:
            sub_criteria.append(_subcriteria_for(withChildren, 'dataSet', 'Children'))

        if sample:
            sub_criteria.append(_subcriteria_for(sample, 'sample'))
        if experiment:
            sub_criteria.append(_subcriteria_for(experiment, 'experiment'))
        if attrs is None: attrs = []

        if project:
            exp_crit = _subcriteria_for(experiment, 'experiment')
            proj_crit = _subcriteria_for(project, 'project')
            exp_crit['criteria'].append(proj_crit)
            sub_criteria.append(exp_crit)
        if tags:
            sub_criteria.append(_subcriteria_for_tags(tags))
        if status:
            sub_criteria.append(_subcriteria_for_status(status))

        if where:
            if properties is None:
                properties = where
            else:
                properties = {**where, **properties}

        if properties is not None:
            for prop in properties:
                sub_criteria.append(_subcriteria_for_properties(prop, properties[prop], entity='dataset'))

        search_criteria = get_search_type_for_entity('dataset')
        search_criteria['criteria'] = sub_criteria
        search_criteria['operator'] = 'AND'

        fetchopts = get_fetchoptions('dataSet', including=['type','parents','children','containers','components'])
        fetchopts['from'] = start_with
        fetchopts['count'] = count

        for option in [
            'tags', 'properties', 'dataStore', 'physicalData', 'linkedData',
            'experiment', 'sample', 'registrator', 'modifier'
        ]:
            fetchopts[option] = fetch_option[option]

        fetchopts['experiment']['project'] = fetch_option['project']

       # else:
       #     # get fetch options for projects and spaces
       #     # via experiment, if requested
       #     for attr in attrs:
       #         if any([entity in attr for entity in ['space','project']]):
       #             fetchopts['experiment'] = fetch_option['experiment']
       #             fetchopts['experiment']['project'] = fetch_option['project']

       #     options = self._get_fetchopts_for_attrs(attrs)
       #     for option in ['tags', 'properties', 'physicalData']+options:
       #         fetchopts[option] = fetch_option[option]

        if kind:
            kind = kind.upper()
            if kind not in ['PHYSICAL_DATA', 'CONTAINER', 'LINK']:
                raise ValueError("unknown dataSet kind: {}. It should be one of the following: PHYSICAL_DATA, CONTAINER or LINK".format(kind))
            fetchopts['kind'] = kind
            raise NotImplementedError('you cannot search for dataSet kinds yet')
        
        request = {
            "method": "searchDataSets",
            "params": [self.token,
                       search_criteria,
                       fetchopts,
                       ],
        }
        resp = self._post_request(self.as_v3, request)

        parse_jackson(resp)
        datasets = []
        for obj in resp['objects']:
            dataset = DataSet(
                openbis_obj = self,
                type = self.get_dataset_type(obj['type']['code']),
                data = obj
            )
            datasets.append(dataset)

        return self._dataset_list_for_response(
            response=resp['objects'],
            attrs=attrs,
            props=props,
            start_with=start_with,
            count=count,
            totalCount=resp['totalCount'],
            objects=datasets,
        )


    def get_experiment(self, code, withAttachments=False, only_data=False):
        """ Returns an experiment object for a given identifier (code).
        """

        fetchopts = fetch_option['experiment']

        search_request = _type_for_id(code, 'experiment')
        for option in ['tags', 'properties', 'attachments', 'project', 'samples', 'registrator', 'modifier']:
            fetchopts[option] = fetch_option[option]


        if withAttachments:
            fetchopts['attachments'] = fetch_option['attachmentsWithContent']

        request = {
            "method": "getExperiments",
            "params": [
                self.token,
                [search_request],
                fetchopts
            ],
        }
        resp = self._post_request(self.as_v3, request)
        if len(resp) == 0:
            raise ValueError(f"No such experiment: {code}")

        parse_jackson(resp)
        for permid in resp:
            if only_data:
                return resp[permid]
            else:
                return Experiment(
                    openbis_obj = self,
                    type = self.get_experiment_type(resp[code]["type"]["code"]),
                    data = resp[permid]
                )
    get_collection = get_experiment  # Alias


    def new_experiment(self, type, code, project, props=None, **kwargs):
        """ Creates a new experiment of a given experiment type.
        """
        return Experiment(
            openbis_obj = self,
            type = self.get_experiment_type(type),
            project = project,
            data = None,
            props = props,
            code = code,
            **kwargs
        )
    new_collection = new_experiment  # Alias


    def update_experiment(self, experimentId, properties=None, tagIds=None, attachments=None):
        params = {
            "experimentId": {
                "permId": experimentId,
                "@type": "as.dto.experiment.id.ExperimentPermId"
            },
            "@type": "as.dto.experiment.update.ExperimentUpdate"
        }
        if properties is not None:
            params["properties"] = properties
        if tagIds is not None:
            params["tagIds"] = tagIds
        if attachments is not None:
            params["attachments"] = attachments

        request = {
            "method": "updateExperiments",
            "params": [
                self.token,
                [params]
            ]
        }
        self._post_request(self.as_v3, request)
    update_collection = update_experiment  # Alias


    def create_external_data_management_system(self, code, label, address, address_type='FILE_SYSTEM'):
        """Create an external DMS.
        :param code: An openBIS code for the external DMS.
        :param label: A human-readable label.
        :param address: The address for accessing the external DMS. E.g., a URL.
        :param address_type: One of OPENBIS, URL, or FILE_SYSTEM
        :return:
        """
        request = {
            "method": "createExternalDataManagementSystems",
            "params": [
                self.token,
                [
                    {
                        "code": code,
                        "label": label,
                        "addressType": address_type,
                        "address": address,
                        "@type": "as.dto.externaldms.create.ExternalDmsCreation",
                    }
                ]
            ],
        }
        resp = self._post_request(self.as_v3, request)
        return self.get_external_data_management_system(resp[0]['permId'])

    def update_sample(self, sampleId, space=None, project=None, experiment=None,
                      parents=None, children=None, components=None, properties=None, tagIds=None, attachments=None):
        params = {
            "sampleId": {
                "permId": sampleId,
                "@type": "as.dto.sample.id.SamplePermId"
            },
            "@type": "as.dto.sample.update.SampleUpdate"
        }
        if space is not None:
            params['spaceId'] = space
        if project is not None:
            params['projectId'] = project
        if properties is not None:
            params["properties"] = properties
        if tagIds is not None:
            params["tagIds"] = tagIds
        if attachments is not None:
            params["attachments"] = attachments

        request = {
            "method": "updateSamples",
            "params": [
                self.token,
                [params]
            ]
        }
        self._post_request(self.as_v3, request)

    update_object = update_sample # Alias


    def delete_entity(self, entity, id, reason, id_name='permId'):
        """Deletes Spaces, Projects, Experiments, Samples and DataSets
        """

        type = get_type_for_entity(entity, 'delete')
        method = get_method_for_entity(entity, 'delete')
        request = {
            "method": method,
            "params": [
                self.token,
                [
                    {
                        id_name: id,
                        "@type": type
                    }
                ],
                {
                    "reason": reason,
                    "@type": type
                }
            ]
        }
        resp = self._post_request(self.as_v3, request)


    def delete_openbis_entity(self, entity, objectId, reason='No reason given'):
        method = get_method_for_entity(entity, 'delete')
        delete_options = get_type_for_entity(entity, 'delete')
        delete_options['reason'] = reason

        request = {
           "method": method,
           "params": [
                self.token,
                [ objectId ],
                delete_options
            ]
        }
        self._post_request(self.as_v3, request)
        return


    def get_deletions(self, start_with=None, count=None):
        search_criteria = {
            "@type": "as.dto.deletion.search.DeletionSearchCriteria"
        }
        fetchopts = fetch_option['deletion']
        fetchoptsDeleted = fetch_option['deletedObjects']
        fetchoptsDeleted['from'] = start_with
        fetchoptsDeleted['count'] = count
        fetchopts['deletedObjects'] = fetchoptsDeleted

        request = {
            "method": "searchDeletions",
            "params": [
                self.token,
                search_criteria,
                fetchopts,
            ]
        }
        resp = self._post_request(self.as_v3, request)
        objects = resp['objects']
        parse_jackson(objects)

        new_objs = []
        for value in objects:
            del_objs = extract_deletion(value)
            if len(del_objs) > 0:
                new_objs.append(*del_objs)

        return DataFrame(new_objs)

    def new_project(self, space, code, description=None, **kwargs):
        return Project(self, None, space=space, code=code, description=description, **kwargs)

    def _gen_fetchoptions(self, options, foType):
        fo = {
            "@type": foType
        }
        for option in options:
            fo[option] = fetch_option[option]
        return fo

    def get_project(self, projectId, only_data=False):
        """Returns a Project object for a given identifier, code or permId.
        """

        project = not only_data and self._object_cache(entity='project',code=projectId)
        if project:
            return project

        options = ['space', 'registrator', 'modifier', 'attachments']
        if is_identifier(projectId) or is_permid(projectId):
            request = self._create_get_request(
                'getProjects', 'project', projectId, options,
                "as.dto.project.fetchoptions.ProjectFetchOptions"
            )
            resp = self._post_request(self.as_v3, request)
            if only_data:
                return resp[projectId]

            project = Project(
                openbis_obj=self, 
                type=None,
                data=resp[projectId]
            )
            if self.use_cache:
                self._object_cache(entity='project', code=projectId, value=project)
            return project

        else:
            search_criteria = _gen_search_criteria({
                'project': 'Project',
                'operator': 'AND',
                'code': projectId
            })
            fo = self._gen_fetchoptions(options, foType="as.dto.project.fetchoptions.ProjectFetchOptions")
            request = {
                "method": "searchProjects",
                "params": [self.token, search_criteria, fo]
            }
            resp = self._post_request(self.as_v3, request)
            if len(resp['objects']) == 0:
                raise ValueError("No such project: %s" % projectId)
            if only_data:
                return resp['objects'][0]

            project = Project(
                openbis_obj=self, 
                type=None,
                data=resp['objects'][0]
            )
            if self.use_cache:
                self._object_cache(entity='project', code=projectId, value=project)
            return project

    def get_projects(
        self, space=None, code=None,
        start_with=None, count=None,
    ):
        """ Get a list of all available projects (DataFrame object).
        """

        sub_criteria = []
        if space:
            sub_criteria.append(_subcriteria_for_code(space, 'space'))
        if code:
            sub_criteria.append(_criteria_for_code(code))

        criteria = {
            "criteria": sub_criteria,
            "@type": "as.dto.project.search.ProjectSearchCriteria",
            "operator": "AND"
        }

        fetchopts = {"@type": "as.dto.project.fetchoptions.ProjectFetchOptions"}
        fetchopts['from'] = start_with
        fetchopts['count'] = count
        for option in ['registrator', 'modifier', 'leader']:
            fetchopts[option] = fetch_option[option]

        request = {
            "method": "searchProjects",
            "params": [self.token,
                       criteria,
                       fetchopts,
                       ],
        }
        resp = self._post_request(self.as_v3, request)

        attrs = ['identifier', 'permId', 'leader', 'registrator', 'registrationDate', 'modifier', 'modificationDate']
        if len(resp['objects']) == 0:
            projects = DataFrame(columns=attrs)        
        else:
            objects = resp['objects']
            parse_jackson(objects)

            projects = DataFrame(objects)

            projects['registrationDate'] = projects['registrationDate'].map(format_timestamp)
            projects['modificationDate'] = projects['modificationDate'].map(format_timestamp)
            projects['leader'] = projects['leader'].map(extract_person)
            projects['registrator'] = projects['registrator'].map(extract_person)
            projects['modifier'] = projects['modifier'].map(extract_person)
            projects['permId'] = projects['permId'].map(extract_permid)
            projects['identifier'] = projects['identifier'].map(extract_identifier)

        return Things(
            openbis_obj = self,
            entity = 'project',
            df = projects[attrs],
            identifier_name = 'identifier',
            start_with = start_with,
            count = count,
            totalCount = resp.get('totalCount'),
        )


    def _create_get_request(self, method_name, entity, permids, options, foType):

        if not isinstance(permids, list):
            permids = [permids]

        type = "as.dto.{}.id.{}".format(entity.lower(), entity.capitalize())
        search_params = []
        for permid in permids:
            # decide if we got a permId or an identifier
            match = re.match('/', permid)
            if match:
                search_params.append(
                    {"identifier": permid, "@type": type + 'Identifier'}
                )
            else:
                search_params.append(
                    {"permId": permid, "@type": type + 'PermId'}
                )

        fo = {
            "@type": foType
        }
        for option in options:
            fo[option] = fetch_option[option]

        request = {
            "method": method_name,
            "params": [
                self.token,
                search_params,
                fo
            ],
        }
        return request

    def clear_cache(self, entity=None):
        """Empty the internal object cache
        If you do not specify any entity, the complete cache is cleared.
        As entity, you can specify either:
        space, project, vocabulary, term, sampleType, experimentType, dataSetType
        """
        if entity:
            self.cache[entity] = {}
        else:
            self.cache = {}

    def _object_cache(self, entity=None, code=None, value=None):

        # return the value, if no value provided
        if value is None:
            if entity in self.cache:
                return self.cache[entity].get(code)
        else:
            if entity not in self.cache:
                self.cache[entity] = {}

            self.cache[entity][code] = value


    def get_terms(self, vocabulary=None, start_with=None, count=None):
        """ Returns information about existing vocabulary terms. 
        If a vocabulary code is provided, it only returns the terms of that vocabulary.
        """

        if self.use_cache and vocabulary is not None and start_with is None and count is None:
            voc = self._object_cache(entity='term',code=vocabulary)
            if voc:
                return voc

        search_request = {}
        if vocabulary is not None:
            search_request = _gen_search_criteria({
                "vocabulary": "VocabularyTerm",
                "criteria": [{
                    "vocabulary": "Vocabulary",
                    "code": vocabulary
                }]
            })
        search_request["@type"] = "as.dto.vocabulary.search.VocabularyTermSearchCriteria"

        fetchopts = fetch_option['vocabularyTerm']
        fetchopts['from'] = start_with
        fetchopts['count'] = count

        request = {
            "method": "searchVocabularyTerms",
            "params": [self.token, search_request, fetchopts]
        }
        resp = self._post_request(self.as_v3, request)

        attrs = 'code vocabularyCode label description registrationDate modificationDate official ordinal'.split()

        if len(resp['objects']) == 0:
            terms = DataFrame(columns=attrs)
        else:
            objects = resp['objects']
            parse_jackson(objects)
            terms = DataFrame(objects)
            terms['vocabularyCode'] = terms['permId'].map(extract_attr('vocabularyCode'))
            terms['registrationDate'] = terms['registrationDate'].map(format_timestamp)
            terms['modificationDate'] = terms['modificationDate'].map(format_timestamp)

        things = Things(
            openbis_obj = self,
            entity = 'term',
            df = terms[attrs],
            identifier_name='code',
            additional_identifier='vocabularyCode',
            start_with = start_with,
            count = count,
            totalCount = resp.get('totalCount'),
        )
        if self.use_cache and vocabulary is not None and start_with is None and count is None:
            self._object_cache(entity='term',code=vocabulary,value=things)

        return things
        

    def new_term(self, code, vocabularyCode, label=None, description=None):
        return VocabularyTerm(
            self, data=None,
            code=code, vocabularyCode=vocabularyCode,
            label=label, description=description
        )


    def get_term(self, code, vocabularyCode, only_data=False):
        search_request = {
            "code": code,
            "vocabularyCode": vocabularyCode,
            "@type": "as.dto.vocabulary.id.VocabularyTermPermId"
        }
        fetchopts = get_fetchoption_for_entity('vocabularyTerm')
        for opt in ['registrator']:
            fetchopts[opt] = get_fetchoption_for_entity(opt)
        
        request = {
            "method": 'getVocabularyTerms',
            "params": [
                self.token,
                [search_request],
                fetchopts
            ],
        }
        resp = self._post_request(self.as_v3, request)

        if resp is None or len(resp) == 0:
            raise ValueError("no VocabularyTerm found with code='{}' and vocabularyCode='{}'".format(code, vocabularyCode))
        else:
            parse_jackson(resp)
            for ident in resp:
                if only_data:
                    return resp[ident]
                else:
                    return VocabularyTerm(self, resp[ident])



    def get_vocabularies(self, code=None, start_with=None, count=None):
        """ Returns information about vocabulary
        """

        sub_criteria = []
        if code:
            sub_criteria.append(_criteria_for_code(code))
        criteria = {
            "criteria": sub_criteria,
            "@type": "as.dto.vocabulary.search.VocabularySearchCriteria",
            "operator": "AND"
        }

        fetchopts = fetch_option['vocabulary']
        fetchopts['from'] = start_with
        fetchopts['count'] = count
        for option in ['registrator']:
            fetchopts[option] = fetch_option[option]

        request = {
            "method": "searchVocabularies",
            "params": [self.token, criteria, fetchopts]
        }
        resp = self._post_request(self.as_v3, request)

        attrs = 'code description managedInternally chosenFromList urlTemplate registrator registrationDate modificationDate'.split()

        if len(resp['objects']) == 0:
            vocs = DataFrame(columns=attrs)
        else:
            objects = resp['objects']
            parse_jackson(resp)
            vocs = DataFrame(objects)
            vocs['registrationDate'] = vocs['registrationDate'].map(format_timestamp)
            vocs['modificationDate'] = vocs['modificationDate'].map(format_timestamp)
            vocs['registrator']      = vocs['registrator'].map(extract_person)

        return Things(
            openbis_obj = self,
            entity = 'vocabulary',
            df = vocs[attrs],
            identifier_name = 'code',
            start_with = start_with,
            count = count,
            totalCount = resp.get('totalCount'),
        )


    def get_vocabulary(self, code, only_data=False):
        """ Returns the details of a given vocabulary (including vocabulary terms)
        """

        code = str(code).upper()
        voc = not only_data and self._object_cache(entity='vocabulary',code=code)
        if voc:
            return voc

        entity = 'vocabulary'
        method_name = get_method_for_entity(entity, 'get')
        objectIds = _type_for_id(code.upper(), entity)
        fetchopts = fetch_option[entity]
        
        request = {
            "method": method_name,
            "params": [
                self.token,
                [objectIds],
                fetchopts
            ],
        }
        resp = self._post_request(self.as_v3, request)

        if len(resp) == 0:
            raise ValueError('no {} found with identifier: {}'.format(entity, code))
        else:
            parse_jackson(resp)
            for ident in resp:
                data = resp[ident]
                if only_data:
                    return data
                vocabulary = Vocabulary( openbis_obj=self, data=data)
                if self.use_cache:
                    self._object_cache(entity='vocabulary', code=code, value=vocabulary)
                return vocabulary


    def new_tag(self, code, description=None):
        """ Creates a new tag (for this user)
        """
        return Tag(self, code=code, description=description)


    def get_tags(self, code=None, start_with=None, count=None):
        """ Returns a DataFrame of all tags
        """

        search_criteria = get_search_type_for_entity('tag', 'AND')

        criteria = []
        fetchopts = fetch_option['tag']
        fetchopts['from'] = start_with
        fetchopts['count'] = count
        for option in ['owner']:
            fetchopts[option] = fetch_option[option]
        if code:
            criteria.append(_criteria_for_code(code))
        search_criteria['criteria'] = criteria
        request = {
            "method": "searchTags",
            "params": [
                self.token,
                search_criteria,
                fetchopts
            ]
        }

        resp = self._post_request(self.as_v3, request)
        return self._tag_list_for_response(response=resp['objects'], totalCount=resp['totalCount'])


    def get_tag(self, permId, only_data=False):
        """ Returns a specific tag
        """

        just_one = True
        identifiers = []
        if isinstance(permId, list):
            just_one = False
            for ident in permId:
                identifiers.append(_type_for_id(ident, 'tag'))
        else:
            tag = not only_data and self._object_cache(entity='tag',code=permId)
            if tag:
                return tag
            identifiers.append(_type_for_id(permId, 'tag'))

        fetchopts = fetch_option['tag']
        for option in ['owner']:
            fetchopts[option] = fetch_option[option]
        request = {
            "method": "getTags",
            "params": [
                self.token,
                identifiers,
                fetchopts
            ],
        }

        resp = self._post_request(self.as_v3, request)

        if just_one:
            if len(resp) == 0:
                raise ValueError('no such tag found: {}'.format(permId))

            parse_jackson(resp)
            for permId in resp:
                if only_data:
                    return resp[permId]
                else:
                    tag = Tag(self, data=resp[permId])
                    if self.use_cache:
                        self._object_cache(entity='tag',code=permId,value=tag)
                    return tag
        else:
            return self._tag_list_for_response( response=list(resp.values()) )

    def _tag_list_for_response(self, response, totalCount=0):

        parse_jackson(response)
        attrs = ['permId', 'code', 'description', 'owner', 'private', 'registrationDate']
        if len(response) == 0:
            tags = DataFrame(columns = attrs)
        else: 
            tags = DataFrame(response)
            tags['registrationDate'] = tags['registrationDate'].map(format_timestamp)
            tags['permId']           = tags['permId'].map(extract_permid)
            tags['description']      = tags['description'].map(lambda x: '' if x is None else x)
            tags['owner']            = tags['owner'].map(extract_person)

        return Things(
            openbis_obj = self,
            entity = 'tag',
            df = tags[attrs],
            identifier_name ='permId',
            totalCount = totalCount,
        )


    def search_semantic_annotations(self, 
        permId=None, entityType=None, propertyType=None, only_data=False
    ):
        """ Get a list of semantic annotations for permId, entityType, propertyType or 
        property type assignment (DataFrame object).
        :param permId: permId of the semantic annotation.
        :param entityType: entity (sample) type to search for.
        :param propertyType: property type to search for
        :param only_data: return result as plain data object.
        :return:  Things of DataFrame objects or plain data object
        """

        criteria = []
        typeCriteria = []

        if permId is not None:
            criteria.append({
                "@type" : "as.dto.common.search.PermIdSearchCriteria",
                "fieldValue" : {
                    "@type" : "as.dto.common.search.StringEqualToValue",
                    "value" : permId
                }
            })

        if entityType is not None:
            typeCriteria.append({
                "@type" : "as.dto.entitytype.search.EntityTypeSearchCriteria",
                "criteria" : [_criteria_for_code(entityType)]
            })

        if propertyType is not None:
            typeCriteria.append({
                "@type" : "as.dto.property.search.PropertyTypeSearchCriteria",
                "criteria" : [_criteria_for_code(propertyType)]
            })

        if entityType is not None and propertyType is not None:
            criteria.append({
                "@type" : "as.dto.property.search.PropertyAssignmentSearchCriteria",
                "criteria" : typeCriteria
            })
        else:
            criteria += typeCriteria

        saCriteria = {
            "@type" : "as.dto.semanticannotation.search.SemanticAnnotationSearchCriteria",
            "criteria" : criteria
        }

        objects = self._search_semantic_annotations(saCriteria)

        if only_data:
            return objects

        attrs = ['permId', 'entityType', 'propertyType', 'predicateOntologyId', 'predicateOntologyVersion', 'predicateAccessionId', 'descriptorOntologyId', 'descriptorOntologyVersion', 'descriptorAccessionId', 'creationDate']
        if len(objects) == 0:
            annotations = DataFrame(columns=attrs)
        else:
            annotations = DataFrame(objects)

        return Things(
            openbis_obj = self,
            entity = 'semantic_annotation',
            df = annotations[attrs],
            identifier_name = 'permId',
        )

    def _search_semantic_annotations(self, criteria):

        fetch_options = {
            "@type": "as.dto.semanticannotation.fetchoptions.SemanticAnnotationFetchOptions",
            "entityType": {"@type": "as.dto.entitytype.fetchoptions.EntityTypeFetchOptions"},
            "propertyType": {"@type": "as.dto.property.fetchoptions.PropertyTypeFetchOptions"},
            "propertyAssignment": {
                "@type": "as.dto.property.fetchoptions.PropertyAssignmentFetchOptions",
                "entityType" : {
                    "@type" : "as.dto.entitytype.fetchoptions.EntityTypeFetchOptions"
                },
                "propertyType" : {
                    "@type" : "as.dto.property.fetchoptions.PropertyTypeFetchOptions"
                }
            }
        }

        request = {
            "method": "searchSemanticAnnotations",
            "params": [self.token, criteria, fetch_options]
        }

        resp = self._post_request(self.as_v3, request)
        if len(resp['objects']) == 0:
            return []
        else:
            objects = resp['objects']
            parse_jackson(objects)
            
            for obj in objects:
                obj['permId'] = obj['permId']['permId']
                if obj.get('entityType') is not None:
                    obj['entityType'] = obj['entityType']['code']
                elif obj.get('propertyType') is not None:
                    obj['propertyType'] = obj['propertyType']['code']
                elif obj.get('propertyAssignment') is not None:
                    obj['entityType'] = obj['propertyAssignment']['entityType']['code']
                    obj['propertyType'] = obj['propertyAssignment']['propertyType']['code']
                obj['creationDate'] = format_timestamp(obj['creationDate'])
                
            return objects


    def get_semantic_annotations(self):
        """ Get a list of all available semantic annotations (DataFrame object).
        """

        objects = self._search_semantic_annotations({
            "@type": "as.dto.semanticannotation.search.SemanticAnnotationSearchCriteria"
        })
        attrs = ['permId', 'entityType', 'propertyType', 'predicateOntologyId', 'predicateOntologyVersion', 'predicateAccessionId', 'descriptorOntologyId', 'descriptorOntologyVersion', 'descriptorAccessionId', 'creationDate']
        if len(objects) == 0:
            annotations = DataFrame(columns=attrs)
        else:
            annotations = DataFrame(objects)
        return Things(
            openbis_obj = self,
            entity = 'semantic_annotation',
            df = annotations[attrs],
            identifier_name = 'permId',
        )

    def get_semantic_annotation(self, permId, only_data = False):
        objects = self.search_semantic_annotations(permId=permId, only_data=True)
        if len(objects) == 0:
            raise ValueError("Semantic annotation with permId " + permId +  " not found.")
        obj = objects[0]
        if only_data:
            return obj
        else:
            return SemanticAnnotation(self, isNew=False, **obj)

    def get_plugins(self, start_with=None, count=None):

        criteria = []
        search_criteria = get_search_type_for_entity('plugin', 'AND')
        search_criteria['criteria'] = criteria

        fetchopts = fetch_option['plugin']
        for option in ['registrator']:
            fetchopts[option] = fetch_option[option]
        fetchopts['from'] = start_with
        fetchopts['count'] = count

        request = {
            "method": "searchPlugins",
            "params": [
                self.token,
                search_criteria,
                fetchopts,
            ],
        }
        resp = self._post_request(self.as_v3, request)
        attrs = ['name', 'description', 'pluginType', 'pluginKind',
        'entityKinds', 'registrator', 'registrationDate', 'permId']

        if len(resp['objects']) == 0:
            plugins = DataFrame(columns=attrs)
        else:
            objects = resp['objects']
            parse_jackson(objects)

            plugins = DataFrame(objects)
            plugins['permId'] = plugins['permId'].map(extract_permid)
            plugins['registrator'] = plugins['registrator'].map(extract_person)
            plugins['registrationDate'] = plugins['registrationDate'].map(format_timestamp)
            plugins['description'] = plugins['description'].map(lambda x: '' if x is None else x)
            plugins['entityKinds'] = plugins['entityKinds'].map(lambda x: '' if x is None else x)

        return Things(
            openbis_obj = self,
            entity = 'plugin',
            df = plugins[attrs],
            identifier_name = 'name',
            start_with = start_with,
            count = count,
            totalCount = resp.get('totalCount'),
        )


    def get_plugin(self, permId, only_data=False, with_script=True):
        search_request = _type_for_id(permId, 'plugin')
        fetchopts = fetch_option['plugin']
        options = ['registrator']
        if with_script:
            options.append('script')

        for option in options:
            fetchopts[option] = fetch_option[option]

        request = {
            "method": "getPlugins",
            "params": [
                self.token,
                [search_request],
                fetchopts
            ],
        }

        resp = self._post_request(self.as_v3, request)
        parse_jackson(resp)

        if resp is None or len(resp) == 0:
            raise ValueError('no such plugin found: ' + permId)
        else:
            for permId in resp:
                if only_data:
                    return resp[permId]
                else:
                    return Plugin(self, data=resp[permId])

    def new_plugin(self, name, pluginType, **kwargs):
        """ Creates a new Plugin in openBIS. 
 
        name        -- name of the plugin
        description --
        pluginType  -- DYNAMIC_PROPERTY, MANAGED_PROPERTY, ENTITY_VALIDATION
        entityKind  -- MATERIAL, EXPERIMENT, SAMPLE, DATA_SET
        script      -- string of the script itself
        available   --
        """
        return Plugin(self, name=name, pluginType=pluginType, **kwargs) 
        

    def new_property_type(self, 
        code,
        label,
        description,
        dataType,
        managedInternally = False,
        vocabulary = None,
        materialType = None,
        schema = None,
        transformation = None,
    ):
        """ Creates a new property type.

        code               -- name of the property type
        managedInternally  -- must be set to True if code starts with a $
        label              -- displayed label of that property
        description        --
        dataType           -- must contain any of these values:
                              INTEGER VARCHAR MULTILINE_VARCHAR
                              REAL TIMESTAMP BOOLEAN HYPERLINK
                              XML CONTROLLEDVOCABULARY MATERIAL
        vocabulary         -- if dataType is CONTROLLEDVOCABULARY, this attribute
                              must contain the code of the vocabulary object.
        materialType       --
        schema             --
        transformation     --

        PropertyTypes can be assigned to
        - sampleTypes
        - dataSetTypes
        - experimentTypes
        - materialTypes (deprecated)
        """

        return PropertyType(
            openbis_obj=self,
            code=code,
            label=label,
            description=description,
            dataType=dataType,
            managedInternally = managedInternally,
            vocabulary = vocabulary,
            materialType = materialType,
            schema = schema,
            transformation = transformation,
        )

    def get_property_type(self, code, only_data=False, start_with=None, count=None):

        if not isinstance(code, list) and start_with is None and count is None:
            code = str(code).upper()
            pt = self.use_cache and self._object_cache(entity='property_type',code=code)
            if pt:
                if only_data:
                    return pt.data
                else:
                    return pt

        identifiers = []
        only_one = False
        if not isinstance(code, list):
            code = [code]
            only_one = True

        for c in code:
            identifiers.append({
                "permId": c.upper(),
                "@type": "as.dto.property.id.PropertyTypePermId"
            })

        fetchopts = fetch_option['propertyType']
        options = ['vocabulary', 'materialType', 'semanticAnnotations', 'registrator']
        for option in options:
            fetchopts[option] = fetch_option[option]

        request = {
            "method": "getPropertyTypes",
            "params": [
                self.token,
                identifiers,
                fetchopts
            ],
        }

        resp = self._post_request(self.as_v3, request)
        parse_jackson(resp)

        if only_one:
            if len(resp) == 0:
                raise ValueError('no such propertyType: {}'.format(code))
            for ident in resp:
                if only_data:
                    return resp[ident]
                else:
                    pt = PropertyType(
                        openbis_obj = self,
                        data=resp[ident]
                    )
                    if self.use_cache:
                        self._object_cache(entity='property_type',code=code[0], value=pt)
                    return pt

        # return a list of objects
        else:
            return self._property_type_things(
                objects    = list(resp.values()),
                start_with = start_with,
                count      = count,
                totalCount = len(resp),
            )

    def get_property_types(self, code=None, start_with=None, count=None):
        fetchopts = fetch_option['propertyType']
        fetchopts['from'] = start_with
        fetchopts['count'] = count
        search_criteria = get_search_criteria('propertyType', code=code)

        request = {
            "method": "searchPropertyTypes",
            "params": [
                self.token,
                search_criteria,
                fetchopts,
            ],
        }

        resp = self._post_request(self.as_v3, request)
        objects = resp['objects']
        parse_jackson(objects)
        return self._property_type_things(
            objects=objects,
            start_with = start_with,
            count      = count,
            totalCount = resp.get('totalCount')
        )

    def _property_type_things(self, objects, start_with=None, count=None, totalCount=None):
        """takes a list of objects and returns a Things object
        """
        attrs = openbis_definitions('propertyType')['attrs']
        if len(objects) == 0:
            df = DataFrame(columns=attrs)
        else:
            df = DataFrame(objects)
            df['registrationDate'] = df['registrationDate'].map(format_timestamp)
            df['registrator'] = df['registrator'].map(extract_person)
            df['vocabulary'] = df['vocabulary'].map(extract_code)
            df['semanticAnnotations'] = df['semanticAnnotations'].map(extract_nested_permids)
        
        return Things(
            openbis_obj = self,
            entity = 'propertyType',
            single_item_method = self.get_property_type,
            df = df[attrs],
            start_with = start_with,
            count = count,
            totalCount = totalCount,
        )

    def get_material_types(self, type=None, start_with=None, count=None):
        """ Returns a list of all available material types
        """
        return self.get_entity_types(
            entity     = 'materialType',
            cls        = MaterialType,
            type       = type,
            start_with = start_with,
            count      = count
        )

    def get_material_type(self, type, only_data=False):
        return self.get_entity_type(
            entity     = 'materialType',
            cls        = MaterialType,
            identifier = type,
            only_data  = only_data,
        )

    def get_experiment_types(self, type=None, start_with=None, count=None):
        """ Returns a list of all available experiment types
        """
        return self.get_entity_types(
            entity     = 'experimentType',
            cls        = ExperimentType,
            type       = type,
            start_with = start_with,
            count      = count
        )
    get_collection_types = get_experiment_types  # Alias

    def get_experiment_type(self, type, only_data=False):
        return self.get_entity_type(
            entity     = 'experimentType',
            cls        = ExperimentType,
            identifier = type,
            only_data  = only_data,
        )
    get_collection_type = get_experiment_type  # Alias

    def get_dataset_types(self, type=None, start_with=None, count=None):
        """ Returns a list of all available dataSet types
        """
        return self.get_entity_types(
            entity     = 'dataSetType',
            cls        = DataSetType,
            type       = type,
            start_with = start_with,
            count      = count
        )

    def get_dataset_type(self, type, only_data=False):
        return self.get_entity_type(
            entity     = 'dataSetType',
            identifier = type,
            cls        = DataSetType,
            only_data  = only_data,
        )

    def get_sample_types(self, type=None, start_with=None, count=None):
        """ Returns a list of all available sample types
        """
        return self.get_entity_types(
            entity     = 'sampleType',
            cls        = SampleType,
            type       = type,
            start_with = start_with,
            count      = count
        )
    get_object_types = get_sample_types # Alias

    def get_sample_type(self, type, only_data=False, with_vocabulary=False):
        return self.get_entity_type(
            entity     = 'sampleType',
            identifier = type,
            cls        = SampleType,
            with_vocabulary = with_vocabulary,
            only_data  = only_data,
        )
    get_object_type = get_sample_type # Alias

    def get_entity_types(
        self, entity, cls, type=None,
        start_with=None, count=None,
        with_vocabulary=False
    ):
        method_name = get_method_for_entity(entity, 'search')
        if type is not None:
            search_request = _subcriteria_for_code(type, entity)
        else:
            search_request = get_type_for_entity(entity, 'search')

        fetch_options = get_fetchoption_for_entity(entity)
        fetch_options['from'] = start_with
        fetch_options['count'] = count

        request = {
            "method": method_name,
            "params": [
                self.token, 
                search_request, 
                fetch_options
            ],
        }
        resp = self._post_request(self.as_v3, request)
        parse_jackson(resp)

        entity_types = []
        defs = get_definition_for_entity(entity)
        attrs = defs['attrs']
        if len(resp['objects']) == 0:
            entity_types = DataFrame(columns=attrs)
        else:
            objects = resp['objects']
            parse_jackson(objects)
            entity_types = DataFrame(objects)
            entity_types['permId'] = entity_types['permId'].map(extract_permid)
            entity_types['modificationDate'] = entity_types['modificationDate'].map(format_timestamp)
            entity_types['validationPlugin'] = entity_types['validationPlugin'].map(extract_nested_permid
            )

        single_item_method = getattr(self, cls._single_item_method_name)
        return Things(
            openbis_obj = self,
            entity = entity,
            df = entity_types[attrs],
            start_with = start_with,
            single_item_method = single_item_method, 
            count = count,
            totalCount = resp.get('totalCount'),
        )

    def get_entity_type(self, entity, identifier, cls, only_data=False, with_vocabulary=False):

        et = not only_data and not isinstance(identifier, list) and self._object_cache(entity=entity, code=identifier)
        if et:
            return et

        method_name = get_method_for_entity(entity, 'get')
        fetch_options = get_fetchoption_for_entity(entity)
        if with_vocabulary:
            fetch_options["propertyAssignments"]["propertyType"]["vocabulary"] = {
                "@type": "as.dto.vocabulary.fetchoptions.VocabularyFetchOptions",
                "terms": {
                    "@type": "as.dto.vocabulary.fetchoptions.VocabularyTermFetchOptions"
                }
            }

        if not isinstance(identifier, list):
            identifier = [identifier]

        identifiers = []
        for ident in identifier:
            identifiers.append({
                "permId": ident,
                "@type" : "as.dto.entitytype.id.EntityTypePermId",
            })

        request = {
            "method": method_name,
            "params": [
                self.token, 
                identifiers,
                fetch_options
            ],
        }
        resp = self._post_request(self.as_v3, request)
        parse_jackson(resp)
        if len(identifiers) == 1:
            if len(resp) == 0:
                raise ValueError('no such {}: {}'.format(entity, identifier[0]))
        for ident in resp:
            if only_data:
                return resp[ident]
            else:
                obj = cls(
                    openbis_obj = self,
                    data = resp[ident]
                )
                if self.use_cache:
                    self._object_cache(entity=entity, code=ident, value=obj)
                return obj


    def _get_types_of(
        self, method_name, entity, type_name=None,
        start_with=None, count=None,
        additional_attributes=None, optional_attributes=None
    ):
        """ Returns a list of all available types of an entity.
        If the name of the entity-type is given, it returns a PropertyAssignments object
        """
        if additional_attributes is None:
            additional_attributes = []

        if optional_attributes is None:
            optional_attributes = []

        search_request = {
            "@type": "as.dto.{}.search.{}TypeSearchCriteria"
            .format(entity.lower(), entity)
        }
        fetch_options = {
            "@type": "as.dto.{}.fetchoptions.{}TypeFetchOptions"
            .format(entity.lower(), entity)
        }
        fetch_options['from'] = start_with
        fetch_options['count'] = count

        if type_name is not None:
            search_request = _gen_search_criteria({
                entity.lower(): entity + "Type",
                "operator": "AND",
                "code": type_name
            })
            fetch_options['propertyAssignments'] = fetch_option['propertyAssignments']
            if self.get_server_information().api_version > '3.3':
                fetch_options['validationPlugin'] = fetch_option['plugin']

        request = {
            "method": method_name,
            "params": [self.token, search_request, fetch_options],
        }
        resp = self._post_request(self.as_v3, request)
        parse_jackson(resp)

        if type_name is not None:
            if len(resp['objects']) == 1:
                return EntityType(
                    openbis_obj = self,
                    data        = resp['objects'][0]
                )
            elif len(resp['objects']) == 0:
                raise ValueError("No such {} type: {}".format(entity, type_name))
            else:
                raise ValueError("There is more than one entry for entity={} and type={}".format(entity, type_name))

        types = []
        attrs = self._get_attributes(type_name, types, additional_attributes, optional_attributes)
        if len(resp['objects']) == 0:
            types = DataFrame(columns=attrs)
        else:
            objects = resp['objects']
            parse_jackson(objects)
            types = DataFrame(objects)
            types['modificationDate'] = types['modificationDate'].map(format_timestamp)
        return Things(
            openbis_obj = self,
            entity = entity.lower() + '_type',
            df = types[attrs],
            start_with = start_with,
            count = count,
            totalCount = resp.get('totalCount'),
        )


    def _get_attributes(self, type_name, types, additional_attributes, optional_attributes):
        attributes = ['code', 'description'] + additional_attributes
        attributes += [attribute for attribute in optional_attributes if attribute in types]
        attributes += ['modificationDate']
        if type_name is not None:
            attributes += ['propertyAssignments']
        return attributes

    def is_session_active(self):
        """ checks whether a session is still active. Returns true or false.
        """
        return self.is_token_valid(self.token)

    def is_token_valid(self, token=None):
        """Check if the connection to openBIS is valid.
        This method is useful to check if a token is still valid or if it has timed out,
        requiring the user to login again.
        :return: Return True if the token is valid, False if it is not valid.
        """
        if token is None:
            token = self.token

        if token is None:
            return False

        request = {
            "method": "isSessionActive",
            "params": [token],
        }
        try:
            resp = self._post_request(self.as_v1, request)
        except Exception:
            return False

        return resp


    def get_dataset(self, permIds, only_data=False, props=None):
        """fetch a dataset and some metadata attached to it:
        - properties
        - sample
        - parents
        - children
        - containers
        - dataStore
        - physicalData
        - linkedData
        :return: a DataSet object
        """

        just_one = True
        identifiers = []
        if isinstance(permIds, list):
            just_one = False
            for permId in permIds:
                identifiers.append(
                    _type_for_id(permId, 'dataset')
                )
        else:
            identifiers.append(
                _type_for_id(permIds, 'dataset')
            )

        fetchopts = fetch_option['dataSet']

        for option in ['tags', 'properties', 'dataStore', 'physicalData', 'linkedData',
                       'experiment', 'sample', 'registrator', 'modifier']:
            fetchopts[option] = fetch_option[option]

        request = {
            "method": "getDataSets",
            "params": [
                self.token,
                identifiers,
                fetchopts,
            ],
        }

        resp = self._post_request(self.as_v3, request)
        if just_one:
            if len(resp) == 0:
                raise ValueError('no such dataset found: {}'.format(permIds))

            parse_jackson(resp)

            for permId in resp:
                if only_data:
                    return resp[permId]
                else:
                    return DataSet(
                        openbis_obj = self,
                        type = self.get_dataset_type(resp[permId]["type"]["code"]),
                        data = resp[permId]
                    )
        else:
            return self._dataset_list_for_response(response=list(resp.values()), props=props)


    def _dataset_list_for_response(
        self, response, attrs=None, props=None, 
        start_with=None, count=None, totalCount=0,
        objects=None
    ):
        """returns a Things object, containing a DataFrame plus some additional information
        """
        def extract_attribute(attribute_to_extract):
            def return_attribute(obj):
                if obj is None: return ''
                return obj.get(attribute_to_extract,'')
            return return_attribute

        parse_jackson(response)

        if attrs is None: attrs=[]
        default_attrs = [
            'permId', 'type', 'experiment', 'sample',
            'registrationDate', 'modificationDate',
            'location', 'status', 'presentInArchive', 'size',
        ]
        display_attrs = default_attrs + attrs

        def extract_project(attr):
            entity, _, attr = attr.partition('.')
            def extract_attr(obj):
                try: 
                    if attr:
                        return obj['project'][attr]
                    else:
                        return obj['project']['identifier']['identifier']
                except KeyError:
                    return ''
            return extract_attr

        def extract_space(attr):
            entity, _, attr = attr.partition('.')
            def extract_attr(obj):
                try: 
                    if attr:
                        return obj['project']['space'][attr]
                    else:
                        return obj['project']['space']['code']
                except KeyError:
                    return ''
            return extract_attr

        if props is None:
            props = []
        else:
            if isinstance(props, str):
                props = [props]

        if len(response) == 0:
            for prop in props:
                if prop == '*': continue
                display_attrs.append(prop)
            datasets = DataFrame(columns=display_attrs)
        else:
            datasets = DataFrame(response)
            for attr in attrs:
                if 'project' in attr:
                    datasets[attr] = datasets['experiment'].map(extract_project(attr))
                elif 'space' in attr:
                    datasets[attr] = datasets['experiment'].map(extract_space(attr))
                elif '.' in attr:
                    entity, attribute_to_extract = attr.split('.')
                    datasets[attr] = datasets[entity].map(extract_attribute(attribute_to_extract))
            for attr in attrs:
                # if no dot supplied, just display the code of the space, project or experiment
                if any(entity == attr for entity in ['experiment', 'sample']):
                    datasets[attr] = datasets[attr].map(extract_nested_identifier)

            datasets['registrationDate'] = datasets['registrationDate'].map(format_timestamp)
            datasets['modificationDate'] = datasets['modificationDate'].map(format_timestamp)
            datasets['experiment'] = datasets['experiment'].map(extract_nested_identifier)
            datasets['sample'] = datasets['sample'].map(extract_nested_identifier)
            datasets['type'] = datasets['type'].map(extract_code)
            datasets['permId'] = datasets['code']
            for column in ['parents','children','components','containers']:
                if column in datasets:
                    datasets[column] = datasets[column].map(extract_identifiers)
            datasets['size'] = datasets['physicalData'].map(lambda x: x.get('size') if x else '')
            datasets['status'] = datasets['physicalData'].map(lambda x: x.get('status') if x else '')
            datasets['presentInArchive'] = datasets['physicalData'].map(lambda x: x.get('presentInArchive') if x else '')
            datasets['location'] = datasets['physicalData'].map(lambda x: x.get('location') if x else '')

            for prop in props:
                if prop == '*':
                    # include all properties in dataFrame.
                    # expand the dataFrame by adding new columns
                    columns = []
                    for i, dataSet in enumerate(response):
                        for prop_name, val in dataSet.get('properties',{}).items():
                            datasets.loc[i, prop_name.upper()] = val
                            columns.append(prop_name.upper())

                    display_attrs += set(columns)
                    continue

                else:
                    # property name is provided
                    for i, dataSet in enumerate(response):
                        val = dataSet.get('properties',{}).get(prop,'') or dataSet.get('properties',{}).get(prop.upper(),'')
                        datasets.loc[i, prop.upper()] = val
                    display_attrs.append(prop.upper())

        return Things(
            openbis_obj = self,
            entity = 'dataset',
            df = datasets[display_attrs],
            identifier_name = 'permId',
            start_with=start_with,
            count=count,
            totalCount=totalCount,
            objects=objects,
        )


    def get_sample(self, sample_ident, only_data=False, withAttachments=False, props=None):
        """Retrieve metadata for the sample.
        Get metadata for the sample and any directly connected parents of the sample to allow access
        to the same information visible in the ELN UI. The metadata will be on the file system.
        :param sample_identifiers: A list of sample identifiers to retrieve.
        """

        only_one = True
        identifiers = []
        if isinstance(sample_ident, list):
            only_one = False
            for ident in sample_ident:
                identifiers.append(
                    _type_for_id(ident, 'sample')
                )
        else:
            identifiers.append(
                _type_for_id(sample_ident, 'sample')
            )

        fetchopts = fetch_option['sample']
        options = ['tags', 'properties', 'attachments', 'space', 'experiment', 'registrator', 'modifier', 'dataSets']
        if self.get_server_information().project_samples_enabled:
            options.append('project')
        for option in options:
            fetchopts[option] = fetch_option[option]

        if withAttachments:
            fetchopts['attachments'] = fetch_option['attachmentsWithContent']

        for key in ['parents','children','container','components']:
            fetchopts[key] = {"@type": "as.dto.sample.fetchoptions.SampleFetchOptions"}

        request = {
            "method": "getSamples",
            "params": [
                self.token,
                identifiers,
                fetchopts
            ],
        }

        resp = self._post_request(self.as_v3, request)

        if only_one:
            if len(resp) == 0:
                raise ValueError('no such sample found: {}'.format(sample_ident))

            parse_jackson(resp)
            for sample_ident in resp:
                if only_data:
                    return resp[sample_ident]
                else:
                    return Sample(
                        openbis_obj = self,
                        type = self.get_sample_type(resp[sample_ident]["type"]["code"]),
                        data = resp[sample_ident]
                    )
        else:
            return self._sample_list_for_response(
                response=list(resp.values()),
                props=props,
            )


    @staticmethod
    def decode_attribute(entity, attribute):
        params = {}
        attribute, *alias = re.split(r'\s+AS\s+', attribute, flags=re.IGNORECASE)
        alias = alias[0] if alias else attribute

        regex = re.compile(
            r"""^                         # beginning of the string
                (?P<requested_entity>\w+) # the entity itself
                (\.(?P<attribute>\w+))?   # capture an optional .attribute
                $                         # end of string
        """, re.X)
        match = re.search(regex, attribute)
        params = match.groupdict()

        if params['requested_entity'] == 'object':
            params['entity'] = 'sample'
        elif params['requested_entity'] == 'collection':
            params['entity'] = 'experiment'
        elif params['requested_entity'] in ['space', 'project']:
            params['entity'] = params['requested_entity']
        else: params['entity'] = params['requested_entity']

        if not params['attribute']: params['attribute'] = 'code'
        params['alias'] = alias

        del(params['requested_entity'])
        return params


    def _decode_property(self, entity, property):
        # match something like: property_name.term.label AS label_alias
        regex = re.compile(
            r"""^
                (?P<alias_alternative>
                (?P<property>[^\.]*  )
                (?:
                    \.
                    (?P<subentity>term|pa) \.
                    (?P<field>code|vocabularyCode|label|description|ordinal|dataType)
                )?
                )
                (
                \s+(?i)AS\s+
                (?P<alias>\w+)
                )?
                \s*
                $
            """, re.X
        )
        match = re.search(regex, property)
        if not match:
            try:
                params = self.decode_attribute(entity, property)
                return params
            except ValueError:
                raise ValueError(f"unable to parse property: {property}")
        params = match.groupdict()
        if not params['alias']: params['alias'] = params['alias_alternative']

        return params


    def _sample_list_for_response(
        self, response, attrs=None, props=None,
        start_with=None, count=None, totalCount=0,
        objects=None
    ):
        """returns a Things object, containing a DataFrame plus additional information
        """
        def extract_attribute(attribute_to_extract):
            def return_attribute(obj):
                if obj is None: return ''
                return obj.get(attribute_to_extract,'')
            return return_attribute

        parse_jackson(response)

        if attrs is None: attrs = []
        default_attrs = ['identifier', 'permId', 'type', 'registrator', 'registrationDate', 'modifier', 'modificationDate']
        display_attrs = default_attrs + attrs

        if props is None:
            props = []
        else:
            if isinstance(props, str):
                props = [props]

        if len(response) == 0:
            for prop in props:
                if prop == '*': continue
                display_attrs.append(prop)
            samples = DataFrame(columns=display_attrs)
        else:
            samples = DataFrame(response)
            for attr in attrs:
                if '.' in attr:
                    entity, attribute_to_extract = attr.split('.')
                    samples[attr] = samples[entity].map(extract_attribute(attribute_to_extract))

            for attr in attrs:
                # if no dot supplied, just display the code of the space, project or experiment
                if attr in ['project', 'experiment']:
                    samples[attr] = samples[attr].map(extract_nested_identifier)
                if attr in ['space']:
                    samples[attr] = samples[attr].map(extract_code)

            samples['registrationDate'] = samples['registrationDate'].map(format_timestamp)
            samples['modificationDate'] = samples['modificationDate'].map(format_timestamp)
            samples['registrator'] = samples['registrator'].map(extract_person)
            samples['modifier'] = samples['modifier'].map(extract_person)
            samples['identifier'] = samples['identifier'].map(extract_identifier)
            samples['container'] = samples['container'].map(extract_nested_identifier)
            for column in ['parents','children','components']:
                if column in samples:
                    samples[column] = samples[column].map(extract_identifiers)
            samples['permId'] = samples['permId'].map(extract_permid)
            samples['type'] = samples['type'].map(extract_nested_permid)

            for prop in props:
                if prop == '*':
                    # include all properties in dataFrame.
                    # expand the dataFrame by adding new columns
                    columns = []
                    for i, sample in enumerate(response):
                        for prop_name, val in sample.get('properties',{}).items():
                            samples.loc[i, prop_name.upper()] = val
                            columns.append(prop_name.upper())

                    display_attrs += set(columns)
                    continue

                else:
                    # property name is provided
                    for i, sample in enumerate(response):
                        val = sample.get('properties',{}).get(prop,'') or sample.get('properties',{}).get(prop.upper(),'')
                        samples.loc[i, prop.upper()] = val
                    display_attrs.append(prop.upper())

        return Things(
            openbis_obj = self,
            entity = 'sample',
            df = samples[display_attrs],
            identifier_name = 'identifier',
            start_with=start_with,
            count=count,
            totalCount=totalCount,
            objects=objects,
        )

    get_object = get_sample # Alias


    def get_external_data_management_systems(self, start_with=None, count=None, only_data=False):
        entity = 'externalDms'

        criteria = get_type_for_entity(entity, 'search')
        fetchopts = get_fetchoption_for_entity(entity)
        request = {
            "method": "searchExternalDataManagementSystems",
            "params": [self.token,
                       criteria,
                       fetchopts,
                       ],
        }
        response = self._post_request(self.as_v3, request)
        parse_jackson(response)
        attrs= "code label address addressType urlTemplate openbis".split()


        if len(response['objects']) == 0:
            entities = DataFrame(columns=attrs)
        else: 
            objects = response['objects']
            parse_jackson(objects)
            entities = DataFrame(objects)
            entities['permId'] = entities['permId'].map(extract_permid)

        totalCount = response.get('totalCount')
        return Things(
            openbis_obj = self,
            entity = 'externalDms',
            df = entities[attrs],
            identifier_name = 'permId',
            start_with=start_with,
            count=count,
            totalCount=totalCount,
        )


    def get_external_data_management_system(self, permId, only_data=False):
        """Retrieve metadata for the external data management system.
        :param permId: A permId for an external DMS.
        :param only_data: Return the result data as a hash-map, not an object.
        """

        request = {
            "method": "getExternalDataManagementSystems",
            "params": [
                self.token,
                [{
                    "@type": "as.dto.externaldms.id.ExternalDmsPermId",
                    "permId": permId
                }],
                {
                    "@type": "as.dto.externaldms.fetchoptions.ExternalDmsFetchOptions",
                },
            ],
        }

        resp = self._post_request(self.as_v3, request)
        parse_jackson(resp)

        if resp is None or len(resp) == 0:
            raise ValueError('no such external DMS found: ' + permId)
        else:
            for ident in resp:
                if only_data:
                    return resp[ident]
                else:
                    return ExternalDMS(self, resp[ident])

    get_externalDms = get_external_data_management_system  # alias


    def new_space(self, **kwargs):
        """ Creates a new space in the openBIS instance.
        """
        return Space(self, None, **kwargs)


    def new_git_data_set(self, data_set_type, path, commit_id, repository_id, dms, sample=None, experiment=None, properties={},
                         dss_code=None, parents=None, data_set_code=None, contents=[]):
        """ Create a link data set.
        :param data_set_type: The type of the data set
        :param data_set_type: The type of the data set
        :param path: The path to the git repository
        :param commit_id: The git commit id
        :param repository_id: The git repository id - same for copies
        :param dms: An external data managment system object or external_dms_id
        :param sample: A sample object or sample id.
        :param dss_code: Code for the DSS -- defaults to the first dss if none is supplied.
        :param properties: Properties for the data set.
        :param parents: Parents for the data set.
        :param data_set_code: A data set code -- used if provided, otherwise generated on the server
        :param contents: A list of dicts that describe the contents:
            {'file_length': [file length],
             'crc32': [crc32 checksum],
             'directory': [is path a directory?]
             'path': [the relative path string]}
        :return: A DataSet object
        """
        return pbds.GitDataSetCreation(self, data_set_type, path, commit_id, repository_id, dms, sample, experiment,
                                       properties, dss_code, parents, data_set_code, contents).new_git_data_set()

    def new_content_copy(self, path, commit_id, repository_id, edms_id, data_set_id):
        """
        Create a content copy in an existing link data set.
        :param path: path of the new content copy
        "param commit_id: commit id of the new content copy
        "param repository_id: repository id of the content copy
        "param edms_id: Id of the external data managment system of the content copy
        "param data_set_id: Id of the data set to which the new content copy belongs
        """
        return pbds.GitDataSetUpdate(self, data_set_id).new_content_copy(path, commit_id, repository_id, edms_id)

    def search_files(self, data_set_id, dss_code=None):
        return pbds.GitDataSetFileSearch(self, data_set_id).search_files()        

    def delete_content_copy(self, data_set_id, content_copy):
        """
        Deletes a content copy from a data set.
        :param data_set_id: Id of the data set containing the content copy
        :param content_copy: The content copy to be deleted
        """
        return pbds.GitDataSetUpdate(self, data_set_id).delete_content_copy(content_copy)        

    @staticmethod
    def sample_to_sample_id(sample):
        """Take sample which may be a string or object and return an identifier for it."""
        return Openbis._object_to_object_id(sample, "as.dto.sample.id.SampleIdentifier", "as.dto.sample.id.SamplePermId")

    @staticmethod
    def experiment_to_experiment_id(experiment):
        """Take experiment which may be a string or object and return an identifier for it."""
        return Openbis._object_to_object_id(experiment, "as.dto.experiment.id.ExperimentIdentifier", "as.dto.experiment.id.SamplePermId")

    @staticmethod
    def _object_to_object_id(obj, identifierType, permIdType):
        object_id = None
        if isinstance(obj, str):
            if (is_identifier(obj)):
                object_id = {
                    "identifier": obj,
                    "@type": identifierType
                }
            else:
                object_id = {
                    "permId": obj,
                    "@type": permIdType
                }
        else:
            object_id = {
                "identifier": obj.identifier,
                "@type": identifierType
            }
        return object_id

    @staticmethod
    def data_set_to_data_set_id(data_set):
        if isinstance(data_set, str):
            code = data_set
        else:
            code = data_set.permId
        return {
            "permId": code,
            "@type": "as.dto.dataset.id.DataSetPermId"
        }

    def external_data_managment_system_to_dms_id(self, dms):
        if isinstance(dms, str):
            dms_id = {
                "permId": dms,
                "@type": "as.dto.externaldms.id.ExternalDmsPermId"
            }
        else:
            dms_id = {
                "identifier": dms.code,
                "@type": "as.dto.sample.id.SampleIdentifier"
            }
        return dms_id

    def new_sample(self, type, project=None, props=None, **kwargs):
        """ Creates a new sample of a given sample type.
        type         -- sampleType code or object: mandatory
        code         -- name/code for the sample, if not generated automatically
        space        -- space code or object
        project      -- project code or object
        experiment   -- experiment code or object
        collection   -- same as above
        props        -- a dictionary containing the properties
        """
        if 'collection' in kwargs:
            kwargs['experiment'] = kwargs['collection']
            kwargs.pop('collection', None)

        if isinstance(type, str):
            sample_type = self.get_sample_type(type)
        else:
            sample_type = type
        return Sample(self, type=sample_type, project=project, data=None, props=props, **kwargs)

    new_object = new_sample # Alias


    def new_transaction(self, *entities):
        return Transaction(*entities)


    def new_sample_type(self,
        code, 
        generatedCodePrefix,
        subcodeUnique=False,
        autoGeneratedCode=False,
        listable=True,
        showContainer=False,
        showParents=True,
        showParentMetadata=False,
        validationPlugin=None
    ):
        """Creates a new sample type.
        """

        return SampleType(self, 
            code=code, 
            generatedCodePrefix = generatedCodePrefix,
            autoGeneratedCode = autoGeneratedCode,
            listable = listable,
            showContainer = showContainer,
            showParents = showParents,
            showParentMetadata = showParentMetadata,
            validationPlugin = validationPlugin,
        )
    new_object_type = new_sample_type

    def new_dataset_type(self, 
        code,
        description=None,
        mainDataSetPattern=None,
        mainDataSetPath=None,
        disallowDeletion=False,
        validationPlugin=None,
    ):
        """Creates a new dataSet type.
        """

        return DataSetType(self,
            code=code, 
            description=description, 
            mainDataSetPattern=mainDataSetPattern,
            mainDataSetPath=mainDataSetPath,
            disallowDeletion=disallowDeletion,
            validationPlugin=validationPlugin,
        )

    def new_experiment_type(self, 
        code, 
        description=None,
        validationPlugin=None,
    ):
        """Creates a new experiment type (collection type)
        """
        return ExperimentType(self,
            code=code, 
            description=description, 
            validationPlugin=validationPlugin,
        )
    new_collection_type = new_experiment_type


    def new_material_type(self,
        code, 
        description=None,
        validationPlugin=None,
    ):
        """Creates a new material type.
        """
        return MaterialType(self,
            code=code,
            description=description,
            validationPlugin=validationPlugin,
        )

    def new_dataset(self, type=None, kind='PHYSICAL_DATA', files=None, file=None, props=None, folder=None, **kwargs):
        """ Creates a new dataset of a given type.

        type         -- sampleType code or object: mandatory
        sample       -- sample code or object
        experiment   -- experiment code or object
        collection   -- same as above
        file         -- path to a single file or a directory
        files        -- list of paths to files. Instead of a file, a directory (or many directories)
                        can be provided, the structure is kept intact in openBIS
        zipfile      -- path to a zipfile, which is unzipped in openBIS
        kind         -- if set to CONTAINER, no files should be provided.
                        Instead, the dataset acts as a container for other datasets.

        props        -- a dictionary containing the properties
        """

        if type is None:
            raise ValueError("Please provide a dataSet type")

        if file:
            files = [file]

        if isinstance(type, str):
            type_obj = self.get_dataset_type(type.upper())
        else:
            type_obj = type

        if 'object' in kwargs:
            kwargs['sample'] = kwargs['object']
            kwargs.pop('object', None)
        if 'collection' in kwargs:
            kwargs['experiment'] = kwargs['collection']
            kwargs.pop('collection', None)

        return DataSet(self, type=type_obj, kind=kind, files=files, folder=folder, props=props, **kwargs)
    
    def new_semantic_annotation(self, entityType=None, propertyType=None, **kwargs):
        """ Note: not functional yet. """
        return SemanticAnnotation(
            openbis_obj=self, isNew=True,
            entityType=entityType, propertyType=propertyType, **kwargs
        )    

    def new_vocabulary(self, code, terms, managedInternally=False, chosenFromList=True, **kwargs):
        """ Creates a new vocabulary
        Usage::
            new_vocabulary(
                code = 'vocabulary_code',
                description = '',
                terms = [
                    { "code": "term1", "label": "label1", "description": "description1" },
                    { "code": "term2", "label": "label2", "description": "description2" },
                ]
            )
        """
        kwargs['code'] = code
        kwargs['managedInternally'] = managedInternally
        kwargs['chosenFromList'] = chosenFromList
        return Vocabulary(self, data=None, terms=terms, **kwargs)

    def _get_dss_url(self, dss_code=None):
        """ internal method to get the downloadURL of a datastore.
        """
        dss = self.get_datastores()
        if dss_code is None:
            return dss['downloadUrl'][0]
        else:
            return dss[dss['code'] == dss_code]['downloadUrl'][0]


class ExternalDMS():
    """ managing openBIS external data management systems
    """

    def __init__(self, openbis_obj, data=None, **kwargs):
        self.__dict__['openbis'] = openbis_obj

        if data is not None:
            self.__dict__['data'] = data

        if kwargs is not None:
            for key in kwargs:
                setattr(self, key, kwargs[key])

    def __getattr__(self, name):
        return self.__dict__['data'].get(name)

    def __dir__(self):
        """all the available methods and attributes that should be displayed
        when using the autocompletion feature (TAB) in Jupyter
        """
        return ['code', 'label', 'urlTemplate', 'address', 'addressType', 'openbis']

    def __str__(self):
        return self.data.get('code', None)


class ServerInformation():
    
    def __init__(self, info):
        self._info = info
        self.attrs = [
            'api_version', 'archiving_configured', 'authentication_service',
            'enabled_technologies', 'project_samples_enabled'
        ]

    def __dir__(self):
        return self.attrs

    def __getattr__(self, name):
        return self._info.get(name.replace('_', '-'))
    
    def get_major_version(self):
        return int(self._info["api-version"].split(".")[0])
    
    def get_minor_version(self):
        return int(self._info["api-version"].split(".")[1])
    
    def is_openbis_1605(self):
        return (self.get_major_version() == 3) and (self.get_minor_version() <= 2)
    
    def is_openbis_1806(self):
        return (self.get_major_version() == 3) and (self.get_minor_version() >= 5)

    def _repr_html_(self):
        html = """
            <table border="1" class="dataframe">
            <thead>
                <tr style="text-align: right;">
                <th>attribute</th>
                <th>value</th>
                </tr>
            </thead>
            <tbody>
        """

        for attr in self.attrs:
            html += "<tr> <td>{}</td> <td>{}</td> </tr>".format(
                attr, getattr(self, attr, '')
            )

        html += """
            </tbody>
            </table>
        """
        return html


class PropertyType(
    OpenBisObject, 
    entity='propertyType',
    single_item_method_name='get_property_type'
):
    pass

class Plugin(
    OpenBisObject,
    entity='plugin',
    single_item_method_name='get_plugin'
):
    pass
