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

# Algorithm
LSTM = 'lstm'
DENSE = 'dense'
PHASED_LSTM = 'phasedlstm'
CONV1D = 'conv1D'

# Inference type
ESTIMATOR = 'Estimator'
CLASSIFIER = 'Classifier'

# Data types
TIMESERIES = 'timeseries'

# Activation functions
LINEAR = 'linear'
SOFTMAX = 'softmax'
RELU = 'relu'
SIGMOID = 'sigmoid'

# Monitors
VAL_LOSS = 'val_loss'

# File extensions
PICKLE_EXTENSION = 'pkl'
MODEL_EXTENSION = 'h5'
WEIGHTS_EXTENSION = 'w.h5'
MODEL_STRUCTURE_EXTENSION = 's.json'
SCALER_EXTENSION = 's.pkl'
LABELENCODER_EXTENSION = 'e.pkl'
ONEHOTENCODER_EXTENSION = 'ohe.pkl'
JSON_EXTENSION = 'json'
PREDICTOR = 'predictor'
TF_LITE_EXTENSION = 'tflite'
TPU_EXTENSION = '_edgetpu.tflite'

# Elasticsearch fields
_ID = '_id'

# Logging levels
DEBUG = 'debug'
INFO = 'info'
WARNING = 'warning'
ERROR = 'error'
PERFORMANCE = 'perf'

# Model storage level
FULL = 'full'
WEIGHTS_ONLY = 'weights_only'
CONFIG_ONLY = 'config_only'