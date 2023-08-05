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

import sys
sys.path.append('..')
sys.path.append('.')

import time
import json

from easierSDK.classes.categories import Categories

class CategoryMetadata():
    """Class to store the repository's metadata information.
    """

    name = ''
    models = {}
    num_models = 0
    datasets = {}
    num_datasets = 0

    def __init__(self, name:str, models:dict, num_models:int, datasets:dict, num_datasets:int):
        """Constructor for RepositoryMetadata class.

        Args:
            name (str): Repository name
            models (list): List of ModelMetadata objects of models under this repository
            num_models (int): Number of models in list
            datasets (list): List of DataSetMetadata objects of datasets under this repository
            num_datasets (int): Number of datasets in list
        """
        self.name = name
        self.models = models
        self.datasets = datasets
        self.num_models = num_models
        self.num_datasets = num_datasets


    def print_models(self):
        """Print the metadata information.
        """
        row_format ="{:<30}" * 4

        print("MODELS:")
        print(row_format.format(*['Name', 'Category', 'Last Modification', 'Num Experiments']))
        for model_metadata in self.models:
            print(row_format.format(*[self.models[model_metadata].name, 
                self.models[model_metadata].category, self.models[model_metadata].last_modified, 
                str(len(self.models[model_metadata].experimentIDs))]))

    def print_datasets(self):
        """Print the metadata information.
        """
        row_format ="{:<30}" * 3
        
        print("DATASETS:")
        print(row_format.format(*['Name', 'Category', 'Last Modification']))
        for dataset_metadata in self.datasets:
            print(row_format.format(*[self.datasets[dataset_metadata].name, self.datasets[dataset_metadata].category, self.datasets[dataset_metadata].last_modified]))
   
    def pretty_print(self):
        """Print the metadata information.
        """
        row_format ="{:<30}" * 4

        print("MODELS:")
        print(row_format.format(*['Name', 'Category', 'Last Modification', 'Num Experiments']))
        for model_metadata in self.models:
            print(row_format.format(*[self.models[model_metadata].name, 
                self.models[model_metadata].category, self.models[model_metadata].last_modified, 
                str(len(self.models[model_metadata].experimentIDs))]))
        
        row_format ="{:<30}" * 3
        print("\nDATASETS:")
        print(row_format.format(*['Name', 'Category', 'Last Modification']))
        for dataset_metadata in self.datasets:
            print(row_format.format(*[self.datasets[dataset_metadata].name, self.datasets[dataset_metadata].category, self.datasets[dataset_metadata].last_modified]))

