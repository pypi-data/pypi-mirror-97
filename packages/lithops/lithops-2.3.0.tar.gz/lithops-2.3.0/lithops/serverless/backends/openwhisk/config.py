#
# (C) Copyright IBM Corp. 2020
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import sys
from lithops.utils import version_str

RUNTIME_DEFAULT = {'3.5': 'lithopscloud/ibmcf-python-v35',
                   '3.6': 'lithopscloud/ibmcf-python-v36',
                   '3.7': 'lithopscloud/ibmcf-python-v37',
                   '3.8': 'lithopscloud/ibmcf-python-v38'}

RUNTIME_TIMEOUT_DEFAULT = 300  # Default: 300 seconds => 5 minutes
RUNTIME_MEMORY_DEFAULT = 256  # Default memory: 256 MB
CONCURRENT_WORKERS_DEFAULT = 100
INVOKE_POOL_THREADS_DEFAULT = 500

FH_ZIP_LOCATION = os.path.join(os.getcwd(), 'lithops_openwhisk.zip')


def load_config(config_data):
    if 'openwhisk' not in config_data:
        raise Exception("openwhisk section is mandatory in configuration")

    required_keys = ('endpoint', 'namespace', 'api_key')
    if not set(required_keys) <= set(config_data['openwhisk']):
        raise Exception('You must provide {} to access to openwhisk'.format(required_keys))

    if 'runtime_memory' not in config_data['serverless']:
        config_data['serverless']['runtime_memory'] = RUNTIME_MEMORY_DEFAULT
    if 'runtime_timeout' not in config_data['serverless']:
        config_data['serverless']['runtime_timeout'] = RUNTIME_TIMEOUT_DEFAULT

    if 'runtime' in config_data['openwhisk']:
        config_data['serverless']['runtime'] = config_data['openwhisk']['runtime']

    if 'runtime' not in config_data['serverless']:
        python_version = version_str(sys.version_info)
        try:
            config_data['serverless']['runtime'] = RUNTIME_DEFAULT[python_version]
        except KeyError:
            raise Exception('Unsupported Python version: {}'.format(python_version))

    if 'workers' not in config_data['lithops']:
        config_data['lithops']['workers'] = CONCURRENT_WORKERS_DEFAULT

    if 'invoke_pool_threads' not in config_data['openwhisk']:
        config_data['openwhisk']['invoke_pool_threads'] = INVOKE_POOL_THREADS_DEFAULT
    config_data['serverless']['invoke_pool_threads'] = config_data['openwhisk']['invoke_pool_threads']
