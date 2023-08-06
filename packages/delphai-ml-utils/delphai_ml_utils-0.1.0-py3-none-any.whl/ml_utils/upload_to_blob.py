import confuse
import logging
import os
from base64 import b64decode
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from kubernetes import client as kube_client, config as kube_config
from kubernetes.config import ConfigException
import azure.core.exceptions as azure_exception

logging.basicConfig(level=logging.DEBUG)

def __load_config():
    try:
        config = confuse.Configuration('ml-utils', __name__)
        config.set_file('config/ml-config.yml')
        return config
    except Exception as ex:
        logging.error('No such file or directory: config/ml-config.yml')
        logging.warn('Make sure to have config/ml-config.yml')
        
        
def __connect_to_kubernetes_incluster():
    try:
        kube_config.load_incluster_config()
    except Exception as ex:
        logging.debug(str(ex))
        kube_config.load_kube_config()

def __connect_to_kubernetes():
    try:
        kube_config.load_kube_config()
    except Exception as ex:
        logging.debug(str(ex))
        kube_config.load_kube_config()

def __get_blob_secret():
    conf = __load_config()
    try:
        kube_secret = conf['dest']['storage_account_secret'].get()
    except Exception as ex:
        logging.error(' storage_account_secret not found in config/ml-config.yml')
        logging.error(ex)
    
    try:
        __connect_to_kubernetes()
    except ConfigException:
        logging.warn(f'Failed to obtain a secret value "kube:{path}": no available configuration')
        return '???'
    except Exception as exc:
        logging.warn(f'Failed to obtain a secret value "kube:{path}": {type(exc).__name__}')
        return '???'
    else:
        try:
            __connect_to_kubernetes()
        except ConfigException:
            logging.warn(f'Failed to configure kubernetes client, no available configuration')
            return '???'
    
    split = kube_secret.split('/')
    namespace = 'default'
    secret_name = split[0]
    secret_key = split[1]
    if len(split) > 2:
        namespace = split[0]
        secret_name = split[1]
        secret_key = split[2]
    v1 = kube_client.CoreV1Api()

    try:
        secret = v1.read_namespaced_secret(secret_name, namespace).data[secret_key]
    except Exception as exc:
        logging.warn(f'Failed to obtain a secret value "kube_secret:{kube_secret}": {type(exc).__name__}')
        return '???'

    secret = b64decode(secret).decode('utf-8')
    return secret

def upload_to_azure_blob():
    conf = __load_config()
    # get model name from ml-config.yml
    try:
        model_name = conf['model_name'].get()
        training_dir = conf['training_dir'].get()
    except Exception as ex:
        logging.error(' model_name not found in config/ml-config.yml')
        logging.error(ex)
    
    # get output dir from ml-config.yml
    try:
        training_dir = conf['training_dir'].get()
    except Exception as ex:
        logging.error(' training_dir not found in config/ml-config.yml')
        logging.error(ex)

    connect_str = __get_blob_secret()
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # get all containers
    containers_obj = blob_service_client.list_containers()
    containers = []
    for c in containers_obj:
        containers.append(c['name'])
    
    if model_name in containers:
        logging.warn(f'Container {model_name} already exists')
    else:
        # Create container if not exists
        blob_service_client.create_container(model_name)


    for r,d,f in os.walk(training_dir):        
        if f:
            for file in f:
                print(file)
                blob_client = blob_service_client.get_blob_client(container=model_name, blob=file)
                upload_file_path = os.path.join(training_dir,file)
                with open(upload_file_path, "rb") as data:
                    blob_client.upload_blob(data)
