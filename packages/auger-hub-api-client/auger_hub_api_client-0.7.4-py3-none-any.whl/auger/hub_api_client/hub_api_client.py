import gzip
import json
import re
import requests
import time

# Python 3
from io import StringIO
from urllib.parse import urljoin
from json.decoder import JSONDecodeError
from bs4 import BeautifulSoup

from requests.exceptions import ConnectionError

class HubApiClient:
    class BaseError(Exception):
        def __init__(self, *args):
            super().__init__(*args)
            self.request_details = None

        def metadata(self):
            return self.args[1]

        # First arg is error message
        # Second arg is metadata
        def __str__(self):
            message = list(map(lambda arg: arg if isinstance(arg, str) else json.dumps(arg), self.args))
            if self.request_details:
                message.append(self.request_details)

            return ' '.join(message)

        def add_request_details(self, method, path, payload):
            self.request_details = ' '.join(['on:', method.upper(), path, json.dumps(payload)])

    # Means that consumer code can't do nothing with this error
    # Only changing of comnsumer source code or config parameters can help
    class FatalApiError(BaseError):
        pass

    # Wrong input, consumer should fix input values
    class InvalidParamsError(BaseError):
        pass

    # Temporary network issue, retry can help
    class NetworkError(BaseError):
        pass

    # Temporary app server issue, retry can help
    class RetryableApiError(BaseError):
        pass

    class MissingParamError(BaseError):
        pass

    class DSLError(Exception):
        pass

    class RetryCounter:
        def __init__(self, hub_api_client=None):
            if hub_api_client:
                self.retries_left = hub_api_client.retries_count
                self.connection_retries_left = hub_api_client.connection_retries_count
            else:
                self.retries_left = 0
                self.connection_retries_left = 0

        def count_retry(self, error):
            if isinstance(error, HubApiClient.RetryableApiError):
                self.retries_left -= 1
            elif isinstance(error, HubApiClient.NetworkError):
                self.connection_retries_left -= 1
            else:
                raise RuntimeError('Unsupported kind of error {error}'.format(error=error))

            return self

        def is_retries_available(self):
            return self.retries_left > 0 and self.connection_retries_left > 0

        @classmethod
        def none(cls):
            return cls()

    API_SCHEMA = {
        'actual': {
            'actions': ['create']
        },
        'cluster_task': {
            'actions': ['index', 'show', 'create', 'update']
        },
        'cluster_status': {
            'actions': ['index']
        },
        'dataset_manifest': {
            'actions': ['index', 'show', 'create', 'update']
        },
        'endpoint': {
            'actions': ['index', 'show', 'create', 'update', 'delete']
        },
        'endpoint_pipeline': {
            'actions': ['create', 'update', 'delete']
        },
        'endpoint_actual': {
            'actions': ['create'],
            'resource_name': 'actual',
            'parent_resource': 'endpoint',
        },
        'endpoint_prediction': {
            'actions': ['index', 'show', 'create'],
            'resource_name': 'prediction',
            'parent_resource': 'endpoint',
        },
        'endpoint_roi_validation': {
            'actions': ['create'],
            'resource_name': 'roi_validation',
            'parent_resource': 'endpoint',
        },
        'experiment': {
            'actions': ['index', 'show', 'create', 'update', 'delete']
        },
        'experiment_session': {
            'actions': ['index', 'show', 'create', 'update'],
        },
        'hyperparameter': {
            'actions': ['index', 'show', 'create']
        },
        'instance_type': {
            'actions': ['index']
        },
        'organization': {
            'actions': ['index', 'show', 'create', 'update', 'delete']
        },
        'pipeline': {
            'actions': ['index', 'show', 'create', 'update']
        },
        'pipeline_file': {
            'actions': ['index', 'show', 'create']
        },
        # Legacy endpoint
        'prediction': {
            'actions': ['index', 'show', 'create']
        },
        # New endpoint
        'prediction_group': {
            'actions': ['index', 'show', 'create']
        },
        'project': {
            'actions': [
                'index',
                'show',
                'create',
                'update',
                'delete',
                {
                    'deploy': 'patch',
                    'undeploy': 'patch'
                }
            ]
        },
        'project_file': {
            'actions': ['index', 'show', 'create', 'delete']
        },
        'project_file_url': {
            'actions': ['create', 'index']
        },
        'pod_log': {
            'actions': ['index']
        },
        'review_alert': {
            'actions': ['index', 'show', 'create', 'update', 'delete']
        },
        'review_alert_item': {
            'actions': ['index', 'show']
        },
        'similar_trials_request': {
            'actions': ['show', 'create']
        },
        'token': {
            'actions': ['create']
        },
        'trial': {
            'actions': ['index', 'show', 'create', 'update']
        },
        'trial_search': {
            'actions': ['index', 'show', 'create', 'update']
        },
        'warm_start_request': {
            'actions': ['show', 'create']
        }
    }

    API_PREFIX = '/api/v1'

    def __init__(self, **config):
        self.base_url = config['hub_app_url']
        self.optimizers_url = config.get('optimizers_url', None)
        self.token = config.get('token', None)
        self.system_token = config.get('hub_system_token', None)
        self.cluster_api_token = config.get('hub_cluster_api_token', None)
        self.project_api_token = config.get('hub_project_api_token', None)
        self.retries_count = config.get('retries_count', 5)
        self.connection_retries_count = config.get('connection_retries_count', self.retries_count)
        self.retry_wait_seconds = config.get('retry_wait_seconds', 5)
        self.debug = config.get('debug', False)

        self.headers = { 'Content-Type': 'application/json' }
        self.gzip_headers = self.headers.copy()
        self.gzip_headers['Content-Encoding'] = 'gzip'

        self.define_actions()

    def log_request(self, method, path, payload):
        if self.debug:
            print('HAC.Req: ' + method.upper() + ' ' + path + ' params: ' + json.dumps(payload))

    def log_response(self, method, path, response):
        if self.debug:
            print('HAC.Res: ' + method.upper() + ' ' + path + ' response: ' + response.text)

    def full_path(self, relative_path, base_url):
        return urljoin(base_url, relative_path)

    WHITE_SPACE_REGEX = re.compile(r'\s+')
    STYLE_TAG_REGEX = re.compile('<style.*>.*</style>')
    ALL_TAG_REGEX = re.compile('<.*?>')

    def extract_plain_text(self, response):
        html = response.text

        if html:
            soup = BeautifulSoup(html, features='lxml') # create a new bs4 object from the html data loaded

            for script in soup(["script", "style"]): # remove all javascript and stylesheet code
                script.extract()

            # get text
            text = soup.get_text()

            # Drop stack trace (from Riails dev mode)
            text = text.split('Extracted source (around line')[0]

            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())

            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            return text
        else:
            return str(response) + ' ' + response.reason

    def tokens_payload(self):
        if self.project_api_token:
            return { 'project_api_token': self.project_api_token }
        elif self.cluster_api_token:
            return { 'cluster_api_token': self.cluster_api_token }
        elif self.token:
            return { 'token': self.token }
        elif self.system_token:
            return { 'system_token': self.system_token }
        else:
            return {}

    def request(self, method_name, path, base_url, payload={}, gzip=False):
        try:
            method = getattr(requests, method_name)

            params = payload.copy()
            params.update(self.tokens_payload())

            full_path = self.full_path(relative_path=path, base_url=base_url)

            if gzip:
                data = self.compress(json.dumps(params))
                return method(full_path, data=data, headers=self.gzip_headers)
            else:
                return method(full_path, json=params, headers=self.headers)
        except ConnectionError as e:
            raise self.NetworkError(str(e))

    def compress(self, data):
        if hasattr(gzip, 'compress'):
            # Python 3
            return gzip.compress(bytes(data, 'utf-8'))

    def handle_response(self, res, plain_text=False):
        if plain_text:
            reponse = res.text
            meta = None
        else:
            try:
                reponse = res.json()
                meta = reponse.get('meta')
            except (JSONDecodeError, ValueError):
                response = res.text
                meta = {}

        if res.status_code == 200 or res.status_code == 201:
            return reponse
        elif res.status_code == 400:
            # Invalid input data, we can't do anyting, consumer should fix source code
            raise self.InvalidParamsError(self.format_response(res), meta)
        elif res.status_code == 401 or res.status_code == 403 or res.status_code == 404 or res.status_code == 500:
            # Invalid token or error in source code, we can't do anyting raise error
            raise self.FatalApiError(self.format_response(res), meta)
        else:
            # In case of another error we can retry
            raise self.RetryableApiError(self.format_response(res), meta)

    def format_api_error(self, error):
        return '{param} {message}'.format(
            param=error['error_param'],
            message=error['message']
        )

    def format_response(self, res):
        try:
            if res.status_code == 400:
                errors = res.json()['meta']['errors']
                return ', '.join(map(lambda error: self.format_api_error(error), errors))
            else:
                return 'status: {}, body: {}'.format(res.status_code, self.extract_plain_text(res))
        except (JSONDecodeError, ValueError) as e:
            raise self.FatalApiError(self.extract_plain_text(res))

    def make_and_handle_request(self, method_name, path, base_url=None, payload={}, retry_counter=None, plain_text=False, gzip=False):
        if not base_url:
            base_url = self.base_url

        if retry_counter is None:
            # Allow retries for get request, because it deosn't modify any data on server
            if method_name == 'get':
                retry_counter = self.RetryCounter(self)
            # But don't allow to retry another (POST, PUT, DELETE, etc) requests
            else:
                retry_counter = self.RetryCounter.none()

        try:
            self.log_request(method_name, path, payload)
            with self.request(method_name, path, base_url, payload, gzip) as res:
                self.log_response(method_name, path, res)
                return self.handle_response(res, plain_text=plain_text)
        except self.RetryableApiError as e:
            if retry_counter.is_retries_available():
                time.sleep(self.retry_wait_seconds)
                return self.make_and_handle_request(method_name, path, base_url, payload, retry_counter.count_retry(e))
            else:
                e.add_request_details(method_name, path, payload)
                raise e
        except self.BaseError as e:
            e.add_request_details(method_name, path, payload)
            raise e

    def get(self, path, payload = {}):
        return self.make_and_handle_request('get', path, payload=payload)

    def get_paginated_response(self, full_path, limit=50, offset=0, **kwargs):
        args = { 'limit': limit, 'offset': offset }
        args.update(kwargs)
        return self.get(full_path, args)

    def iterate_all_resource_pages(self, method_name, handler, **kwargs):
        offset = 0
        while True:
            method = getattr(self, method_name)

            args = { 'offset': offset }
            args.update(kwargs)

            res = method(**args)

            for item in res['data']:
                handler(item)

            count = res['meta']['pagination']['count']

            if count > 0:
                offset += count
            else:
                break;

    def build_full_resource_path(self, resource_name, parent_resource_name):
        if parent_resource_name:
            return '/api/v1/{parent_resource_name}{parent_ending}/{{parent_id}}/{resource_name}{ending}'.format(
                resource_name=resource_name,
                parent_resource_name=parent_resource_name,
                parent_ending=self.plural_ending(parent_resource_name),
                ending=self.plural_ending(resource_name),
            )
        else:
            return '{api_prefix}/{resource_name}{ending}'.format(
                api_prefix=self.API_PREFIX,
                resource_name=resource_name,
                ending=self.plural_ending(resource_name),
            )

    def define_actions(self):
        for resource_name, options in self.API_SCHEMA.items():
            url_resource_name = options.get('resource_name', resource_name)
            parent_resource_name = options.get('parent_resource', None)
            path = self.build_full_resource_path(url_resource_name, parent_resource_name)

            for action_name in options['actions']:
                if isinstance(action_name, str):
                    self.define_action(action_name, path, resource_name, parent_resource_name)
                elif isinstance(action_name, dict):
                    for custom_action_name, http_method in action_name.items():
                        self.define_action(custom_action_name, path, resource_name, parent_resource_name, http_method)
                else:
                    raise self.DSLError('Unsupported action in DSL: `{action_name}`'.format(action_name=action_name))

    def format_full_resource_path(self, path_template, parent_resource_name, kwargs):
        if parent_resource_name:
            parent_id_key = parent_resource_name + '_id'
            parent_id = kwargs.get(parent_id_key, None)
            if parent_id:
                return path_template.format(parent_id=parent_id)
            else:
                raise self.MissingParamError(
                    '{name} parameter is required'.format(name=parent_id_key)
                )
        elif not parent_resource_name:
            return path_template
        else:
            raise self.FatalApiError('missing parent_id parameter')

    def plural_ending(self, resource_name):
        if resource_name.endswith('us') or resource_name.endswith('ch'):
            return 'es'
        else:
            return 's'

    def define_action(self, action_name, path_template, resource_name, parent_resource_name, http_method=None):
        if action_name == 'index':
            ending = self.plural_ending(resource_name)
            index_proc_name = 'get_{resource_name}{ending}'.format(resource_name=resource_name, ending=ending)
            iterate_proc_name = 'iterate_all_{resource_name}{ending}'.format(resource_name=resource_name, ending=ending)

            def index(self, **kwargs):
                path = self.format_full_resource_path(path_template, parent_resource_name, kwargs)
                return self.get_paginated_response(path, **kwargs)

            def iterate(self, handler, **kwargs):
                return self.iterate_all_resource_pages(index_proc_name, handler, **kwargs)

            setattr(self.__class__, index_proc_name, index)
            setattr(self.__class__, iterate_proc_name, iterate)

        elif action_name == 'show':
            show_proc_name = 'get_{resource_name}'.format(resource_name=resource_name)

            def show(self, id, **kwargs):
                path = self.format_full_resource_path(path_template, parent_resource_name, kwargs)
                return self.make_and_handle_request('get', '{path}/{id}'.format(path=path, id=id))

            setattr(self.__class__, show_proc_name, show)

        elif action_name == 'create':
            create_proc_name = 'create_{resource_name}'.format(resource_name=resource_name)

            def create(self, **kwargs):
                path = self.format_full_resource_path(path_template, parent_resource_name, kwargs)
                return self.make_and_handle_request('post', path, payload=kwargs)

            setattr(self.__class__, create_proc_name, create)

        elif action_name == 'update':
            update_proc_name = 'update_{resource_name}'.format(resource_name=resource_name)

            def update(self, id, **kwargs):
                path = self.format_full_resource_path(path_template, parent_resource_name, kwargs)
                if id:
                    path='{path}/{id}'.format(path=path, id=id)
                return self.make_and_handle_request('patch', path, payload=kwargs)

            setattr(self.__class__, update_proc_name, update)
        elif action_name == 'delete':
            delete_proc_name = 'delete_{resource_name}'.format(resource_name=resource_name)

            def delete(self, id):
                path = self.format_full_resource_path(path_template, parent_resource_name, {})
                return self.make_and_handle_request('delete', '{path}/{id}'.format(path=path, id=id))

            setattr(self.__class__, delete_proc_name, delete)
        elif http_method:
            custom_proc_name = '{action_name}_{resource_name}'.format(
                action_name=action_name,
                resource_name=resource_name
            )

            def custom_action(self, id, **kwargs):
                path = self.format_full_resource_path(path_template, parent_resource_name, kwargs)
                path = '{path}/{id}/{action_name}'.format(path=path, id=id, action_name=action_name)
                return self.make_and_handle_request(http_method, path, payload=kwargs)

            setattr(self.__class__, custom_proc_name, custom_action)
        else:
            raise self.DSLError('Unsupported REST action `{name}`'.format(name=action_name))


    # Deviations, not pure RESTfull endpoints

    # Updates a bunch of trials for project run
    def update_trials(self, **kwargs):
        return self.update_trial(id=None, **kwargs)

    def get_project_logs(self, id, **kwargs):
        path = '{api_prefix}/projects/{id}/logs'.format(api_prefix=self.API_PREFIX, id=id)
        return self.make_and_handle_request('get', path, plain_text=True)

    def get_project_file_url(self, **kwargs):
        return self.get_project_file_urls(**kwargs)

    def get_status(self, object, id):
        path = '{api_prefix}/status'.format(api_prefix=self.API_PREFIX)
        return self.make_and_handle_request('get', path, payload={'object': object, 'id': id})

    def delete_actuals(self, **kwargs):
        path = '{api_prefix}/actuals'.format(api_prefix=self.API_PREFIX)
        return self.make_and_handle_request('delete', path, payload=kwargs)

    def refit_trial(self, id, refit_data_path):
        return self.create_trial(id=id, refit_data_path=refit_data_path)

    def delete_endpoint_actuals(self, endpoint_id, **kwargs):
        path = '{api_prefix}/endpoints/{id}/actuals'.format(api_prefix=self.API_PREFIX, id=endpoint_id)
        return self.make_and_handle_request('delete', path, payload=kwargs)

    # Optimizers service client
    def _post_optimizer_service(self, url, payload={}):
        if self.optimizers_url:
            return self.make_and_handle_request('post', url,
                payload=payload,
                base_url=self.optimizers_url,
                retry_counter=self.RetryCounter(self),
                gzip=True
            )
        else:
            raise self.MissingParamError('pass optimizers_url in HubApiClient constructor')

    def get_next_trials(self, payload={}):
        return self._post_optimizer_service('/next_trials', payload)

    def get_next_trials_v2(self, payload={}):
        return self._post_optimizer_service('/v2/next_trials', payload)

    def get_fte(self, payload={}):
        return self._post_optimizer_service('/fte', payload)
