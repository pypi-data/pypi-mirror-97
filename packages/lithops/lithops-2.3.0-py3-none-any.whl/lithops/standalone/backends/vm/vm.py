import logging

from lithops.constants import COMPUTE_CLI_MSG
from lithops.util.ssh_client import SSHClient

logger = logging.getLogger(__name__)


class VMBackend:

    def __init__(self, vm_config, mode):
        logger.debug("Creating Virtual Machine client")
        self.name = 'vm'
        self.config = vm_config
        self.mode = mode
        self.master = None

        msg = COMPUTE_CLI_MSG.format('Virtual Machine')
        logger.info("{}".format(msg))

    def init(self):
        """
        Initialize the VM backend
        """
        if self.mode == 'consume':
            logger.debug('Initializing VM backend (Consume mode)')
            self.master = VMInstance(self.config)
        else:
            raise Exception('Create mode is not allowed in the VM backend')

    def clean(self):
        pass

    def clear(self):
        pass

    def dismantle(self):
        pass

    def get_runtime_key(self, runtime_name):
        runtime = runtime_name.replace('/', '-').replace(':', '-')
        runtime_key = '/'.join([self.name, self.config['ip_address'], runtime])
        return runtime_key


class VMInstance:

    def __init__(self, config):
        self.ip_address = self.config['ip_address']
        self.ssh_client = None
        self.ssh_credentials = {
            'username': self.config.get('ssh_user', 'root'),
            'password': self.config.get('ssh_password', None),
            'key_filename': self.config.get('ssh_key_filename', None)
        }
        logger.debug('{} created'.format(self))

    def __str__(self):
        return 'VM instance {}'.format(self.ip_address)

    def get_ssh_client(self):
        """
        Creates an ssh client against the VM only if the Instance is the master
        """
        if self.ip_address:
            if not self.ssh_client:
                self.ssh_client = SSHClient(self.ip_address, self.ssh_credentials)
        return self.ssh_client

    def del_ssh_client(self):
        """
        Deletes the ssh client
        """
        if self.ssh_client:
            self.ssh_client.close()
            self.ssh_client = None

    def create(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def delete(self):
        pass
