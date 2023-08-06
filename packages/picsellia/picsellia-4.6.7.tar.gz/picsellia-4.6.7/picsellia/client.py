import json
import os
import sys
import io
import requests
from PIL import Image, ImageDraw, ExifTags
from multiprocessing.pool import ThreadPool
from multiprocessing import Pool, Value
import picsellia.pxl_multithreading as mlt
import time
import zipfile
import picsellia.pxl_exceptions as exceptions
from uuid import UUID, uuid4
from picsellia.pxl_utils import is_uuid
import picsellia.pxl_utils as utils
from picsellia.pxl_urls_v2 import Urls as urls
from pathlib import Path
from functools import partial

class Client:
    def __init__(self, api_token, organization_id=None,  host="https://beta.picsellia.com/sdk/v2/", interactive=True):
        """[summary]

        Args:
            api_token ([token]): [Your api token accessible in Profile Page]
            host (str, optional): [description]. Defaults to "https://beta.picsellia.com/sdk/v2".
            interactive (bool, optional): [set verbose mode]. Defaults to True.

        Raises:
            exceptions.NetworkError: [If Platform Not responding]
        """

        self.supported_img_types = ("png", "jpg", "jpeg", "JPG", "JPEG", "PNG")
        self.auth = {"Authorization": "Token " + api_token}
        self.host = host

        try:
            r = requests.get(self.host + 'ping', headers=self.auth)
        except Exception:
            raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")  

        # User Variables 
        self.username = r.json()["username"]

        # Project Variables
        self.project_name_list = None
        self.project_token = None
        self.project_id = None
        self.project_infos = None
        self.project_name = None
        self.project_type = None

        # Dataset Variables 

        # Network Variables
        self.network_names = None
        self.network_id = None
        self.network_name = None
        

        # Directory Variables
        self.png_dir = None
        self.base_dir = None
        self.metrics_dir = None
        self.checkpoint_dir = None
        self.record_dir = None
        self.config_dir = None
        self.results_dir = None
        self.exported_model_dir = None

        # Experiment Variables
        self.experiment_id = None
        self.exp_name = None
        self.exp_description = None 
        self.exp_status = None 
        self.exp_parameters = None
        self.line_nb = 0
        self.training_id = None
        self.annotation_type = None
        self.dict_annotations = {}
        self.train_list_id = None
        self.eval_list_id = None
        self.train_list = None
        self.eval_list = None
        self.index_url = None
        self.checkpoint_index = None
        self.checkpoint_data = None
        self.config_file = None
        self.model_selected = None
        self.label_path = None
        self.label_map = None
        self.urls = urls(self.host, self.auth)
        self.datalake = self.Datalake(self.host, api_token, organization_id)
        # self.dataset = self.Dataset(self.host, self.auth)
        self.experiment = self.Experiment(self.host, api_token)
        self.network = self.Network(self.host, self.auth)
        self.project = self.Project(self.host, self.auth)
        self.interactive = interactive
        print(f"Hi {self.username}, welcome back.")

    class Experiment:

        def __init__(self, api_token=None, host="https://beta.picsellia.com/sdk/v2/", project_token=None, id=None, name=None, interactive=True):
            self.host = host
            self.auth = {"Authorization": "Token " + api_token}
            self.id = id
            if name is not None:
                self.experiment_name = name
            else:
                self.experiment_name = ""
            self.urls = urls(self.host, self.auth)
            self.interactive = interactive
            self.project_token = project_token
            self.base_dir = self.experiment_name
            self.png_dir = os.path.join(self.base_dir, 'images')

        def check_identifier(self, id=None, name=None, project_token=None):
            
            return 

        def checkout(self, name=None, id=None,  project_token=None, tree=False, with_file=False, with_data=False):
            identifier = None
            if self.id != None:
                identifier = self.id
            elif self.project_token != None:
                if self.experiment_name != "":
                    identifier = self.experiment_name
                elif name != None:
                    identifier = name
            elif id != None:
                identifier = id
            elif project_token != None:
                self.project_token = project_token
                if self.experiment_name != None:
                    identifier = self.experiment_name
                elif name != None:
                    identifier = name
            if identifier == None:
                raise Exception('No corresponding experiment found, please enter a correct experiment id or a correct experiment name + project token')
            experiment = self._get(with_file=with_file, with_data=with_data, identifier=identifier)
            self.files = experiment["files"]
            self.data = experiment["data"]
            self.id = experiment["id"]
            self.experiment_name = experiment["name"]
            self.project_token = experiment["project"]
            if tree:
                self.setup_dirs()
                if with_file:
                    for f in self.files:
                        object_name = f["object_name"]
                        name = f["name"]
                        filename = f["object_name"].split('/')[-1]
                        if f["large"]:
                            if name == 'checkpoint-data-latest':
                                self.dl_large_file(object_name, os.path.join(self.checkpoint_dir, filename))
                            elif name == 'model-latest':
                                self.dl_large_file(object_name, os.path.join(self.exported_model_dir, filename))
                            else:
                                self.dl_large_file(object_name, os.path.join(self.base_dir, filename))
                        else:
                            if name == 'config':
                                self.dl_file(object_name, os.path.join(self.config_dir, filename))
                            elif name == 'checkpoint-index-latest':
                                self.dl_file(object_name, os.path.join(self.checkpoint_dir, filename))
                            else:
                                self.dl_file(object_name, os.path.join(self.base_dir, filename))
            else:
                if with_file:
                    self.base_dir = self.experiment_name
                    self._create_dir(self.base_dir)
                    for f in self.files:
                        object_name = f["object_name"]
                        filename = f["object_name"].split('/')[-1]
                        if f["large"]:
                            self.dl_large_file(object_name, os.path.join(self.base_dir, filename))
                        else:
                            self.dl_file(object_name, os.path.join(self.base_dir, filename))
            return self


        def publish(self, name=None):
            assert self.id != None or id != None, "Please checkout an experiment or enter the desired experiment id"
            data = json.dumps({
                "name": name
            })
            try:
                r = requests.post(self.host + 'experiment/{}/publish'.format(self.id), data=data, headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.AuthenticationError(r.json()["error"])
            return r.json()

            
        def list(self, project_token=None):
            """[summary]

            Raises:
                exceptions.NetworkError: [description]
                exceptions.AuthenticationError: [description]

            Returns:
                [type]: [description]
            """
            assert project_token != None or self.project_token != None, "Please checkout a project or enter your project token on initialization"
            if self.project_token != None:
                token = self.project_token
            elif project_token != None:
                token = project_token
            try:
                r = requests.get(self.host + 'experiment/{}'.format(token), headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.AuthenticationError(r.json()["error"])
            return r.json()["experiments"]

        def _get(self, with_file=False, with_data=False, identifier=None):
            """[summary]

            Args:
                identifier ([type]): can be dataset_name (str) or uuid
            Raises:
                exceptions.NetworkError: [description]
                exceptions.AuthenticationError: [description]

            Returns:
                [type]: [description]
            """
            assert self.project_token != None, "Please checkout a project or enter your project token on initialization"
            data = {
                'with_file': with_file,
                'with_data': with_data
            }
            try:
                if is_uuid(identifier):
                    r = requests.get(self.host + 'experiment/{}/{}'.format(self.project_token, identifier), data,  headers=self.auth)
                else:
                    r = requests.get(self.host + 'experiment/{}/by_name/{}'.format(self.project_token, identifier), data, headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            if r.status_code == 404:
                raise exceptions.ResourceNotFoundError("Not Found {}".format(self.host + 'experiment/{}'.format(self.project_token)))
            if r.status_code != 200:
                raise exceptions.ResourceNotFoundError(r.json()["error"])
            if len(r.json()["experiment"])>0:
                return r.json()["experiment"][0]
            else:
                raise exceptions.ResourceNotFoundError("Experiment Not found")
                

        def create(self, name=None, description='', previous=None, dataset=None, source=None, with_file=False, with_data=False):
            """[summary]

            Args:
                dataset_name ([str]): [description]
                description (str, optional): [description]. Defaults to "".
                private (bool, optional): [description]. Defaults to True.

            Raises:
                exceptions.NetworkError: [description]
                exceptions.ResourceNotFoundError: [description]

            Returns:
                [type]: [description]
            """
            data = json.dumps({
                "name": name,
                "description": description,
                "previous": previous,
                "dataset": dataset,
                "source": source,
                "with_file": with_file,
                "with_data": with_data
            })
            try:
                r = requests.post(self.host + 'experiment/{}'.format(self.project_token), data=data, headers=self.auth)
            except Exception:
                raise exceptions.NetworkError(r.json()["error"])
            if r.status_code == 404:
                raise exceptions.ResourceNotFoundError("Not Found {}".format(self.host + 'experiment/{}'.format(self.project_token)))
            if r.status_code != 201:
                raise exceptions.ResourceNotFoundError(r.json()["error"])
            print(r.json())
            experiment = r.json()
            self.id = experiment["id"]
            self.experiment_name = experiment["name"]
            return self

        def update(self, identifier=None, **kwargs):
            """[summary]

            Args:
                dataset_name ([str]): [description]
                description (str, optional): [description]. Defaults to "".
                private (bool, optional): [description]. Defaults to True.

            Raises:
                exceptions.NetworkError: [description]
                exceptions.ResourceNotFoundError: [description]

            Returns:
                [type]: [description]
            """
            data = json.dumps(kwargs)
            try:
                if is_uuid(identifier):
                    r = requests.patch(self.host + 'experiment/{}/{}'.format(self.project_token, identifier), data=data, headers=self.auth)
                else:
                    r = requests.patch(self.host + 'experiment/{}/by_name/{}'.format(self.project_token, identifier), data=data, headers=self.auth)
            except Exception:
                raise exceptions.NetworkError(r.json()["error"])
            
            if r.status_code != 201:
                raise exceptions.ResourceNotFoundError(r.json()["error"])
            
            return r.json()

        def delete(self, identifier):
            """[summary]

            Args:
                identifier ([type]): can be dataset_name (str) or uuid
            Raises:
                exceptions.NetworkError: [description]
                exceptions.AuthenticationError: [description]

            Returns:
                [type]: [description]
            """
            assert self.project_token != None, "Please checkout a project or enter your project token on initialization"
            try:
                if is_uuid(identifier):
                    r = requests.delete(self.host + 'experiment/{}/{}'.format(self.project_token, identifier), headers=self.auth)
                else:
                    r = requests.delete(self.host + 'experiment/{}/by_name/{}'.format(self.project_token, identifier), headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.ResourceNotFoundError(r.json()["error"])

            return True

        def delete_all(self, project_token):
            """[summary]

            Raises:
                exceptions.NetworkError: [description]
                exceptions.AuthenticationError: [description]

            Returns:
                [type]: [description]
            """
            assert self.project_token != None, "Please checkout a project or enter your project token on initialization"
            try:
                r = requests.delete(self.host + 'experiment/{}'.format(self.project_token), headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.AuthenticationError(r.json()["error"])
            return True
        
        def list_files(self,):
            """[summary]

            Raises:
                exceptions.NetworkError: [description]
                exceptions.AuthenticationError: [description]

            Returns:
                [type]: [description]
            """
            assert self.id != None, "Please checkout or create an experiment first"

            try:
                r = requests.get(self.host + 'experiment/{}/file'.format(self.id), headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.AuthenticationError(r.json()["error"])
            return r.json()["files"]
        
        def delete_all_files(self,):
            """[summary]

            Raises:
                exceptions.NetworkError: [description]
                exceptions.AuthenticationError: [description]

            Returns:
                [type]: [description]
            """
            assert self.id != None, "Please checkout or create an experiment first"

            try:
                r = requests.delete(self.host + 'experiment/{}/file'.format(self.id), headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.AuthenticationError(r.json()["error"])
            return True
        
        def create_file(self, name="", object_name="", large=False):
            """[summary]

            Args:
                dataset_name ([str]): [description]
                description (str, optional): [description]. Defaults to "".
                private (bool, optional): [description]. Defaults to True.

            Raises:
                exceptions.NetworkError: [description]
                exceptions.ResourceNotFoundError: [description]

            Returns:
                [type]: [description]
            """
            assert self.id != None , "Please checkout or create an experiment first"

            data = json.dumps({ '0': {
                'name': name,
                'object_name': object_name,
                'large': large
            }
            })
            try:
                r = requests.put(self.host + 'experiment/{}/file'.format(self.id), data=data, headers=self.auth)
            except Exception:
                raise exceptions.NetworkError(r.json()["error"])
            
            if r.status_code != 201:
                raise exceptions.ResourceNotFoundError(r.json()["error"])
            
            return r.json()
        
        def get_file(self, name=None):
            """[summary]

            Raises:
                exceptions.NetworkError: [description]
                exceptions.AuthenticationError: [description]

            Returns:
                [type]: [description]
            """
            assert self.id != None , "Please checkout or create an experiment first"

            assert name != None, "Please enter a valid file name"
            try:
                r = requests.get(self.host + 'experiment/{}/file/{}'.format(self.id, name), headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.AuthenticationError(r.json()["error"])
            if len(r.json()["file"])>0:
                return r.json()["file"][0]
            else:
                return r.json()["file"]

        def delete_file(self, name=None):
            """[summary]

            Raises:
                exceptions.NetworkError: [description]
                exceptions.AuthenticationError: [description]

            Returns:
                [type]: [description]
            """
            assert self.id != None, "Please checkout or create an experiment first"

            assert name != None, "Please enter a valid file name"
            try:
                r = requests.delete(self.host + 'experiment/{}/file/{}'.format(self.id, name), headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.AuthenticationError(r.json()["error"])
            return True
        
        def update_file(self, file_name=None, **kwargs):
            """[summary]

            Args:
                dataset_name ([str]): [description]
                description (str, optional): [description]. Defaults to "".
                private (bool, optional): [description]. Defaults to True.

            Raises:
                exceptions.NetworkError: [description]
                exceptions.ResourceNotFoundError: [description]

            Returns:
                [type]: [description]
            """
            assert self.id != None, "Please checkout or create an experiment first"

            assert file_name != None, "Please enter a valid file name"
            data = json.dumps(kwargs)
            try:
                r = requests.patch(self.host + 'experiment/{}/file/{}'.format(self.id, file_name), data=data, headers=self.auth)
            except Exception:
                raise exceptions.NetworkError(r.json()["error"])
            
            if r.status_code != 201:
                raise exceptions.ResourceNotFoundError(r.json()["error"])
            
            return r.json()
        
        def list_data(self,):
            """[summary]

            Raises:
                exceptions.NetworkError: [description]
                exceptions.AuthenticationError: [description]

            Returns:
                [type]: [description]
            """
            assert self.id != None, "Please checkout or create an experiment first"

            try:
                r = requests.get(self.host + 'experiment/{}/data'.format(self.id), headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.AuthenticationError(r.json()["error"])
            return r.json()["data_assets"]
        
        def delete_all_data(self,):
            """[summary]

            Raises:
                exceptions.NetworkError: [description]
                exceptions.AuthenticationError: [description]

            Returns:
                [type]: [description]
            """
            assert self.id != None, "Please checkout or create an experiment first"

            try:
                r = requests.delete(self.host + 'experiment/{}/data'.format(self.id), headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.AuthenticationError(r.json()["error"])
            return True
        
        def create_data(self, name="", data={}, type=None):
            """[summary]

            Args:
                dataset_name ([str]): [description]
                description (str, optional): [description]. Defaults to "".
                private (bool, optional): [description]. Defaults to True.

            Raises:
                exceptions.NetworkError: [description]
                exceptions.ResourceNotFoundError: [description]

            Returns:
                [type]: [description]
            """
            assert self.id != None, "Please checkout or create an experiment first"

            data = json.dumps({ '0': {
                'name': name,
                'data': data,
                'type': type
            }
            })
            try:
                r = requests.put(self.host + 'experiment/{}/data'.format(self.id), data=data, headers=self.auth)
            except Exception:
                raise exceptions.NetworkError(r.json()["error"])
            
            if r.status_code != 201:
                raise exceptions.ResourceNotFoundError(r.json()["error"])
            
            return r.json()
        
        def get_data(self, name=None):
            """[summary]

            Raises:
                exceptions.NetworkError: [description]
                exceptions.AuthenticationError: [description]

            Returns:
                [type]: [description]
            """
            assert self.id != None, "Please checkout or create an experiment first"

            assert name != None, "Please enter a valid data asset name"
            try:
                r = requests.get(self.host + 'experiment/{}/data/{}'.format(self.id, name), headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.AuthenticationError(r.json()["error"])
            if len(r.json()["data_asset"])>0:
                return r.json()["data_asset"][0]["data"]
            else:
                return r.json()["data_asset"]

        def delete_data(self, name=None):
            """[summary]

            Raises:
                exceptions.NetworkError: [description]
                exceptions.AuthenticationError: [description]

            Returns:
                [type]: [description]
            """
            assert self.id != None, "Please checkout or create an experiment first"

            assert name != None, "Please enter a valid data asset name"
            try:
                r = requests.delete(self.host + 'experiment/{}/data/{}'.format(self.id, name), headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.AuthenticationError(r.json()["error"])
            return True
        
        def update_data(self, name=None, **kwargs):
            """[summary]

            Args:
                dataset_name ([str]): [description]
                description (str, optional): [description]. Defaults to "".
                private (bool, optional): [description]. Defaults to True.

            Raises:
                exceptions.NetworkError: [description]
                exceptions.ResourceNotFoundError: [description]

            Returns:
                [type]: [description]
            """
            assert self.id != None, "Please checkout or create an experiment first"

            assert name != None, "Please enter a valid data asset name"
            data = json.dumps(kwargs)
            try:
                r = requests.patch(self.host + 'experiment/{}/data/{}'.format(self.id, name), data=data, headers=self.auth)
            except Exception:
                raise exceptions.NetworkError(r.json()["error"])
            
            if r.status_code != 201:
                raise exceptions.ResourceNotFoundError(r.json()["error"])
            
            return r.json()["data"][0]

        def append_data(self, name=None, **kwargs):
            """[summary]

            Args:
                dataset_name ([str]): [description]
                description (str, optional): [description]. Defaults to "".
                private (bool, optional): [description]. Defaults to True.

            Raises:
                exceptions.NetworkError: [description]
                exceptions.ResourceNotFoundError: [description]

            Returns:
                [type]: [description]
            """
            assert self.id != None, "Please checkout or create an experiment first"

            assert name != None, "Please enter a valid data asset name"
            data = json.dumps(kwargs)
            try:
                r = requests.post(self.host + 'experiment/{}/data/{}'.format(self.id, name), data=data, headers=self.auth)
            except Exception:
                raise exceptions.NetworkError(r.json()["error"])
            
            if r.status_code != 201:
                raise exceptions.ResourceNotFoundError(r.json()["error"])
            
            return r.json()["success"]

        def _send_large_file(self, path=None, name=None, object_name=None, network_id=None):
            error_message = "Please checkout or create an experiment/network or enter the desired experiment id/network_id"
            assert self.id != None or network_id != None, error_message

            self.urls._init_multipart(object_name)
            parts = self.urls._upload_part(path, object_name)

            if self.urls._complete_part_upload(parts, object_name, None):
                self._create_or_update_file(name, path, object_name=object_name, large=True)

        def _send_file(self, path=None, name=None, object_name=None, network_id=None):
            error_message = "Please checkout an experiment/network or enter the desired experiment id/network_id"
            assert self.id != None or network_id != None, error_message

            response = self.urls._get_presigned_url(method='post', object_name=object_name, bucket_model=True)
            try:
                with open(path, 'rb') as f:
                    files = {'file': (path, f)}
                    http_response = requests.post(response['url'], data=response['fields'], files=files)
                if http_response.status_code == 204:
                    self._create_or_update_file(name, path, object_name=object_name, large=False)
            except Exception as e:
                raise exceptions.NetworkError(str(e))

        def log(self, name="", data={}, type=None, replace=False):
            assert self.id != None, "Please checkout or create an experiment first"

            stored = self.get_data(name)
            if type == 'value':
                data = {'value': data}
            if stored == []:
                assert type != None, "Please specify a type for your data vizualization, check the docs to see all available types"
                self.create_data(name, data=data, type=type)
            elif stored is not [] and replace:
                asset = stored
                self.update_data(name, data=data, type=type)
            elif stored is not [] and not replace and type is 'line':
                asset = stored
                self.append_data(name, data=data, type=type)
            elif stored is not [] and not replace and type is not 'line':
                asset = stored
                self.update_data(name, data=data, type=type)
            
        def _create_or_update_file(self, file_name="", path="", **kwargs):
            assert self.id != None, "Please checkout or create an experiment first"
            stored = self.get_file(file_name)
            if stored == []:
                self.create_file(file_name, kwargs["object_name"], kwargs["large"])
            else:
                self.update_file(file_name=file_name, **kwargs)

        def store(self, name="", path=None, zip=False):
            assert self.id != None, "Please checkout or create an experiment first"

            if path != None:
                if zip:
                    path = utils.zipdir(path)
                filesize = Path(path).stat().st_size
                if filesize < 5*1024*1024:
                    filename = path.split('/')[-1]
                    if name == 'model-latest':
                        object_name = os.path.join(self.id, '0', filename)
                    else:
                        object_name = os.path.join(self.id, filename)
                    self._send_file(path, name, object_name, None)
                else:
                    filename = path.split('/')[-1]
                    if name == 'model-latest':
                        object_name = os.path.join(self.id, '0', filename)
                    else:
                        object_name = os.path.join(self.id, filename)
                    self._send_large_file(path, name, object_name, None)
            else:
                if name == 'config':
                    if not os.path.isfile(os.path.join(self.config_dir, "pipeline.config")):
                        raise FileNotFoundError("No config file found")
                    path = os.path.join(self.config_dir, "pipeline.config")
                    object_name = os.path.join(self.id, "pipeline.config")
                    self._send_file(path, name, object_name, None)
                elif name == 'checkpoint-data-latest':
                    file_list = os.listdir(self.checkpoint_dir)
                    ckpt_id = max([int(p.split('-')[1].split('.')[0]) for p in file_list if 'index' in p])
                    ckpt_data_file = None
                    for f in file_list:
                        if "{}.data".format(ckpt_id) in f:
                            ckpt_data_file = f
                    if ckpt_data_file is None:
                        raise exceptions.ResourceNotFoundError("Could not find matching data file with index")
                    path = os.path.join(self.checkpoint_dir, ckpt_data_file)
                    object_name = os.path.join(self.id, ckpt_data_file)
                    self._send_large_file(path, name, object_name, None)
                elif name == 'checkpoint-index-latest':
                    file_list = os.listdir(self.checkpoint_dir)
                    ckpt_id = max([int(p.split('-')[1].split('.')[0]) for p in file_list if 'index' in p])
                    ckpt_index = "ckpt-{}.index".format(ckpt_id)
                    path = os.path.join(self.checkpoint_dir, ckpt_index)
                    object_name = os.path.join(self.id, ckpt_index)
                    self._send_file(path, name, object_name, None)
                elif name == 'model-latest':
                    file_path = os.path.join(self.exported_model_dir, 'saved_model')
                    path = utils.zipdir(file_path)
                    object_name = os.path.join(self.id, '0', 'saved_model.zip')
                    self._send_large_file(path, name, object_name, None)
            return object_name

        def download(self, name, path='', large=None):
            assert self.id != None, "Please checkout or create an experiment first"
            f = self.get_file(name)
            object_name = f["object_name"]
            if large == None:
                large = f["large"]
            if large:
                self.dl_large_file(object_name, os.path.join(path, object_name.split('/')[-1]))
            else:
                self.dl_file(object_name, os.path.join(path, object_name.split('/')[-1]))
            print('{} downloaded successfully'.format(object_name.split('/')[-1]))
            
        def dl_large_file(self, object_name, path):
            url = self.urls._get_presigned_url('get', object_name, bucket_model=True)
            with open(path, 'wb') as handler:
                filename = url.split('/')[-1]
                print("Downloading {}".format(filename))
                print('-----')    
                response = requests.get(url, stream=True)
                total_length = response.headers.get('content-length')
                if total_length is None:  # no content length header
                    print("Couldn't download {} file".format(filename.split('?')[0]))
                else:
                    dl = 0
                    count = 0
                    total_length = int(total_length)
                    for data in response.iter_content(chunk_size=4096):
                        dl += len(data)
                        handler.write(data)
                        done = int(50 * dl / total_length)
                        if self.interactive:
                            sys.stdout.write(f"\r[{'=' * done}{' ' * (50 - done)}]")
                            sys.stdout.flush()
                        else:
                            if count%500==0:
                                print('['+'='* done+' ' * (50 - done)+']')
                        count += 1
            print('--*--')
        
        def dl_file(self, object_name, path):
            url = self.urls._get_presigned_url('get', object_name, bucket_model=True)
            with open(path, 'wb') as handler:
                filename = url.split('/')[-1]
                response = requests.get(url, stream=True)
                total_length = response.headers.get('content-length')
                if total_length is None:  # no content length header
                    print("Couldn't download {} file".format(filename))
                else:
                    print("Downloading {}".format(filename.split('?')[0]))
                    for data in response.iter_content(chunk_size=1024):
                        handler.write(data)

        def setup_dirs(self):
            self.base_dir = self.experiment_name
            self.metrics_dir = os.path.join(self.base_dir, 'metrics')
            self.png_dir = os.path.join(self.base_dir, 'images')
            self.checkpoint_dir = os.path.join(self.base_dir, 'checkpoint')
            self.record_dir = os.path.join(self.base_dir, 'records')
            self.config_dir = os.path.join(self.base_dir, 'config')
            self.results_dir = os.path.join(self.base_dir, 'results')
            self.exported_model_dir = os.path.join(self.base_dir, 'exported_model')

            if not os.path.isdir(self.experiment_name):
                print("No directory for this project has been found, creating directory and sub-directories...")
                os.mkdir(self.experiment_name)

            self._create_dir(self.base_dir)
            self._create_dir(self.png_dir)
            self._create_dir(self.checkpoint_dir)
            self._create_dir(self.metrics_dir)
            self._create_dir(self.record_dir)
            self._create_dir(self.config_dir)
            self._create_dir(self.results_dir)
            self._create_dir(self.exported_model_dir)

        def _create_dir(self, dir_name):
            if not os.path.isdir(dir_name):
                os.mkdir(dir_name)

        def dl_annotations(self, option="all"):
            """ Download all the annotations made on Picsell.ia Platform for your project.
            Called when checking out a network
            Args:
                option (str): Define what type of annotation to export (accepted or all)

            Raises:
                NetworkError: If Picsell.ia server is not responding or host is incorrect.
                ResourceNotFoundError: If we can't find any annotations for that project.
            """

            print("Downloading annotations ...")
            assert self.id != None, "self.id"

            try:
                to_send = {"type": option}
                r = requests.get(self.host + 'experiment/{}/dl_annotations'.format(self.id),
                                data=json.dumps(to_send), headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            if r.status_code != 200:
                raise exceptions.ResourceNotFoundError(r.text)

            self.dict_annotations = r.json()

            if len(self.dict_annotations.keys()) == 0:
                raise exceptions.ResourceNotFoundError("You don't have any annotations")
            return r.json()

        def dl_pictures(self):
            """Download your training set on the machine (Use it to dl images to Google Colab etc.)
            Save it to /project_id/images/*
            Perform train_test_split & send the repartition to Picsell.ia Platform

            Raises:
                ResourceNotFoundError : If no annotations in the Picsell.ia Client yet or images can't be downloaded"""

            if not hasattr(self, "dict_annotations"):
                raise exceptions.ResourceNotFoundError("Please dl_annotations model with dl_annotations()")

            if "images" not in self.dict_annotations.keys():
                raise exceptions.ResourceNotFoundError("Please run dl_annotations function first")

            print("Downloading images ...")

            if not os.path.isdir(self.png_dir):
                os.makedirs(self.png_dir)

            lst = []
            for info in self.dict_annotations["images"]:
                lst.append(info["external_picture_url"])
            t = len(set(lst))
            print('-----')
            nb_threads = 20
            infos_split = list(mlt.chunks(self.dict_annotations["images"], nb_threads))
            counter = Value('i', 0)
            p = Pool(nb_threads, initializer=mlt.pool_init, 
                initargs=(t, self.png_dir, counter,self.interactive,))
            p.map(mlt.dl_list, infos_split)
            print('--*--')
            print("Images downloaded")

        def generate_labelmap(self):
            """THIS FUNCTION IS MAINTAINED FOR TENSORFLOW 1.X
            ----------------------------------------------------------
            Genrate the labelmap.pbtxt file needed for Tensorflow training at:
                - project_id/
                    network_id/
                        training_id/
                            label_map.pbtxt
            Raises:
                ResourceNotFoundError : If no annotations in the Picsell.ia Client yet or images can't be downloaded
                                        If no directories have been created first."""

            print("Generating labelmap ...")
            if not hasattr(self, "dict_annotations") or not hasattr(self, "base_dir"):
                raise exceptions.ResourceNotFoundError("Please run create_network() or checkout_network() then dl_annotations()")

            self.label_path = os.path.join(self.base_dir, "label_map.pbtxt")

            if "categories" not in self.dict_annotations.keys():
                raise exceptions.ResourceNotFoundError("Please run dl_annotations() first")

            categories = self.dict_annotations["categories"]
            labels_Network = {}
            try:
                with open(self.label_path, "w+") as labelmap_file:
                    for k, category in enumerate(categories):
                        name = category["name"]
                        labelmap_file.write("item {\n\tname: \"" + name + "\"" + "\n\tid: " + str(k + 1) + "\n}\n")
                        # if self.project_type == 'classification':
                        #     labels_Network[str(k)] = name
                        # else:
                        labels_Network[str(k + 1)] = name
                    labelmap_file.close()
                print(f"Label_map.pbtxt created @ {self.label_path}")

            except Exception:
                raise exceptions.ResourceNotFoundError("No directory found, please call checkout_network() or create_network() function first")

            self.label_map = labels_Network

        def train_test_split(self, prop=0.8):

            if not hasattr(self, "dict_annotations"):
                raise exceptions.ResourceNotFoundError("Please download annotations first")

            if "images" not in self.dict_annotations.keys():
                raise exceptions.ResourceNotFoundError("Please download annotations first")

            self.train_list = []
            self.eval_list = []
            self.train_list_id = []
            self.eval_list_id = []
            self.index_url = utils.train_valid_split_obj_simple(self.dict_annotations, prop)

            total_length = len(self.dict_annotations["images"])
            for info, idx in zip(self.dict_annotations["images"], self.index_url):
                pic_name = os.path.join(self.png_dir, info['external_picture_url'])
                if idx == 1:
                    self.train_list.append(pic_name)
                    self.train_list_id.append(info["internal_picture_id"])
                else:
                    self.eval_list.append(pic_name)
                    self.eval_list_id.append(info["internal_picture_id"])

            print(f"{len(self.train_list_id)} images used for training and {len(self.eval_list_id)} images used for validation")

            label_train, label_test, cate = utils.get_labels_repartition_obj_detection(self.dict_annotations, self.index_url)
            self.train_repartition = label_train
            self.test_repartition = label_test
            self.categories = cate


    class Datalake:
        def __init__(self, host, api_token, organization_id=None):
            """[summary]

            Args:
                host ([type]): [description]
                auth ([type]): [description]
                dataset_id ([type], optional): [description]. Defaults to None.
            """
            self.host = host
            self.organization_id = organization_id
            self.fetched_pictures = []
            self.auth = {"Authorization": "Token " + api_token}
            self.picture = self.Picture(host=self.host, auth=self.auth, organization_id=self.organization_id)
            self.dataset = self.Dataset(host=self.host, auth=self.auth, organization_id=self.organization_id)
        

        def push_dataset(self, name=None, description=None, tags=[], imgdir=None, annotations_path=None, format=None, only_annotations=False):
            """
            This method is a wrapper around Dataset objects, this will push image to your lake, create a dataset and import annotations automatically


            Args:
                imgdir ([type], optional): [description]. Defaults to None.
                annotations_path ([type], optional): [description]. Defaults to None.
                source ([type], optional): [description]. Defaults to None.
            """
            if imgdir is None and (format != "legacy" or annotations_path is None):
                raise exceptions.InvalidQueryError("You did not provide any `imgdir` and you are not pushing a Dataset from our Legacy Platform")

            if annotations_path is not None and format == "legacy" and not only_annotations and imgdir is None:
                try:
                    with open(annotations_path, 'rb') as f:
                        dict_annotations = json.load(f)
                except Exception as e:
                    raise exceptions.InvalidQueryError(str(e))

                if not os.path.isdir('tmp'):
                    os.mkdir('tmp')

                if "images" not in dict_annotations.keys():
                    raise exceptions.ResourceNotFoundError("Please run dl_annotations function first")

                print("Downloading images ...")

                
                lst = []
                for info in dict_annotations["images"]:
                    lst.append(info["external_picture_url"])
                t = len(set(lst))
                print('-----')
                nb_threads = 20
                infos_split = list(mlt.chunks(dict_annotations["images"], nb_threads))
                counter = Value('i', 0)
                p = Pool(nb_threads, initializer=mlt.pool_init, 
                    initargs=(t, 'tmp', counter,False,))
                p.map(mlt.dl_list, infos_split)
                print('--*--')
                print("Images downloaded")

                print('--*--')
                print('Uploading Images to your Lake')


                list_path = [os.path.join('tmp', e) for e in os.listdir('tmp')]
                t = len(set(lst))

                list_path_split = list(mlt.chunks(list_path, nb_threads))
                p = Pool(nb_threads)
                func = partial(self.picture.upload, tags=tags, source="sdk")
                p.map(func, list_path_split)
                
                print('--*--')
                print('Creating Dataset')

                pictures = self.picture.fetch(tags=tags)

                dataset_id = self.dataset.create(name=name, pictures=pictures)

                print('--*--')
                print('Scanning Annotations')

                # dataset = self.dataset.fetch(name=name) 
                label_to_create = []

                p2 = Pool(nb_threads)

                upload = partial(
                    self.dataset.add_annotation_legacy, 
                    dataset_id=dataset_id,
                    new_picture=True
                )
                list_annotations = list(mlt.chunks(dict_annotations["annotations"], nb_threads))
                p2.map(upload, list_annotations)


                for annotations in dict_annotations["annotations"]:
                    for ann in annotations["annotations"]:
                        tmp = [ann["type"], ann["label"]]
                        if tmp not in label_to_create:
                            label_to_create.append(tmp)

                print('--*--')
                print('Wrapping it up')

                for l in label_to_create:
                    self.dataset.create_labels(dataset_id=dataset_id, ann_type=l[0], name=l[1])

                print('Annotations uploaded :D ')

            elif annotations_path is not None and format == "legacy" and not only_annotations and imgdir is None:
                try:
                    with open(annotations_path, 'rb') as f:
                        dict_annotations = json.load(f)
                except Exception as e:
                    raise exceptions.InvalidQueryError(str(e))

                if not os.path.isdir('tmp'):
                    os.mkdir('tmp')

                if "images" not in dict_annotations.keys():
                    raise exceptions.ResourceNotFoundError("Please run dl_annotations function first")

                print("Downloading images ...")

                
                lst = []
                for info in dict_annotations["images"]:
                    lst.append(info["external_picture_url"])
                t = len(set(lst))
                print('-----')
                nb_threads = 20
                infos_split = list(mlt.chunks(dict_annotations["images"], nb_threads))
                counter = Value('i', 0)
                p = Pool(nb_threads, initializer=mlt.pool_init, 
                    initargs=(t, 'tmp', counter,False,))
                p.map(mlt.dl_list, infos_split)
                print('--*--')
                print("Images downloaded")

                print('--*--')
                print('Uploading Images to your Lake')


                list_path = [os.path.join(img_dir, e) for e in os.listdir(img_dir)]
                t = len(set(lst))

                list_path_split = list(mlt.chunks(list_path, nb_threads))
                p = Pool(nb_threads)
                func = partial(self.picture.upload, tags=tags, source="sdk")
                p.map(func, list_path_split)
                
                print('--*--')
                print('Creating Dataset')

                pictures = self.picture.fetch(tags=tags)

                dataset_id = self.dataset.create(name=name, pictures=pictures)

                print('--*--')
                print('Scanning Annotations')

                # dataset = self.dataset.fetch(name=name) 
                label_to_create = []

                p2 = Pool(nb_threads)

                upload = partial(
                    self.dataset.add_annotation_legacy, 
                    dataset_id=dataset_id,
                    new_picture=True
                )
                list_annotations = list(mlt.chunks(dict_annotations["annotations"], nb_threads))
                p2.map(upload, list_annotations)


                for annotations in dict_annotations["annotations"]:
                    for ann in annotations["annotations"]:
                        tmp = [ann["type"], ann["label"]]
                        if tmp not in label_to_create:
                            label_to_create.append(tmp)

                print('--*--')
                print('Wrapping it up')

                for l in label_to_create:
                    self.dataset.create_labels(dataset_id=dataset_id, ann_type=l[0], name=l[1])

                print('Annotations uploaded :D ')

            elif only_annotations:
                try:
                    with open(annotations_path, 'rb') as f:
                        dict_annotations = json.load(f)
                except Exception as e:
                    raise exceptions.InvalidQueryError(str(e))

                nb_threads = 20

                dataset = self.dataset.fetch(name=name) 

                print("Dataset Fetched")
                label_to_create = []

                p2 = Pool(nb_threads)

                upload = partial(
                    self.dataset.add_annotation_legacy, 
                    dataset_id=dataset["dataset_id"],
                    new_picture=False
                )
                list_annotations = list(mlt.chunks(dict_annotations["annotations"], nb_threads))
                p2.map(upload, list_annotations)

                print("Uploading annotations ...")
                for annotations in dict_annotations["annotations"]:
                    for ann in annotations["annotations"]:
                        tmp = [ann["type"], ann["label"]]
                        if tmp not in label_to_create:
                            label_to_create.append(tmp)

                print('--*--')
                print('Wrapping it up')

                for l in label_to_create:
                    self.dataset.create_labels(dataset_id=dataset['dataset_id'], ann_type=l[0], name=l[1])

                print('Annotations uploaded :D ')
            return
            
        class Picture:
            def __init__(self, host, auth, organization_id=None):
                """[summary]

                Args:
                    host ([type]): [description]
                    auth ([type]): [description]
                    dataset_id ([type], optional): [description]. Defaults to None.
                """
                self.host = host
                self.auth = auth 
                self.organization_id = organization_id
                self.fetched_pictures = []

            def status(self):

                if self.fetched_pictures == []:
                    print("No assets selected")
                else:
                    print("Number of Assets selected : {} \n".format(len(self.fetched_pictures)))

            def list(self):
                """[summary]
                List all the pictures of your datalake

                Raises:
                    exceptions.NetworkError: [Server Not responding]
                    exceptions.AuthenticationError: [Token Invalid]

                Returns:
                    [dict]: [datasets infos]
                """
                try:
                    if self.organization_id is None:
                        r = requests.get(self.host + 'datalake/none', headers=self.auth)
                    else:
                        r = requests.get(self.host + 'datalake/{}'.format(self.organization_id), headers=self.auth)
                except Exception:
                    raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
                
                if r.status_code != 200:
                    print(r.text)
                    raise exceptions.AuthenticationError('The project_token provided does not match any of the known project_token for your profile.')

                self.fetched_pictures = r.json()['pictures']
                return r.json()

            def fetch(self, quantity=1, tags= []):
                try:
                    data = {
                        'tags': tags,
                        'quantity': quantity
                    }
                    if self.organization_id == None:
                        r = requests.post(self.host + 'datalake/search/none', data=json.dumps(data), headers=self.auth)
                    else:
                        r = requests.post(self.host + 'datalake/search/{}'.format(self.organization_id), data=json.dumps(data), headers=self.auth)
                except Exception:
                    raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
                
                if r.status_code != 200:
                    raise exceptions.AuthenticationError('The project_token provided does not match any of the known project_token for your profile.')

                self.fetched_pictures = r.json()['pictures']

                if len(self.fetched_pictures) < 1:
                    print("No assets found for tags {}".format(tags))
                return self.fetched_pictures

            def delete(self, pictures=None):

                if pictures is None:
                    pictures= self.fetched_pictures

                if len(pictures) < 1:
                    print("No assets selected, please run Client.Datalake.Pictures.Fetch() first")
                    return 
                else:
                    try:
                        data = {
                            'to_delete': pictures
                        }
                        if self.organization_id == None:
                            r = requests.post(self.host + 'datalake/delete/none', data=json.dumps(data), headers=self.auth)
                        else:
                            r = requests.post(self.host + 'datalake/delete/{}'.format(self.organization_id), data=json.dumps(data), headers=self.auth)
                    except Exception:
                        raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
                    
                    if r.status_code != 200:
                        raise exceptions.AuthenticationError('The project_token provided does not match any of the known project_token for your profile.')

                    print(len(pictures), "assets deleted from Lake")

                    return self

            def add_tags(self,pictures=None, tags=[]):

                if pictures is None:
                    pictures= self.fetched_pictures

                if len(pictures) < 1:
                    print("No assets selected, please run Client.Datalake.Pictures.Fetch() first")
                    return 
                elif len(tags) < 1:
                    print("You can't use picture.tag() with an empty tags list")
                    return
                else:
                    try:
                        data = {
                            'tags': tags,
                            'to_tag': pictures
                        }
                        if self.organization_id == None:
                            r = requests.post(self.host + 'datalake/tag/none', data=json.dumps(data), headers=self.auth)
                        else:
                            r = requests.post(self.host + 'datalake/tag/{}'.format(self.organization_id), data=json.dumps(data), headers=self.auth)
                    except Exception:
                        raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
                    
                    if r.status_code != 200:
                        raise exceptions.AuthenticationError('The project_token provided does not match any of the known project_token for your profile.')

                    print(len(tags), " tags added to {} assets ".format(len(pictures)))

                    return self

            def remove_tags(self,pictures=None, tags=[]):
                if pictures is None:
                    pictures= self.fetched_pictures

                if len(pictures) < 1:
                    print("No assets selected, please run Client.datalake.pictures.fetch() first")
                    return 
                elif len(tags) < 1:
                    print("You can't use picture.remove_tags() with an empty tags list")
                    return
                else:
                    try:
                        data = {
                            'tags': tags,
                            'to_delete_tag': pictures
                        }
                        if self.organization_id == None:
                            r = requests.post(self.host + 'datalake/delete_tag/none', data=json.dumps(data), headers=self.auth)
                        else:
                            r = requests.post(self.host + 'datalake/delete_tag/tag/{}'.format(self.organization_id), data=json.dumps(data), headers=self.auth)
                    except Exception:
                        raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
                    
                    if r.status_code != 200:
                        raise exceptions.AuthenticationError('Please provide a valide api_token')

                    print(len(tags), "tags deleted to {} assets ".format(len(pictures)))

                    return self

            def upload(self, filepath, tags=[], source='sdk'):
                urls_utils = urls(self.host, self.auth)
                    
                try:
                    if isinstance(filepath, list):
                        for path in filepath:
                            internal_key = os.path.join(str(uuid4()))+ '.' + path.split('/')[-1].split('.')[-1]
                            external_url = path.split('/')[-1]   
                            try: 
                                width, height = Image.open(path).size
                            except Exception as e:
                                print(e)
                                return
                            response = urls_utils._get_presigned_url("post", object_name=internal_key)
                            with open(path, 'rb') as f:
                                r = requests.post(response["url"], data=response["fields"], files = {'file': (internal_key, f)})
                                
                                if r.status_code == 204:
                                    data = json.dumps({
                                        'internal_key': internal_key,
                                        'external_url': external_url,
                                        'height': height,
                                        'width': width,
                                        'tags': tags,
                                        'source': source
                                    })
                                    if self.organization_id == None:
                                        r = requests.put(self.host + 'picture/upload/none', data=data, headers=self.auth)
                                    else:
                                        r = requests.put(self.host + 'picture/upload/{}'.format(self.organization_id), data=data, headers=self.auth)
                                else:
                                    print(r.text)
                        print("{} Assets uploaded".format(len(filepath)))
                    else:
                        internal_key = os.path.join(str(uuid4()))+ '.' + filepath.split('/')[-1].split('.')[-1]
                        external_url = filepath.split('/')[-1]   
                        try: 
                            width, height = Image.open(filepath).size
                        except Exception as e:
                            print(e)
                            return
                        response = urls_utils._get_presigned_url("post", object_name=internal_key)
                        with open(filepath, 'rb') as f:
                            r = requests.post(response["url"], data=response["fields"], files = {'file': (internal_key, f)})
                            
                            if r.status_code == 204:
                                data = json.dumps({
                                    'internal_key': internal_key,
                                    'external_url': external_url,
                                    'height': height,
                                    'width': width,
                                    'tags': tags,
                                    'source': source
                                })
                                if self.organization_id == None:
                                    r = requests.put(self.host + 'picture/upload/none', data=data, headers=self.auth)
                                else:
                                    r = requests.put(self.host + 'picture/upload/{}'.format(self.organization_id), data=data, headers=self.auth)
                            else:
                                print(r.text)
                        print("Asset uploaded")
                    
                except Exception as e:
                    print("{} was not uploaded : {}".format(filepath, str(e)))
                    return
        
        class Dataset:

            def __init__(self, host, auth, organization_id=None):
                """[summary]

                Args:
                    host ([type]): [description]
                    auth ([type]): [description]
                    dataset_id ([type], optional): [description]. Defaults to None.
                """
                self.host = host
                self.auth = auth 
                self.dataset_id = None 
                self.organization_id = organization_id
                self.fetched_dataset = {}
                # self.urls = urls(self.host, self.auth)

            ###########################################
            ###### DATASET ( LIST, GET, CREATE, DELETE)
            ###########################################

            def fetch(self, name=None, version=None):
                
                if name is None:
                    print("Please select a name")
                    return
                
                if version is None and name is None:
                    print("Type at least a dataset name")
                    return

                try:
                    if version is None:
                        version = "latest"
                    if self.organization_id == None:
                        r = requests.get(self.host + 'dataset/none/{}/{}'.format(name, version), headers=self.auth)
                    else:
                        r = requests.get(self.host + 'dataset/{}/{}/{}'.format(self.organization_id, name, version), headers=self.auth)

                except Exception:
                    raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
                
                if r.status_code != 200:
                    raise exceptions.AuthenticationError('The project_token provided does not match any of the known project_token for your profile.')

                self.dataset_id = r.json()['dataset']['dataset_id']
                self.fetched_dataset = r.json()['dataset']

                return self.fetched_dataset

            def list(self):
                """[summary]
                List all your Datasets

                Raises:
                    exceptions.NetworkError: [Server Not responding]
                    exceptions.AuthenticationError: [Token Invalid]

                Returns:
                    [dict]: [datasets infos]
                """
                try:
                    if self.organization_id == None:
                        r = requests.get(self.host + 'dataset/none', headers=self.auth)
                    else:
                        r = requests.get(self.host + 'dataset/{}'.format(self.organization_id), headers=self.auth)
                except Exception:
                    raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
                
                if r.status_code != 200:
                    raise exceptions.AuthenticationError('The project_token provided does not match any of the known project_token for your profile.')

                for ds in r.json()['datasets']:
                    print('-------------\nDataset Name: {}\nDataset Version: {}\nNb Assets: {}\n-------------'.format(ds['dataset_name'], ds['version'], ds['size']) )

                return self

          
            def create(self, name: str='', description: str='', private: bool=True, pictures=[]):
                """[summary]

                Args:
                    dataset_name ([str]): [description]
                    description (str, optional): [description]. Defaults to "".
                    private (bool, optional): [description]. Defaults to True.

                Raises:
                    exceptions.NetworkError: [description]
                    exceptions.ResourceNotFoundError: [description]

                Returns:
                    [type]: [description]
                """

                
                data = json.dumps({ 
                    'dataset_name': name,
                    'description': description,
                    'private': private,
                    'pictures': pictures
                
                })

                if len(pictures) <1:
                    print('Please specify the assets to add to dataset')
                    return 

                try:
                    
                    if self.organization_id == None:
                        r = requests.put(self.host + 'dataset/none', data=data, headers=self.auth)
                    else:
                        r = requests.put(self.host + 'dataset/{}'.format(self.organization_id), data=data, headers=self.auth)
                    
                except Exception:
                    raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
                
                if r.status_code != 201:
                    raise exceptions.ResourceNotFoundError(r.text)
                
                print(f"Dataset {name} created with {len(pictures)} assets in it")
                self.dataset_id = r.json()["pk"]
                return self.dataset_id

            def new_version(self, name: str='', version: str='', pictures=[], from_version='latest'):
                """[summary]

                Args:
                    dataset_name ([str]): [description]
                    description (str, optional): [description]. Defaults to "".
                    private (bool, optional): [description]. Defaults to True.

                Raises:
                    exceptions.NetworkError: [description]
                    exceptions.ResourceNotFoundError: [description]

                Returns:
                    [type]: [description]
                """
                data = json.dumps({ 
                    'name': name,
                    'version': version,
                    'pictures': pictures,
                    'from_version': from_version
                
                })

                # if len(pictures) <1:
                #     print('Please specify the assets to upload to dataset')
                #     return 

                try:
                    
                    if self.organization_id == None:
                        r = requests.put(self.host + 'dataset/none/new_version', data=data, headers=self.auth)
                    else:
                        r = requests.put(self.host + 'dataset/{}/new_version'.format(self.organization_id), data=data, headers=self.auth)
                    
                except Exception:
                    raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
                
                if r.status_code != 201:
                    raise exceptions.ResourceNotFoundError(r.text)
                
                self.dataset_id = r.json()['pk']
                return self

            def add_data(self, name: str='', version: str='latest', pictures=[]):
                """[summary]

                Args:
                    dataset_name ([str]): [description]
                    description (str, optional): [description]. Defaults to "".
                    private (bool, optional): [description]. Defaults to True.

                Raises:
                    exceptions.NetworkError: [description]
                    exceptions.ResourceNotFoundError: [description]

                Returns:
                    [type]: [description]
                """

                dataset_id = self.dataset_id if self.dataset_id is not None else ''
                data = json.dumps({ 
                    'name': name,
                    'version': version,
                    'pictures': pictures,
                    'pk': dataset_id
                
                })

                if len(pictures) <1:
                    print('Please specify the assets to add to dataset')
                    return 

                try:
                    
                    if self.organization_id == None:
                        r = requests.post(self.host + 'dataset/none', data=data, headers=self.auth)
                    else:
                        r = requests.post(self.host + 'dataset/{}'.format(self.organization_id), data=data, headers=self.auth)
                    
                except Exception:
                    raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
                
                if r.status_code != 201:
                    raise exceptions.ResourceNotFoundError(r.text)
                
                print(f"{len(pictures)} assets added to Dataset {name}/{version}")
                return self

            def delete(self, name, version='latest'):

                try:
                    if self.organization_id == None:
                        r = requests.delete(self.host + 'dataset/none/{}/{}'.format(name, version), headers=self.auth)
                    else:
                        r = requests.delete(self.host + 'dataset/{}/{}/{}'.format(self.organization_id, name, version), headers=self.auth)
                    
                except Exception:
                    raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
                
                if r.status_code != 201:
                    raise exceptions.ResourceNotFoundError(r.text)
                
                print(f"Dataset {name} deleted")
                return 



            

            #############################################
            ################# PICTURE ( ADD, DELETE )
            ##############################################
            
            
            ##########################################
            ########## ANNOTATION ( LIST, ADD, DELETE)
            ##########################################
            def list_annotations(self, dataset_id=None):

                if self.dataset_id is None and dataset_id is None:
                    raise exceptions.InvalidQueryError('Please specify a dataset ID or fetch a dataset first')
                
                else:
                    dataset_id = self.dataset_id if self.dataset_id is not None else dataset_id 

                try:
                    if is_uuid(dataset_id):
                        r = requests.get(self.host + 'annotation/' + dataset_id, headers=self.auth)
                    else:
                        print("Please provide a valid uuid")
                        return
                except Exception:
                    raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
                
                if r.status_code != 200:
                    raise exceptions.ResourceNotFoundError(r.text)
                
                return r.json()
                

            def add_annotation(self, dataset_id, picture_id, new_picture=False,  **kwargs ):
                """[summary]

                Args:
                    project_id ([type]): [description]
                    picture_id ([type]): [description]
                    annotation

                Raises:
                    exceptions.NetworkError: [description]
                    exceptions.ResourceNotFoundError: [description]

                Returns:
                    [type]: [description]
                """
                try:
                    if not new_picture:
                        if is_uuid(dataset_id) and is_uuid(picture_id):
                            r = requests.put(self.host + 'annotation/' + dataset_id + '/' + picture_id, data=json.dumps(kwargs), headers=self.auth)
                        else:
                            print("Please provide a valid uuid")
                            return
                    else:
                        if is_uuid(dataset_id):
                            r = requests.put(self.host + 'annotation/new/' + dataset_id + '/' + picture_id, data=json.dumps(kwargs), headers=self.auth)
                        else:
                            print("Please provide a valid uuid")
                            return
                except Exception:
                    raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
                
                if r.status_code != 201:
                    raise exceptions.ResourceNotFoundError(r.text)
                
                return r.json()
            

            def add_annotation_legacy(self, annotation_yield, dataset_id="", new_picture=False):
                """[summary]

                Args:
                    project_id ([type]): [description]
                    picture_id ([type]): [description]
                    annotation

                Raises:
                    exceptions.NetworkError: [description]
                    exceptions.ResourceNotFoundError: [description]

                Returns:
                    [type]: [description]
                """
                for annotations in annotation_yield:
                    picture_id = annotations["external_picture_url"]
                    args= {
                        "picture_id": picture_id,
                        "nb_instances": annotations["nb_labels"],
                        "duration": annotations["time_spent"],
                        "data": annotations["annotations"]
                    }
                    try:
                        if not new_picture:
                            if is_uuid(dataset_id):
                                r = requests.put(self.host + 'annotation/new/' + dataset_id + '/' + picture_id, data=json.dumps(args), headers=self.auth)
                            else:
                                print("Please provide a valid uuid")
                                return
                        else:
                            if is_uuid(dataset_id):
                                r = requests.put(self.host + 'annotation/new/' + dataset_id + '/' + picture_id, data=json.dumps(args), headers=self.auth)
                            else:
                                print("Please provide a valid uuid")
                                return
                    except Exception:
                        raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
                    
                    if r.status_code != 201:
                        raise exceptions.ResourceNotFoundError(r.text)
            
            
            def delete_annotations(self, dataset_id=None, picture_id=None, all_annotations=False):
                """[summary]

                Args:
                    project_id ([type]): [description]
                    picture_id ([type]): [description]
                    annotation

                Raises:
                    exceptions.NetworkError: [description]
                    exceptions.ResourceNotFoundError: [description]

                Returns:
                    [type]: [description]
                """


                if self.dataset_id is None and dataset_id is None:
                    raise exceptions.InvalidQueryError('Please specify a dataset ID or fetch a dataset first')
                
                else:
                    dataset_id = self.dataset_id if self.dataset_id is not None else dataset_id 

                if picture_id is None and not all_annotations:
                    raise exceptions.InvalidQueryError('You did not specify a picture ID and the `all_annotations` parameter is False')

                if picture_id is not None:
                    try:
                        if is_uuid(dataset_id) and is_uuid(picture_id):
                            r = requests.delete(self.host + 'annotation/' + dataset_id + '/' + picture_id, headers=self.auth)
                        else:
                            print("Please provide a valid uuid")
                            return
                    except Exception:
                        raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
                    
                    if r.status_code != 200:
                        raise exceptions.ResourceNotFoundError(r.text)
                
                else:
                    try:
                        if is_uuid(dataset_id):
                            r = requests.delete(self.host + 'annotation/' + dataset_id, headers=self.auth)
                        else:
                            print("Please provide a valid uuid")
                            return
                    except Exception:
                        raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
                    
                    if r.status_code != 200:
                        raise exceptions.ResourceNotFoundError(r.text)
                
                return r.json()

        
            def create_labels(self, dataset_id=None, name=None, ann_type=None):
                try:
                   
                    if self.dataset_id is None and dataset_id is None:
                        raise exceptions.InvalidQueryError("You did not provide a dataset_id of fetched a dataset before creating labels")

                    else:
                        dataset_id = self.dataset_id if dataset_id is None else dataset_id
                    
                    if is_uuid(dataset_id):
                        r = requests.put(self.host + 'label/{}/{}/{}'.format(dataset_id, name, ann_type), headers=self.auth)
                    else:
                        print("Please provide a valid uuid")
                        return
                   
                except Exception:
                    raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
                
                if r.status_code == 200:
                    print("Label {} already exists".format(name))
                
                elif r.status_code == 201:
                    pass 

                else:
                    raise exceptions.InvalidQueryError("Label creation failed")
                
                return r.json()
            
            #############################################
            ################# PICTURE ( ADD, DELETE )
            ##############################################
                    
    class Network:

        def __init__(self, api_token, host, network_id=None):
            """[summary]

            Args:
                host ([type]): [description]
                auth ([type]): [description]
                dataset_id ([type], optional): [description]. Defaults to None.
            """
            self.host = host
            self.auth = {"Authorization": "Token " + api_token} 
            self.network_id = network_id
            self.network_name = ""
            self.urls = urls(self.host, self.auth)

        def list(self, organization="null"):
            """[summary]
            List all your Datasets

            Raises:
                exceptions.NetworkError: [Server Not responding]
                exceptions.AuthenticationError: [Token Invalid]

            Returns:
                [dict]: [datasets infos]
            """
            data = {
                'organization': organization
            }
            try:
                r = requests.get(self.host + 'network/'+organization, headers=self.auth, data=data)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.AuthenticationError(r.json()["error"])

            return r.json()

        def get(self, identifier=None, organization='null'):
            """[summary]

            Args:
                identifier ([type]): can be dataset_name (str) or uuid
            Raises:
                exceptions.NetworkError: [description]
                exceptions.AuthenticationError: [description]

            Returns:
                [type]: [description]
            """
            
            try:
                if is_uuid(identifier):
                    if self.network_id is not None:
                        r = requests.get(self.host + 'network/' + organization + '/' + self.network_id, headers=self.auth)
                    else:
                        r = requests.get(self.host + 'network/' + organization + '/' + identifier, headers=self.auth)
                else:
                    r = requests.get(self.host + 'network/by_name/' + organization + '/' + identifier, headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.ResourceNotFoundError(r.text)
            self.network_id = r.json()["model_id"]
            self.network_name = r.json()["network_name"]
            self.files = r.json()["files"]
            self.organization_name = r.json()["organization"]["name"]
            return self

        def create(self, name=None, organization='null', type=""):
            """[summary]

            Args:
                dataset_name ([str]): [description]
                description (str, optional): [description]. Defaults to "".
                private (bool, optional): [description]. Defaults to True.

            Raises:
                exceptions.NetworkError: [description]
                exceptions.ResourceNotFoundError: [description]

            Returns:
                [type]: [description]
            """
            data = json.dumps({
                "name": name,
                "type": type
            })
            try:
                r = requests.post(self.host + 'network/'+organization, data=data, headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 201:
                raise exceptions.ResourceNotFoundError(r.json()["error"])
            self.network_id = r.json()["model_id"]
            self.network_name = r.json()["network_name"]
            self.organization_name = r.json()["organization"]["name"]
            self.files = r.json()["files"]
            print(f"Network created.\nYou can attach I to your experiment.")
            return self

        def delete(self, identifier=None, organization="null"):

            try:
                if self.network_id is not None:
                    r = requests.delete(self.host + 'network/' + organization + '/' + self.network_id, headers=self.auth)
                else:
                    if is_uuid(identifier):
                        r = requests.delete(self.host + 'network/' + organization + '/' + identifier, headers=self.auth)
                    else:
                        r = requests.delete(self.host + 'network/by_name/' + organization + '/' + identifier, headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.ResourceNotFoundError(r.text)

            return r.json()

        def update(self, identifier="", organization="null", **kwargs):
            try:
                if is_uuid(identifier):
                    if self.network_id is not None:   
                        r = requests.put(self.host + 'network/' + organization + '/' + self.network_id, data=json.dumps(kwargs), headers=self.auth)
                    else:
                        r = requests.put(self.host + 'network/' + organization + '/' + identifier, data=json.dumps(kwargs), headers=self.auth)
                else:
                    r = requests.put(self.host + 'network/by_name/' + organization + '/' + identifier, data=json.dumps(kwargs),headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 201:
                raise exceptions.ResourceNotFoundError(r.text)
            
            print(f"Network {identifier} updated.")
            return r.json()

        def _create_or_update_file(self, file_name="", path="", object_name=""):

            files = self.files
            print(files)
            print(file_name)
            if file_name in files.keys():
                self.update(identifier=self.network_id, organization=self.organization_name, files=files)
            else:
                files[file_name] = object_name
                self.update(identifier=self.network_id, organization=self.organization_name, files=files)

        def _send_large_file(self, path=None, file_name=None, object_name=None):
            self.urls._init_multipart(object_name)
            parts = self.urls._upload_part(path, object_name)

            if self.urls._complete_part_upload(parts, object_name, None):
                self._create_or_update_file(file_name, path, object_name=object_name)

        def _send_file(self, path=None, file_name=None, object_name=None):
            response = self.urls._get_presigned_url(method='post', object_name=object_name, bucket_model=True)
            try:
                with open(path, 'rb') as f:
                    files = {'file': (path, f)}
                    http_response = requests.post(response['url'], data=response['fields'], files=files)
                if http_response.status_code == 204:
                    self._create_or_update_file(file_name, path, object_name=object_name)
            except Exception as e:
                raise exceptions.NetworkError(str(e))
        
        def store(self, organization="null", name="", path=None, zip=False):
            if path != None:
                if zip:
                    path = utils.zipdir(path)
                filesize = Path(path).stat().st_size
                filename = path.split('/')[-1]
                if name == 'model-latest':
                    object_name = os.path.join(self.network_id, '0', filename)
                else:
                    object_name = os.path.join(self.network_id, filename)
                if filesize < 5*1024*1024:
                    self._send_file(path, name, object_name)
                else:
                    self._send_large_file(path, name, object_name)

        def update_thumb(self, path=None, organization="null"):
            if path != None:
                filesize = Path(path).stat().st_size
                if filesize < 5*1024*1024:
                    filename = path.split('/')[-1]
                    object_name = os.path.join(self.network_id, filename)
                    response = self.urls._get_presigned_url(method='post', object_name=object_name, bucket_model=False)
                    try:
                        with open(path, 'rb') as f:
                            files = {'file': (path, f)}
                            http_response = requests.post(response['url'], data=response['fields'], files=files)
                        if http_response.status_code == 204:
                            self.update(identifier=self.network_id, organization=self.organization_name, thumb_object_name=object_name)
                    except Exception as e:
                        raise exceptions.NetworkError(str(e))
                else:
                    raise "File too large, must be under 5Mb."
        
        def labels(self, labels):
            self.update(identifier=self.network_id, organization=self.organization_name, labels=labels)


    class Project:

        def __init__(self, host, auth, project_id=None):
            """[summary]

            Args:
                host ([type]): [description]
                auth ([type]): [description]
                dataset_id ([type], optional): [description]. Defaults to None.
            """
            self.host = host
            self.auth = auth 
            self.project_id = project_id
            self.worker = self.Worker(host=self.host, auth= self.auth, project_id=self.project_id)

        def list(self):
            """[summary]
            List all your Datasets

            Raises:
                exceptions.NetworkError: [Server Not responding]
                exceptions.AuthenticationError: [Token Invalid]

            Returns:
                [dict]: [datasets infos]
            """
            try:
                r = requests.get(self.host + 'project', headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.AuthenticationError('The project_token provided does not match any of the known project_token for your profile.')

            return r.json()

        def delete(self):
            try:
                r = requests.delete(self.host + 'project', headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.AuthenticationError('The project_token provided does not match any of the known project_token for your profile.')

            return r.json()

        def create(self, **kwargs):
            try:
                r = requests.put(self.host + 'project', data=json.dumps(kwargs), headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 201:
                raise Exception(r.text)

            return r.json()

        def update(self, identifier, **kwargs):
            try:
                if is_uuid(identifier):
                    if self.project_id is not None:   
                        r = requests.patch(self.host + 'project/' + self.project_id, data=json.dumps(kwargs), headers=self.auth)
                    else:
                        r = requests.patch(self.host + 'project/' + identifier, data=json.dumps(kwargs), headers=self.auth)
                else:
                    r = requests.patch(self.host + 'project/by_name/' + identifier, data=json.dumps(kwargs),headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 201:
                raise exceptions.ResourceNotFoundError(r.text)
            
            print(f"Project {identifier} updated.")
            return r.json()

        class Worker:

            def __init__(self, host, auth, project_id=None):
                """[summary]

                Args:
                    host ([type]): [description]
                    auth ([type]): [description]
                    dataset_id ([type], optional): [description]. Defaults to None.
                """
                self.host = host
                self.auth = auth 
                self.project_id = project_id

            def list(self, identifier):
                try:
                    if is_uuid(identifier):
                        if self.project_id is not None:   
                            r = requests.get(self.host + 'worker/' + self.project_id,  headers=self.auth)
                        else:
                            r = requests.get(self.host + 'worker/' + identifier,  headers=self.auth)
                    else:
                        r = requests.get(self.host + 'worker/by_project_name/' + identifier, headers=self.auth)
                except Exception:
                    raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
                if r.status_code != 200:
                    raise exceptions.ResourceNotFoundError(r.text)
    
                return r.json()
