""" Utilities for deploying applications to Sermos.

    Example CLI Usage::

        $ honcho run -e .env sermos deploy
        $ honcho run -e .env sermos status

    Example Programmatic Usage::

        from sermos.deploy import SermosDeploy

        sd = SermosDeploy(
            os.environ.get("SERMOS_ACCESS_KEY", None),
            pkg_name="sermos_demo_client"
        )

        # To Invoke
        status = sd.invoke_deployment()
        print(status)

        # To Check Status:
        status = sd.get_deployment_status()
        print(status)

"""
import json
import subprocess
import base64
import logging
import requests
from sermos.utils.module_utils import get_access_key, get_client_pkg_name
from sermos.sermos_yaml import load_sermos_config
from sermos.constants import DEFAULT_DEPLOY_URL

logger = logging.getLogger(__name__)


class SermosDeploy():
    """ Primary Sermos Deployment class for invocation and status updates.
    """
    def __init__(self,
                 access_key: str = None,
                 pkg_name: str = None,
                 sermos_yaml_filename: str = None,
                 commit_hash: str = None,
                 deploy_url: str = None,
                 deploy_branch: str = 'main'):
        """ Arguments:
                access_key (optional): Access key, issued by Sermos, that
                    dictates the environment into which this request will be
                    deployed. Defaults to checking the environment for
                    `SERMOS_ACCESS_KEY`. If not found, will exit.
                pkg_name (optional): Directory name for your Python
                    package. e.g. my_package_name . If none provided, will check
                    environment for `SERMOS_CLIENT_PKG_NAME`. If not found,
                    will exit.
                sermos_yaml_filename (optional): Relative path to find your
                    `sermos.yaml` configuration file. Defaults to `sermos.yaml`
                    which should be found inside your `pkg_name`
                commit_hash (optional): The specific commit hash of your git
                    repo to deploy. If not provided, then current HEAD as of
                    invocation will be used. This is the default usage, and is
                    useful in the case of a CI/CD pipeline such that the Sermos
                    deployment is invoked after your integration passes.
                deploy_url (optional): Defaults to primary sermos deployment
                    endpoint. Only modify this if there is a specific, known
                    reason to do so.

        """
        super(SermosDeploy, self).__init__()
        self.access_key = get_access_key(access_key)
        self.pkg_name = get_client_pkg_name(pkg_name)
        self.sermos_yaml_filename = sermos_yaml_filename
        self.commit_hash = commit_hash
        self.sermos_yaml = None  # Established later, only on `invoke`
        self.encoded_sermos_yaml = None  # Established later, only on `invoke`
        self.deploy_payload = None  # Established later, only on `invoke`
        self.deploy_url = deploy_url if deploy_url\
            else DEFAULT_DEPLOY_URL
        self.deploy_branch = deploy_branch

        # Note: Sermos Cloud's API expects `apikey`
        self.headers = {
            'Content-Type': 'application/json',
            'apikey': self.access_key
        }

    def _set_commit_hash(self):
        """ Retrieve the commit hash of the current git state and set to
            current deployment object.
        """
        if self.commit_hash is None:
            self.commit_hash = subprocess.check_output(
                ["git", "rev-parse", "--verify",
                 "HEAD"]).strip().decode('utf-8')

    def _set_encoded_sermos_yaml(self):
        """ Provide the b64 encoded sermos.yaml file as part of request.
            Primarily used to get the custom workers definitions, etc. so
            the deployment endpoint can generate the values.yaml.
        """
        self.sermos_yaml = load_sermos_config(self.pkg_name,
                                              self.sermos_yaml_filename,
                                              as_dict=False)
        self.encoded_sermos_yaml = base64.b64encode(
            self.sermos_yaml.encode('utf-8')).decode('utf-8')

    def _set_deploy_payload(self):
        """ Set the deployment payload correctly.
        """
        self._set_commit_hash()
        self._set_encoded_sermos_yaml()
        self.deploy_payload = {
            "sermos_yaml": self.encoded_sermos_yaml,
            "commit_hash": self.commit_hash,
            "deploy_branch": self.deploy_branch,
            "client_package_name": self.pkg_name
        }

    def get_deployment_status(self):
        """ Info on a specific deployment
        """
        this_url = self.deploy_url + '/status'
        r = requests.get(this_url, headers=self.headers)
        return r

    def validate_deployment(self, output_file: str = None):
        """ Test rendering sermos.yaml and validate.
        """
        # Running this will raise an exception if something is invalid.
        self._set_deploy_payload()

        if output_file:
            with open(output_file, 'w') as f:
                f.write(self.sermos_yaml)

        # Additional validation based on logical requirements (validation of
        # the schemaa is handled by Marshmallow but there can be 'valid' entries
        # that would result in a failed deployment, such as an invalid
        # application under appConfig.appPath, for example)

        return True

    def invoke_deployment(self):
        """ Invoke a Sermos AI Deployment

            If no commit_hash was provided, use the "current" commit hash
            of the client package during this invocation.

            Required convention is that your client's python package
            version number is specified in the file `my_package/__init__.py`
            and is defined as a string assigned to the variable `__version__`,
            e.g. `__version__ = '0.1.0'`
        """
        self._set_deploy_payload()

        # Make request to your environment's endpoint
        r = requests.post(self.deploy_url,
                          headers=self.headers,
                          data=json.dumps(self.deploy_payload))
        return r
