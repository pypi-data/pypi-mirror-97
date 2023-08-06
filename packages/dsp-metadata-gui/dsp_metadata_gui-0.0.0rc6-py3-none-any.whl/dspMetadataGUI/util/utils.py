"""
This module holds utility classes, functions and enums for metadata.
"""

import os
import re
import platform
import subprocess
from typing import List
from rdflib import Graph, Namespace, RDF, URIRef, BNode
import validators
import random
from enum import Enum
from urllib.parse import urlparse


dsp_repo = Namespace("http://ns.dasch.swiss/repository#")


def open_file(path: str):
    """
    Open a file with default application, OS independent.

    Args:
        path (str): path of the file to open.
    """
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


def areURLs(urls: List[str]) -> bool:
    """
    Checks if a list of strings contains only valid URLs.

    Args:
        urls (List[str]): a list with (potential) URLs.

    Returns:
        bool: True, if all strings are valid URLs; false otherwise.
    """
    for url in urls:
        if not url:
            continue
        if not isURL(url):
            return False
    return True


def isURL(url: str) -> bool:
    """
    Checks if a string is a valid URL.

    Args:
        url (str): the (potential) URL string.

    Returns:
        bool: True, if a valid URL; False otherwise.
    """
    if url and not url.isspace():
        if validators.url(url):
            return True
        if validators.url('http://' + url):
            return True
        # LATER: good enough?
        # if validators.url('http://www.' + url):
        #     return True
    return False


def get_url_property_id(url: str) -> str:
    """
    This method tries to guess the propetyID for a URL.

    For certain pre-defined cases, a reasonable propertyID is chosen;
    otherwise, the net location is being extracted, if possible.

    Args:
        url (str): a URL

    Returns:
        str: a propertyID
    """
    if re.search(r'skos\.um\.es', url):
        return "SKOS UNESCO Nomenclature"
    if re.search(r'geonames\.org', url):
        return "Geonames"
    if re.search(r'pleiades\.stoa\.org', url):
        return "Pleiades"
    if re.search(r'orcid\.org', url):
        return "ORCID"
    if re.search(r'viaf\.org', url):
        return "VIAF"
    if re.search(r'\/gnd\/', url) or re.search(r'portal\.dnb\.de', url):
        return "GND"
    if re.search(r'n2t\.net\/ark\:\/99152', url):
        return "Periodo"
    if re.search(r'chronontology\.dainst\.org', url):
        return "ChronOntology"
    if re.search(r'creativecommons\.', url):
        return "Creative Commons"
    # LATER: propertyID's for common institutions
    loc = urlparse(url).netloc
    if len(loc.split('.')) > 2:
        return '.'.join(loc.split('.')[1:])
    if loc:
        return loc
    return url[:12]


def are_emails(mails: List[str]) -> bool:
    """
    Checks if the list contains only valid e-mail addresses.

    Args:
        mails (List[str]): A list with (potential) e-mail addresses.

    Returns:
        bool: True, if all strings are valid e-mail addresses; False otherwise.
    """
    for mail in mails:
        if not mail:
            continue
        if not is_email(mail):
            return False
    return True


def is_email(mail: str) -> bool:
    """
    Checks, if a string is a valid mail address.

    Args:
        mail (str): The (potential) e-mail address.

    Returns:
        bool: True, if a valid e-mail address; false otherwise.
    """
    if mail and not mail.isspace():
        if validators.email(mail):
            return True
    return False


def get_coherent_graph(g: Graph) -> Graph:
    """
    Gets a coherent subgraph from a graph.

    That is, if a Property is not connected to the main part of the graph, it will be left out.

    Args:
        g (Graph): A RDF graph, potentially not coherent.

    Returns:
        Graph: A coherent subgraph of the graph.
    """
    project = list(g.subjects(RDF.type, dsp_repo.Project))[0]
    traversed = []
    to_visit = [project]

    while to_visit:
        x = to_visit.pop()
        traversed.append(x)
        for _, p, o in g.triples((x, None, None)):
            if p != RDF.type and isinstance(o, (URIRef, BNode)) and o not in traversed:
                to_visit.append(o)
        for new_x in g.subjects(object=x):
            if new_x not in traversed:
                to_visit.append(new_x)

    for s, p, o in g:
        if s not in traversed:
            g.remove((s, None, None))

    return g


class Validity(Enum):
    """
    Enumeration of validity states.
    """
    UNDEFINED = -1
    """Undefined Value. Should never happen."""
    VALID = 0
    """Valid: The value is valid."""
    INVALID_VALUE = 1
    """Invalid: The given value is invalid."""
    REQUIRED_VALUE_MISSING = 2
    """Invalid: No value given on required property."""
    OPTIONAL_VALUE_MISSING = 3
    """Ignored: No value given on optional field."""


class Cardinality(Enum):
    """
    Enumeration of cardinalities that may be used for properties.
    """
    UNBOUND = 0
    """0-n"""
    ONE = 1
    """1"""
    ZERO_OR_ONE = 2
    """0-1"""
    ONE_TO_UNBOUND = 3
    """1-n"""
    ONE_TO_TWO = 4
    """1-2"""
    ZERO_TO_TWO = 5
    """0-2"""
    ONE_TO_UNBOUND_ORDERED = 6
    """1-n ordered"""

    def get_optionality_string(card) -> str:
        """
        Returns wether or not a cardinality is optional.

        Args:
            card (Cardinality): the cardinality in question

        Returns:
            str: "Mandatory" or "Optional", depending on the cardinality
        """
        if Cardinality.isMandatory(card):
            return "Mandatory"
        else:
            return "Optional"

    def isMandatory(card) -> bool:
        """
        Checks if a cardinality is mandatory/required.

        Args:
            card (Cardinality): the cardinality in question.

        Returns:
            bool: True, if mandatory; false, if optional.
        """
        if card == Cardinality.ONE \
                or card == Cardinality.ONE_TO_TWO \
                or card == Cardinality.ONE_TO_UNBOUND \
                or card == Cardinality.ONE_TO_UNBOUND_ORDERED:
            return True
        if card == Cardinality.UNBOUND \
                or card == Cardinality.ZERO_OR_ONE \
                or card == Cardinality.ZERO_TO_TWO:
            return False

    def as_sting(card) -> str:
        """
        Get a human readable string representation of the cardinality in question.

        Args:
            card (Cardinality): The cardinality in question.

        Returns:
            str: String representation of the cardinality.
        """
        if card == Cardinality.UNBOUND:
            return "Unbound: 0-n values"
        elif card == Cardinality.ONE:
            return "Exactly one value"
        elif card == Cardinality.ZERO_OR_ONE:
            return "Optional: Zero or one value"
        elif card == Cardinality.ONE_TO_UNBOUND:
            return "Mandatory unbound: 1-n values"
        elif card == Cardinality.ONE_TO_TWO:
            return "One or two values"
        elif card == Cardinality.ZERO_TO_TWO:
            return "Optional: Zero, one or two values"
        elif card == Cardinality.ONE_TO_UNBOUND_ORDERED:
            return "Mandatory unbound: 1-n values (ordered)"


class Datatype(Enum):
    """
    Enumeration of cardinalities that may be used for properties.
    """
    STRING = 0
    """String literal"""
    DATE = 1
    """Date (yyyy-mm-dd)"""
    STRING_OR_URL = 2
    """String or URL"""
    PLACE = 3
    """Place (represented by URL to authority files)"""
    PERSON_OR_ORGANIZATION = 4
    """Person or Organization (Reference to object)"""
    GRANT = 5
    """Grant (Reference to object)"""
    DATA_MANAGEMENT_PLAN = 6
    """Data Management Plan"""
    URL = 7
    """URL"""
    CONTROLLED_VOCABULARY = 8
    """Controlled Vocabulary"""
    PROJECT = 9
    """Project (reference to object)"""
    ATTRIBUTION = 10
    """Attribution (Role and Agent)"""
    EMAIL = 11
    """E-mail address"""
    ADDRESS = 12
    """Postal address"""
    PERSON = 13
    """Person (reference to object)"""
    ORGANIZATION = 14
    """Organization (reference to object)"""
    DOWNLOAD = 15
    """Download"""
    SHORTCODE = 16
    """Shortcode"""


class IRIFactory:
    """
    Factory class to generate unique IRIs.
    """

    @staticmethod
    def _get_all_iris(object_type: str, meta):
        try:
            if object_type == 'dataset':
                return [d.iri_suffix for d in meta.dataset]
            elif object_type == 'person':
                return [d.iri_suffix for d in meta.persons]
            elif object_type == 'organization':
                return [d.iri_suffix for d in meta.organizations]
            elif object_type == 'grant':
                return [d.iri_suffix for d in meta.grants]
            else:
                return []
        except Exception:
            return []

    @classmethod
    def get_unique_iri(cls, object_type: str, meta) -> str:
        """
        Get a IRI for a object, that is unique to a MetaDataSet.

        Args:
            object_type (str): Type of the object.
            meta (MetaDataSet): The MetaDataSet to which the IRI should be unique.

        Returns:
            str: Unique IRI.
        """
        existing = cls._get_all_iris(object_type, meta)
        for i in range(999):
            new = f"-{object_type}-{str(i).zfill(3)}"
            if new not in existing:
                return new
        return f"-{object_type}-{str(random.randint(1000,1000000)).zfill(7)}"
