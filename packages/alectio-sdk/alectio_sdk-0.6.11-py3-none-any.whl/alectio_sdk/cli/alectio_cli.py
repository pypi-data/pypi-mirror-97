import requests
import os
import json
import asyncio
import aiohttp
import sys
import uuid
import yaml
from envyaml import EnvYAML

from datetime import datetime

from gql import Client, gql
from aiogqlc import GraphQLClient

from gql.client import RetryError
from gql.transport.requests import RequestsHTTPTransport

from alectio_sdk.api.project import Project
from alectio_sdk.api.experiment import Experiment
from alectio_sdk.api.model import Model
from alectio_sdk.api.job import Job

from alectio_sdk.tools.utils import extract_id, credentials_exists, get_credentials
from alectio_sdk.tools.fragments import *
from alectio_sdk.tools.mutations import *
from alectio_sdk.tools.utils import credentials_exists
from alectio_sdk.exceptions import APIKeyNotFound
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AlectioClient:
    def __init__(self, environ=os.environ, api_key = None):
        self._environ = environ
            
        if not api_key and 'ALECTIO_API_KEY' not in self._environ and not credentials_exists:
            raise APIKeyNotFound

        self._client_token = None
        # cli user settings
        self._settings = {
            'git_remote': "origin",
            #'base_url': "https://api.alectio.com"
            'env_base_url': "http://localhost:5005",
            'prod_base_url': "https://api.alectio.com"
        }

            
        if api_key:
            os.environ['ALECTIO_API_KEY'] = api_key
            self._environ['ALECTIO_API_KEY'] = api_key
            self._api_key = self._environ['ALECTIO_API_KEY'] if 'ALECTIO_API_KEY' in self._environ else api_key
            try:
                headers = {"Authorization": "Bearer " + api_key}
                r = requests.get(self._settings['env_base_url']+'/api/me', headers=headers)
                if r.status_code == 401:
                    print("Expired or Wrong API Key. Please run alectio login YOU_API_KEY")
                elif r.status_code == 200:
                    self._user_id = r.get_json()['id']
                else:
                    print('Something Went wrong. Check you API Key')
            except:
                print('\n Alectio Error: Something Went wrong.\n')

        else:
            self._api_key_data = get_credentials()
            print(self._api_key_data)
            os.environ['ALECTIO_API_KEY'] = self._api_key_data['api_key']
            self._environ['ALECTIO_API_KEY'] =  self._api_key_data['api_key']
            self._api_key = self._api_key_data['api_key']
            self._user_id = self._api_key_data['user_id']


        # self._endpoint = f'{self._settings['base_url']}/graphql'
        self._endpoint = self._settings['env_base_url'] + "/graphql"

        # graphql client
        self._client = Client(
            transport=RequestsHTTPTransport(
                url=self._endpoint,
                verify=False,
                retries=3,
                headers={'APIKEY': self._api_key}
            ),
            fetch_schema_from_transport=True,
        )

        # client to upload files, images, etc.
        # uses https://pypi.org/project/aiogqlc/
        self._upload_client = GraphQLClient(self._endpoint) # change for dev
        self._oauth_server = 'https://auth.alectio.com/'
        # need to retrive user_id based on token @ DEVI from OPENID
        self._user_id = "82b4fb909f1f11ea9d300242ac110002" # ideally this should be set already. Dummy one will be set when init is invoked
        # compnay id = 7774e1ca972811eaad5238c986352c36s
        # self.dir_path = os.path.dirname(os.path.realpath(__file__))


    def set_user_id(self, token):
        headers = {"Authorization": "Bearer " + self._client_token['access_token']}
        requests_data = requests.get(
            url=self._oauth_server + 'api/me', headers=headers)
        if requests_data.status_code == 401:
            print("Client Token Expired. Please run alectio-kms --refresh")
        elif requests_data.status_code == 200:
            requests_data = requests_data.json()
            self._user_id = requests_data['id']

    def init(self, token=None,file_path='/opt/alectio/client_token.json'):
        if token:
            self.set_user_id(token)
        else:
            if file_path and self._client_token is None:
                with open(file_path, 'r') as f:
                    self._client_token = json.load(f)
                self.set_user_id(self._client_token['access_token'])


    def get_single(self, resource, query_string, params):
        """
        return a single object for the requested resource.
        :params: resource - name of the resource to obtain i.e experiments, projects, models, etc.
        :params: query_string - graphql string to invoke.
        :params: params - variables required to invoke query string in the client.
        """
        query = gql(query_string)
        class_name = lambda class_name: getattr(sys.modules[__name__], class_name)
        singular = self._client.execute(query, params)[resource][0]
        class_to_init = class_name(resource.title())
        hash_key =  extract_id(singular['pk'])
        if resource == "project":
           hash_key = extract_id(singular['sk'])

        if not resource == "job":
            singular_object = class_to_init(self._client, singular, self._user_id, hash_key)
            return singular_object

        # job object class is slighty different in design
        singular_object = class_to_init(self._upload_client, singular, self._user_id, hash_key)
        return singular_object


    def mutate_single(self, query_string, params):
        """
        return a single object for the requested resource.
        :params: resource - name of the resource to obtain i.e experiments, projects, models, etc.
        :params: query_string - graphql string to invoke.
        :params: params - variables required to invoke query string in the client.
        """
        query = gql(query_string)
        singular = self._client.execute(query, params)
        print(singular)
        return singular


    def get_collection(self, resource, query_string, params):
        """
        return a collection of objects for the requested resource.
        :params: resource - name of the resource to obtain i.e experiments, projects, models, etc.
        :params: query_string - graphql string to invoke.
        :params: params - variables required to invoke query string in the client.
        """
        query = gql(query_string)
        singular_resource =  lambda resource_name: str(resource_name.title()[0:-1]) # format resource name to match one of the existing classes
        class_name = lambda class_name: getattr(sys.modules[__name__], class_name) # convert string to class name
        collection = self._client.execute(query, params)[resource]
        class_to_init = class_name(singular_resource(resource))

        collection_objects = []
        if not resource == "jobs":
            collection_objects = [class_to_init(self._client, item, self._user_id, extract_id(item['sk'])) for item in collection]
            return collection_objects
        # jobs resource
        collection_objects = [class_to_init(self._upload_client, item, self._user_id, extract_id(item['pk'])) for item in collection]
        return collection_objects


    def projects(self):
        """
        retrieve user projects
        :params: user_id - a uuid
        """
        params = {
            "id": str(self._user_id),
        }
        return self.get_collection("projects", PROJECTS_QUERY_FRAGMENT, params)


    def experiments(self, project_id):
        """
        retreive experiments that belong to a project
        :params: project_id - a uuid
        """
        params = {
            "id": str(project_id),
        }
        return self.get_collection("experiments", EXPERIMENTS_QUERY_FRAGMENT, params)


    def experiment(self, experiment_id):
        """
        retreive experiments that belong to a project
        :params: project_id - a uuid
        """
        params = {
            "id": str(experiment_id),
        }
        return self.get_single("experiment", EXPERIMENT_QUERY_FRAGMENT, params)


    # grab user id + project id
    def project(self, project_id):
        """
        retrieve a single user project
        :params: project_id - a uuid
        """
        params = {
             "userId": str(self._user_id),
             "projectId": str(project_id)
        }
        return self.get_single("project", PROJECT_QUERY_FRAGMENT, params)


    def models(self, organization_id):
        """
        retrieve models associated with a user / organization.
        :params: project_id - a uuid
        """
        params = {
            "id": str(organization_id),
        }
        return self.get_collection("models", MODELS_QUERY_FRAGMENT, params)


    def model(self, model_id):
        """
        retrieve a single user model
        :params: project_id - a uuid
        """
        params = {
            "id": str(model_id),
        }
        return self.get_single("model", MODEL_QUERY_FRAGMENT, params)


    def job(self, job_id, project_id):
        """
        returns a single labeling job
        :params: job_id - job uuid
        """
        params = {
            "id": str(job_id),
            "projectId": str(project_id)
        }
        return self.get_single("job", JOB_QUERY_FRAGMENT, params)


    def create_project(self, file):
        """
        create user project
        """
        with open(file, 'r') as yaml_in:
            yaml_object = yaml.safe_load(yaml_in) # yaml_object will be a list or a dict
            project_dict = yaml_object['Project']
            project_dict['userId'] = self._user_id
            now = datetime.now()
            project_dict['date'] = now.strftime("%Y/%m/%d") # We probably should not allow cli to decide DATE
            print(project_dict)
            params = project_dict
            response =  self.mutate_single(PROJECT_CREATE_FRAGMENT, params)
            new_project_created = response["createProject"]["ok"]
            return self.project(new_project_created)

        return f"Failed to open file {file}"


    def upload_class_labels(self, class_labels_file, project_id):
        """
        Precondition: create_project has been called
        This method will upload the meta.json file to the S3 storage bucket of the newly created project.
        """

        data = {}

        with open(class_labels_file) as f:
            data = json.load(f) #serialize json object to a string to be sent to server
            #upload to project_id/meta.json

            data = json.dumps(data)

            params = {
                "userId": self._user_id,
                "projectId": project_id,
                "classLabels": data
            }

            response = self.mutate_single(UPLOAD_CLASS_LABELS_MUTATION, params)


    def create_experiment(self, file):
        """
        create user experient
        """

        env = EnvYAML(file)
        project_id = env['Experiment.projectId']
        if project_id is None:
            print("no project id was set")
            return

        with open(file, 'r') as yaml_in:
            yaml_object = yaml.safe_load(yaml_in) # yaml_object will be a list or a dict
            experiment_dict = yaml_object['Experiment']
            experiment_dict['experimentId'] = "".join(str(uuid.uuid1()).split("-"))
            experiment_dict['userId'] = self._user_id
            now = datetime.now()
            experiment_dict['date'] = now.strftime("%m-%d-%Y")
            # project id from the env variable
            experiment_dict['projectId'] = project_id
            response =  self.mutate_single(EXPERIMENT_CREATE_FRAGMENT, experiment_dict)
            new_experiment_created = response["createExperiment"]["ok"]

        return self.experiment(new_experiment_created)


    def create_model(self, model_path):
        """
        upload model checksum and verify there are enough models to check
        :returns: model object
        """
        return Model("", "", "", "")
