import re
import os
import six
import json
import subprocess
from localstack import config as localstack_config
from localstack import constants as localstack_constants

FALSE_STRINGS = localstack_constants.FALSE_STRINGS

# api server config
API_PATH = '/v1'
API_PORT_LOCAL = 8183
API_URL = localstack_constants.API_ENDPOINT

# api endpoints
API_PATH_USER = '%s/user' % API_PATH
API_PATH_ORGANIZATIONS = '%s/organizations' % API_PATH
API_PATH_SIGNIN = '%s/signin' % API_PATH_USER
API_PATH_SIGNUP = '%s/signup' % API_PATH_USER
API_PATH_RECOVER = '%s/recover' % API_PATH_USER
API_PATH_RESEND = '%s/resend' % API_PATH_USER
API_PATH_ACTIVATE = '%s/activate' % API_PATH_USER
API_PATH_UNSUBSCRIBE = '%s/unsubscribe' % API_PATH_USER
API_PATH_KEY_ACTIVATE = '%s/activate' % API_PATH
API_PATH_CARDS = '%s/cards' % API_PATH_USER
API_PATH_PLANS = '%s/plans' % API_PATH
API_PATH_SUBSCRIPTIONS = '%s/subscriptions' % API_PATH_PLANS
API_PATH_INVOICES = '%s/invoices' % API_PATH_PLANS
API_PATH_CLOUDPODS = '%s/cloudpods' % API_PATH
API_PATH_EVENTS = '%s/events' % API_PATH
API_PATH_STATS = '%s/stats' % API_PATH_EVENTS
API_PATH_GITHUB = '%s/github' % API_PATH
API_PATH_CONFIG = '%s/config' % API_PATH
API_PATH_CI = '%s/ci' % API_PATH
API_PATH_ADMIN = '%s/admin' % API_PATH
API_PATH_STRIPE_WEBHOOK = '%s/webhooks/stripe' % API_PATH

ROOT_FOLDER = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

PROTECTED_FOLDERS = ('services', 'utils')

# database connection settings
DB_NAME = 'localstack'
DB_USER = os.environ.get('DB_USER') or 'localstack'
DB_PASS = os.environ.get('DB_PASS')

# localhost IP address
LOCALHOST_IP = '127.0.0.1'

# bind address of local DNS server
DNS_ADDRESS = os.environ.get('DNS_ADDRESS') or '0.0.0.0'

# IP address that AWS endpoints should resolve to in our local DNS server. By default,
# hostnames resolve to 127.0.0.1, which allows to use the LocalStack APIs transparently
# from the host machine. If your code is running in Docker, this should be configured
# to resolve to the Docker bridge network address, e.g., DNS_RESOLVE_IP=172.17.0.1
DNS_RESOLVE_IP = os.environ.get('DNS_RESOLVE_IP') or LOCALHOST_IP

# fallback DNS server to send upstream requests to
DNS_SERVER = os.environ.get('DNS_SERVER', '8.8.8.8')

# SMTP settings (required, e.g., for Cognito)
SMTP_HOST = os.environ.get('SMTP_HOST', '')
SMTP_USER = os.environ.get('SMTP_USER', '')
SMTP_PASS = os.environ.get('SMTP_PASS', '')
SMTP_EMAIL = os.environ.get('SMTP_EMAIL', '')

# whether to automatically start up utility containers (e.g., Spark/Hadoop for EMR, Presto for Athena)
AUTOSTART_UTIL_CONTAINERS = localstack_config.is_env_true('AUTOSTART_UTIL_CONTAINERS')

# optional flags to pass when starting the bigdata Docker container
BIGDATA_DOCKER_FLAGS = os.environ.get('BIGDATA_DOCKER_FLAGS', '')

# Comma-separated list of regex patterns for DNS names to resolve locally.
# Any DNS name not matched against any of the patterns on this whitelist
# will resolve to the real DNS entry, rather than the local one.
DNS_LOCAL_NAME_PATTERNS = os.environ.get('DNS_LOCAL_NAME_PATTERNS', '')

# whether to use static ports and IDs (e.g., cf-<port>) for CloudFormation distributions
CLOUDFRONT_STATIC_PORTS = localstack_config.is_env_true('CLOUDFRONT_STATIC_PORTS')

# whether to enforce IAM policies when processing requests
ENFORCE_IAM = localstack_config.is_env_true('ENFORCE_IAM')

# folder with persistent API backend states
BACKEND_STATES_DIR = os.path.join(localstack_config.DATA_DIR, 'api_states')

# whether to require Pro features and exit with a fault if the API key cannot be activated
REQUIRE_PRO = localstack_config.is_env_true('REQUIRE_PRO')


def use_custom_dns():
    return str(DNS_ADDRESS) not in FALSE_STRINGS


# set USE_SSL to true by default
# TODO fix this!
# localstack_config.USE_SSL = os.environ.get('USE_SSL', '').lower().strip() not in FALSE_STRINGS

# backend service ports
DEFAULT_PORT_LOCAL_DAEMON = 4535
DEFAULT_PORT_LOCAL_DAEMON_ROOT = 4534

# port ranges for service instances (e.g., Postgres DBs, ElastiCache clusters, ...)
SERVICE_INSTANCES_PORTS_START = int(os.environ.get('SERVICE_INSTANCES_PORTS_START') or 4510)
SERVICE_INSTANCES_PORTS_END = int(os.environ.get('SERVICE_INSTANCES_PORTS_END') or
    (SERVICE_INSTANCES_PORTS_START + 30))

# port for Azure APIs
PORT_AZURE = 12121

# add default service ports (TODO needed?)
localstack_constants.DEFAULT_SERVICE_PORTS['azure'] = PORT_AZURE

# Docker host name resolvable from containers
DOCKER_HOST_NAME = 'host.docker.internal'

# Port where Hive/metastore/Spark are available for EMR/Athena
PORT_HIVE_METASTORE = 9083
PORT_HIVE_SERVER = 10000
PORT_SPARK_MASTER = 7077

if localstack_config.DOCKER_HOST_FROM_CONTAINER == DOCKER_HOST_NAME:
    # special case when we're running tests outside of Docker
    if not localstack_config.in_docker():
        image_name = localstack_constants.DOCKER_IMAGE_NAME
        cmd = "docker run --rm --entrypoint= -it %s bash -c 'ping -c 1 %s'" % (image_name, DOCKER_HOST_NAME)
        try:
            out = subprocess.check_output(cmd, shell=True)
            out = out.decode('utf-8') if isinstance(out, six.binary_type) else out
            ip = re.match(r'PING[^\(]+\(([^\)]+)\).*', out, re.MULTILINE | re.DOTALL)
            ip = ip and ip.group(1)
            if ip:
                localstack_config.DOCKER_HOST_FROM_CONTAINER = ip
        except Exception:
            # Swallow this error - Docker daemon potentially not running?
            pass

# update variable names that need to be passed as arguments to Docker
localstack_config.CONFIG_ENV_VARS += [
    'SMTP_HOST', 'SMTP_USER', 'SMTP_PASS', 'SMTP_EMAIL', 'DNS_SERVER', 'DNS_ADDRESS', 'ENFORCE_IAM',
    'DNS_RESOLVE_IP', 'DNS_LOCAL_NAME_PATTERNS', 'AUTOSTART_UTIL_CONTAINERS', 'CLOUDFRONT_STATIC_PORTS',
    'REQUIRE_PRO', 'AZURE', 'BIGDATA_DOCKER_FLAGS'
]

# re-initialize configs in localstack
localstack_config.populate_configs()


def load_config_file():
    from localstack.utils.common import get_or_create_file, to_str
    content = get_or_create_file(localstack_config.CONFIG_FILE_PATH)
    configs = json.loads(to_str(content))
    return configs
