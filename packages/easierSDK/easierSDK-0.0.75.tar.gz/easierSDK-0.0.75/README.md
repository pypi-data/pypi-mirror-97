# Quick start with EasierSDK

This first tutorial will cover some basic functionalities about interacting with EASIER in oder to "start playing" with the available Models and Datasets in the platform, with these key topics:

*   How to connect the platform
*   Search for Models and Datasets
*   Get information from Models and Datastes
*   Download and play with an image classifier Model
*   Create and upload your first Model




## Getting the library and connecting to the platform

So, lets start downloading the library and login with your EASIER's user. EasierSDK library allows you to interact, donwload, execute these Models and Datasets. 



```
%pip install -U easierSDK
```


```
from easierSDK.easier import EasierSDK
from easierSDK.classes.categories import Categories  
import easierSDK.classes.constants as Constants 
```


```
#- Initializations
easier_access = ""
easier_secret = ""
easier = EasierSDK(easier_user=easier_access, easier_password=easier_secret)

```

## Taking a look to the available Models and Datasets

The first thing you can do is to take a look into the Easier catalogue composed by Models and Datasets. These are organized in different available repositories. Some of them are provided (public) by other users of the platform and also, you will find others officially provided by the Easier provider. Getting the information would take a little bit of time depending on the size of the Repository.


```
repositories = easier.get_repositories_metadata(category=None) # Returns dict of Repo objects

for repo_name in repositories.keys():
  print(repo_name)

```

    adrian.arroyo-public
    jose.gato-public
    easier-public
    easier-private


We can see the public/private repository of our user, but also, other available ones. Lets dig into the one from "easier-public". In order to do this, you can use the dictionary-like python syntax. There are some built-in functions that print the content of the repository for you.




```
repositories["easier-public"].print_models()
print("-----------------------------------------------------------------------------------------------------------------------")
repositories["easier-public"].print_datasets()
```

    MODELS:
    Name                          Category                      Last Modification             Num Experiments               
    seriot_anomaly_detection      Categories.MISC               11:50:00 - 10/12/2015         0                             
    legendary-pokemon-classifier  Categories.MISC               2021/01/15 08:28:52           1                             
    resnet50_v2                   Categories.MISC               11:50:00 - 10/12/2015         4                             
    -----------------------------------------------------------------------------------------------------------------------
    DATASETS:
    Name                          Category                      Last Modification             
    kaggle-pokemon-data           Categories.MISC               2021/01/18 12:41:59           
    kaggle_flowers_recognition    Categories.MISC               2021/01/14 14:26:24           
    robot_sim_decenter_2          Categories.MISC               2020-12-12 12:00:00           
    robot_sim_decenter_4          Categories.MISC               2020-12-12 12:00:00           


This repository contains a set of Models and Datasets, and you can see these are organized by **categories**. So you can use these categories to refine your search finding out your desired Model or Dataset.



```
repositories["easier-public"].print_categories()
print("-----------------------------------------------------------------------------------------------------------------------")
repositories["easier-public"].categories["misc"].pretty_print()
```

    Category                      Num Models                    Num Datasets                  
    health                        0                             0                             
    transport                     0                             0                             
    security                      0                             0                             
    airspace                      0                             0                             
    education                     0                             0                             
    misc                          3                             4                             
    -----------------------------------------------------------------------------------------------------------------------
    MODELS:
    Name                          Category                      Last Modification             Num Experiments               
    seriot_anomaly_detection      Categories.MISC               11:50:00 - 10/12/2015         0                             
    legendary-pokemon-classifier  Categories.MISC               2021/01/15 08:28:52           1                             
    resnet50_v2                   Categories.MISC               11:50:00 - 10/12/2015         4                             
    
    DATASETS:
    Name                          Category                      Last Modification             
    kaggle-pokemon-data           Categories.MISC               2021/01/18 12:41:59           
    kaggle_flowers_recognition    Categories.MISC               2021/01/14 14:26:24           
    robot_sim_decenter_2          Categories.MISC               2020-12-12 12:00:00           
    robot_sim_decenter_4          Categories.MISC               2020-12-12 12:00:00           


Or you can print Models and Datasets separatly per category.



```
repositories["easier-public"].categories["misc"].print_models()
print("-----------------------------------------------------------------------------------------------------------------------")
repositories["easier-public"].categories["misc"].print_datasets()
```

    MODELS:
    Name                          Category                      Last Modification             Num Experiments               
    seriot_anomaly_detection      Categories.MISC               11:50:00 - 10/12/2015         0                             
    legendary-pokemon-classifier  Categories.MISC               2021/01/15 08:28:52           1                             
    resnet50_v2                   Categories.MISC               11:50:00 - 10/12/2015         4                             
    -----------------------------------------------------------------------------------------------------------------------
    DATASETS:
    Name                          Category                      Last Modification             
    kaggle-pokemon-data           Categories.MISC               2021/01/18 12:41:59           
    kaggle_flowers_recognition    Categories.MISC               2021/01/14 14:26:24           
    robot_sim_decenter_2          Categories.MISC               2020-12-12 12:00:00           
    robot_sim_decenter_4          Categories.MISC               2020-12-12 12:00:00           


You can go more in details with each dataset or model using the same syntax.


```
repositories["easier-public"].categories['misc'].datasets["robot_sim_decenter_4"].pretty_print()
```

    Category:                     misc                          
    Name:                         robot_sim_decenter_4          
    Size:                         100                           
    Description:                  DECENTER UC2 simulation images of person and robot
    Last modified:                2020-12-12 12:00:00           
    Version:                      0                             
    Row number:                   0                             
    Features:                     {}                            
    Dataset type:                 images                        
    File extension:               jpeg                          



```
repositories["easier-public"].categories['misc'].models["resnet50_v2"].pretty_print()
```

    Category:                     misc                          
    Name:                         resnet50_v2                   
    Description:                  Pre-trained Keras model, processing functions in: 'tensorflow.keras.applications.resnet50'. Some .jpg are stored as examples.
    Last modified:                11:50:00 - 10/12/2015         
    Version:                      0                             
    Features:                     N/A                           


Great, this one seems pretty interesting, resnet50 models are used to clasify images. Thanks to the respository owner for providing us with such an interesting model. Actualy, it has been already trained, so, it should work out of the box. We could use it to clasify our images. 

## Playing with an existing Model

In our previous search for a cool model, we found a resnet50 trained one. Now we will download it to start clasifying images.

We will use the method get_model from the **Models API** to load the model into an object of type **EasierModel**. 


```
# Returns an object of type EasierModel
easier_resnet_model = easier.models.get_model(repo_name=repositories["easier-public"].name, 
                                              category= Categories.MISC, 
                                              model_name=repositories["easier-public"].categories['misc'].models["resnet50_v2"].name,
                                              experimentID=0)                                            
                                              
```

    WARNING:tensorflow:No training configuration found in the save file, so the model was *not* compiled. Compile it manually.


Each model is available in multiple Experiments (or versions). This time we will take the first one (experimentID=0). By default, if you do not provide the experimentID, it takes the most recent version.
Others versions would work better (or not), would use different algorithms, features, etc. This is up to the provider and it could give your more details with metadata info. For example, for the experimentID=1:



```
# Returns an object of type ModelMetadata
easier.models.show_model_info(repo_name="easier-public", 
                               category=Categories.MISC, 
                               model_name="resnet50_v2", 
                               experimentID=1)
```

    Category:                     misc                          
    Name:                         resnet50_v2                   
    Description:                  resnet50v2 for person vs robot images
    Last modified:                11:50:00 - 10/12/2015         
    Version:                      1                             
    Features:                     N/A                           
    previous_experimentID:        0                             





    <easierSDK.classes.model_metadata.ModelMetadata at 0x7fe7df50b6d0>



In order to play with the original resnet50 model, we will need to use some libraries. In this case we will use the framework Keras. This will require a minimum knowledge about using this framework for preprocessing the images for the model, but not too deep. 



```
import PIL 
from keras.preprocessing.image import load_img 
from keras.preprocessing.image import img_to_array 
from keras.applications.imagenet_utils import decode_predictions 
import matplotlib.pyplot as plt 
import numpy as np 
from keras.applications import resnet50

import matplotlib.pyplot as plt  
```

Well, as an image classifier Model, we will need some images. 

Lets download and prepare the image accordingly to the Model's input. Basically, transform the image into an array. The EasierSDK provides you with a method to turn an image into an array.



```
!wget https://upload.wikimedia.org/wikipedia/commons/a/ac/NewTux.png

```

    --2021-01-21 16:35:59--  https://upload.wikimedia.org/wikipedia/commons/a/ac/NewTux.png
    Resolving upload.wikimedia.org (upload.wikimedia.org)... 91.198.174.208, 2620:0:862:ed1a::2:b
    Connecting to upload.wikimedia.org (upload.wikimedia.org)|91.198.174.208|:443... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 120545 (118K) [image/png]
    Saving to: ‘NewTux.png.2’
    
    NewTux.png.2        100%[===================>] 117,72K  --.-KB/s    in 0,1s    
    
    2021-01-21 16:35:59 (985 KB/s) - ‘NewTux.png.2’ saved [120545/120545]
    



```
filename = './NewTux.png'

original = load_img(filename, target_size = (224, 224)) 
plt.imshow(original) 
plt.show()

# Transform image into an array to use as input for models
image_batch= easier.datasets.codify_image(filename, target_size = (224, 224))

```


    
![png](EASIER_SDK_files/EASIER_SDK_25_0.png)
    


So ths is a nice Tux, let see what our classifier says about it, easily with:


```
processed_image = resnet50.preprocess_input(image_batch.copy())

predictions = easier_resnet_model.get_model().predict(processed_image) 
# convert the probabilities to class labels 
label = decode_predictions(predictions) 

print(label)
```

    [[('n04286575', 'spotlight', 0.24322352), ('n04557648', 'water_bottle', 0.083833), ('n04380533', 'table_lamp', 0.058811724), ('n04328186', 'stopwatch', 0.048403606), ('n03793489', 'mouse', 0.039514534)]]


It seems the model is not very sure about what this image is about ;). As you can see, accessing the model is very easy with the **get_model()** method of the object.

Now we will try again with other images. But this time, instead of dowloading from internet, we will use an available dataset in EASIER (containing images). We have previously seen one about flowers inside the EASIER Repository:


```
repositories["easier-public"].categories['misc'].datasets["kaggle_flowers_recognition"].pretty_print()
```

    Category:                     misc                          
    Name:                         kaggle_flowers_recognition    
    Size:                         228.29                        
    Description:                  Kaggle Flowers Recognition Dataset from: https://www.kaggle.com/alxmamaev/flowers-recognition
    Last modified:                2021/01/14 14:26:24           
    Version:                      0                             
    Row number:                   0                             
    Features:                     []                            
    Dataset type:                 images                        
    File extension:               zip                           


EasierSDK provides a method to donwload a selected DataSet locally.


```
success = easier.datasets.download(repo_name="easier-public", 
                         category=Categories.MISC, 
                         dataset_name="kaggle_flowers_recognition", 
                         path_to_download="./")
```

Let's unzip the content of the dataset.


```
!unzip  ./datasets/misc/kaggle_flowers_recognition/flowers_kaggle_dataset.zip -d datasets/misc/kaggle_flowers_recognition/
```

Now, let's plot an image of this dataset.


```
filename = './datasets/misc/kaggle_flowers_recognition/flowers/sunflower/1022552002_2b93faf9e7_n.jpg'

image_batch = easier.datasets.codify_image(filename)

original = load_img(filename, target_size = (224, 224)) 
plt.imshow(original) 
plt.show()
```


    
![png](EASIER_SDK_files/EASIER_SDK_35_0.png)
    


This image is ok and shows a nice flower. Could the classifier  detect it correctly?


```
processed_image = resnet50.preprocess_input(image_batch.copy())

predictions = easier_resnet_model.get_model().predict(processed_image) 
# convert the probabilities to class labels 
label = decode_predictions(predictions) 

print(label)
```

    [[('n11939491', 'daisy', 0.9527386), ('n04522168', 'vase', 0.016293569), ('n11879895', 'rapeseed', 0.008986354), ('n02190166', 'fly', 0.0033192327), ('n02206856', 'bee', 0.0023540645)]]


Great job, it detects it is a flower. Actually, **it detects it is a daisy flower. With a probability of 95%.**

In summary, in this tutorial we have learnt how to play with the different models, make predictions and download existing datasets.

## Create your very first simple Model

This is a very simple example to create an Model in EASIER. The model will not be trained but, instead, we will focus on how to interact with EASIER in order to save your model. 

Let's first use Tensorflow to create and compile a simple sequential model for binary classification:


```
import tensorflow as tf

# - Create model from scratch
my_tf_model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(224,)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.1),
    tf.keras.layers.Dense(1, activation="sigmoid")
  ])

my_tf_model.compile(optimizer='adam',
            loss=tf.keras.losses.categorical_crossentropy,
            metrics=[tf.keras.metrics.mean_squared_error])

my_tf_model.summary()
```

    Model: "sequential"
    _________________________________________________________________
    Layer (type)                 Output Shape              Param #   
    =================================================================
    dense (Dense)                (None, 128)               28800     
    _________________________________________________________________
    dropout (Dropout)            (None, 128)               0         
    _________________________________________________________________
    dense_1 (Dense)              (None, 64)                8256      
    _________________________________________________________________
    dropout_1 (Dropout)          (None, 64)                0         
    _________________________________________________________________
    dense_2 (Dense)              (None, 1)                 65        
    =================================================================
    Total params: 37,121
    Trainable params: 37,121
    Non-trainable params: 0
    _________________________________________________________________


Now that we have our tensorflow model, let's create an **EasierModel** object that will be the placeholder for it, as long as some other model-related objects like the scaler or the label encoder.


```
from easierSDK.classes.easier_model import EasierModel

# Create Easier Model
my_easier_model = EasierModel()

# Set the tensorflow model 
my_easier_model.set_model(my_tf_model)
```

Now that we have our model in our EASIER placeholder, we need to create some metadata for it, before being allowed to upload the model to the platform. 

You can use the ModelMetadata class for that:


```
from easierSDK.classes.model_metadata import ModelMetadata
from datetime import datetime

# # - Create ModelMetadata
mymodel_metadata = ModelMetadata()
mymodel_metadata.category = Categories.HEALTH
mymodel_metadata.name = 'my-simple-classifier'
mymodel_metadata.last_modified = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
mymodel_metadata.description = 'My Simple Clasifier'
mymodel_metadata.version = 0
mymodel_metadata.features = []

my_easier_model.set_metadata(mymodel_metadata)
```

Now that our model has some metadata information, let's upload it to our private repository. We can download later on this model to continue working with it. 


```
success = easier.models.upload(easier_model=my_easier_model)
```

    Uploaded model: 
    
    Category:                     health                        
    Name:                         my-simple-classifier          
    Description:                  My Simple Clasifier           
    Last modified:                2021/01/21 16:40:16           
    Version:                      3                             
    Features:                     []                            
    previous_experimentID:        0                             


## Create a new Dataset

You can create an EASIER Dataset from any kind of data: images, csv, files, whatever. Here as an example, we will use the [Columbia University Image Library](https://www1.cs.columbia.edu/CAVE/software/softlib/coil-100.php)


```
!wget http://www.cs.columbia.edu/CAVE/databases/SLAM_coil-20_coil-100/coil-100/coil-100.tar.gz 
!mkdir -p ./datasets/misc/coil-100-objects/
!tar -xf ./coil-100.tar.gz -C ./datasets/misc/coil-100-objects/
```

    --2021-01-21 16:40:27--  http://www.cs.columbia.edu/CAVE/databases/SLAM_coil-20_coil-100/coil-100/coil-100.tar.gz
    Resolving www.cs.columbia.edu (www.cs.columbia.edu)... 128.59.11.206
    Connecting to www.cs.columbia.edu (www.cs.columbia.edu)|128.59.11.206|:80... connected.
    HTTP request sent, awaiting response... 301 Moved Permanently
    Location: https://www.cs.columbia.edu/CAVE/databases/SLAM_coil-20_coil-100/coil-100/coil-100.tar.gz [following]
    --2021-01-21 16:40:27--  https://www.cs.columbia.edu/CAVE/databases/SLAM_coil-20_coil-100/coil-100/coil-100.tar.gz
    Connecting to www.cs.columbia.edu (www.cs.columbia.edu)|128.59.11.206|:443... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 261973331 (250M) [application/x-gzip]
    Saving to: ‘coil-100.tar.gz.1’
    
    coil-100.tar.gz.1    61%[===========>        ] 154,74M  17,7MB/s    eta 7s     ^C
    ^C


Now, like the previous example, we will use the Datasets API to create a new **EasierDataset**. First, let's fill the proper Metadata and, then, we can upload it to our repository.


```
from datetime import datetime
from easierSDK.classes.dataset_metadata import DatasetMetadata


metadata = DatasetMetadata()
metadata.category = Categories.MISC
metadata.name = 'coil-100'
metadata.last_modified = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
metadata.description = "Columbia University Image Library - Objects in ppm format"
metadata.size = 125
metadata.dataset_type = "images"
metadata.file_extension = ".tar.gz"

```

With your Dataset downloaded and the DatasetMetadata completed, you can invoke the method upload. This method will take a directory as parameter and make a compressed file with all the content inside it. When uploading the data, it will also attach the filled metadata. We will make it available in our public repository under Misc category.


```
easier.datasets.upload(category=metadata.category,
                       dataset_name=metadata.name, 
                       local_path="./datasets/misc/coil-100-objects", 
                       metadata=metadata, 
                       public=True) 
```

    Finished uploading dataset with no errors.





    True



FInally, we will take a last look to **our repository** to check if our Dataset is available.  The easier object contains information about the name of your public and private repo. You can use it as index to search for the Dataset we have just upload with your user. First, It is needed to refresh our repositories variable



```
repositories = easier.get_repositories_metadata(category=None) # Returns dict of Repo objects
repositories[easier.my_public_repo].print_datasets()
```

    DATASETS:
    Name                          Category                      Last Modification             
    coil-100                      Categories.MISC               2021/01/21 16:40:42           



```
repositories[easier.my_public_repo].categories['misc'].datasets["coil-100"].pretty_print()
```

    Category:                     misc                          
    Name:                         coil-100                      
    Size:                         125                           
    Description:                  Columbia University Image Library - Objects in ppm format
    Last modified:                2021/01/21 16:40:42           
    Version:                      0                             
    Row number:                   0                             
    Features:                     {}                            
    Dataset type:                 images                        
    File extension:               .tar.gz                       


# Advanced tutorials

These tutorials aim for more advanced users, they require some prior knowledge about developing ML/DL models and using the Tensorflow framework. However, every step taken is very state of art and everything is very well explained.

## [Advanced User] Create a new model from scratch (Pokemons Classifier)

---



In the previous tutorial *Creating your very first simple Model*, we created an empty (no functional) Model. This time we will create a more serious one, to clasify Pokemons. We will create the model from scratch, we will use an exsiting Dataset from EASIER repository, and finally, we will upload this new model to our repository of models.  


```
repositories["easier-public"].categories['misc'].datasets["kaggle-pokemon-data"].pretty_print()
```

    Category:                     misc                          
    Name:                         kaggle-pokemon-data           
    Size:                         10400                         
    Description:                  Pokemon Data from Kaggle      
    Last modified:                2021/01/18 12:41:59           
    Version:                      0                             
    Row number:                   800                           
    Features:                     ['#', 'Name', 'Type 1', 'Type 2', 'Total', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Generation', 'Legendary']
    Dataset type:                 structured                    
    File extension:               csv                           


We see that the creator filled the **features** information on the dataset's metadata showing that it is a typical structured dataset. Let's download the dataset.


```
easier.datasets.download(repo_name="easier-public", category=Categories.MISC, dataset_name="kaggle-pokemon-data", path_to_download="./")
```




    True



Let's see what's we have downloaded. The download method will create a structure of folders, following the same structure of the repositories: two main folders **datasets and models**. In this case, the dataset belongs to Category MISC, so the data is downloaded into this folder. Inside it, there will be a folder with the same name as the dataset:


```
!ls  ./datasets/misc/kaggle-pokemon-data/
```

    kaggle-pokemon-data.tar.gz  metadata.json  pokemon


Let's uncompress the data


```
!tar -xvf  ./datasets/misc/kaggle-pokemon-data/kaggle-pokemon-data.tar.gz -C  ./datasets/misc/kaggle-pokemon-data/
```

    pokemon/
    pokemon/pokemon_data/
    pokemon/pokemon_data/data.txt
    pokemon/Pokemon.csv



```
!ls  ./datasets/misc/kaggle-pokemon-data/pokemon
```

    Pokemon.csv  pokemon_data


We see that the data is placed in a .csv file. Let's load the data into a DataFrame. The datasets API has a built-in method for loading csv files into **pandas DataFrames**. Or, you can load the data as you prefer ;)


```
pokemon_df = easier.datasets.load_csv(local_path="./datasets/misc/kaggle-pokemon-data/pokemon/Pokemon.csv", separator=',')
```


```
print(pokemon_df.describe())
print(pokemon_df.info())
```

                    #      Total          HP      Attack     Defense     Sp. Atk  \
    count  800.000000  800.00000  800.000000  800.000000  800.000000  800.000000   
    mean   362.813750  435.10250   69.258750   79.001250   73.842500   72.820000   
    std    208.343798  119.96304   25.534669   32.457366   31.183501   32.722294   
    min      1.000000  180.00000    1.000000    5.000000    5.000000   10.000000   
    25%    184.750000  330.00000   50.000000   55.000000   50.000000   49.750000   
    50%    364.500000  450.00000   65.000000   75.000000   70.000000   65.000000   
    75%    539.250000  515.00000   80.000000  100.000000   90.000000   95.000000   
    max    721.000000  780.00000  255.000000  190.000000  230.000000  194.000000   
    
              Sp. Def       Speed  Generation  
    count  800.000000  800.000000   800.00000  
    mean    71.902500   68.277500     3.32375  
    std     27.828916   29.060474     1.66129  
    min     20.000000    5.000000     1.00000  
    25%     50.000000   45.000000     2.00000  
    50%     70.000000   65.000000     3.00000  
    75%     90.000000   90.000000     5.00000  
    max    230.000000  180.000000     6.00000  
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 800 entries, 0 to 799
    Data columns (total 13 columns):
     #   Column      Non-Null Count  Dtype 
    ---  ------      --------------  ----- 
     0   #           800 non-null    int64 
     1   Name        800 non-null    object
     2   Type 1      800 non-null    object
     3   Type 2      414 non-null    object
     4   Total       800 non-null    int64 
     5   HP          800 non-null    int64 
     6   Attack      800 non-null    int64 
     7   Defense     800 non-null    int64 
     8   Sp. Atk     800 non-null    int64 
     9   Sp. Def     800 non-null    int64 
     10  Speed       800 non-null    int64 
     11  Generation  800 non-null    int64 
     12  Legendary   800 non-null    bool  
    dtypes: bool(1), int64(9), object(3)
    memory usage: 75.9+ KB
    None


We see that there is a column *Legendary* with boolean type. We can use that column as the label to build a binary classifier of pokemons being legendary or not, according to the data of the rest of the columns.

Let's clear the dataframe first:


```
pokemon_df = pokemon_df.drop(columns=["#", "Name"])
pokemon_df = pokemon_df.dropna()
```

Before doing any more operations, we see that there are two columns with type *object*: 'Type 1' and 'Type 2'. This means that they are probably categorical data:


```
print(pokemon_df['Type 1'].values[0])

print(pokemon_df['Type 2'].values[0])
```

    Grass
    Poison


This data needs to be encoded so that our Tensorflow model is able to learn from it. There are many ways of doing this operation and you can do it as you think is the best. 

The datasets API also includes a method to encode this kind of data, using a *One Hot Encoder* from SKLearn. Let's use that function. We can pass the label *Legenday* as parameter since it is not going to be used for training. We will get in return a pandas DataFrame with the encoded data in new columns, and the encoder object used to encode the data. 


```
encoded_pokemon, one_hot_encoder = easier.datasets.one_hot_encode_data(pokemon_df, labels=["Legendary"])
```


```
encoded_pokemon.info()
```

    <class 'pandas.core.frame.DataFrame'>
    Int64Index: 207 entries, 0 to 413
    Data columns (total 46 columns):
     #   Column      Non-Null Count  Dtype  
    ---  ------      --------------  -----  
     0   index       207 non-null    float64
     1   Total       207 non-null    float64
     2   HP          207 non-null    float64
     3   Attack      207 non-null    float64
     4   Defense     207 non-null    float64
     5   Sp. Atk     207 non-null    float64
     6   Sp. Def     207 non-null    float64
     7   Speed       207 non-null    float64
     8   Generation  207 non-null    float64
     9   0           207 non-null    float64
     10  1           207 non-null    float64
     11  2           207 non-null    float64
     12  3           207 non-null    float64
     13  4           207 non-null    float64
     14  5           207 non-null    float64
     15  6           207 non-null    float64
     16  7           207 non-null    float64
     17  8           207 non-null    float64
     18  9           207 non-null    float64
     19  10          207 non-null    float64
     20  11          207 non-null    float64
     21  12          207 non-null    float64
     22  13          207 non-null    float64
     23  14          207 non-null    float64
     24  15          207 non-null    float64
     25  16          207 non-null    float64
     26  17          207 non-null    float64
     27  18          207 non-null    float64
     28  19          207 non-null    float64
     29  20          207 non-null    float64
     30  21          207 non-null    float64
     31  22          207 non-null    float64
     32  23          207 non-null    float64
     33  24          207 non-null    float64
     34  25          207 non-null    float64
     35  26          207 non-null    float64
     36  27          207 non-null    float64
     37  28          207 non-null    float64
     38  29          207 non-null    float64
     39  30          207 non-null    float64
     40  31          207 non-null    float64
     41  32          207 non-null    float64
     42  33          207 non-null    float64
     43  34          207 non-null    float64
     44  35          207 non-null    float64
     45  Legendary   207 non-null    object 
    dtypes: float64(45), object(1)
    memory usage: 76.0+ KB


There are now quite a bit more columns ;).

The next step should be to encode the labels into an understandable format. Similarly, you can use your own method, but the datasets API has also a built-in method to do it for you, using a *Label Encoder* object from SKLearn. 


```
labels, label_encoder = easier.datasets.encode_labels(encoded_pokemon, labels=["Legendary"])
```


```
print(encoded_pokemon.values[0])
print(labels[0])
```

    [0.0 318.0 45.0 49.0 49.0 65.0 65.0 45.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
     0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
     0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 False]
    [1. 0.]


Class [1 0] will be a non-legendary pokemon, and class [0 1] will be for a legendary pokemon.

Final step before being able to train is to scale the data into a typical DL range. Same as before, you can bring or create your own scaler, but the datasets API has a built-in one. It also allows you to pass the range of the scaled data. Similarly, it will return the scaled data in a pandas DataFrame and the scaler used, in this case a *MinMaxScaler* from SKLearn.


```
scaled_pokemon, scaler = easier.datasets.scale_data(encoded_pokemon.drop(columns=["Legendary"]), ft_range=(0, 1))
```

Let's divide the data into train and test. The datasets API can also do that for us. It even accepts the split ratio, by default it is 80% of the data for training and 20% for testing.  


```
x_train, y_train, x_test, y_test = easier.datasets.train_test_split_data(scaled_pokemon, labels)
```

Now that our data is ready to be used in a Tensorflow model, let's create one:


```
# - Create model from scratch
import tensorflow as tf

my_tf_model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(x_train.shape[1],)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.1),
    tf.keras.layers.Dense(len(label_encoder.classes_))
  ])

my_tf_model.compile(optimizer='adam',
            loss=tf.keras.losses.categorical_crossentropy,
            metrics=[tf.keras.metrics.mean_squared_error])
my_tf_model.summary()
```

    Model: "sequential_1"
    _________________________________________________________________
    Layer (type)                 Output Shape              Param #   
    =================================================================
    dense_3 (Dense)              (None, 128)               5888      
    _________________________________________________________________
    dropout_2 (Dropout)          (None, 128)               0         
    _________________________________________________________________
    dense_4 (Dense)              (None, 64)                8256      
    _________________________________________________________________
    dropout_3 (Dropout)          (None, 64)                0         
    _________________________________________________________________
    dense_5 (Dense)              (None, 2)                 130       
    =================================================================
    Total params: 14,274
    Trainable params: 14,274
    Non-trainable params: 0
    _________________________________________________________________


Let's fit the model to our data and test it against our validation data. We'll do only 10 epochs so that it does not take much time, as this is only the tutorial.




```
my_tf_model.fit(x_train, y_train, epochs=10, validation_split=0.1)

scores = my_tf_model.evaluate(x_test, y_test, verbose=1)
```

    Epoch 1/10
    5/5 [==============================] - 1s 76ms/step - loss: 2.4325 - mean_squared_error: 0.6744 - val_loss: 0.0774 - val_mean_squared_error: 0.8471
    Epoch 2/10
    5/5 [==============================] - 0s 13ms/step - loss: 0.6087 - mean_squared_error: 0.9572 - val_loss: 0.0062 - val_mean_squared_error: 1.0861
    Epoch 3/10
    5/5 [==============================] - 0s 14ms/step - loss: 0.9383 - mean_squared_error: 1.1683 - val_loss: 0.0027 - val_mean_squared_error: 1.2019
    Epoch 4/10
    5/5 [==============================] - 0s 14ms/step - loss: 0.5629 - mean_squared_error: 1.2896 - val_loss: 0.0210 - val_mean_squared_error: 1.2601
    Epoch 5/10
    5/5 [==============================] - 0s 14ms/step - loss: 0.9354 - mean_squared_error: 1.3206 - val_loss: 0.0372 - val_mean_squared_error: 1.2976
    Epoch 6/10
    5/5 [==============================] - 0s 13ms/step - loss: 0.1897 - mean_squared_error: 1.3742 - val_loss: 0.0481 - val_mean_squared_error: 1.3225
    Epoch 7/10
    5/5 [==============================] - 0s 14ms/step - loss: 0.4628 - mean_squared_error: 1.3869 - val_loss: 0.0483 - val_mean_squared_error: 1.3395
    Epoch 8/10
    5/5 [==============================] - 0s 15ms/step - loss: 0.2216 - mean_squared_error: 1.4494 - val_loss: 0.0455 - val_mean_squared_error: 1.3503
    Epoch 9/10
    5/5 [==============================] - 0s 14ms/step - loss: 0.7074 - mean_squared_error: 1.4282 - val_loss: 0.0406 - val_mean_squared_error: 1.3624
    Epoch 10/10
    5/5 [==============================] - 0s 15ms/step - loss: 0.4242 - mean_squared_error: 1.4443 - val_loss: 0.0404 - val_mean_squared_error: 1.3601
    2/2 [==============================] - 0s 3ms/step - loss: 0.0165 - mean_squared_error: 1.6065



```
print(my_tf_model.metrics_names[0] + " = " + str(scores[0]))
print(my_tf_model.metrics_names[1] + " = " + str(scores[1]))
```

    loss = 0.016472503542900085
    mean_squared_error = 1.6064611673355103


We can see that we did not do so bad, even for 10 epochs :).

Now that we have our trained model, it is time to upload it to our repository. First, let's create some metadata for it


```
# # - Create ModelMetadata
import datetime
from easierSDK.classes.model_metadata import ModelMetadata

mymodel_metadata = ModelMetadata()
mymodel_metadata.category = Categories.MISC
mymodel_metadata.name = 'legendary-pokemon-classifier'
mymodel_metadata.last_modified = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
mymodel_metadata.description = 'My Clasifier of Legendary Pokemons implementation'
mymodel_metadata.version = 0
mymodel_metadata.features = pokemon_df.columns.values.tolist()


mymodel_metadata.pretty_print()
```

    Category:                     misc                          
    Name:                         legendary-pokemon-classifier  
    Description:                  My Clasifier of Legendary Pokemons implementation
    Last modified:                2021/01/21 16:49:41           
    Version:                      0                             
    Features:                     ['Type 1', 'Type 2', 'Total', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Generation', 'Legendary']


Now that we have the metadata, let's create an EasierModel and store our trained model.


```
from easierSDK.classes.easier_model import EasierModel

my_easier_model = EasierModel()
my_easier_model.set_metadata(mymodel_metadata)
my_easier_model.set_model(my_tf_model)
```

Remember all the encoders that we used? the EasierModel object has a placeholder for them:


```
my_easier_model.set_label_encoder(label_encoder)
my_easier_model.set_feature_encoder(one_hot_encoder)
my_easier_model.set_scaler(scaler)
```

There are getters and setters for every attribute of the EasierModel object:


```
my_easier_model.get_model()
```




    <tensorflow.python.keras.engine.sequential.Sequential at 0x7fe7ff9e3fd0>




```
my_easier_model.get_scaler()
```




    MinMaxScaler()



Now that we have our trained model inside an EasierModel variable, along with the scalers used to train the model, let's upload it to our public repository. All the objects, including the encoders and the scalers, will be uploaded.


```
success = easier.models.upload(my_easier_model, public=True)
```

    Uploaded model: 
    
    Category:                     misc                          
    Name:                         legendary-pokemon-classifier  
    Description:                  My Clasifier of Legendary Pokemons implementation
    Last modified:                2021/01/21 16:50:00           
    Version:                      2                             
    Features:                     ['Type 1', 'Type 2', 'Total', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Generation', 'Legendary']
    previous_experimentID:        0                             


Let's refresh the repositories data and see the model uploaded:


```
repositories = easier.get_repositories_metadata()
```


```
repositories[easier.my_public_repo].categories["misc"].models["legendary-pokemon-classifier"].pretty_print()
```

    Category:                     misc                          
    Name:                         legendary-pokemon-classifier  
    Description:                  My Clasifier of Legendary Pokemons implementation
    Last modified:                2021/01/19 12:15:58           
    Version:                      0                             
    Features:                     ['Type 1', 'Type 2', 'Total', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Generation', 'Legendary']
    previous_experimentID:        0                             


By default, the upload method not only uploads the model into a '.h5` file, but also it uploads the weights and the model config in separate files. The function has a parameter to modify the kind of upload you want, in case you only want to upload the model weights, for example. There is also a built-in method for checking a model's configuration from the repository:


```
easier.models.show_model_config(repo_name="jose.gato-public",
                                category=Categories.MISC,
                                model_name="legendary-pokemon-classifier",
                                experimentID=0)
```

    {"class_name": "Sequential", "config": {"name": "sequential_1", "layers": [{"class_name": "InputLayer", "config": {"batch_input_shape": [null, 45], "dtype": "float32", "sparse": false, "ragged": false, "name": "dense_5_input"}}, {"class_name": "Dense", "config": {"name": "dense_5", "trainable": true, "batch_input_shape": [null, 45], "dtype": "float32", "units": 128, "activation": "relu", "use_bias": true, "kernel_initializer": {"class_name": "GlorotUniform", "config": {"seed": null}}, "bias_initializer": {"class_name": "Zeros", "config": {}}, "kernel_regularizer": null, "bias_regularizer": null, "activity_regularizer": null, "kernel_constraint": null, "bias_constraint": null}}, {"class_name": "Dropout", "config": {"name": "dropout_4", "trainable": true, "dtype": "float32", "rate": 0.2, "noise_shape": null, "seed": null}}, {"class_name": "Dense", "config": {"name": "dense_6", "trainable": true, "dtype": "float32", "units": 64, "activation": "relu", "use_bias": true, "kernel_initializer": {"class_name": "GlorotUniform", "config": {"seed": null}}, "bias_initializer": {"class_name": "Zeros", "config": {}}, "kernel_regularizer": null, "bias_regularizer": null, "activity_regularizer": null, "kernel_constraint": null, "bias_constraint": null}}, {"class_name": "Dropout", "config": {"name": "dropout_5", "trainable": true, "dtype": "float32", "rate": 0.1, "noise_shape": null, "seed": null}}, {"class_name": "Dense", "config": {"name": "dense_7", "trainable": true, "dtype": "float32", "units": 2, "activation": "linear", "use_bias": true, "kernel_initializer": {"class_name": "GlorotUniform", "config": {"seed": null}}, "bias_initializer": {"class_name": "Zeros", "config": {}}, "kernel_regularizer": null, "bias_regularizer": null, "activity_regularizer": null, "kernel_constraint": null, "bias_constraint": null}}]}, "keras_version": "2.4.0", "backend": "tensorflow"}





    '{"class_name": "Sequential", "config": {"name": "sequential_1", "layers": [{"class_name": "InputLayer", "config": {"batch_input_shape": [null, 45], "dtype": "float32", "sparse": false, "ragged": false, "name": "dense_5_input"}}, {"class_name": "Dense", "config": {"name": "dense_5", "trainable": true, "batch_input_shape": [null, 45], "dtype": "float32", "units": 128, "activation": "relu", "use_bias": true, "kernel_initializer": {"class_name": "GlorotUniform", "config": {"seed": null}}, "bias_initializer": {"class_name": "Zeros", "config": {}}, "kernel_regularizer": null, "bias_regularizer": null, "activity_regularizer": null, "kernel_constraint": null, "bias_constraint": null}}, {"class_name": "Dropout", "config": {"name": "dropout_4", "trainable": true, "dtype": "float32", "rate": 0.2, "noise_shape": null, "seed": null}}, {"class_name": "Dense", "config": {"name": "dense_6", "trainable": true, "dtype": "float32", "units": 64, "activation": "relu", "use_bias": true, "kernel_initializer": {"class_name": "GlorotUniform", "config": {"seed": null}}, "bias_initializer": {"class_name": "Zeros", "config": {}}, "kernel_regularizer": null, "bias_regularizer": null, "activity_regularizer": null, "kernel_constraint": null, "bias_constraint": null}}, {"class_name": "Dropout", "config": {"name": "dropout_5", "trainable": true, "dtype": "float32", "rate": 0.1, "noise_shape": null, "seed": null}}, {"class_name": "Dense", "config": {"name": "dense_7", "trainable": true, "dtype": "float32", "units": 2, "activation": "linear", "use_bias": true, "kernel_initializer": {"class_name": "GlorotUniform", "config": {"seed": null}}, "bias_initializer": {"class_name": "Zeros", "config": {}}, "kernel_regularizer": null, "bias_regularizer": null, "activity_regularizer": null, "kernel_constraint": null, "bias_constraint": null}}]}, "keras_version": "2.4.0", "backend": "tensorflow"}'



This gives us information about the layers, activation functions and other parameters of the model, without the need to load the model itself into memory.

## [Advanced User] Creating a new version of a model after a transfer learning technique: Model experiments

In this  tutorial, we will explore the concept of **model experiments in EASIER**. Taking an existing model as a base, we will make some modifications (new version or experiment), in order to solve a different problem. The baseline model will be an existing resnet model (image clasifier), and we will re-train it to support the distinction between humans and robots. We will use an existing Dataset with robots/humans images.

First, let's load the dataset that is in 'easier-public' repository.


```
repositories["easier-public"].categories['misc'].datasets["robot_sim_decenter_4"].pretty_print()
```

    Category:                     misc                          
    Name:                         robot_sim_decenter_4          
    Size:                         100                           
    Description:                  DECENTER UC2 simulation images of person and robot
    Last modified:                2020-12-12 12:00:00           
    Version:                      0                             
    Row number:                   0                             
    Features:                     {}                            
    Dataset type:                 images                        
    File extension:               jpeg                          



```
easier.datasets.download(repo_name="easier-public", category=Categories.MISC, dataset_name="robot_sim_decenter_4", path_to_download="./")
```




    True




```
!tar -xvf datasets/misc/robot_sim_decenter_4/robot_sim_decenter_4.tar.gz -C datasets/misc/robot_sim_decenter_4/
```


We can see that the dataset is already separated into training and testing. There are some images in '.jpg' format. Some of them belong to a person and others to a robot. Every image is taken from a simulation environment.


```
!ls datasets/misc/robot_sim_decenter_4/JPEG_Images/train
```

    uc2-0001_person_front.jpg  uc2-0030_robot_front.jpg   uc2-0054_robot_rear.jpg
    uc2-0001_robot_front.jpg   uc2-0031_person__1.31.jpg  uc2-0055_person__1.31.jpg
    uc2-0001_robot_rear.jpg    uc2-0031_person_1.83.jpg   uc2-0055_person_rear.jpg
    uc2-0003_robot_front.jpg   uc2-0031_robot_rear.jpg    uc2-0056_person_1.83.jpg
    uc2-0003_robot_rear.jpg    uc2-0032_person__1.83.jpg  uc2-0056_person_front.jpg
    uc2-0004_person_front.jpg  uc2-0032_person_1.83.jpg   uc2-0056_robot_rear.jpg
    uc2-0005_person__1.31.jpg  uc2-0032_person_rear.jpg   uc2-0057_person_1.83.jpg
    uc2-0005_robot_front.jpg   uc2-0032_robot_front.jpg   uc2-0057_person_front.jpg
    uc2-0005_robot_rear.jpg    uc2-0033_person_front.jpg  uc2-0057_person_rear.jpg
    uc2-0007_person_front.jpg  uc2-0033_robot_rear.jpg    uc2-0058_person_1.83.jpg
    uc2-0007_robot_front.jpg   uc2-0034_person__1.83.jpg  uc2-0058_person_front.jpg
    uc2-0007_robot_rear.jpg    uc2-0034_robot_front.jpg   uc2-0058_robot_rear.jpg
    uc2-0009_person_1.31.jpg   uc2-0035_person_rear.jpg   uc2-0059_person_1.83.jpg
    uc2-0009_person_front.jpg  uc2-0035_robot_rear.jpg    uc2-0059_person_front.jpg
    uc2-0009_person_rear.jpg   uc2-0036_robot_front.jpg   uc2-0060_person_1.83.jpg
    uc2-0010_person__1.83.jpg  uc2-0037_robot_rear.jpg    uc2-0060_person_front.jpg
    uc2-0011_person_1.31.jpg   uc2-0038_person_front.jpg  uc2-0060_person_rear.jpg
    uc2-0011_robot_front.jpg   uc2-0038_robot_front.jpg   uc2-0061_person_1.83.jpg
    uc2-0012_person__1.83.jpg  uc2-0039_person__1.83.jpg  uc2-0061_person_front.jpg
    uc2-0012_person_rear.jpg   uc2-0039_person_rear.jpg   uc2-0061_robot_front.jpg
    uc2-0013_person_1.31.jpg   uc2-0039_robot_rear.jpg    uc2-0062_person__1.83.jpg
    uc2-0013_person_front.jpg  uc2-0040_robot_front.jpg   uc2-0062_person_1.83.jpg
    uc2-0013_robot_front.jpg   uc2-0041_person_rear.jpg   uc2-0062_person_front.jpg
    uc2-0014_person__1.83.jpg  uc2-0042_person_1.83.jpg   uc2-0063_person_1.83.jpg
    uc2-0015_person_1.31.jpg   uc2-0042_person_front.jpg  uc2-0063_person_front.jpg
    uc2-0016_person__1.31.jpg  uc2-0042_robot_front.jpg   uc2-0063_person_rear.jpg
    uc2-0016_person__1.83.jpg  uc2-0043_person_1.83.jpg   uc2-0063_robot_front.jpg
    uc2-0016_person_front.jpg  uc2-0044_person__1.31.jpg  uc2-0064_person_rear.jpg
    uc2-0016_robot_rear.jpg    uc2-0047_person_front.jpg  uc2-0065_person_rear.jpg
    uc2-0018_person_rear.jpg   uc2-0047_person_rear.jpg   uc2-0065_robot_front.jpg
    uc2-0018_robot_rear.jpg    uc2-0048_person_1.31.jpg   uc2-0065_robot_rear.jpg
    uc2-0019_person__1.83.jpg  uc2-0048_person_1.83.jpg   uc2-0066_person_rear.jpg
    uc2-0020_person_1.83.jpg   uc2-0048_robot_rear.jpg    uc2-0067_person__1.31.jpg
    uc2-0020_robot_rear.jpg    uc2-0049_person_1.31.jpg   uc2-0067_person_rear.jpg
    uc2-0021_person_1.83.jpg   uc2-0050_person_1.31.jpg   uc2-0067_robot_front.jpg
    uc2-0022_person_front.jpg  uc2-0050_person__1.83.jpg  uc2-0067_robot_rear.jpg
    uc2-0022_person_rear.jpg   uc2-0050_person_front.jpg  uc2-0068_person_rear.jpg
    uc2-0022_robot_rear.jpg    uc2-0050_person_rear.jpg   uc2-0069_person_rear.jpg
    uc2-0025_person__1.83.jpg  uc2-0050_robot_rear.jpg    uc2-0069_robot_front.jpg
    uc2-0026_person_front.jpg  uc2-0051_person_1.31.jpg   uc2-0069_robot_rear.jpg
    uc2-0027_person__1.83.jpg  uc2-0052_person_rear.jpg   uc2-0070_person_rear.jpg
    uc2-0027_person_rear.jpg   uc2-0052_robot_rear.jpg    uc2-0071_person_rear.jpg
    uc2-0029_person_front.jpg  uc2-0053_person_1.83.jpg   uc2-0071_robot_front.jpg
    uc2-0030_person__1.83.jpg  uc2-0053_person_front.jpg



```
from keras.preprocessing.image import load_img 
import matplotlib.pyplot as plt 

image = 'datasets/misc/robot_sim_decenter_4/JPEG_Images/train/uc2-0007_robot_front.jpg' 

img = load_img(image, target_size = (224, 224)) 
plt.imshow(img) 
plt.show()
```


    
![png](EASIER_SDK_files/EASIER_SDK_113_0.png)
    


Let's explore the models in 'easier-public' repository to see if we can use any model.


```
repositories["easier-public"].print_models()
```

    MODELS:
    Name                          Category                      Last Modification             Num Experiments               
    seriot_anomaly_detection      Categories.MISC               11:50:00 - 10/12/2015         0                             
    legendary-pokemon-classifier  Categories.MISC               2021/01/15 08:28:52           1                             
    resnet50_v2                   Categories.MISC               11:50:00 - 10/12/2015         4                             


We can use an image classifier, resnet50 (which was used in previous tutorials) to see how well it performs with our images. 

From the output of the previous function we see that there are already 4 experiments performed with this model. An experiment is just an update on the original model (with experimentID=0) that may add some layers to the model, retrain the model or any other operation that the user thinks.

From the repositories we can only print the information of the baseline model as:


```
repositories["easier-public"].categories['misc'].models["resnet50_v2"].pretty_print()
```

    Category:                     misc                          
    Name:                         resnet50_v2                   
    Description:                  Pre-trained Keras model, processing functions in: 'tensorflow.keras.applications.resnet50'. Some .jpg are stored as examples.
    Last modified:                11:50:00 - 10/12/2015         
    Version:                      0                             
    Features:                     N/A                           


In order to get information about specific experiments, we need to use the models API, with this function.


```
experiments = easier.models.get_model_experiments(repo_name="easier-public", category=Categories.MISC, model_name="resnet50_v2")
```

It returns a list of ModelMetadata objects, that belong to each of the **experiments that the model has in that repository and for that category**.


```
experiments[1].pretty_print()
```

    Category:                     misc                          
    Name:                         resnet50_v2                   
    Description:                  resnet50v2 for person vs robot images
    Last modified:                11:50:00 - 10/12/2015         
    Version:                      1                             
    Features:                     N/A                           
    previous_experimentID:        0                             



```
print(experiments[1].last_modified)
```

    11:50:00 - 10/12/2015


The version 1 already solves the problem we wanted to resolve. So, we will start from the version 0 (which is the generic) classifier, in order to create our own new persons/robots classifier. We  would say that...  we dont like the existing robots/persons classifier (version 1), so we will take the original model to make our own new implementation. 

We will load the entire model. Remember that models can be uploaded in different formats: FULL model, just the weights or just the model config. Remember to add this information in the ModelMetadata when uploading a model.


```
from easierSDK.classes import constants

easier_resnet_model = easier.models.get_model(repo_name=repositories["easier-public"].name, 
                                              category='misc', 
                                              model_name="resnet50_v2",
                                              load_level=constants.FULL, 
                                              experimentID=0)
```

    WARNING:tensorflow:No training configuration found in the save file, so the model was *not* compiled. Compile it manually.


Now let's test the model with our images. We use the same libraries as the previous tutorials to transform our images into a resnet50 understandable format.


```
import PIL 
from keras.preprocessing.image import load_img 
from keras.preprocessing.image import img_to_array 
from keras.applications.imagenet_utils import decode_predictions 
import matplotlib.pyplot as plt 
import numpy as np 
from keras.applications import resnet50

```


```
# filename = 'datasets/misc/robot_sim_decenter_4/JPEG_Images/train/uc2-0001_person_front.jpg' 
filename = 'datasets/misc/robot_sim_decenter_4/JPEG_Images/train/uc2-0001_person_front.jpg'

original = load_img(filename, target_size = (224, 224)) 
plt.imshow(original) 
plt.show()

image_batch = easier.datasets.codify_image(filename)

processed_image = resnet50.preprocess_input(image_batch.copy())

predictions = easier_resnet_model.get_model().predict(processed_image) 
# print(predictions)
# convert the probabilities to class labels 
label = decode_predictions(predictions) 
print(label)
```


    
![png](EASIER_SDK_files/EASIER_SDK_127_0.png)
    


    [[('n03141823', 'crutch', 0.43280146), ('n02865351', 'bolo_tie', 0.36387572), ('n04228054', 'ski', 0.03425013), ('n04485082', 'tripod', 0.031230666), ('n04579432', 'whistle', 0.02533402)]]


Sadly, resnet50 model (version 0) cannot classify our images correctly. We need to do something about it.

Let's apply some transfer learing techniques to train a new version of the model that is able to correctly classify our images. In order to do that, we will fix the previous model weights, remove the last layer and add some new layers at the end that will learn the separation between people and robots.


```
# Transfer learning
import tensorflow as tf

resnet = easier_resnet_model.get_model()

for layer in resnet.layers:
    layer.trainable=False

inputs = resnet.input

my_tf_model = tf.keras.layers.Conv2D(2, kernel_size=(3, 3), activation='relu')(resnet.layers[-3].output)
my_tf_model = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))(my_tf_model)
my_tf_model = tf.keras.layers.Flatten()(my_tf_model)
my_tf_model = tf.keras.layers.Dense(1, activation='sigmoid')(my_tf_model)

my_tf_model = tf.keras.Model(inputs, my_tf_model)
my_tf_model.compile(loss='binary_crossentropy',
                     optimizer='rmsprop',
                     metrics=['accuracy'])
my_tf_model.summary()
```

    n[0][0]          
    __________________________________________________________________________________________________
    conv4_block1_2_conv (Conv2D)    (None, 14, 14, 256)  590080      conv4_block1_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv4_block1_2_bn (BatchNormali (None, 14, 14, 256)  1024        conv4_block1_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block1_2_relu (Activation (None, 14, 14, 256)  0           conv4_block1_2_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block1_0_conv (Conv2D)    (None, 14, 14, 1024) 525312      conv3_block4_out[0][0]           
    __________________________________________________________________________________________________
    conv4_block1_3_conv (Conv2D)    (None, 14, 14, 1024) 263168      conv4_block1_2_relu[0][0]        
    __________________________________________________________________________________________________
    conv4_block1_0_bn (BatchNormali (None, 14, 14, 1024) 4096        conv4_block1_0_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block1_3_bn (BatchNormali (None, 14, 14, 1024) 4096        conv4_block1_3_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block1_add (Add)          (None, 14, 14, 1024) 0           conv4_block1_0_bn[0][0]          
                                                                     conv4_block1_3_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block1_out (Activation)   (None, 14, 14, 1024) 0           conv4_block1_add[0][0]           
    __________________________________________________________________________________________________
    conv4_block2_1_conv (Conv2D)    (None, 14, 14, 256)  262400      conv4_block1_out[0][0]           
    __________________________________________________________________________________________________
    conv4_block2_1_bn (BatchNormali (None, 14, 14, 256)  1024        conv4_block2_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block2_1_relu (Activation (None, 14, 14, 256)  0           conv4_block2_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block2_2_conv (Conv2D)    (None, 14, 14, 256)  590080      conv4_block2_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv4_block2_2_bn (BatchNormali (None, 14, 14, 256)  1024        conv4_block2_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block2_2_relu (Activation (None, 14, 14, 256)  0           conv4_block2_2_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block2_3_conv (Conv2D)    (None, 14, 14, 1024) 263168      conv4_block2_2_relu[0][0]        
    __________________________________________________________________________________________________
    conv4_block2_3_bn (BatchNormali (None, 14, 14, 1024) 4096        conv4_block2_3_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block2_add (Add)          (None, 14, 14, 1024) 0           conv4_block1_out[0][0]           
                                                                     conv4_block2_3_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block2_out (Activation)   (None, 14, 14, 1024) 0           conv4_block2_add[0][0]           
    __________________________________________________________________________________________________
    conv4_block3_1_conv (Conv2D)    (None, 14, 14, 256)  262400      conv4_block2_out[0][0]           
    __________________________________________________________________________________________________
    conv4_block3_1_bn (BatchNormali (None, 14, 14, 256)  1024        conv4_block3_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block3_1_relu (Activation (None, 14, 14, 256)  0           conv4_block3_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block3_2_conv (Conv2D)    (None, 14, 14, 256)  590080      conv4_block3_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv4_block3_2_bn (BatchNormali (None, 14, 14, 256)  1024        conv4_block3_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block3_2_relu (Activation (None, 14, 14, 256)  0           conv4_block3_2_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block3_3_conv (Conv2D)    (None, 14, 14, 1024) 263168      conv4_block3_2_relu[0][0]        
    __________________________________________________________________________________________________
    conv4_block3_3_bn (BatchNormali (None, 14, 14, 1024) 4096        conv4_block3_3_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block3_add (Add)          (None, 14, 14, 1024) 0           conv4_block2_out[0][0]           
                                                                     conv4_block3_3_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block3_out (Activation)   (None, 14, 14, 1024) 0           conv4_block3_add[0][0]           
    __________________________________________________________________________________________________
    conv4_block4_1_conv (Conv2D)    (None, 14, 14, 256)  262400      conv4_block3_out[0][0]           
    __________________________________________________________________________________________________
    conv4_block4_1_bn (BatchNormali (None, 14, 14, 256)  1024        conv4_block4_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block4_1_relu (Activation (None, 14, 14, 256)  0           conv4_block4_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block4_2_conv (Conv2D)    (None, 14, 14, 256)  590080      conv4_block4_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv4_block4_2_bn (BatchNormali (None, 14, 14, 256)  1024        conv4_block4_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block4_2_relu (Activation (None, 14, 14, 256)  0           conv4_block4_2_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block4_3_conv (Conv2D)    (None, 14, 14, 1024) 263168      conv4_block4_2_relu[0][0]        
    __________________________________________________________________________________________________
    conv4_block4_3_bn (BatchNormali (None, 14, 14, 1024) 4096        conv4_block4_3_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block4_add (Add)          (None, 14, 14, 1024) 0           conv4_block3_out[0][0]           
                                                                     conv4_block4_3_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block4_out (Activation)   (None, 14, 14, 1024) 0           conv4_block4_add[0][0]           
    __________________________________________________________________________________________________
    conv4_block5_1_conv (Conv2D)    (None, 14, 14, 256)  262400      conv4_block4_out[0][0]           
    __________________________________________________________________________________________________
    conv4_block5_1_bn (BatchNormali (None, 14, 14, 256)  1024        conv4_block5_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block5_1_relu (Activation (None, 14, 14, 256)  0           conv4_block5_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block5_2_conv (Conv2D)    (None, 14, 14, 256)  590080      conv4_block5_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv4_block5_2_bn (BatchNormali (None, 14, 14, 256)  1024        conv4_block5_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block5_2_relu (Activation (None, 14, 14, 256)  0           conv4_block5_2_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block5_3_conv (Conv2D)    (None, 14, 14, 1024) 263168      conv4_block5_2_relu[0][0]        
    __________________________________________________________________________________________________
    conv4_block5_3_bn (BatchNormali (None, 14, 14, 1024) 4096        conv4_block5_3_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block5_add (Add)          (None, 14, 14, 1024) 0           conv4_block4_out[0][0]           
                                                                     conv4_block5_3_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block5_out (Activation)   (None, 14, 14, 1024) 0           conv4_block5_add[0][0]           
    __________________________________________________________________________________________________
    conv4_block6_1_conv (Conv2D)    (None, 14, 14, 256)  262400      conv4_block5_out[0][0]           
    __________________________________________________________________________________________________
    conv4_block6_1_bn (BatchNormali (None, 14, 14, 256)  1024        conv4_block6_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block6_1_relu (Activation (None, 14, 14, 256)  0           conv4_block6_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block6_2_conv (Conv2D)    (None, 14, 14, 256)  590080      conv4_block6_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv4_block6_2_bn (BatchNormali (None, 14, 14, 256)  1024        conv4_block6_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block6_2_relu (Activation (None, 14, 14, 256)  0           conv4_block6_2_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block6_3_conv (Conv2D)    (None, 14, 14, 1024) 263168      conv4_block6_2_relu[0][0]        
    __________________________________________________________________________________________________
    conv4_block6_3_bn (BatchNormali (None, 14, 14, 1024) 4096        conv4_block6_3_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block6_add (Add)          (None, 14, 14, 1024) 0           conv4_block5_out[0][0]           
                                                                     conv4_block6_3_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block6_out (Activation)   (None, 14, 14, 1024) 0           conv4_block6_add[0][0]           
    __________________________________________________________________________________________________
    conv5_block1_1_conv (Conv2D)    (None, 7, 7, 512)    524800      conv4_block6_out[0][0]           
    __________________________________________________________________________________________________
    conv5_block1_1_bn (BatchNormali (None, 7, 7, 512)    2048        conv5_block1_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv5_block1_1_relu (Activation (None, 7, 7, 512)    0           conv5_block1_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv5_block1_2_conv (Conv2D)    (None, 7, 7, 512)    2359808     conv5_block1_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv5_block1_2_bn (BatchNormali (None, 7, 7, 512)    2048        conv5_block1_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv5_block1_2_relu (Activation (None, 7, 7, 512)    0           conv5_block1_2_bn[0][0]          
    __________________________________________________________________________________________________
    conv5_block1_0_conv (Conv2D)    (None, 7, 7, 2048)   2099200     conv4_block6_out[0][0]           
    __________________________________________________________________________________________________
    conv5_block1_3_conv (Conv2D)    (None, 7, 7, 2048)   1050624     conv5_block1_2_relu[0][0]        
    __________________________________________________________________________________________________
    conv5_block1_0_bn (BatchNormali (None, 7, 7, 2048)   8192        conv5_block1_0_conv[0][0]        
    __________________________________________________________________________________________________
    conv5_block1_3_bn (BatchNormali (None, 7, 7, 2048)   8192        conv5_block1_3_conv[0][0]        
    __________________________________________________________________________________________________
    conv5_block1_add (Add)          (None, 7, 7, 2048)   0           conv5_block1_0_bn[0][0]          
                                                                     conv5_block1_3_bn[0][0]          
    __________________________________________________________________________________________________
    conv5_block1_out (Activation)   (None, 7, 7, 2048)   0           conv5_block1_add[0][0]           
    __________________________________________________________________________________________________
    conv5_block2_1_conv (Conv2D)    (None, 7, 7, 512)    1049088     conv5_block1_out[0][0]           
    __________________________________________________________________________________________________
    conv5_block2_1_bn (BatchNormali (None, 7, 7, 512)    2048        conv5_block2_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv5_block2_1_relu (Activation (None, 7, 7, 512)    0           conv5_block2_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv5_block2_2_conv (Conv2D)    (None, 7, 7, 512)    2359808     conv5_block2_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv5_block2_2_bn (BatchNormali (None, 7, 7, 512)    2048        conv5_block2_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv5_block2_2_relu (Activation (None, 7, 7, 512)    0           conv5_block2_2_bn[0][0]          
    __________________________________________________________________________________________________
    conv5_block2_3_conv (Conv2D)    (None, 7, 7, 2048)   1050624     conv5_block2_2_relu[0][0]        
    __________________________________________________________________________________________________
    conv5_block2_3_bn (BatchNormali (None, 7, 7, 2048)   8192        conv5_block2_3_conv[0][0]        
    __________________________________________________________________________________________________
    conv5_block2_add (Add)          (None, 7, 7, 2048)   0           conv5_block1_out[0][0]           
                                                                     conv5_block2_3_bn[0][0]          
    __________________________________________________________________________________________________
    conv5_block2_out (Activation)   (None, 7, 7, 2048)   0           conv5_block2_add[0][0]           
    __________________________________________________________________________________________________
    conv5_block3_1_conv (Conv2D)    (None, 7, 7, 512)    1049088     conv5_block2_out[0][0]           
    __________________________________________________________________________________________________
    conv5_block3_1_bn (BatchNormali (None, 7, 7, 512)    2048        conv5_block3_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv5_block3_1_relu (Activation (None, 7, 7, 512)    0           conv5_block3_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv5_block3_2_conv (Conv2D)    (None, 7, 7, 512)    2359808     conv5_block3_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv5_block3_2_bn (BatchNormali (None, 7, 7, 512)    2048        conv5_block3_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv5_block3_2_relu (Activation (None, 7, 7, 512)    0           conv5_block3_2_bn[0][0]          
    __________________________________________________________________________________________________
    conv5_block3_3_conv (Conv2D)    (None, 7, 7, 2048)   1050624     conv5_block3_2_relu[0][0]        
    __________________________________________________________________________________________________
    conv5_block3_3_bn (BatchNormali (None, 7, 7, 2048)   8192        conv5_block3_3_conv[0][0]        
    __________________________________________________________________________________________________
    conv5_block3_add (Add)          (None, 7, 7, 2048)   0           conv5_block2_out[0][0]           
                                                                     conv5_block3_3_bn[0][0]          
    __________________________________________________________________________________________________
    conv5_block3_out (Activation)   (None, 7, 7, 2048)   0           conv5_block3_add[0][0]           
    __________________________________________________________________________________________________
    conv2d (Conv2D)                 (None, 5, 5, 2)      36866       conv5_block3_out[0][0]           
    __________________________________________________________________________________________________
    max_pooling2d (MaxPooling2D)    (None, 2, 2, 2)      0           conv2d[0][0]                     
    __________________________________________________________________________________________________
    flatten (Flatten)               (None, 8)            0           max_pooling2d[0][0]              
    __________________________________________________________________________________________________
    dense_6 (Dense)                 (None, 1)            9           flatten[0][0]                    
    ==================================================================================================
    Total params: 23,624,587
    Trainable params: 36,875
    Non-trainable params: 23,587,712
    __________________________________________________________________________________________________


That's quite a big model. You can see our layers at the bottom.

Let's prepare the data to train.


```
import os

base_path = 'datasets/misc/robot_sim_decenter_4/JPEG_Images/train/'
x = []
y = []
for f in os.listdir(base_path):
  if os.path.isfile(base_path + '/' + f):
    image = load_img(filename, target_size = (224, 224))
    numpy_image = img_to_array(image) 
    x.append(numpy_image)
    if len(f.split('person'))>1:
      y.append(0)
    else:
      y.append(1)

processed_images = np.array(x)
labels = np.array(y)
```

And now, we just need to fit the model to the new data. 

For the sake of time, the tutorial only uses 1 epoch which, of course, does not give very good results ;)


```
my_tf_model.fit(x=processed_images, y=labels, epochs=1)
```

    5/5 [==============================] - 9s 2s/step - loss: 0.6926 - accuracy: 0.6870





    <tensorflow.python.keras.callbacks.History at 0x7fe7feb92580>



Let's test again our model against the data


```
filename = 'datasets/misc/robot_sim_decenter_4/JPEG_Images/train/uc2-0067_person__1.31.jpg' 
# filename = 'datasets/misc/robot_sim_decenter_4/JPEG_Images/train/uc2-0071_robot_front.jpg' 

## load an image in PIL format 
original = load_img(filename, target_size = (224, 224)) 
plt.imshow(original) 
plt.show()

image_batch = easier.datasets.codify_image(filename, target_size = (224, 224))

processed_image = resnet50.preprocess_input(image_batch.copy())

predictions = my_tf_model.predict(processed_image) 
print(predictions)
```


    
![png](EASIER_SDK_files/EASIER_SDK_135_0.png)
    


    [[0.4982892]]


As expected, since we only did 1 epoch for training, the accurazy of the prediction is not good, but the model seems to work (if prediction is < 0.5, then it is a 'person'). 

EASIER allows you to upload this model and **continue the work later on, downloading the model in the current state**. So, we will upload this new model to our repo. We cannot upload this model to original repo, because this belongs to other user and we dont haver perms. Later, we could download it again (this time from our repo), and continue working. For example, you could re-fit it with more epochs to improve the accurazy

Let's put it into an EasierModel object. We can reuse the previous object and set the new model.


```
easier_resnet_model.set_model(my_tf_model)
```

Remember to update the model's metadata. **The version of the model (experimentID) is updated by EASIER for you** when it is uploaded.


```
easier_resnet_model.metadata.description = "resnet50_v2 for person vs robot images (testing with only 1 epoch)"
```


```
success = easier.models.upload(easier_resnet_model, storage_level=constants.FULL)
```

    Uploaded model: 
    
    Category:                     misc                          
    Name:                         resnet50_v2                   
    Description:                  resnet50_v2 for person vs robot images (testing with only 1 epoch)
    Last modified:                2021/01/21 17:06:46           
    Version:                      3                             
    Features:                     N/A                           
    previous_experimentID:        0                             


With this tutorial we have learnt a very interesting part of EASIER about Models versioning or experimentsID. You can start from any model, any experiment, make modifications and upload it again. The number of the experimentID will be automatically increaded +1 when the model already exists in the repository. Or, it will be 0, in the case you are uploading it to a repository where the model does not exists. You can play with this, make more changes, upload the model again, and the versioning counter will be increased.
