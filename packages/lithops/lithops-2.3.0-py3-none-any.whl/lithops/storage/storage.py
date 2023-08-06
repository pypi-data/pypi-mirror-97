
# (C) Copyright IBM Corp. 2020
# (C) Copyright Cloudlab URV 2020
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
import json
import logging
import itertools
import importlib
from lithops.version import __version__
from lithops.constants import CACHE_DIR, RUNTIMES_PREFIX, JOBS_PREFIX, TEMP_PREFIX
from lithops.utils import is_lithops_worker
from lithops.storage.utils import create_status_key, create_output_key, \
    status_key_suffix, init_key_suffix, CloudObject, StorageNoSuchKeyError,\
    create_job_key
from lithops.config import extract_storage_config, default_storage_config

logger = logging.getLogger(__name__)


class Storage:
    """
    An Storage object is used by partitioner and other components to access
    underlying storage backend without exposing the the implementation details.
    """
    def __init__(self, config=None, backend=None, storage_config=None):
        """ Creates an Storage instance

        :param config: lithops configuration dict
        :param backend: storage backend name

        :return: Storage instance.
        """

        if storage_config:
            self.storage_config = storage_config
        else:
            storage_config = default_storage_config(config_data=config,
                                                    backend=backend)
            self.storage_config = extract_storage_config(storage_config)

        self.backend = self.storage_config['backend']
        self.bucket = self.storage_config['bucket']

        try:
            module_location = 'lithops.storage.backends.{}'.format(self.backend)
            sb_module = importlib.import_module(module_location)
            StorageBackend = getattr(sb_module, 'StorageBackend')
            self.storage_handler = StorageBackend(self.storage_config[self.backend])
        except Exception as e:
            logger.error("An exception was produced trying to create the "
                         "'{}' storage backend".format(self.backend))
            raise e

        self._created_cobjects_n = itertools.count()

    def get_client(self):
        """
        Retrieves the underlying storage client.
        :return: storage backend client
        """
        return self.storage_handler.get_client()

    def get_storage_config(self):
        """
        Retrieves the configuration of this storage handler.
        :return: storage configuration
        """
        return self.storage_config

    def put_object(self, bucket, key, body):
        return self.storage_handler.put_object(bucket, key, body)

    def get_object(self, bucket, key, stream=False, extra_get_args={}):
        return self.storage_handler.get_object(bucket, key, stream, extra_get_args)

    def head_object(self, bucket, key):
        return self.storage_handler.head_object(bucket, key)

    def delete_object(self, bucket, key):
        return self.storage_handler.delete_object(bucket, key)

    def delete_objects(self, bucket, key_list):
        return self.storage_handler.delete_objects(bucket, key_list)

    def head_bucket(self, bucket):
        return self.storage_handler.head_bucket(bucket)

    def list_objects(self, bucket, prefix=None):
        return self.storage_handler.list_objects(bucket, prefix)

    def list_keys(self, bucket, prefix=None):
        return self.storage_handler.list_keys(bucket, prefix)

    def put_cloudobject(self, body, bucket=None, key=None):
        """
        Put CloudObject into storage.
        :param body: data content
        :param bucket: destination bucket
        :param key: destination key
        :return: CloudObject instance
        """
        prefix = os.environ.get('__LITHOPS_SESSION_ID', '')
        coid = hex(next(self._created_cobjects_n))[2:]
        coname = 'cloudobject_{}'.format(coid)
        name = '/'.join([prefix, coname]) if prefix else coname
        key = key or '/'.join([TEMP_PREFIX, name])
        bucket = bucket or self.bucket
        self.storage_handler.put_object(bucket, key, body)

        return CloudObject(self.backend, bucket, key)

    def get_cloudobject(self, cloudobject, stream=False):
        """
        Get CloudObject from storage.
        :param cloudobject: CloudObject instance
        :param bucket: destination bucket
        :param key: destination key
        :return: body text
        """
        if cloudobject.backend == self.backend:
            bucket = cloudobject.bucket
            key = cloudobject.key
            return self.storage_handler.get_object(bucket, key, stream=stream)
        else:
            raise Exception("CloudObject: Invalid Storage backend")

    def delete_cloudobject(self, cloudobject):
        """
        Get CloudObject from storage.
        :param cloudobject: CloudObject instance
        :param bucket: destination bucket
        :param key: destination key
        :return: body text
        """
        if cloudobject.backend == self.backend:
            bucket = cloudobject.bucket
            key = cloudobject.key
            return self.storage_handler.delete_object(bucket, key)
        else:
            raise Exception("CloudObject: Invalid Storage backend")

    def delete_cloudobjects(self, cloudobjects):
        """
        Get CloudObject from storage.
        :param cloudobject: CloudObject instance
        :param bucket: destination bucket
        :param key: destination key
        :return: body text
        """
        cobjs = {}
        for co in cloudobjects:
            if co.backend not in cobjs:
                cobjs[co.backend] = {}
            if co.bucket not in cobjs[co.backend]:
                cobjs[co.backend][co.bucket] = []
            cobjs[co.backend][co.bucket].append(co.key)

        for backend in cobjs:
            if backend == self.backend:
                for bucket in cobjs[backend]:
                    self.storage_handler.delete_objects(bucket, cobjs[backend][co.bucket])
            else:
                raise Exception("CloudObject: Invalid Storage backend")


class InternalStorage:
    """
    An InternalStorage object is used by executors and other components to access
    underlying storage backend without exposing the the implementation details.
    """

    def __init__(self, storage_config):
        """ Creates an InternalStorage instance
        :param storage_config: Storage config dictionary

        :return: InternalStorage instance
        """
        self.storage = Storage(storage_config=storage_config)
        self.backend = self.storage.backend
        self.bucket = self.storage.bucket

    def get_client(self):
        """
        Retrieves the underlying storage client.
        :return: storage backend client
        """
        return self.storage.get_client()

    def get_storage_config(self):
        """
        Retrieves the configuration of this storage handler.
        :return: storage configuration
        """
        return self.storage.get_storage_config()

    def put_data(self, key, data):
        """
        Put data object into storage.
        :param key: data key
        :param data: data content
        :return: None
        """
        return self.storage.put_object(self.bucket, key, data)

    def put_func(self, key, func):
        """
        Put serialized function into storage.
        :param key: function key
        :param func: serialized function
        :return: None
        """
        return self.storage.put_object(self.bucket, key, func)

    def get_data(self, key, stream=False, extra_get_args={}):
        """
        Get data object from storage.
        :param key: data key
        :return: data content
        """
        return self.storage.get_object(self.bucket, key, stream, extra_get_args)

    def get_func(self, key):
        """
        Get serialized function from storage.
        :param key: function key
        :return: serialized function
        """
        return self.storage.get_object(self.bucket, key)

    def get_job_status(self, executor_id, job_id):
        """
        Get the status of a callset.
        :param executor_id: executor's ID
        :return: A list of call IDs that have updated status.
        """
        job_key = create_job_key(executor_id, job_id)
        callset_prefix = '/'.join([JOBS_PREFIX, job_key])
        keys = self.storage.list_keys(self.bucket, callset_prefix)

        running_keys = [k.split('/') for k in keys if init_key_suffix in k]
        running_callids = [(tuple(k[1].rsplit("-", 1)+[k[2]]),
                            k[3].replace(init_key_suffix, ''))
                           for k in running_keys]

        done_keys = [k.split('/')[1:] for k in keys if status_key_suffix in k]
        done_callids = [tuple(k[0].rsplit("-", 1) + [k[1]]) for k in done_keys]

        return set(running_callids), set(done_callids)

    def get_call_status(self, executor_id, job_id, call_id):
        """
        Get status of a call.
        :param executor_id: executor ID of the call
        :param call_id: call ID of the call
        :return: A dictionary containing call's status, or None if no updated status
        """
        status_key = create_status_key(JOBS_PREFIX, executor_id, job_id, call_id)
        try:
            data = self.storage.get_object(self.bucket, status_key)
            return json.loads(data.decode('ascii'))
        except StorageNoSuchKeyError:
            return None

    def get_call_output(self, executor_id, job_id, call_id):
        """
        Get the output of a call.
        :param executor_id: executor ID of the call
        :param call_id: call ID of the call
        :return: Output of the call.
        """
        output_key = create_output_key(JOBS_PREFIX, executor_id, job_id, call_id)
        try:
            return self.storage.get_object(self.bucket, output_key)
        except StorageNoSuchKeyError:
            return None

    def get_runtime_meta(self, key):
        """
        Get the metadata given a runtime name.
        :param runtime: name of the runtime
        :return: runtime metadata
        """

        path = [RUNTIMES_PREFIX, __version__,  key+".meta.json"]
        filename_local_path = os.path.join(CACHE_DIR, *path)

        if not is_lithops_worker() and os.path.exists(filename_local_path):
            logger.debug("Runtime metadata found in local cache")
            with open(filename_local_path, "r") as f:
                runtime_meta = json.loads(f.read())
            return runtime_meta
        else:
            logger.debug("Runtime metadata not found in local cache. Retrieving it from storage")
            try:
                obj_key = '/'.join(path).replace('\\', '/')
                logger.debug('Trying to download runtime metadata from: {}://{}/{}'
                             .format(self.backend, self.bucket, obj_key))
                json_str = self.storage.get_object(self.bucket, obj_key)
                logger.debug('Runtime metadata found in storage')
                runtime_meta = json.loads(json_str.decode("ascii"))

                # Save runtime meta to cache
                try:
                    if not os.path.exists(os.path.dirname(filename_local_path)):
                        os.makedirs(os.path.dirname(filename_local_path))

                    with open(filename_local_path, "w") as f:
                        f.write(json.dumps(runtime_meta))
                except Exception as e:
                    logger.error("Could not save runtime meta to local cache: {}".format(e))

                return runtime_meta
            except StorageNoSuchKeyError:
                logger.debug('Runtime metadata not found in storage')
                return None

    def put_runtime_meta(self, key, runtime_meta):
        """
        Puit the metadata given a runtime config.
        :param runtime: name of the runtime
        :param runtime_meta metadata
        """
        path = [RUNTIMES_PREFIX, __version__,  key+".meta.json"]
        obj_key = '/'.join(path).replace('\\', '/')
        logger.debug("Uploading runtime metadata to: {}://{}/{}"
                     .format(self.backend, self.bucket, obj_key))
        self.storage.put_object(self.bucket, obj_key, json.dumps(runtime_meta))

        if not is_lithops_worker():
            filename_local_path = os.path.join(CACHE_DIR, *path)
            logger.debug("Storing runtime metadata into local cache: {}".format(filename_local_path))

            if not os.path.exists(os.path.dirname(filename_local_path)):
                os.makedirs(os.path.dirname(filename_local_path))

            with open(filename_local_path, "w") as f:
                f.write(json.dumps(runtime_meta))

    def delete_runtime_meta(self, key):
        """
        Puit the metadata given a runtime config.
        :param runtime: name of the runtime
        :param runtime_meta metadata
        """
        path = [RUNTIMES_PREFIX, __version__,  key+".meta.json"]
        obj_key = '/'.join(path).replace('\\', '/')
        filename_local_path = os.path.join(CACHE_DIR, *path)
        if os.path.exists(filename_local_path):
            os.remove(filename_local_path)
        self.storage.delete_object(self.bucket, obj_key)
