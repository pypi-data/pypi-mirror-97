#   Copyright  2020 Atos Spain SA. All rights reserved.
 
#   This file is part of EASIER AI.
 
#   EASIER AI is free software: you can redistribute it and/or modify it under the terms of Apache License, either version 2 of the License, or
#   (at your option) any later version.
 
#   THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT ANY WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING 
#   BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT,
#   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#   WHETHER IN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
#   OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#   See  LICENSE file for full license information  in the project root.

from setuptools import setup, find_packages
 
setup(name='easierSDK',
      version='0.0.76',
      url='https://scm.atosresearch.eu/ari/easier/easier-sdk',
      license='ATOS',
      author='AIDR Unit',
      author_email='adrian.arroyo@atos.net',
      description='This library contains code for interacting with EASIER.AI platform in Python.',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      packages=find_packages(exclude=['easierSDK.tests']),
      install_requires =[
            'minio==6.0.0',
            'tensorflow>=1.14.0',
            'joblib>=0.17.0',
            'scikit-learn==0.23.2',
            'seaborn>=0.11.0',
            'pandas>=1.1.4',
            'h5py < 3.0.0',
            'Pillow==8.1.0',
            'matplotlib==3.3.4',
            'kubernetes==12.0.1'
      ],
      zip_safe=False)
