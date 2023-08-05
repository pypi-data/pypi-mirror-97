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
import os
import joblib
import random
import string
from shutil import copyfile
import tensorflow as tf
import numpy

import easierSDK.classes.constants as constants
from easierSDK.classes.categories import Categories
from easierSDK.classes.model_metadata import ModelMetadata

class EasierModel():
    """Class to control the Easier model's objects.
    """

    metadata = None
    model = None
    scaler = None
    label_encoder = None
    feature_encoder = None
    tf_lite_model_path = ''
    tpu_model_path = ''
    gpu_model_path = ''
    model_dir = ''
    samples = None

    def __init__(self, metadata:ModelMetadata=None):
        """Constructor for the model class.

        Args:
            metadata (ModelMetadata, optional): model's metadata. Defaults to None.
        """
        self.metadata = metadata

    def set_metadata(self, metadata:ModelMetadata):
        """Set model's metadata.

        Args:
            metadata (ModelMetadata): model's metadata.
        """
        self.metadata = metadata
    def get_metadata(self) -> ModelMetadata:
        """Return model's metadata.

        Returns:
            ModelMetadata: model's metadata.
        """
        return self.metadata

    def set_model(self, model:object):
        """Set the model variable.

        Args:
            model (object): Your model variable.
        """
        self.model = model
    def get_model(self) -> object:
        """Return the model variable.

        Returns:
            object: model.
        """
        return self.model
    
    def set_scaler(self, scaler:object):
        """Set scaler for the model.

        Args:
            scaler (object): scaler for the model.
        """
        self.scaler = scaler
    def get_scaler(self) -> object:
        """Return scaler for the model.

        Returns:
            object: scaler for the model.
        """
        return self.scaler
    
    def set_label_encoder(self, label_encoder:object):
        """Set label encoder for the model.

        Args:
            label_encoder (object): label encoder for the model.
        """
        self.label_encoder = label_encoder
    def get_label_encoder(self) -> object:
        """Return label encoder for the model.

        Returns:
            object: label encoder for the model.
        """
        return self.label_encoder
    
    def set_feature_encoder(self, feature_encoder:object):
        """Set feature encoder for the model.

        Args:
            feature_encoder (object): feature encoder for the model.
        """
        self.feature_encoder = feature_encoder
    def get_feature_encoder(self) -> object:
        """Return feature encoder for the model.

        Returns:
            object: feature encoder for the model.
        """
        return self.feature_encoder
    
    def set_tf_lite_model_path(self, tf_lite_model_path:str):
        """Set path to store the TFLITE version of the model.

        Args:
            tf_lite_model_path (str): path to store the TFLITE version of the model.
        """
        self.tf_lite_model_path = tf_lite_model_path
    def get_tf_lite_model_path(self):
        """Return path to TFLITE version of the model.

        Returns:
            [type]: path to TFLITE version of the model.
        """
        return self.tf_lite_model_path

    def set_tpu_model_path(self, tpu_model_path:str):
        """Set path to store the TPU version of the model.

        Args:
            tpu_model_path (str): path to store the TPU version of the model.
        """
        self.tpu_model_path = tpu_model_path
    def get_tpu_model_path(self):
        """Return path to TPU version of the model.

        Returns:
            str: path to TPU version of the model.
        """
        return self.tpu_model_path
    
    def set_gpu_model_path(self, gpu_model_path:str):
        """Set path to store the GPU version of the model.

        Args:
            gpu_model_path (str): path to store the GPU version of the model.
        """
        self.gpu_model_path = gpu_model_path
    def get_gpu_model_path(self) -> str:
        """Return path to GPU version of the model.

        Returns:
            str: path to GPU version of the model.
        """
        return self.gpu_model_path

    def set_representative_data(self, samples:list):
        """Set representative data of the model.

        Args:
            samples (list): representative data of the model.
        """
        self.samples = samples
    def get_representative_data(self) -> list:
        """Return representative data of the model.

        Returns:
            list: representative data of the model.
        """
        return self.samples
    
    def _get_random_string(self) -> str:
        """Returns a random string.

        Returns:
            str: random string
        """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(random.randint(1, 16))) 

    def store(self, model_path:str=None, storage_level=constants.FULL, print_files:bool=True) -> str:
        """Save the model's objects to files.

        Args:
            model_path (str, optional): Path to which to store the files. Defaults to None to create a random local folder.
            print_files (bool, optional): Whether to print which files are stored or not. Defaults to True.

        Returns:
            str: path in which the files were stored.
        """
        files_print = ""
        if model_path is None:
            path = '/tmp/' + self._get_random_string()
            while os.path.isdir(path): path += self._get_random_string()
            os.mkdir(path)
        else:
            path = model_path
        self.metadata.dump_to_file(path)

        if storage_level == constants.FULL:
            try:
                self.model.save(path + "/" + self.metadata.name + '.' + constants.MODEL_EXTENSION)
                files_print += "\n\t- " + self.metadata.name + '.' + constants.MODEL_EXTENSION    
            except Exception as e:
                print("[ERROR] Couldn't save model as HDF5: " + str(e))
                print("Trying with joblib...")
                try: 
                    joblib.dump(self.model, path + "/" + 'model.h5')
                except Exception as e2:
                    print("[ERROR] Couldn't save model with joblib: " + str(e2))
        
        if storage_level == constants.FULL or storage_level == constants.WEIGHTS_ONLY:
            try:
                self.model.save_weights(path + "/" + self.metadata.name + '.' + constants.WEIGHTS_EXTENSION)
                files_print += "\n\t- " + self.metadata.name + '.' + constants.WEIGHTS_EXTENSION
            except Exception as e:
                print("[ERROR] Couldn't save weights as HDF5: " + str(e))

        try:
            json_config = self.model.to_json()
            with open(path + "/" + self.metadata.name + '.' + constants.MODEL_STRUCTURE_EXTENSION, 'w') as json_file:
                json.dump(json_config, json_file)
            files_print += "\n\t- " + self.metadata.name + '.' + constants.MODEL_STRUCTURE_EXTENSION
        except Exception as e:
            print("[ERROR] Couldn't save model structure to JSON: " + str(e))
        
        if self.scaler: 
            joblib.dump(self.scaler, path + "/" + 'scaler.s.pkl')
            files_print += "\n\t- scaler.s.pkl"
        if self.label_encoder: 
            joblib.dump(self.label_encoder, path + "/" + 'label_encoder.e.pkl')
            files_print += "\n\t- label_encoder.e.pkl"
        if self.feature_encoder: 
            joblib.dump(self.feature_encoder, path + "/" + 'feature_encoder.ohe.pkl')
            files_print += "\n\t- feature_encoder.ohe.pkl"
        if self.tf_lite_model_path: 
            copyfile(self.tf_lite_model_path, path + "/" + self.tf_lite_model_path.split('/')[-1])
            files_print += "\n\t- " + self.tf_lite_model_path.split('/')[-1]
        if self.tpu_model_path: 
            copyfile(self.tpu_model_path, path + "/" + self.tpu_model_path.split('/')[-1])
            files_print += "\n\t- " + self.tpu_model_path.split('/')[-1]
        if self.gpu_model_path: 
            copyfile(self.gpu_model_path, path + "/" + self.gpu_model_path.split('/')[-1])
            files_print += "\n\t- " + self.gpu_model_path.split('/')[-1]
        
        if print_files:
            print("Stored files in " + path + ":\n\t- metadata.json" + ":\n\t- " + self.metadata.name + '.h5' + files_print)
        return path

    def representative_dataset_gen(self):
        """Generator for the samples that the model was trained with.

        Yields:
            list: list with a sample that the model was trained with.
        """
        for i in range(len(self.samples)):
            data = numpy.array(self.samples[i: i + 1], dtype=numpy.float32)
            yield [data]
