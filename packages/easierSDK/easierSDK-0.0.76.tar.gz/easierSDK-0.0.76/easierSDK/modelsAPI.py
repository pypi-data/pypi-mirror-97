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
import urllib3
import os
import subprocess
import tensorflow as tf
import joblib
from shutil import rmtree
import json
import tensorflow.keras.backend as K
import glob
import datetime

from easierSDK.classes.categories import Categories
from easierSDK.classes.model_metadata import ModelMetadata
from easierSDK.classes.easier_model import EasierModel
import easierSDK.classes.constants as constants


class ModelsAPI():
    """Class to control the Models API of EasierSDK.
    """

    _GLOBAL = 'global'
    _MODELS = 'models'
    _DATASETS = 'datasets'
    _BASE_MODELS_PATH = './models'
    _MAX_FOLDER_SIZE = 2000 # Kbytes = 2M
    _MAX_FOLDER_SIZE_STR = '2MB'

    def __init__(self, minio_client, my_public_repo, my_private_repo):
        """Constructor for the ModelsAPI.

        Args:
            minio_client (Minio): Minio client object with user session initialized.
            my_public_repo (str): Name of the public bucket of the user.
            my_private_repo (str): Name of the private bucket of the user.
        """
        if not os.path.isdir(self._BASE_MODELS_PATH): os.mkdir(self._BASE_MODELS_PATH)
        self.minio_client = minio_client
        self.my_public_repo = my_public_repo
        self.my_private_repo = my_private_repo

    def _count_model_experiments(self, repo_name:str, category:str, model_name:str) -> int:
        """Count number of experiments in Minio of a model.

        Args:
            repo_name (str): Name of the Minio repository.
            category (str): Category of the model.
            model_name (str): EasierModel name in repository.

        Returns:
            int: number of experiments of the model.
        """
        if isinstance(category, Categories):
           category = category.value

        num_experiments = 0
        already_counted = []
        for item in self.minio_client.list_objects(repo_name, prefix=self._MODELS + '/' + category + '/' + model_name, recursive=True):
            if item.object_name == self._MODELS + '/' + category + '/' + model_name + "/metadata.json":
                continue
            experimentID = item.object_name.split('/')[3]
            if experimentID in already_counted:
                continue
            num_experiments += 1
            already_counted.append(experimentID)
        return num_experiments, already_counted     

    def get_model_experiments(self, repo_name:str, category:Categories, model_name:str) -> list:
        """Get a list of metadata information of a specific model experiments.

        Args:
            repo_name (str): Name of the repository that contains the model.
            category (Categories): Category that contains the model.
            model_name (str): Name of the model.
            
        Returns:
            list: list of ModelMetadata objects with the experiments information.
        """
        metadata = []
        if isinstance(category, str):
           category = Categories[category.upper()]

        if not self.minio_client.bucket_exists(repo_name):
            print('[ERROR] Repository name does not exist. Please check and try again')
            return None
        num_experiments, _ = self._count_model_experiments(repo_name, category.value, model_name)
        for experiment in range(num_experiments):
            filename = self._MODELS + '/' + category.value + '/' + model_name + '/' + str(experiment) + '/' + 'metadata.json'
            local_file = './models/' + filename
            try:
                minio_obj = self.minio_client.fget_object(repo_name, filename, local_file)
            except minio.error.NoSuchKey as ex:
                print('[ERROR] Wrong model information, please check: category, name and experimentID and try again.')
                return None
            
            with open(local_file, 'r') as f:
                model_metadata = ModelMetadata(json.load(f))
                metadata.append(model_metadata)

            if os.path.exists(local_file):
                os.remove(local_file)
        return metadata

    def show_model_info(self, repo_name:str, category:Categories, model_name:str, experimentID:int=-1) -> ModelMetadata:
        """Show metadata information of a specific model and/or a specific experimentID.

        Args:
            repo_name (str): Name of the repository that contains the model.
            category (Categories): Category that contains the model.
            model_name (str): Name of the model.
            experimentID (int, optional): ExperimentID of the model to which information is going to be shown. Defaults to -1 to show contextual model information without references to any experimentID.

        Returns:
            ModelMetadata: object with the model information.
        """
        if isinstance(category, str):
           category = Categories[category.upper()]

        if not self.minio_client.bucket_exists(repo_name):
            print('[ERROR] Repository name does not exist. Please check and try again')
            return None
        if experimentID == -1:
            # Show model metadata instead of experiment metadata
            # experimentID, _ = self._count_model_experiments(repo_name, category.value, model_name) - 1        
            filename = self._MODELS + '/' + category.value + '/' + model_name + '/' + 'metadata.json'
        else:
            filename = self._MODELS + '/' + category.value + '/' + model_name + '/' + str(experimentID) + '/' + 'metadata.json'
        local_file = './models/' + filename
        try:
            minio_obj = self.minio_client.fget_object(repo_name, filename, local_file)
        except minio.error.NoSuchKey as ex:
            print('[ERROR] Wrong model information, please check: category, name and experimentID and try again.')
            return None
        
        with open(local_file, 'r') as f:
            metadata = ModelMetadata(json.load(f))
            metadata.pretty_print()

        if os.path.exists(local_file):
            os.remove(local_file)
        return metadata
        
    def show_model_config(self, repo_name:str, category:Categories, model_name:str, experimentID:int=-1):
        """Show model's configuration in a JSON file of a specific model and/or a specific experimentID. 

        Args:
            repo_name (str): Name of the repository that contains the model.
            category (Categories): Category that contains the model.
            model_name (str): Name of the model.
            experimentID (int, optional): ExperimentID of the model to which information is going to be shown. Defaults to -1 to show contextual model information without references to any experimentID.

        Returns:
            JSON: JSON object with the model's configuration.
        """
        if isinstance(category, str):
           category = Categories[category.upper()]

        if not self.minio_client.bucket_exists(repo_name):
            print('[ERROR] Repository name does not exist. Please check and try again')
            return None
        if experimentID == -1:
            # Show last experiment ID model configuration
            experimentID, _ = self._count_model_experiments(repo_name, category.value, model_name) - 1        
    
        filename = self._MODELS + '/' + category.value + '/' + model_name + '/' + str(experimentID) + '/' + model_name + '.' + constants.MODEL_STRUCTURE_EXTENSION
        local_file = './models/' + filename
        try:
            minio_obj = self.minio_client.fget_object(repo_name, filename, local_file)
        except minio.error.NoSuchKey as ex:
            print('[ERROR] The model you indicated does not have a JSON configuration file or you provided wrong model information, please check: category, name and experimentID and try again.')
            return None
        
        with open(local_file, 'r') as f:
            configuration = json.load(f)
            print(configuration)

        return configuration

    def download(self, repo_name:str, category:Categories, model_name:str, path_to_download:str, experimentID:int=-1) -> str:
        """Downloads a model and its attached objets in a specific path.

        Args:
            repo_name (str): Name of the repository that contains the model.
            category (Categories): Category that contains the model.
            model_name (str): Name of the model.
            path_to_download (str): Local path in which to store all files.
            experimentID (int, optional): ExperimentID of the model to download. Defaults to -1 to download the last experiment.

        Returns:
            str: path under path_to_download folder where files were stored
        """
        if isinstance(category, str):
           category = Categories[category.upper()]

        if not self.minio_client.bucket_exists(repo_name):
            print('[ERROR] Repository name does not exist. Please check and try again')
            return None
        if experimentID == -1:
            # Download last experiment
            experimentID, _ = self._count_model_experiments(repo_name, category.value, model_name) - 1
        # TODO check if models will be saved in HDF5 .h5 or tf SavedModel format (folder)
        minio_path = self._MODELS + '/' + category.value + '/' + model_name + '/' + str(experimentID)
        local_path = path_to_download + "/" + minio_path
        try:
            objects = self.minio_client.list_objects(repo_name, prefix=minio_path, recursive=True)
            for minio_object in objects:
                minio_obj = self.minio_client.fget_object(repo_name, minio_object.object_name, path_to_download + "/" + minio_object.object_name)
        except minio.error.NoSuchKey as ex:
            print('[ERROR] Wrong model name or category, please check and try again.')
            return None
        return local_path

    def _load_model_from_path(self, path:str, load_level=constants.FULL, print_files=False, easier_model:EasierModel=None) -> EasierModel:
        if easier_model is None: easier_model = EasierModel()
    
        model_name = glob.glob(path + '/' + '*.s.json')[0]
        model_name = model_name.split('.s.json')[0]
        model_name = model_name.split('/')[-1]

        if load_level == constants.CONFIG_ONLY or load_level == constants.WEIGHTS_ONLY:
            # First we need to load the config/structure of the model as json
            try:
                with open(path + '/' + model_name + '.s.json') as json_file:
                    json_model = json.load(json_file)
                    json_model = tf.keras.models.model_from_json(json_model)
                if print_files: print("Loaded model's config from JSON. File stored in: " + path + '/' + model_name + '.s.json')
            except Exception as e:
                print("[ERROR] Could not load model's config from JSON: " + str(e)) 
            
            if load_level == constants.WEIGHTS_ONLY:
                # Load the weights in case it is necessary
                try:
                    load_status = json_model.load_weights(filepath=path + '/' + model_name + '.w.' + constants.MODEL_EXTENSION)
                    load_status.assert_consumed()
                except Exception as e:
                    print("[ERROR] Could not load model's weights properly: " + str(e)) 
            # Set the model for EasierModel variable
            easier_model.set_model(json_model)
        elif load_level == constants.FULL:
            try:
                # Load model from file (HDF5 default)
                easier_model.set_model(tf.keras.models.load_model(path + '/' + model_name + '.' + constants.MODEL_EXTENSION))
                if print_files: print("Loaded model. File stored in: " + path + '/' + model_name + '.' + constants.MODEL_EXTENSION)
            except Exception as e:
                print("[ERROR] Could not load full model: " + str(e))
        else:
            print("[ERROR] Load level: " + str(load_level) + " not supported. Use constants.CONFIG_ONLY, constants.WEIGHTS_ONLY or constants.FULL")

        return easier_model


    def _load_file(self, path:str, load_level=constants.FULL, print_files=False, easier_model:EasierModel=None) -> EasierModel:
        """Loads files from a path onto an EASIER model variable depending on the file's extension.

        Args:
            path (str): path of the file
            print_files (bool, optional): Whether or not to print which files are being loaded. Defaults to False.
            easier_model (EasierModel, optional): EASIER EasierModel variable to to load the files. Defaults to None to create a new model.

        Returns:
            EasierModel: EASIER model variable with file loaded
        """
        if easier_model is None: easier_model = EasierModel()

        easier_model = self._load_model_from_path(path, load_level=load_level, print_files=print_files, easier_model=easier_model)

        for obj in os.listdir(path):
            extension = obj.split(".")[-1]

            if extension == constants.MODEL_EXTENSION:
               continue          

            elif extension == constants.PICKLE_EXTENSION:
                extension_pkl = obj.split(".")[-2:]
                extension_pkl = '.'.join(extension_pkl)
                if extension_pkl == constants.SCALER_EXTENSION:
                    easier_model.set_scaler(joblib.load(path + '/' + obj))
                    if print_files: print("Loaded scaler. File stored in: " + path + '/' + obj)
                elif extension_pkl == constants.LABELENCODER_EXTENSION:
                    easier_model.set_label_encoder(joblib.load(path + '/' + obj))
                    if print_files: print("Loaded label encoder. File stored in: " + path + '/' + obj)
                elif extension_pkl == constants.ONEHOTENCODER_EXTENSION:
                    easier_model.set_feature_encoder(joblib.load(path + '/' + obj))
                    if print_files: print("Loaded one hot encoder. File stored in: " + path + '/' + obj)

            elif extension == constants.JSON_EXTENSION:
                obj_name = obj.split('.')[-2]
                if obj_name == 'metadata':
                    with open(path + '/' + obj, 'r') as f:
                        metadata = ModelMetadata(f=json.load(f))
                        easier_model.set_metadata(metadata)
                    if print_files: print("Loaded model's metadata. File stored in: " + path + '/' + obj)
                else:
                    # Load model from JSON configuration
                    continue
                        
            elif extension == constants.TF_LITE_EXTENSION: 
                extension_tflite = obj.split("_")[-1]    
                if '_' + extension_tflite == constants.TPU_EXTENSION:
                    easier_model.set_tpu_model_path(path + '/' + obj)
                    if print_files: print("Downloaded tpu model version. File stored in: " + path + '/' + obj)
                else:
                    easier_model.set_tf_lite_model_path(path + '/' + obj)
                    if print_files: print("Downloaded tf lite model version. File stored in: " + path + '/' + obj)
            else:
                if print_files: print("Couldn't load file with extension: ." + str(extension))

        return easier_model

    def load_from_local(self, path:str, load_level=constants.FULL, print_files=False) -> EasierModel:
        """Loads a model into memory from a local path.

        Args:
            path (str): Local path where model files are stored.
            print_files (bool, optional): Whether to print which files are loaded. Defaults to False.

        Returns:
            EasierModel: object with the loaded model and its attached elements like scalers.
        """
        easier_model = self._load_file(path, load_level=load_level, print_files=print_files)
                
        return easier_model

    def get_model(self, repo_name:str, category:Categories, model_name:str, experimentID:int=-1, load_level=constants.FULL, print_files=False) -> EasierModel:
        """Loads a model into memory from a repository.

        Args:
            repo_name (str): Name of the repository that contains the model.
            category (Categories): Category that contains the model.
            model_name (str): Name of the model.
            experimentID (int, optional): ExperimentID of the model to download. Defaults to -1 to load the last experiment.
            load_level (str, optional): Levels of loading a model: FULL_MODEL, WEIGHTS_ONLY, CONFIG_ONLY. Defaults to FULL_MODEL.
            print_files (bool, optional): Whether to print which files are loaded. Defaults to False.

        Returns:
            EasierModel:  object with the loaded model and its attached elements like scalers.
        """
        if isinstance(category, str):
           category = Categories[category.upper()]

        if not os.path.isdir('/tmp/download'): os.mkdir('/tmp/download')

        if experimentID == -1:
            # Load last experiment
            experimentID, _ = self._count_model_experiments(repo_name, category.value, model_name) - 1
        
        path = self.download(repo_name, category, model_name, path_to_download='/tmp/download', experimentID=experimentID)
        if print_files: print("Files are stored in: " + path)
        
        easier_model = self._load_file(path, load_level=load_level, print_files=print_files)
        easier_model.metadata.previous_experimentID = experimentID
        
        return easier_model

    def upload(self, easier_model:EasierModel, category:Categories=None, public:bool=False, storage_level:str=constants.FULL, remove_dir:bool=True) -> bool:
        """Upload a model and its attached elements to the user's repository. *Important*: This function updates your model version and last_experimentID according to repository's information. 

        Args:
            category (Categories): Category that contains the model.
            easier_model (EasierModel): Object with the model and its attached elements.
            public (bool, optional): Whether to upload the model in the public version of the repository. Defaults to False.
            storage_level (str, optional): Levels of storage for a model: FULL_MODEL, WEIGHTS_ONLY, CONFIG_ONLY
            remove_dir (bool, optional): Whether to remove the folder in which the files to be uploaded were created. Defaults to True.

        Returns:
            bool: True if successful upload. False otherwise.
        """
        if easier_model.metadata is None or easier_model.metadata.name is None:
            print("[ERROR] Cannot upload model without a ModelMetadata and a ModelMetadata.name")
            return False
        
        if '.' in easier_model.metadata.name:
            print("[ERROR] Cannot upload model with '.' in its name. Please modify the name accordingly.")
            return False

        if storage_level.lower() != constants.FULL and storage_level.lower() != constants.WEIGHTS_ONLY and storage_level.lower() != constants.CONFIG_ONLY:
            print("[ERROR] Model storage level (" + str(storage_level) + ") not supported.")
            print("Supported model storage levels: full (constants.FULL), weights_only (constants.WEIGHTS_ONLY), config_only (constants.CONFIG_ONLY)")
            return False

        if not category:
            if isinstance(easier_model.metadata.category, Categories):
                category = easier_model.metadata.category.value
            else:
                category = easier_model.metadata.category
        else:
            if isinstance(category, Categories):
                category = category.value

        if public:
            bucket = self.my_public_repo
        else:
            bucket = self.my_private_repo
        
        # Create bucket if doesn't exist
        if not self.minio_client.bucket_exists(bucket): self.minio_client.make_bucket(bucket, location='es')

        # Check last experiment
        last_experimentID, _ = self._count_model_experiments(bucket, category, easier_model.metadata.name)

        # Update version to new experimentID
        easier_model.metadata.previous_experimentID = easier_model.metadata.version
        easier_model.metadata.version = last_experimentID

        # Update last modified timestamp in metadata 
        easier_model.metadata.last_modified = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        
        # Store files to be uploaded
        path = easier_model.store(storage_level=storage_level, print_files=False)
        minio_path = self._MODELS + '/' + category + '/' + easier_model.metadata.name
                        
        try:
            for obj in os.listdir(path):
                self.minio_client.fput_object(bucket, minio_path + '/' + str(last_experimentID) + '/' + obj, path + '/' + obj)
            # If it is a new model, upload a metadata file on top of experiments representing the first model.
            if last_experimentID == 0:
                self.minio_client.fput_object(bucket, minio_path + '/' + "metadata.json", path + '/' + "metadata.json")
            if remove_dir: rmtree(path)
        except Exception as ex:
            print("[ERROR] Error uploading model to MINIO: " + str(ex))
            return False
        print("Uploaded model: \n")
        easier_model.metadata.pretty_print()
        return True

    def compile_tflite(self, easier_model:EasierModel, calibration_data: list, path:str=_BASE_MODELS_PATH + "/storage/"):
        """Compiles a Tensorflow model to its Lite version.

        Args:
            easier_model (EasierModel): EasierModel object with the Tensorflow model to be compiled.
            calibration_data (list): List with some example data that the model was trained with.
            path (str, optional): Path to store the tflite file. Defaults to "./models/storage/".
        """
        # TODO check model type (h5 vs SavedModel)
        # TODO check usage of path
        if not os.path.isdir(path): os.mkdir(path)
        if not os.path.isdir("/tmp/storage/"): os.mkdir("/tmp/storage/")
        easier_model.set_representative_data(samples = calibration_data)

        if easier_model.model is None and easier_model.model_dir != '':
            converter = tf.lite.TFLiteConverter.from_saved_model(easier_model.model_dir)
        elif easier_model.model is not None:
            if tf.__version__.split(".")[0] == '1':
                easier_model.model.save("/tmp/storage/" + easier_model.metadata.name + "." + constants.MODEL_EXTENSION)
                # Clear graph in prep for next step.
                try:
                    K.clear_session()
                except Exception as e:
                    pass                
                converter = tf.lite.TFLiteConverter.from_keras_model_file("/tmp/storage/" + easier_model.metadata.name + "." + constants.MODEL_EXTENSION)
            else:    
                converter = tf.lite.TFLiteConverter.from_keras_model(easier_model.model)

        converter.representative_dataset = easier_model.representative_dataset_gen
        converter.optimizations = [tf.lite.Optimize.DEFAULT]

        try:
            tflite_model = converter.convert()
        except Exception as e:
            print("Error converting model to tf lite: " + str(e))
            return

        if easier_model.model_dir != '':
            tf_lite_model_path = path + easier_model.model_dir + "/" + easier_model.metadata.name + "." + constants.TF_LITE_EXTENSION
            open(tf_lite_model_path, "wb").write(tflite_model)
            print("Converted tf model " + str(easier_model.model_dir) + " to tf lite")
        else:
            tf_lite_model_path = path + easier_model.metadata.name + "." + constants.TF_LITE_EXTENSION
            open(tf_lite_model_path, "wb").write(tflite_model)
            # Clear graph in prep for next step.
            try:
                K.clear_session()
            except Exception as e:
                pass
            print("Converted keras model " + easier_model.metadata.name + " to tf lite")

        easier_model.set_tf_lite_model_path(tf_lite_model_path)

    def compile_tpu(self,  easier_model:EasierModel, calibration_data, path:str=_BASE_MODELS_PATH + "/storage/"):
        """Compiles a Tensorflow model to its TPU version.

        Args:
            easier_model (EasierModel): EasierModel object with the Tensorflow model to be compiled.
            calibration_data (list): List with some example data that the model was trained with.
            path (str, optional): Path to store the tflite.edge_tpu file. Defaults to "./models/storage/".
        """
        # TODO check model type (h5 vs SavedModel)
        # TODO check usage of path

        if not os.path.isdir(path): os.mkdir(path)
        if not os.path.isdir("/tmp/storage/"): os.mkdir("/tmp/storage/")
        easier_model.set_representative_data(samples = calibration_data)

        if easier_model.model_dir != '':
            converter = tf.lite.TFLiteConverter.from_saved_model(easier_model.model_dir)
        else:
            if tf.__version__.split(".")[0] == '1':
                if not os.path.isfile("/tmp/storage/" + easier_model.metadata.name + "." + constants.MODEL_EXTENSION):
                    easier_model.model.save("/tmp/storage/" + easier_model.metadata.name + "." + constants.MODEL_EXTENSION)
                try:
                    K.clear_session()
                except Exception as e:
                    pass
                converter = tf.lite.TFLiteConverter.from_keras_model_file("/tmp/storage/" + easier_model.metadata.name + "." + constants.MODEL_EXTENSION)
            else:    
                converter = tf.lite.TFLiteConverter.from_keras_model(easier_model.model)

        if tf.__version__.split(".")[0] == '1':
            converter.target_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]        
        else:
            converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
        converter.representative_dataset = easier_model.representative_dataset_gen
        converter.inference_input_type = tf.uint8
        converter.inference_output_type = tf.uint8
        converter.optimizations = [tf.lite.Optimize.DEFAULT]

        try:
            tflite_model = converter.convert()
        except Exception as e:
            print("Error converting model to tf lite: " + str(e))
            return

        if easier_model.model_dir is not None:
            open('/tmp/storage/' + easier_model.model_dir + "/" + easier_model.metadata.name + "." + constants.TF_LITE_EXTENSION, "wb").write(
                tflite_model)
            try:
                K.clear_session()
            except Exception as e:
                pass
            print("Converted tf model " + str(easier_model.model_dir) + " to tf lite specific for TPU")
            tpu_model_path = "/tmp/storage/" + easier_model.model_dir + "/" + easier_model.metadata.name + "." + constants.TF_LITE_EXTENSION
            cmd = ['edgetpu_compiler', tpu_model_path, '-o', '/tmp/storage']
            tpu_model_path = "/tmp/storage/" + easier_model.model_dir + "/" + easier_model.metadata.name + "_edgetpu." + constants.TF_LITE_EXTENSION
        else:
            try:
                open('/tmp/storage/' + easier_model.metadata.name + "." + constants.TF_LITE_EXTENSION, "wb").write(
                    tflite_model)
                try:
                    K.clear_session()
                except Exception as e:
                    pass
                print("Converted keras model " + easier_model.metadata.name + " to tf lite specific for TPU")
            except Exception as e:
                print("Error saving tf lite model to file: " + str(e))
                try:
                    K.clear_session()
                except Exception as e:
                    pass
                return
            tpu_model_path = "/tmp/storage/" +  easier_model.metadata.name + "." + constants.TF_LITE_EXTENSION
            cmd = ['edgetpu_compiler', '-o', '/tmp/storage', tpu_model_path]
            tpu_model_path = "/tmp/storage/" +  easier_model.metadata.name + "_edgetpu." + constants.TF_LITE_EXTENSION
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE)
            easier_model.set_tpu_model_path(tpu_model_path)
        except FileNotFoundError as e:
            print('The edge tpu complier is not installed: ' + str(e))
            return
        except Exception as e:
            print('The edge tpu complier throwed an error: ' + str(e))
            return

    # TODO check if necessary
    def _compile_gpu(self):
        pass      
    
    def _dockerize(self, easier_model:EasierModel, image_name:str=None):
        raise NotImplementedError()
    
        if not os.path.isdir("/dockerized_model"): os.mkdir("/dockerized_model")

        easier_model.store(model_path="/dockerized_model", print_files=False)
        if image_name is None: image_name = easier_model.metadata.name + '_' + easier_model._get_random_string()
        cmd = ['docker', 'build', '-f', 'Dockerfile_model', '-t', image_name]
        subprocess.run(cmd, stdout=subprocess.PIPE)

        cmd = ['docker', 'save', image_name, '--output', image_name + '.tar']
        subprocess.run(cmd, stdout=subprocess.PIPE)