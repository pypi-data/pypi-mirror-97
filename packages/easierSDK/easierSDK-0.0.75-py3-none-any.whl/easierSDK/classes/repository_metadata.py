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

class RepositoryMetadata():
    """Class to store the repository's metadata information.
    """

    name = ''
    categories = {}

    def __init__(self, name:str, categories:dict):
        """Constructor for RepositoryMetadata class.

        Args:
            name (str): Repository name
            categories (dict): Dictionary of Category.value, CategoryMetadata
        """
        self.name = name
        self.categories = categories

    def print_categories(self):
        """Print the categories metadata information.
        """
        row_format ="{:<30}" * 3
        print(row_format.format(*['Category', 'Num Models', 'Num Datasets']))
        for category in self.categories:
            print(row_format.format(*[self.categories[category].name, self.categories[category].num_models, self.categories[category].num_datasets]))


    def print_models(self):
        """Print the metadata information.
        """
        row_format ="{:<30}" * 4

        print("MODELS:")
        print(row_format.format(*['Name', 'Category', 'Last Modification', 'Num Experiments']))
        for category in self.categories:
            for model_metadata in self.categories[category].models:
                print(row_format.format(*[self.categories[category].models[model_metadata].name, 
                    self.categories[category].models[model_metadata].category, 
                    self.categories[category].models[model_metadata].last_modified,
                    str(len(self.categories[category].models[model_metadata].experimentIDs))]))

    def print_datasets(self):
        """Print the metadata information.
        """
        row_format ="{:<30}" * 3
        
        print("DATASETS:")
        print(row_format.format(*['Name', 'Category', 'Last Modification']))
        for category in self.categories:
            for dataset_metadata in self.categories[category].datasets:
                print(row_format.format(*[self.categories[category].datasets[dataset_metadata].name, 
                    self.categories[category].datasets[dataset_metadata].category, 
                    self.categories[category].datasets[dataset_metadata].last_modified]))
   
    def pretty_print(self):
        """Print the metadata information.
        """
        row_format ="{:<30}" * 4

        print("MODELS:")
        print(row_format.format(*['Name', 'Category', 'Last Modification', 'Num Experiments']))
        for category in self.categories:
            for model_metadata in self.categories[category].models:
                print(row_format.format(*[self.categories[category].models[model_metadata].name, 
                    self.categories[category].models[model_metadata].category, 
                    self.categories[category].models[model_metadata].last_modified,
                    str(len(self.categories[category].models[model_metadata].experimentIDs))]))
        
        row_format ="{:<30}" * 3
        print("\nDATASETS:")
        print(row_format.format(*['Name', 'Category', 'Last Modification']))
        for category in self.categories:
            for dataset_metadata in self.categories[category].datasets:
                print(row_format.format(*[self.categories[category].datasets[dataset_metadata].name, 
                    self.categories[category].datasets[dataset_metadata].category, 
                    self.categories[category].datasets[dataset_metadata].last_modified]))

