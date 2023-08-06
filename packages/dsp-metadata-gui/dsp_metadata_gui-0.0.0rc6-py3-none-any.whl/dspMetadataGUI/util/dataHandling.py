"""
This module holds data handling capabilities for metadatasets.

Concretely, the UI has a globally accessible data handler of type `DataHandling` that will take care of the datasets held by the GUI.
"""

import os
import pickle
import shutil
from typing import List

from rdflib.graph import Graph

from .metaDataSet import MetaDataSet
from .utils import open_file


class DataHandling:
    """ This class handles data.

    It checks for availability in the filesystem, and
    if not, creates the data structure. It also takes care for the storage on disk.
    The data are stored as a pickle file.

    The class should not be called as a static.
    Rather, there should at any given time be an instance of this class (`data_handler`) be available.
    All calls should be done on this instance, as it holds the actual data representation.
    """

    def __init__(self):
        self.current_window = None
        self.projects: List[MetaDataSet] = []
        self.tabs = []
        self.data_storage = os.path.expanduser("~") + "/DaSCH/config/repos.data"
        # LATER: path could be made customizable
        self.load_data()

    def add_project(self, folder_path: str, shortcode: str, files: list):
        """
        Add a new project.

        This project adds a new project folder to the collection after the user specified the folder.

        The Project is appended at the end of the list.

        Args:
            folder_path (str): path to the project folder
            shortcode (str): the project shortcode
            files (list): the files in the project folder
        """
        folder_name = os.path.basename(folder_path)
        dataset = MetaDataSet(folder_name, folder_path, shortcode)
        self.projects.append(dataset)
        dataset.files += files
        self.save_data()

    def remove_project(self, project: MetaDataSet):
        """
        Removes a specific project.

        Args:
            project (MetaDataSet): The project to remove.
        """
        if project and project in self.projects:
            self.projects.remove(project)
            self.save_data()

    def load_data(self):
        """
        Load data from previous runtimes (if any).

        Currently, this checks `~/DaSCH/config/repos.data`.
        """
        if not os.path.exists(self.data_storage):
            os.makedirs(os.path.dirname(self.data_storage), exist_ok=True)
            return
        with open(self.data_storage, 'rb') as file:
            self.projects = pickle.load(file)

    def save_data(self, dataset: MetaDataSet = None):
        """
        Save data to disc.

        Currently, the data are stored under `~/DaSCH/config/repos.data`.

        Args:
            dataset (MetaDataSet, optional): A `Metadataset` to serialize before saving. Defaults to None.
        """
        # LATER: could let the user decide where to store the data.
        # LATER: export metadata here, once export logic is improved
        if dataset:
            dataset.generate_rdf_graph()
        with open(self.data_storage, 'wb') as file:
            pickle.dump(self.projects, file)

    def validate_and_export_data(self, index: int) -> tuple:
        """
        Validate a given project and export its RDF data.

        Args:
            index (int): The index of the `MetaDataSet` to export.

        Returns:
            tuple: The result of the validation (see `MetaDataSet.validate_graph()`).
        """
        project = self.projects[index]
        validation_result = self.validate_graph(project)
        try:
            graph = project.generate_rdf_graph()
            if not graph:
                raise Exception('No Graph')
        except Exception:
            print('Warning: could not load graph from cache. Performance may be decreased.')
            # LATER: remove with next breaking change
            graph = project.graph
        self.export_rdf(project.path, graph)
        return validation_result

    def import_project(self, path: str):
        """
        Import a single MetaDataSet from a pickle.

        Args:
            path (str): path to the pickle to import.
        """
        try:
            with open(path, 'rb') as f:
                dataset = pickle.load(f)
                self.projects.append(dataset)
        except Exception:
            import traceback
            traceback.print_exc()
            print(f'\n\n--------\n\nCould not import file: {path}')

    def export_rdf(self, path: str, graph: Graph, show: bool = True):
        """
        Export RDF serializations to local files.

        Args:
            path (str): The path where to store the files.
            graph (Graph): The RDF graph of the data.
            show (bool, optional): Flag true, if the folder should be opened after saving the files. Defaults to True.
        """
        path += '/metadata'
        if not os.path.exists(path):
            os.makedirs(path)
        p = path + '/metadata.ttl'
        with open(p, 'w') as f:
            s = graph.serialize(format='turtle').decode("utf-8")
            f.write(s)
        p = path + '/metadata.json'
        with open(p, 'w') as f:
            s = graph.serialize(format='json-ld').decode("utf-8")
            f.write(s)
        p = path + '/metadata.xml'
        with open(p, 'w') as f:
            s = graph.serialize(format='xml').decode("utf-8")
            f.write(s)
        if show:
            open_file(path)

    def zip_and_export(self, dataset: MetaDataSet, target: str):
        """
        Zips all data of a project and saves it to a file.

        The ZIP archive will contain a pickle of the data, all associated files and RDF serializations of the data.

        Args:
            dataset (MetaDataSet): The dataset to export.
            target (str): The path where to store the export.
        """
        if not dataset:
            return
        if not target:
            target = dataset.path
        target_file = os.path.join(target, dataset.name)
        try:
            graph = dataset.generate_rdf_graph()
            if not graph:
                raise Exception('No Graph')
        except Exception:
            print('Warning: could not load graph from cache. Performance may be decreased.')
            # LATER: remove with next breaking change
            graph = dataset.graph
        self.export_rdf(dataset.path, graph)
        p = dataset.path
        tmp = os.path.join(p, '.tmp')
        meta = os.path.join(p, 'metadata')
        os.makedirs(tmp, exist_ok=True)
        tmp_m = os.path.join(tmp, 'metadata')
        os.makedirs(tmp_m, exist_ok=True)
        pickle_path = os.path.join(tmp, 'binary')
        os.makedirs(pickle_path, exist_ok=True)
        for f in dataset.files:
            shutil.copy(os.path.join(p, f), tmp)
        shutil.copytree(meta, tmp_m, dirs_exist_ok=True)
        shortcode = dataset.shortcode
        with open(os.path.join(pickle_path, f'project_{shortcode}.data'), mode='wb') as pick:
            pickle.dump(dataset, pick)
        shutil.make_archive(target_file, 'zip', tmp)
        shutil.rmtree(tmp, ignore_errors=True)
        open_file(target)

    def validate_graph(self, dataset: MetaDataSet) -> tuple:
        """
        Validates all properties in a specific `MetaDataSet.`

        Does not validate each of the properties separately,
        but rather generates the RDF graph, which then gets validated.

        Args:
            dataset (MetaDataSet): The dataset to validate.

        Returns:
            tuple: Validation result (see `MetaDataSet.validate_graph()`).
        """
        try:
            graph = dataset.generate_rdf_graph()
            if not graph:
                raise Exception('No Graph')
        except Exception:
            print('Warning: could not load graph from cache. Performance may be decreased.')
            # LATER: remove with next breaking change
            graph = dataset.graph
        return dataset.validate_graph(graph)

    def update_all(self):
        """
        Update data according to the values currently in the GUI.

        Calling this function iterates over each Property in the dataset
        and updates it with the value found in its corresponding GUI component.
        """
        for tab in self.tabs:
            tab.update_data()
        self.refresh_ui()

    def refresh_ui(self):
        """
        Refresh all values in the UI according to the saved values.

        This method also invokes on-the-fly validation.
        Note: Calling this method discards all changes that have not been updated in the metaDataSet.
        """
        for tab in self.tabs:
            tab.refresh_ui()

    def get_project_by_shortcode(self, shortcode: str) -> MetaDataSet:
        """
        Get the project with a specific shortcode.

        Args:
            shortcode (str): The shortcode of the project to be found.

        Returns:
            MetaDataSet: The Project with said shortcode.
        """
        for p in self.projects:
            if p.shortcode == shortcode:
                return p
