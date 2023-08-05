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

class DatasetMetadata():
    """Class to store the dataset's metadata information.
    """

    category = ''
    name = ''
    last_modified = ''
    size = 0
    description = ''
    version = 0
    features = {}
    row_number = 0
    dataset_type = ''
    file_extension = ''

    def __init__(self, f:dict=None):
        """Constructor for the Dataset Metadata Class.

        Args:
            f (dict, optional): Dictionary with the dataset's metadata information.
        """
        if f is not None:
            if 'category' in f: 
                try:
                    self.category = Categories(f['category'])
                except:
                    print("[DatasetMetadata] Category " + str(f['category']) + " not recognized. Using 'misc' as categoriy")
                    self.category = Categories.MISC
            if 'name' in f: self.name = f['name']
            if 'last_modified' in f: 
                try:
                    self.last_modified = time.strftime('%H:%M:%S - %d/%m/%Y', f['last_modified'])
                except:
                    # print("[DatasetMetadata] Couldn't parse time in 'last-modified'. Keeping as str")
                    self.last_modified = f['last_modified']
            if 'size' in f: self.size = f['size']
            if 'description' in f: self.description = f['description']
            if 'version' in f: self.version = f['version']
            if 'features' in f: self.features = f['features']
            if 'row_number' in f: self.row_number = f['row_number']
            if 'dataset_type' in f: self.dataset_type = f['dataset_type']
            if 'file_extension' in f: self.file_extension = f['file_extension']
        else:
            pass

    # def seria
    def pretty_print(self):
        """Print the metadata information.
        """
        if isinstance(self.category, str):
            category = Categories[self.category.upper()]
        else:
            category = self.category.value
        row_format ="{:<30}" * 2
        print(row_format.format(*['Category:', category]))
        print(row_format.format(*['Name:', self.name]))
        print(row_format.format(*['Size:', self.size]))
        print(row_format.format(*['Description:', self.description]))
        print(row_format.format(*['Last modified:', str(self.last_modified)]))
        print(row_format.format(*['Version:', self.version]))
        print(row_format.format(*['Row number:', self.row_number]))
        print(row_format.format(*['Features:', str(self.features)]))
        print(row_format.format(*['Dataset type:', self.dataset_type]))
        print(row_format.format(*['File extension:', self.file_extension]))

    def dump_to_file(self, path:str):
        """Dump metadata information to a file.

        Args:
            path (str): Path to store the file with the metadata information.
        """
        if isinstance(self.category, str):
            self.category = Categories[self.category.upper()]
        else:
            self.category = self.category.value
        with open(path+'/metadata.json', 'w') as f:
            f.write(json.dumps(self.__dict__, default=lambda o: str(o.value), 
            sort_keys=True, indent=4))

