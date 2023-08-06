"""
This module holds the data structure that is used for modelling metadata.

The classes defined here aim to represent a metadata-set, closely following the
[metadata ontology](https://github.com/dasch-swiss/dsp-ontologies/blob/main/dsp-repository/v1/dsp-repository.shacl.ttl).
"""

from abc import ABC, abstractmethod
import re
from typing import List, Tuple
import pyshacl
import validators
from rdflib import Graph, URIRef, RDF, Literal, Namespace, BNode
from rdflib.namespace import SDO, XSD

from . import utils
from .utils import Cardinality, Datatype, Validity, IRIFactory


ontology_url = "https://raw.githubusercontent.com/dasch-swiss/dsp-ontologies/main/dsp-repository/v1/dsp-repository.shacl.ttl"
dsp_repo = Namespace("http://ns.dasch.swiss/repository#")
prov = Namespace("http://www.w3.org/ns/prov#")


class MetaDataSet:
    """ Representation of a data set.

    This class represents a data set of project metadata.
    It holds the following properties:

    - name: the repo/project name.
      Typically the name of the folder that was selected.
    - path: the full path of the folder that was selected.
    - files: a list of relevant files in the folder.
    - graph: the RDF graph of the metadata.
    - turtle: the turtle serialization of the overall graph.
    - validation_result: the validation result of the current graph state.
    - project: a `metaDataSet.Project` representation of the actual metadata (as specified by the ontology).
    - dataset: a list of `metaDataSet.Dataset`
    - persons: a list of `metaDataSet.Person`
    - organizations: a list of `metaDataSet.Organization`

    """

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, path: str):
        self.__path = path

    @property
    def files(self):
        return self.__files

    @files.setter
    def files(self, files: list):
        self.__files = files

    @property
    def graph(self):
        return self.__graph

    @graph.setter
    def graph(self, graph: Graph):
        self.__graph = graph
        ttl = graph.serialize(format='turtle').decode("utf-8")
        self.turtle = ttl
        val = self.validate_graph(graph)[0]
        self.validation_result = val

    @property
    def turtle(self):
        return self.__turtle

    @turtle.setter
    def turtle(self, turtle: str):
        self.__turtle = turtle

    @property
    def validation_result(self):
        return self.__validity

    @validation_result.setter
    def validation_result(self, validity: bool):
        self.__validity = validity

    def __init__(self, name: str, path: str, shortcode: str):
        """
        Initiates the object.

        Args:
            name (str): project name
            path (str): path to the folder associated with the project
            shortcode (str): 4 digit hexadecimal project shortcode
        """
        self.shortcode = shortcode
        self.name = name
        self.path = path
        self.files = []
        self.project: Project = Project(name, shortcode, self)
        self.dataset: List[Dataset] = [Dataset(name, self.project, self)]
        self.persons: List[Person] = [Person(self)]
        self.organizations: List[Organization] = [Organization(self)]
        self.grants: List[Grant] = [Grant(self)]

    def __str__(self):
        return str({
            "name": self.name,
            "path": self.path,
            "files": self.files,
            "metadata": [
                self.project,
                self.dataset,
                self.persons,
                self.organizations,
                self.grants,
            ]
        })

    def get_all_properties(self) -> list:
        """
        Returns a list of all properties held by fields of this class. (person, dataset, etc.)

        Returns:
            list[Property]: a List of all properties in this metadataset.
        """
        res = self.project.get_properties()
        for p in self.dataset:
            res.extend(p.get_properties())
        for p in self.persons:
            res.extend(p.get_properties())
        for o in self.organizations:
            res.extend(o.get_properties())
        for o in self.grants:
            res.extend(o.get_properties())
        return res

    def validate_graph(self, graph) -> tuple:
        """
        Validates the graph of the entire data against the SHACL ontology.

        Returns:
            tuple: The validation result.
        """
        conforms, results_graph, results_text = pyshacl.validate(graph, shacl_graph=ontology_url)
        return conforms, results_graph, results_text

    def generate_rdf_graph(self) -> Graph:
        """
        Generates the RFD graph of the entire dataset.

        Returns:
            Graph: The RDF graph
        """
        graph = Graph(base=dsp_repo)
        graph.bind("dsp-repo", dsp_repo)
        graph.bind("schema", SDO)
        graph.bind("xsd", XSD)
        graph.bind("prov", prov)
        self.project.add_rdf_to_graph(graph, "Project")
        for elem in self.dataset:
            elem.add_rdf_to_graph(graph, "Dataset")
        for elem in self.persons:
            elem.add_rdf_to_graph(graph, "Person")
        for elem in self.organizations:
            elem.add_rdf_to_graph(graph, "Organization")
        for elem in self.grants:
            elem.add_rdf_to_graph(graph, "Grant")
        try:
            graph = utils.get_coherent_graph(graph)
            self.graph = graph
        except Exception:
            print('Warning: Graph could not be cached.')
            # LATER: remove with next breaking change
        return graph

    def get_by_string(self, s: str):  # returns DataClass
        # LATER: if the data classes are moved to another file, and imported, then this could be typed too.
        """
        Get a data object by its string representation.

        Checks all available objects for a matching one by its string.

        Args:
            s (str): string of the object

        Returns:
            DataClass|None: The object matching the string.
        """
        if not s or s.isspace():
            return
        if str(self.project) == s:
            return self.project
        id_str = s.split(':')[0]
        for o in self.dataset:
            if str(o).startswith(id_str):
                return o
        for o in self.persons:
            if str(o).startswith(id_str):
                return o
        for o in self.organizations:
            if str(o).startswith(id_str):
                return o
        for o in self.grants:
            if str(o).startswith(id_str):
                return o

    def add_dataset(self):
        """Add a new dataset"""
        new = Dataset(self.name, self.project, self)
        self.dataset.append(new)

    def add_person(self):
        """Add a new person"""
        new = Person(self)
        self.persons.append(new)

    def add_organization(self):
        """Add a new organization"""
        new = Organization(self)
        self.organizations.append(new)

    def add_grant(self):
        """Add a new grant"""
        new = Grant(self)
        self.grants.append(new)

    def remove(self, obj):
        """
        remove a DataClass Object

        Args:
            obj (Dataclass): The object to remove.
        """
        if obj in self.dataset:
            self.dataset.remove(obj)
            if not self.dataset:
                self.add_dataset()
        if obj in self.persons:
            self.persons.remove(obj)
            if not self.persons:
                self.add_person()
        if obj in self.organizations:
            self.organizations.remove(obj)
            if not self.organizations:
                self.add_organization()
        if obj in self.grants:
            self.grants.remove(obj)
            if not self.grants:
                self.add_grant()

    def get_status(self) -> str:
        """
        Get the status of the dataset.

        Indicates if the data is valid according to the SHACL ontology, and how many properties are missing.

        Returns:
            str: description of the dataset status.
        """
        try:
            g = self.graph
            if not g:
                raise Exception('no graph')
        except Exception:
            print('Warning: Could not load cached graph. Performance may be decreased')
            # LATER: remove with next breaking change
            g = self.generate_rdf_graph()
        try:
            val = self.validation_result
        except Exception:
            # LATER: remove with next breaking change
            print('Warning: no cached validation result available. Performance may be decreased.')
            val = self.validate_graph(g)[0]
        if val:
            overall = 'Valid'
        else:
            overall = 'Invalid'
        invalid = 0
        missing = 0
        optional = 0
        valid = 0
        for p in self.get_all_properties():
            v, _ = p.validate()
            if v == Validity.INVALID_VALUE:
                invalid += 1
            elif v == Validity.REQUIRED_VALUE_MISSING:
                missing += 1
            elif v == Validity.OPTIONAL_VALUE_MISSING:
                optional += 1
            elif v == Validity.VALID:
                valid += 1
            elif v == Validity.UNDEFINED:
                print("Warning: Unexpected Validity 'Undefined'.")
                return "Error during validation."
        return f"{overall}  --  {invalid + missing} Problems; {valid} Values"

    def get_turtle(self) -> str:
        """
        Get the turtle representation of the data.

        Returns:
            str: a turtle serialization of the data.
        """
        try:
            ttl = self.turtle
            if not isinstance(ttl, str):
                raise Exception('turtle was not a string')
            if ttl:
                return ttl
            else:
                raise Exception('no turtle found')
        except Exception as e:
            print('Warning: No turtle cached. Performance may be decreased.')
            print(f'    (Exception: {e})')
            # LATER: remove with next breaking change
            g = self.generate_rdf_graph()
            return g.serialize(format='turtle').decode("utf-8")


class DataClass(ABC):
    """
    Abstract parent class of all classes holding data.
    """

    def get_metadataset(self) -> MetaDataSet:
        """
        Returns the `MetaDataSet` to which this class belongs

        Returns:
            MetaDataSet: The owner MetaDataSet
        """
        return self.meta

    def add_rdf_to_graph(self, graph: Graph, typename: str):
        """
        Adds the RDF representation of this class to a graph

        Args:
            graph (Graph): the `rdflib.Graph` to which the triples should be added
            typename (str): the type name of this class
        """
        iri = self.get_rdf_iri()
        type = dsp_repo[typename]
        graph.add((iri, RDF.type, type))
        for prop in self.get_properties():
            graph += prop.get_triples(iri)

    def get_rdf_iri(self) -> URIRef:
        """
        Return the IRI of the object.

        This can be called to use the object as subject of an RDF triple.

        Returns:
            URIRef: the IRI
        """
        shortcode = self.get_metadataset().project.shortcode.value
        if not shortcode:
            shortcode = "xxxx"
        classname = 'dsp-' + shortcode + self.iri_suffix
        return URIRef(dsp_repo[classname])

    @abstractmethod
    def get_properties(self) -> list:
        """
        Return a list of all `Property` fields of this class
        """
        raise NotImplementedError

    def get_prop_by_name(self, name):
        for p in self.get_properties():
            if p.name == name:
                return p


class Project(DataClass):
    """
    Project shape.

    Corresponds to `dsp-repo:Project` in our ontology.

    Args:
        name (str): The name of the project
        shortcode (str): The project shortcode
        meta (MetaDataSet): the owning `MetaDataSet`
    """

    def __init__(self, name: str, shortcode: str, meta: MetaDataSet):
        self.meta = meta
        self.iri_suffix = "-project"
        self.name = Property(meta, "Name",
                             "The name of the Project",
                             "Test Project",
                             Datatype.STRING,
                             Cardinality.ONE,
                             name,
                             predicate=dsp_repo.hasName)

        msg = "This is a test project. All properties have been used to test these."
        msg += "\nYou will just describe your project briefly."
        self.description = Property(meta, "Description",
                                    "Description of the Project",
                                    msg,
                                    Datatype.STRING,
                                    Cardinality.ONE,
                                    predicate=dsp_repo.hasDescription,
                                    multiline=True)

        msg = "mathematics, science, history of science, history of mathematics."
        msg += "\nUse the plus sign to have a new field for each key word."
        self.keywords = Property(meta, "Keywords",
                                 "Keywords and tags",
                                 msg,
                                 Datatype.STRING,
                                 Cardinality.ONE_TO_UNBOUND,
                                 predicate=dsp_repo.hasKeywords)

        msg = "Discipline and research fields from UNESCO nomenclature: https://skos.um.es/unesco6/?l=en"
        msg += "\nor from http://www.snf.ch/SiteCollectionDocuments/allg_disziplinenliste.pdf"
        self.discipline = Property(meta, "Discipline",
                                   msg,
                                   "http://skos.um.es/unesco6/11",
                                   Datatype.STRING_OR_URL,
                                   Cardinality.ONE_TO_UNBOUND,
                                   predicate=dsp_repo.hasDiscipline)

        self.startDate = Property(meta, "Start Date",
                                  "The date when the project started, e. g. when funding was granted.",
                                  "2000-07-26T21:32:52",
                                  Datatype.DATE,
                                  Cardinality.ONE,
                                  predicate=dsp_repo.hasStartDate)

        msg = "The date when the project was finished, e. g. when the last changes to the project data where completed."
        self.endDate = Property(meta, "End Date",
                                msg,
                                "2000-07-26T21:32:52",
                                Datatype.DATE,
                                Cardinality.ZERO_OR_ONE,
                                predicate=dsp_repo.hasEndDate)

        self.temporalCoverage = Property(meta, "Temporal Coverage",
                                         "Temporal coverage of the project from http://perio.do/en/\nor https://chronontology.dainst.org/",
                                         "http://chronontology.dainst.org/period/Ef9SyESSafJ1",
                                         Datatype.STRING_OR_URL,
                                         Cardinality.ONE_TO_UNBOUND,
                                         predicate=dsp_repo.hasTemporalCoverage)

        self.spatialCoverage = Property(meta, "Spatial Coverage",
                                        "Spatial coverage of the project from Geonames URL: https://www.geonames.org/\nor from Pleiades URL: https://pleiades.stoa.org/places",
                                        "https://www.geonames.org/6255148/europe.html",
                                        Datatype.PLACE,
                                        Cardinality.ONE_TO_UNBOUND,
                                        predicate=dsp_repo.hasSpatialCoverage)

        self.funder = Property(meta, "Funder",
                               "Funding person or institution of the project",
                               "",
                               Datatype.PERSON_OR_ORGANIZATION,
                               Cardinality.ONE_TO_UNBOUND,
                               predicate=dsp_repo.hasFunder)

        self.grant = Property(meta, "Grant",
                              "Grant of the project",
                              "",
                              Datatype.GRANT,
                              predicate=dsp_repo.hasGrant)

        self.url = Property(meta, "URL",
                            "Landing page or Website of the project. We recommend DSP Landing Page.\nOptionally, a second URL can be added too.",
                            "https://test.dasch.swiss/",
                            Datatype.URL,
                            Cardinality.ONE_TO_TWO,
                            predicate=dsp_repo.hasURL)

        self.shortcode = Property(meta, "Shortcode",
                                  "Internal shortcode of the project",
                                  "0000",
                                  Datatype.SHORTCODE,
                                  Cardinality.ONE,
                                  value=shortcode,
                                  predicate=dsp_repo.hasShortcode)

        self.alternateName = Property(meta, "Alternate Name",
                                      "Alternative name of the project, e.g. in case of an overly long official name",
                                      "Another Title",
                                      Datatype.STRING,
                                      predicate=dsp_repo.hasAlternateName)

        self.dataManagementPlan = Property(meta, "Data Management Plan",
                                           "Data Management Plan of the project",
                                           "",
                                           Datatype.DATA_MANAGEMENT_PLAN,
                                           Cardinality.ZERO_OR_ONE,
                                           predicate=dsp_repo.hasDataManagementPlan)

        self.publication = Property(meta, "Publications",
                                    "Publications produced during the lifetime of the project",
                                    "Doe, J. (2000). A Publication.",
                                    Datatype.STRING,
                                    predicate=dsp_repo.hasPublication,
                                    multiline=True)

        self.contactPoint = Property(meta, "Contact Point",
                                     "Contact information",
                                     "",
                                     Datatype.PERSON_OR_ORGANIZATION,
                                     Cardinality.ZERO_OR_ONE,
                                     predicate=dsp_repo.hasContactPoint)

    def get_properties(self):
        # LATER: if Property is in another file and imported, this can be typed
        """
        Get all properties held by the object.

        Returns:
            List[Property]: A list with all the Properties held by the object.
        """
        return [
            self.name,
            self.shortcode,
            self.url,
            self.description,
            self.keywords,
            self.discipline,
            self.startDate,
            self.endDate,
            self.temporalCoverage,
            self.spatialCoverage,
            self.funder,
            self.grant,
            self.alternateName,
            self.dataManagementPlan,
            self.publication,
            self.contactPoint
        ]

    def __str__(self):
        return str(self.get_rdf_iri())


class Dataset(DataClass):
    """
    Dataset Shape.

    Corresponds to `dsp-repo:Dataset` in the ontology.
    """

    def __init__(self, name, project, meta):
        self.meta = meta
        self.iri_suffix = IRIFactory.get_unique_iri('dataset', meta)
        self.title = Property(meta, "Title",
                              "Title of the dataset",
                              "Dataset-Title",
                              Datatype.STRING,
                              Cardinality.ONE,
                              value=f"Dataset of {name}",
                              predicate=dsp_repo.hasTitle)

        self.alternativeTitle = Property(meta, "Alternative Title",
                                         "Alternative title of the dataset",
                                         "Another Dataset-Title",
                                         Datatype.STRING,
                                         Cardinality.ZERO_OR_ONE,
                                         predicate=dsp_repo.hasAlternativeTitle)

        self.abstract = Property(meta, "Abstract",
                                 "Description of the dataset",
                                 "This is merely an exemplary dataset",
                                 Datatype.STRING_OR_URL,
                                 Cardinality.ONE_TO_UNBOUND,
                                 predicate=dsp_repo.hasAbstract,
                                 multiline=True)

        self.sameAs = Property(meta, "Alternative URL",
                               "Alternative URL to the dataset, if applicable",
                               "https://test.dasch.swiss/",
                               Datatype.URL,
                               Cardinality.UNBOUND,
                               predicate=dsp_repo.sameAs)

        self.typeOfData = Property(meta, "Type of Data",
                                   "Type of data related to the dataset",
                                   "xml",
                                   Datatype.CONTROLLED_VOCABULARY,
                                   Cardinality.ONE_TO_UNBOUND,
                                   value_options=["XML", "Text",
                                                  "Image", "Movie", "Audio"],
                                   predicate=dsp_repo.hasTypeOfData)

        self.documentation = Property(meta, "Documentation",
                                      "Additional documentation",
                                      '"http://www.example.org/documentation.md" or "Work in Progress"',
                                      Datatype.STRING_OR_URL,
                                      Cardinality.UNBOUND,
                                      predicate=dsp_repo.hasDocumentation)

        self.license = Property(meta, "License",
                                "The license terms of the dataset",
                                "https://creativecommons.org/licenses/by/3.0",
                                Datatype.URL,
                                Cardinality.ONE_TO_UNBOUND,
                                predicate=dsp_repo.hasLicense)

        self.accessConditions = Property(meta, "Conditions of Access",
                                         "Access conditions of the data",
                                         "Open Access",
                                         Datatype.STRING,
                                         Cardinality.ONE,
                                         predicate=dsp_repo.hasConditionsOfAccess)

        self.howToCite = Property(meta, "How to Cite",
                                  "How to cite the data",
                                  "Test-project (test), 2002, https://test.dasch.swiss",
                                  Datatype.STRING,
                                  Cardinality.ONE,
                                  predicate=dsp_repo.hasHowToCite)

        self.status = Property(meta, "Dataset Status",
                               "Current status of a dataset",
                               "The dataset is work in progress",
                               Datatype.CONTROLLED_VOCABULARY,
                               Cardinality.ONE,
                               value_options=['In planning', 'Ongoing', 'On hold', 'Finished'],
                               predicate=dsp_repo.hasStatus)

        self.datePublished = Property(meta, "Date Published",
                                      "Date of publication",
                                      "2000-08-01",
                                      Datatype.DATE,
                                      Cardinality.ZERO_OR_ONE,
                                      predicate=dsp_repo.hasDatePublished)

        self.language = Property(meta, "Language",
                                 "Language(s) of the dataset",
                                 "English",
                                 Datatype.STRING,
                                 Cardinality.ONE_TO_UNBOUND,
                                 predicate=dsp_repo.hasLanguage)

        self.project = Property(meta, "is Part of",
                                "The project to which the data set belongs",
                                "",
                                Datatype.PROJECT,
                                Cardinality.ONE,
                                value=project,
                                predicate=dsp_repo.isPartOf)

        self.attribution = Property(meta, "Qualified Attribution",
                                    "Persons/Organization involved in the creation of the dataset",
                                    '<person> + "editor"',
                                    Datatype.ATTRIBUTION,
                                    Cardinality.ONE_TO_UNBOUND,
                                    predicate=dsp_repo.hasQualifiedAttribution)

        self.dateCreated = Property(meta, "Date Created",
                                    "Creation of the dataset",
                                    "2000-08-01",
                                    Datatype.DATE,
                                    Cardinality.ZERO_OR_ONE,
                                    predicate=dsp_repo.hasDateCreated)

        self.dateModified = Property(meta, "Date Modified",
                                     "Last modification of the dataset",
                                     "2000-08-01",
                                     Datatype.DATE,
                                     Cardinality.ZERO_OR_ONE,
                                     predicate=dsp_repo.hasDateModified)

        self.distribution = Property(meta, "Distribution",
                                     "A downloadable form of this dataset, at a specific location, in a specific format",
                                     "https://test.dasch.swiss",
                                     Datatype.DOWNLOAD,
                                     Cardinality.ZERO_OR_ONE,
                                     predicate=dsp_repo.hasDistribution)

    def get_properties(self):
        # LATER: if Property is in another file and imported, this can be typed
        """
        Get all properties held by the object.

        Returns:
            List[Property]: A list with all the Properties held by the object.
        """
        return [
            self.project,
            self.title,
            self.abstract,
            self.language,
            self.typeOfData,
            self.attribution,
            self.license,
            self.howToCite,
            self.accessConditions,
            self.status,
            self.sameAs,
            self.alternativeTitle,
            self.documentation,
            self.datePublished,
            self.dateCreated,
            self.dateModified,
            self.distribution,
        ]

    def __str__(self):
        classname = str(self.get_rdf_iri()).split('#')[1]
        n1 = "<title missing>"
        if self.title.value:
            n1 = self.title.value
        return f"{classname}: {n1}"


class Person(DataClass):
    """
    Person Shape.

    Corresponds to `dsp-repo:Person` in the ontology.
    """

    def __init__(self, meta):
        self.meta = meta
        self.iri_suffix = IRIFactory.get_unique_iri('person', meta)
        self.sameAs = Property(meta, "Alternative URL",
                               "Alternative URL, pointing to an authority file (ORCID, VIAF, GND, ...)",
                               "https://orcid.org/000-000-000-000",
                               Datatype.URL,
                               Cardinality.UNBOUND,
                               predicate=dsp_repo.sameAs)

        self.givenName = Property(meta, "Given Name",
                                  "Given name of the person",
                                  "John",
                                  Datatype.STRING,
                                  Cardinality.ONE_TO_UNBOUND_ORDERED,
                                  predicate=dsp_repo.hasGivenName)

        self.familyName = Property(meta, "Family Name",
                                   "Family name of the person. (Note that you can separate multiple family names with ';' if need be)",
                                   "Doe",
                                   Datatype.STRING,
                                   Cardinality.ONE,
                                   predicate=dsp_repo.hasFamilyName)

        self.email = Property(meta, "E-mail",
                              "E-mail address of the person",
                              "john.doe@dasch.swiss",
                              Datatype.EMAIL,
                              Cardinality.ZERO_TO_TWO,
                              predicate=dsp_repo.hasEmail)

        self.address = Property(meta, "Address",
                                "Postal address of the person",
                                "",
                                Datatype.ADDRESS,
                                Cardinality.UNBOUND,
                                predicate=dsp_repo.hasAddress)

        self.memberOf = Property(meta, "Member of",
                                 "Affiliation of the person",
                                 "",
                                 Datatype.ORGANIZATION,
                                 Cardinality.ONE_TO_UNBOUND,
                                 predicate=dsp_repo.isMemberOf)

        self.jobTitle = Property(meta, "Job Title",
                                 "Position/Job title of the person",
                                 "Dr.",
                                 Datatype.STRING,
                                 Cardinality.ONE_TO_UNBOUND,
                                 predicate=dsp_repo.hasJobTitle)

    def get_properties(self):
        # LATER: if Property is in another file and imported, this can be typed
        """
        Get all properties held by the object.

        Returns:
            List[Property]: A list with all the Properties held by the object.
        """
        return [
            self.familyName,
            self.givenName,
            self.memberOf,
            self.jobTitle,
            self.email,
            self.sameAs,
            self.address,
        ]

    def __str__(self):
        classname = str(self.get_rdf_iri()).split('#')[1]
        # classname = str(self.get_rdf_iri())
        n1 = "<first name missing>"
        if self.givenName.value:
            n1 = " ".join(self.givenName.value)
        n2 = "<family name missing>"
        if self.familyName.value:
            n2 = self.familyName.value
        return f"{classname}: {n1} {n2}"


class Organization(DataClass):
    """
    Organization Shape.

    Corresponds to `dsp-repo:Organization` in the ontology.
    """

    def __init__(self, meta):
        self.meta = meta
        self.iri_suffix = IRIFactory.get_unique_iri('organization', meta)

        self.name = Property(meta, "Legal Name",
                             "Legal name of the organization",
                             "DaSCH",
                             Datatype.STRING,
                             Cardinality.ONE_TO_UNBOUND,
                             predicate=dsp_repo.hasName)

        self.email = Property(meta, "E-mail",
                              "E-mail address of the organization",
                              "info@dasch.swiss",
                              Datatype.EMAIL,
                              Cardinality.ZERO_OR_ONE,
                              predicate=dsp_repo.hasEmail)

        self.address = Property(meta, "Address",
                                "Postal address of the organization",
                                "",
                                Datatype.ADDRESS,
                                Cardinality.UNBOUND,
                                predicate=dsp_repo.hasAddress)

        self.url = Property(meta, "URL",
                            "URL of the organization",
                            "https://dasch.swiss",
                            Datatype.URL,
                            Cardinality.ZERO_OR_ONE,
                            predicate=dsp_repo.hasURL)

    def get_properties(self):
        # LATER: if Property is in another file and imported, this can be typed
        """
        Get all properties held by the object.

        Returns:
            List[Property]: A list with all the Properties held by the object.
        """
        return [
            self.name,
            self.email,
            self.url,
            self.address,
        ]

    def __str__(self):
        classname = str(self.get_rdf_iri()).split('#')[1]
        n1 = "<name missing>"
        if self.name.value:
            n1 = " / ".join(self.name.value)
        return f"{classname}: {n1}"


class Grant(DataClass):
    """
    Grant Shape.

    Corresponds to `dsp-repo:Grant` in the ontology.
    """

    def __init__(self, meta):
        self.meta = meta
        self.iri_suffix = IRIFactory.get_unique_iri('grant', meta)

        self.name = Property(meta, "Name",
                             "Name of the grant",
                             "Ambizione",
                             Datatype.STRING,
                             Cardinality.ZERO_OR_ONE,
                             predicate=dsp_repo.hasName)

        self.url = Property(meta, "URL",
                            "URL of the grant",
                            "https://www.snf.ch/grants/001",
                            Datatype.URL,
                            Cardinality.ZERO_OR_ONE,
                            predicate=dsp_repo.hasURL)

        self.number = Property(meta, "Number",
                               "The number of the grant.",
                               "00012345",
                               Datatype.STRING,
                               Cardinality.ZERO_OR_ONE,
                               predicate=dsp_repo.hasNumber)

        self.funder = Property(meta, "Funder",
                               "Funding person or institution of the project",
                               "",
                               Datatype.PERSON_OR_ORGANIZATION,
                               Cardinality.ONE_TO_UNBOUND,
                               predicate=dsp_repo.hasFunder)

    def get_properties(self):
        # LATER: if Property is in another file and imported, this can be typed
        """
        Get all properties held by the object.

        Returns:
            List[Property]: A list with all the Properties held by the object.
        """
        return [
            self.funder,
            self.name,
            self.number,
            self.url,
        ]

    def __str__(self):
        classname = str(self.get_rdf_iri()).split('#')[1]
        n1 = "<funder missing>"
        v = self.funder.value
        if v:
            if isinstance(v, list):
                v = v[0]
            n1 = str(v)
        return f"{classname}: [{n1}]"


class Property():
    """
    General representation of a property.

    Corresponds to `sh:property`
    """

    def __init__(self, meta: MetaDataSet, name: str, description: str, example: str, datatype: Datatype.STRING,
                 cardinality=Cardinality.UNBOUND, value=None, value_options=None,
                 predicate=dsp_repo.whatever, multiline=False):
        self.meta = meta
        self.name = name
        self.description = description
        self.example = example
        self.datatype = datatype
        self.cardinality = cardinality
        self.value = value
        self.value_options = value_options
        self.predicate = predicate
        self.multiline = multiline

    def get_url_property_id(self, url: str) -> str:
        """
        This method tries to guess the propetyID for a URL.

        For certain pre-defined cases, a reasonable propertyID is chosen;
        otherwise, the net location is being extracted, if possible.

        Args:
            url (str): a URL

        Returns:
            str: a propertyID
        """
        # LATER: remove this method with next breaking change, and leave it to the utils entirely
        return utils.get_url_property_id(url)

    def get_triples(self, subject: URIRef) -> Graph:
        """
        Returns a Graph containing the triples that represent this property, in respect to a given subject.

        Args:
            subject (URIRef): the subject to which the property is object

        Returns:
            Graph: a graph containing one or multiple triples that represent the property
        """
        g = Graph()
        # Ensure the data can be looped
        vals = self.value
        if not isinstance(vals, list):
            vals = [vals]
        if self.datatype == Datatype.STRING and \
                self.cardinality == Cardinality.ONE_TO_UNBOUND_ORDERED and \
                vals and vals[0]:
            vals = [';'.join(vals)]
        for v in vals:
            if not v:
                continue
            if isinstance(v, str) and v.isspace():
                continue
            # resolve datatype ambiguity
            datatype = self.datatype
            if datatype == Datatype.STRING_OR_URL:
                if v and validators.url(str(v)):
                    datatype = Datatype.URL
                elif v and v.startswith('www.'):
                    v = "http://" + v
                    datatype = Datatype.URL
                else:
                    datatype = Datatype.STRING
            if datatype == Datatype.PERSON_OR_ORGANIZATION:
                if isinstance(v, Person):
                    datatype = Datatype.PERSON
                else:
                    datatype = Datatype.ORGANIZATION
            # Handle datatypes
            if datatype == Datatype.STRING \
                    or datatype == Datatype.CONTROLLED_VOCABULARY \
                    or datatype == Datatype.SHORTCODE:
                g.add((subject, self.predicate, Literal(v, datatype=XSD.string)))
            elif datatype == Datatype.DATE:
                g.add((subject, self.predicate, Literal(v, datatype=XSD.date)))
            elif datatype == Datatype.URL:
                blank = BNode()
                g.add((subject, self.predicate, blank))
                g.add((blank, RDF.type, SDO.URL))
                b2 = BNode()
                g.add((blank, SDO.propertyID, b2))
                g.add((b2, RDF.type, SDO.PropertyValue))
                g.add((b2, SDO.propertyID, Literal(utils.get_url_property_id(url=v))))
                g.add((blank, SDO.url, Literal(v)))
            elif datatype == Datatype.PLACE:
                b0 = BNode()
                g.add((subject, self.predicate, b0))
                g.add((b0, RDF.type, SDO.Place))
                b1 = BNode()
                g.add((b0, SDO.url, b1))
                g.add((b1, RDF.type, SDO.URL))
                g.add((b1, SDO.url, Literal(v)))
                b2 = BNode()
                g.add((b1, SDO.propertyID, b2))
                g.add((b2, RDF.type, SDO.PropertyValue))
                g.add((b2, SDO.propertyID, Literal(utils.get_url_property_id(v), datatype=XSD.string)))
            elif datatype == Datatype.PERSON:
                g.add((subject, self.predicate, v.get_rdf_iri()))
            elif datatype == Datatype.ORGANIZATION:
                g.add((subject, self.predicate, v.get_rdf_iri()))
            elif datatype == Datatype.PROJECT:
                g.add((subject, self.predicate, v.get_rdf_iri()))
            elif datatype == Datatype.DATA_MANAGEMENT_PLAN:
                if v[0] or v[1]:
                    try:
                        dmp = URIRef(dsp_repo[f'dsp-{self.meta.shortcode}-dmp'])
                    except Exception as e:
                        print(f'Warning: DMP has non-unique IRI ({e})')
                        # LATER: this should not be necessary anymore. remove with next breaking changes
                        dmp = URIRef(dsp_repo['dmp'])
                    g.add((subject, self.predicate, dmp))
                    g.add((dmp, RDF.type, dsp_repo.DataManagementPlan))
                    if v[0]:
                        g.add((dmp, dsp_repo.isAvailable, Literal(
                            v[0], datatype=XSD.boolean)))
                    if v[1]:
                        b1 = BNode()
                        g.add((dmp, dsp_repo.hasURL, b1))
                        g.add((b1, RDF.type, SDO.URL))
                        g.add((b1, SDO.url, Literal(v[1])))
            elif datatype == Datatype.ADDRESS:
                if not v[0] and not v[1] and not v[2]:
                    return g
                b0 = BNode()
                g.add((subject, self.predicate, b0))
                g.add((b0, RDF.type, SDO.PostalAddress))
                g.add((b0, SDO.streetAddress, Literal(
                    v[0], datatype=XSD.string)))
                g.add((b0, SDO.postalCode, Literal(v[1], datatype=XSD.string)))
                g.add((b0, SDO.addressLocality, Literal(
                    v[2], datatype=XSD.string)))
            elif datatype == Datatype.GRANT:
                g.add((subject, self.predicate, v.get_rdf_iri()))
            elif datatype == Datatype.ATTRIBUTION:
                b0 = BNode()
                g.add((subject, self.predicate, b0))
                g.add((b0, RDF.type, prov.Attribution))
                g.add((b0, dsp_repo.hasRole, Literal(v[0], datatype=XSD.string)))
                g.add((b0, prov.agent, v[1].get_rdf_iri()))
            elif datatype == Datatype.DOWNLOAD:
                b0 = BNode()
                g.add((subject, self.predicate, b0))
                g.add((b0, RDF.type, SDO.DataDownload))
                g.add((b0, SDO.url, Literal(v)))
            elif datatype == Datatype.EMAIL:
                if isinstance(v, tuple):
                    if v and v[0]:
                        g.add((subject, self.predicate, Literal(v[0])))
                    if v and v[1]:
                        g.add((subject, self.predicate, Literal(v[1])))
                else:
                    if v and not v.isspace():
                        g.add((subject, self.predicate, Literal(v)))
            else:
                print(f"{datatype}: {v}\n-> don't know how to serialize this.\n")
        return g

    def validate(self) -> Tuple[Validity, str]:
        """
        Validates the current value of the property.

        Returns:
            Tuple[Validity, str]: Returns a tuple: First element is a value of the `Validity` enum,
                                  the second one is a human readable validation result.
        """
        datatype = self.datatype
        cardinality = self.cardinality
        value = self.value

        missing = "Required value is missing."
        valid = "The current value is valid."
        optional = "This field is optional"
        no_url = "Invalid URL"
        no_mail = "Invalid e-mail address"

        if not value:
            if Cardinality.isMandatory(cardinality):
                return Validity.REQUIRED_VALUE_MISSING, missing
            else:
                return Validity.OPTIONAL_VALUE_MISSING, valid

        if datatype == Datatype.STRING or \
                datatype == Datatype.STRING_OR_URL or \
                datatype == Datatype.DOWNLOAD:
            if cardinality == Cardinality.ONE:
                if value and not value.isspace():
                    return Validity.VALID, valid
                else:
                    return Validity.REQUIRED_VALUE_MISSING, missing
            elif cardinality == Cardinality.ONE_TO_TWO:
                if value[0] and not value[0].isspace():
                    return Validity.VALID, valid
                else:
                    return Validity.REQUIRED_VALUE_MISSING, missing
            elif cardinality == Cardinality.ZERO_OR_ONE:
                if value and not value.isspace():
                    return Validity.VALID, valid
                else:
                    return Validity.OPTIONAL_VALUE_MISSING, optional
            elif cardinality == Cardinality.ONE_TO_UNBOUND or \
                    cardinality == Cardinality.ONE_TO_UNBOUND_ORDERED:
                if len(value) > 0 and value[0] and not value[0].isspace():
                    return Validity.VALID, valid
                else:
                    return Validity.REQUIRED_VALUE_MISSING, missing
            elif cardinality == Cardinality.UNBOUND:
                if len(value) > 0 and value[0] and not value[0].isspace():
                    return Validity.VALID, valid
                else:
                    return Validity.OPTIONAL_VALUE_MISSING, optional

        elif datatype == Datatype.SHORTCODE:
            if re.match('[a-zA-Z0-9]{4}$', value):
                return Validity.VALID, valid
            else:
                return Validity.INVALID_VALUE, "Shortcode must be exactly 4 alphanumeric characters."

        elif datatype == Datatype.URL or \
                datatype == Datatype.PLACE:
            if cardinality == Cardinality.UNBOUND:
                if len(value) > 0 and value[0] and not value[0].isspace():
                    if utils.areURLs(value):
                        return Validity.VALID, valid
                    else:
                        return Validity.INVALID_VALUE, no_url
                else:
                    return Validity.OPTIONAL_VALUE_MISSING, optional
            elif cardinality == Cardinality.ZERO_OR_ONE:
                if value and not value.isspace():
                    if utils.isURL(value):
                        return Validity.VALID, valid
                    else:
                        return Validity.INVALID_VALUE, no_url
                else:
                    return Validity.OPTIONAL_VALUE_MISSING, optional
            elif cardinality == Cardinality.ONE_TO_TWO or \
                    cardinality == Cardinality.ONE_TO_UNBOUND:
                if value[0] and not value[0].isspace():
                    if utils.areURLs(value):
                        return Validity.VALID, valid
                    else:
                        return Validity.INVALID_VALUE, no_url
                else:
                    return Validity.REQUIRED_VALUE_MISSING, missing

        elif datatype == Datatype.EMAIL:
            if cardinality == Cardinality.ZERO_OR_ONE:
                if value and not value.isspace():
                    if utils.is_email(value):
                        return Validity.VALID, valid
                    else:
                        return Validity.INVALID_VALUE, no_mail
                else:
                    return Validity.OPTIONAL_VALUE_MISSING, optional
            elif cardinality == Cardinality.ZERO_TO_TWO:
                if value[0] and not value[0].isspace():
                    if utils.are_emails(value):
                        return Validity.VALID, valid
                    else:
                        return Validity.INVALID_VALUE, no_mail
                else:
                    return Validity.OPTIONAL_VALUE_MISSING, optional

        elif datatype == Datatype.GRANT or \
                datatype == Datatype.PROJECT or \
                datatype == Datatype.PERSON or \
                datatype == Datatype.ORGANIZATION or \
                datatype == Datatype.PERSON_OR_ORGANIZATION:
            if cardinality == Cardinality.UNBOUND:
                if len(value) > 0 and value[0]:
                    return Validity.VALID, valid
                else:
                    return Validity.OPTIONAL_VALUE_MISSING, optional
            if cardinality == Cardinality.ONE_TO_UNBOUND:
                if len(value) > 0 and value[0]:
                    return Validity.VALID, valid
                else:
                    return Validity.REQUIRED_VALUE_MISSING, missing
            if cardinality == Cardinality.ONE:
                if value:
                    return Validity.VALID, valid
                else:
                    return Validity.REQUIRED_VALUE_MISSING, missing
            if cardinality == Cardinality.ZERO_OR_ONE:
                if value:
                    return Validity.VALID, valid
                else:
                    return Validity.OPTIONAL_VALUE_MISSING, optional

        elif datatype == Datatype.DATE:
            if not value or value.isspace():
                if cardinality == Cardinality.ONE:
                    return Validity.REQUIRED_VALUE_MISSING, missing
                elif cardinality == Cardinality.ZERO_OR_ONE:
                    return Validity.OPTIONAL_VALUE_MISSING, optional
            elif value and re.match(r'\d{4}-\d{2}-\d{2}$', value):
                return Validity.VALID, valid
            else:
                return Validity.INVALID_VALUE, "Not a valid date."

        elif datatype == Datatype.ADDRESS:
            if cardinality == Cardinality.UNBOUND:
                if value[0] and not value[0].isspace() and \
                        value[1] and not value[1].isspace() and \
                        value[2] and not value[2].isspace():
                    return Validity.VALID, valid
                elif (not value[0] or value[0].isspace()) and \
                        (not value[1] or value[1].isspace()) and \
                        (not value[2] or value[2].isspace()):
                    return Validity.OPTIONAL_VALUE_MISSING, optional
                else:
                    return Validity.INVALID_VALUE, "Not a valid address."

        elif datatype == Datatype.CONTROLLED_VOCABULARY:
            if cardinality == Cardinality.ONE_TO_UNBOUND:
                for v in value:
                    if v not in self.value_options:
                        return Validity.INVALID_VALUE, f"Value '{v}' not allowed."
                return Validity.VALID, valid
            elif cardinality == Cardinality.ONE:
                if value not in self.value_options:
                    return Validity.INVALID_VALUE, f"Value '{value}' not allowed."
                return Validity.VALID, valid

        elif datatype == Datatype.ATTRIBUTION:
            if cardinality == Cardinality.ONE_TO_UNBOUND:
                for v in value:
                    if (not v[0] or v[0].isspace()) or \
                            (not v[1] or not isinstance(v[1], (Person, Organization))):
                        return Validity.INVALID_VALUE, "Not a valid address."
                return Validity.VALID, valid

        elif datatype == Datatype.DATA_MANAGEMENT_PLAN:
            if cardinality == Cardinality.ZERO_OR_ONE:
                if value[0] or (value[1] and not value[1].isspace()):
                    return Validity.VALID, valid
                else:
                    return Validity.OPTIONAL_VALUE_MISSING, optional

        print(f'Warning: Behavior undefined!\ncard: {cardinality}\ntype: {datatype}\n')
        return Validity.UNDEFINED, ""

    def __str__(self):
        if self.value:
            return str(self.value)
        return f"<Property '{self.name}' undefined>"
