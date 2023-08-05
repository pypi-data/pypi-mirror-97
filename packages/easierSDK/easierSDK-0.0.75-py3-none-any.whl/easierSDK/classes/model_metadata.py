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

class ModelMetadata():
    """Class to store the model's metadata information.
    """

    category = ''
    name = ''
    last_modified = ''
    description = ''
    version = 0
    features = []
    previous_experimentID = -1
    experimentIDs = []

    def __init__(self, f:dict=None):
        """Constructor for the EasierModel Metadata Class.

        Args:
            f (dict, optional): Dictionary with the model's metadata information.
        """
        if f is not None :
            if 'category' in f: 
                try:
                    self.category = Categories(f['category'])
                except:
                    print("[ModelMetadata] Category " + str(f['category']) + " not recognized. Using 'misc' as categoriy")
                    self.category = Categories.MISC
            if 'name' in f: self.name = f['name']
            if 'last_modified' in f: 
                try:
                    self.last_modified = time.strftime('%H:%M:%S - %d/%m/%Y', f['last_modified'])
                except:
                    # print("[ModelMetadata] Couldn't parse time in 'last-modified'. Keeping as str")
                    self.last_modified = f['last_modified']
            if 'description' in f: self.description = f['description']
            if 'version' in f: self.version = f['version']
            if 'features' in f: self.features = f['features']
            if 'previous_experimentID' in f: self.previous_experimentID = int(f['previous_experimentID'])
        else:
            pass

    # def seria
    def pretty_print(self):
        """Print the metadata information.
        """
        if isinstance(self.category, str):
            category = Categories[category.upper()]
        else:
            category = self.category.value
        row_format ="{:<30}" * 2
        print(row_format.format(*['Category:', category]))
        print(row_format.format(*['Name:', self.name]))
        print(row_format.format(*['Description:', self.description]))
        print(row_format.format(*['Last modified:', str(self.last_modified)]))
        print(row_format.format(*['Version:', self.version]))
        print(row_format.format(*['Features:', str(self.features)]))
        if self.previous_experimentID > -1: print(row_format.format(*['previous_experimentID:', str(self.previous_experimentID)]))

    def dump_to_file(self, path:str):
        """Dump metadata information to a file.

        Args:
            path (str): Path to store the file with the metadata information.
        """
        if isinstance(self.category, str):
            category = Categories[category.upper()]
        else:
            category = self.category.value
        with open(path+'/metadata.json', 'w') as f:
            metadata = {}
            metadata["category"] = category
            metadata["name"] = self.name
            metadata["last_modified"] = self.last_modified
            metadata["description"] = self.description
            metadata["version"] = self.version
            metadata["features"] = self.features
            if self.previous_experimentID > -1: metadata["previous_experimentID"] = self.previous_experimentID
            f.write(json.dumps(metadata, sort_keys=True, indent=4))

