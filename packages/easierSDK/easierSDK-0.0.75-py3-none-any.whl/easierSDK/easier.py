#   Copyright  2020 Atos Spain SA. All rights reserved.
 
#   This file is part of EASIER AI.
 
#   EASIER AI is free software: you can redistribute it and/or modify it under the terms of Apache License, either version 2 of the License, or
#   (at your option) any later version.
 
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT ANY WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING 
#   BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT,
#   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#   WHETHER IN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
#   OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#   See  LICENSE file for full license information  in the project root.

import minio
from minio import Minio
import os
import json
import certifi
import urllib3

from easierSDK import modelsAPI, datasetsAPI
from easierSDK.classes.categories import Categories
from easierSDK.classes.repository_metadata import RepositoryMetadata
from easierSDK.classes.model_metadata import ModelMetadata
from easierSDK.classes.dataset_metadata import DatasetMetadata
from easierSDK.classes.category_metadata import CategoryMetadata

from easierSDK.serving import servingAPI

class EasierSDK():
    """Higher level class to interact with the EASIER platform.
    """

    _MODELS = 'models'
    _DATASETS = 'datasets'
    
    def __init__(self, easier_user:str, easier_password:str, easier_url:str="minio.easier-ai.eu", secure=True, region='es'):
        """Initializer for the class.

        Args:
            easier_url (str): URL to an EASIER MINIO deployment.
            easier_user (str): Username.
            easier_password (str): Password.
        """
        self.my_easier_user = easier_user

        # Load CA certificates from SSL_CERT_FILE file if set
        ca_certs = os.environ.get('SSL_CERT_FILE') or certifi.where()
        _http = urllib3.PoolManager(
            timeout=1,
            maxsize=minio.helpers.MAX_POOL_SIZE,
            cert_reqs='CERT_REQUIRED',
            ca_certs=ca_certs,
            retries=urllib3.Retry(
                total=3,
                backoff_factor=0.2,
                status_forcelist=[500, 502, 503, 504]
            )
        )

        self.minio_client = Minio(easier_url, access_key=easier_user, secret_key=easier_password, secure=secure, region=region, http_client=_http)
        
        # Test Connection
        try:
            self.minio_client.list_buckets()
        except Exception as e:
            raise Exception("ERROR when connecting to EASIER Repositories. Check input parameters.")

        # IF test is ok, then we reinit with default parameters of the http lib
        _http = urllib3.PoolManager(
            timeout=urllib3.Timeout.DEFAULT_TIMEOUT,
            maxsize=minio.helpers.MAX_POOL_SIZE,
            cert_reqs='CERT_REQUIRED',
            ca_certs=ca_certs,
            retries=urllib3.Retry(
                total=5,
                backoff_factor=0.2,
                status_forcelist=[500, 502, 503, 504]
            )
        )

        self.minio_client = Minio(easier_url, access_key=easier_user, secret_key=easier_password, secure=secure, region=region, http_client=_http)
        
        self.my_public_repo = easier_user + '-public'
        self.my_private_repo = easier_user + '-private' 

        self.models = modelsAPI.ModelsAPI(self.minio_client, self.my_public_repo, self.my_private_repo)
        self.datasets = datasetsAPI.DatasetsAPI(self.minio_client, self.my_public_repo, self.my_private_repo)

        self.serving = servingAPI.ServingAPI(easier_user, easier_password,  self.minio_client, 
                self.my_public_repo, self.my_private_repo)

    def get_repositories_metadata(self, category:Categories=None):
        
        if isinstance(category, str):
           category = Categories[category.upper()]

        if category is None:
            categories = [cat for cat in Categories]
        else:
            categories = [category]
        
        repositories = {}
        repo_list = self.minio_client.list_buckets()
        
        for repo in repo_list:
            cat_dict = {}
            for cat in categories: 
                num_models, models_list = self._count_repo_models(repo.name, cat)
                cat_models = {}
                for model_path in models_list:
                    minio_path = model_path + '/' + 'metadata.json'
                    filename = minio_path.split('/')[1:]
                    filename = '/'.join(filename)
                    local_file = '/tmp/metadata.json'
                    try:
                        self.minio_client.fget_object(repo.name, filename, local_file)
                    except minio.error.NoSuchKey as ex:
                        continue
                    
                    with open(local_file, 'r') as f:
                        model_metadata = ModelMetadata(json.load(f))
                    if os.path.exists(local_file):
                        os.remove(local_file)
                    
                    _, model_metadata.experimentIDs = self.models._count_model_experiments(repo.name, cat.value, model_metadata.name)
                    cat_models[model_metadata.name] = model_metadata

                num_datasets, datasets_list = self._count_repo_datasets(repo.name, cat)
                cat_datasets = {}
                for dataset_path in datasets_list:
                    minio_path = dataset_path + '/' + 'metadata.json'
                    filename = minio_path.split('/')[1:]
                    filename = '/'.join(filename)
                    local_file = '/tmp/metadata.json'
                    try:
                        self.minio_client.fget_object(repo.name, filename, local_file)
                    except minio.error.NoSuchKey as ex:
                        continue
                    
                    with open(local_file, 'r') as f:
                        dataset_metadata = DatasetMetadata(json.load(f))
                    if os.path.exists(local_file):
                        os.remove(local_file)

                    cat_datasets[dataset_metadata.name] = dataset_metadata

                cat_metadata = CategoryMetadata(cat.value, cat_models, num_models, cat_datasets, num_datasets)
                cat_dict[cat.value] = cat_metadata

            repo_metadata = RepositoryMetadata(repo.name, cat_dict)
            repositories[repo.name] = repo_metadata

        return repositories

    def _count_repo_models(self, repo_name:str, category_name:str=None) -> (int, list):
        """Count number of models under a repository.

        Args:
            repo_name (str): Repository to count models from.
            category_name (str): Category to count models from.

        Returns:
            int: Number of models under the repository.
            list: List of models in the repository.
        """
        
        num_models = 0
        models_list = []
        
        if category_name:
            if isinstance(category_name, str):
                category_name = Categories[category_name.upper()]
            categories = [category_name]
        else:
            categories = [cat for cat in Categories]

        for category in categories:
            for obs in self.minio_client.list_objects(repo_name, prefix=self._MODELS + '/' + category.value, recursive=True):
                experiment_model = obs.object_name.split('/')[0:3]
                experiment_model = repo_name + '/' + '/'.join(experiment_model)
                if experiment_model not in models_list:
                    num_models += 1
                    models_list.append(experiment_model)
        return num_models, models_list

    def _count_repo_datasets(self, repo_name:str, category_name:str=None) -> (int, list):
        """Count number of datasets under a repository.

        Args:
            repo_name (str): Repository to count datasets from.
            category_name (str): Category to count models from.

        Returns:
            int: Number of datasets under the repository.
            list: List of datasets in the repository.
        """
        num_datasets = 0
        datasets_list = []

        if category_name:
            if isinstance(category_name, str):
                category_name = Categories[category_name.upper()]
            categories = [category_name]
        else:
            categories = [cat for cat in Categories]

        for category in categories:
            for obs in self.minio_client.list_objects(repo_name, prefix=self._DATASETS + '/' + category.value, recursive=True):
                experiment_dataset = obs.object_name.split('/')[0:3]
                experiment_dataset = repo_name + '/' + '/'.join(experiment_dataset)
                if experiment_dataset not in datasets_list:
                    num_datasets += 1
                    datasets_list.append(experiment_dataset)
        return num_datasets, datasets_list
        
    def _count_category_models(self, category:Categories) -> (int, list):
        """Count all available models under a specific category.

        Args:
            category (Categories): Category to which count the models from.

        Returns:
            int: number of models under the category
            list: list of models under the category
        """
        if isinstance(category, str):
           category = Categories[category.upper()]

        num_models = 0
        models_list = []
        repo_list = self.minio_client.list_buckets()
        for repo in repo_list:
            for obs in self.minio_client.list_objects(repo.name, prefix=self._MODELS + '/' + category.value, recursive=True):
                experiment_model = obs.object_name.split('/')[0:3]
                experiment_model = repo.name + '/' + '/'.join(experiment_model)            
                if experiment_model not in models_list:
                    num_models += 1
                    models_list.append(experiment_model)
        return num_models, models_list
    
    def _count_category_datasets(self, category:Categories) -> (int, list):
        """Count all available datasets under a specific category.

        Args:
            category (Categories): Category to which count the datasets from.

        Returns:
            int: number of datasets under the category
            list: list of datasets under the category
        """
        if isinstance(category, str):
           category = Categories[category.upper()]
           
        num_datasets = 0
        datasets_list = []
        repo_list = self.minio_client.list_buckets()
        for repo in repo_list:
            for obs in self.minio_client.list_objects(repo.name, prefix=self._DATASETS + '/' + category.value, recursive=True):
                experiment_dataset = obs.object_name.split('/')[0:3]
                experiment_dataset = repo.name + '/' + '/'.join(experiment_dataset)
                if experiment_dataset not in datasets_list:
                    num_datasets += 1
                    datasets_list.append(experiment_dataset)
        return num_datasets, datasets_list
