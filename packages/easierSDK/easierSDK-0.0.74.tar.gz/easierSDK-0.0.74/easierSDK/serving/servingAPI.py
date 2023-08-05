import os
import kubernetes
import yaml
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import string
import random

from easierSDK.classes.categories import Categories
from easierSDK.serving import easier_serving_config_map
from easierSDK.serving import easier_serving_deployment
from easierSDK.serving import easier_serving_service 
from easierSDK.serving import easier_serving_ingress 

class ServingAPI():
    """Class to control the Serving API of EasierSDK.
    """

    _easier_user = None
    _easier_password = None

    def __init__(self, easier_user, easier_password, minio_client, my_public_repo, my_private_repo):
        """Constructor for the ServingAPI.

        Args:
            minio_client (Minio): Minio client object with user session initialized.
            my_public_repo (str): Name of the public bucket of the user.
            my_private_repo (str): Name of the private bucket of the user.
        """
        self._easier_user = easier_user
        self._easier_password = easier_password
        self.minio_client = minio_client
        self.my_public_repo = my_public_repo
        self.my_private_repo = my_private_repo
        
    def initialize(self, kube_config_path=None):
        if kube_config_path:
            kubernetes.config.load_kube_config(kube_config_path)
            with open(os.path.join(os.path.dirname(__file__), kube_config_path)) as f:
                kubeconfig = yaml.safe_load(f)
                self.namespace = kubeconfig['contexts'][0]['context']['namespace']
        else:
            kubernetes.config.load_kube_config()
            with open(os.path.join(os.path.dirname(__file__), os.environ.get('KUBECONFIG', '~/.kube/config'))) as f:
                kubeconfig = yaml.safe_load(f)
                self.namespace = kubeconfig['contexts'][0]['context']['namespace']

        print("Current context on namespace: " + str(self.namespace))
        
    def id_generator(self, size=16, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def create_model_serving(self, repo_name:str, category:Categories, model_name:str, experimentID:int, namespace=None):
        
        if isinstance(category, str):
           category = Categories[category.upper()]
        
        # Test if model can be loaded
        from easierSDK.easier import EasierSDK
        easier = EasierSDK(easier_user=self._easier_user, easier_password=self._easier_password)
        easier_model = easier.models.get_model(repo_name=repo_name, category=category, model_name=model_name, experimentID=experimentID)    
        if easier_model.get_model() is None:
            print("ERROR: Could not load model " + str(model_name) +
                    " from repository " + repo_name + " and category " + category.value)
            return None
        
        if namespace == None:
            namespace = self.namespace  
        
        # Enter a context with an instance of the API kubernetes.client
        with kubernetes.client.ApiClient() as api_client:
            # Create an instance of the API class
            api_instance = kubernetes.client.CoreV1Api(api_client)
            
            random_name = self.id_generator(size=5)
            
            # config_map = None
            # with open(os.path.join(os.path.dirname(__file__), "easier-serving-config_map.yaml")) as f:
            config_map = yaml.safe_load(easier_serving_config_map.config_map)

            config_map['metadata']['name'] += '-' + self._easier_user.replace('.', '-') + '-' +  random_name
            config_map['data']['easier_user'] = self._easier_user
            config_map['data']['easier_password'] = self._easier_password
            config_map['data']['repo'] = repo_name
            config_map['data']['category'] = category.value
            config_map['data']['model_name'] = model_name
            config_map['data']['experimentID'] = str(experimentID)
            
            try:
                api_response = api_instance.create_namespaced_config_map(namespace, config_map, pretty='true')
                # print(api_response)
            except ApiException as e:
                print("Exception when calling CoreV1Api->create_namespaced_config_map: %s\n" % e)

            # deployment = None
            # with open(os.path.join(os.path.dirname(__file__), "easier-serving-deployment.yaml")) as f:
            deployment = yaml.safe_load(easier_serving_deployment.deployment)
        
            deployment['metadata']['name'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name
            deployment['metadata']['labels']['app'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name
            deployment['spec']['selector']['matchLabels']['app'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name
            deployment['spec']['template']['metadata']['labels']['app'] += '-' + self._easier_user.replace('.', '-') + '-' +  random_name
            deployment['spec']['containers'][0]['name'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name
            deployment['spec']['containers'][0]['envFrom'][0]['configMapRef']['name'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name
    
            try:
                api_response = api_instance.create_namespaced_pod(namespace, deployment, pretty='true')
                # print(api_response)
            except ApiException as e:
                print("Exception when calling CoreV1Api->create_namespaced_pod: %s\n" % e)

            # service = None
            # with open(os.path.join(os.path.dirname(__file__), "easier-serving-service.yaml")) as f:
            service = yaml.safe_load(easier_serving_service.service)
        
            service['metadata']['name'] += '-' + self._easier_user.replace('.', '-') + '-' +  random_name
            service['metadata']['labels']['app'] += '-' + self._easier_user.replace('.', '-') + '-' +  random_name
            service['spec']['selector']['app'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name

            try:
                api_response = api_instance.create_namespaced_service(namespace, service, pretty='true')
                # print(api_response)
            except ApiException as e:
                print("Exception when calling CoreV1Api->create_namespaced_service: %s\n" % e)
        
            networking_v1_beta1_api = kubernetes.client.NetworkingV1beta1Api()
            hostname = None
            # ingress = None
            # with open(os.path.join(os.path.dirname(__file__), "easier-serving-ingress.yaml")) as f:
            ingress = yaml.safe_load(easier_serving_ingress.ingress)
        
            ingress['metadata']['name'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name
            ingress['metadata']['labels']['app'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name
            ingress['spec']['rules'][0]['host'] = model_name + '-' + 'easier-serving' + '-' + self._easier_user.replace('.', '-') + '-' + random_name + '.easier-ai.eu'
            ingress['spec']['rules'][0]['http']['paths'][0]['backend']['serviceName'] += '-' + self._easier_user.replace('.', '-') + '-' + random_name

            try:
                api_response = networking_v1_beta1_api.create_namespaced_ingress(namespace, ingress, pretty='true')
                # print(api_response)
            except ApiException as e:
                print("Exception when calling CoreV1Api->create_namespaced_ingress: %s\n" % e)
            
            hostname = ingress['spec']['rules'][0]['host']
            
            if hostname:
                print("Your model will be served shortly in: " + str(hostname))
            else:
                print("There was a problem serving your model")

        return hostname

    def delete_serving():
        raise NotImplementedError
    