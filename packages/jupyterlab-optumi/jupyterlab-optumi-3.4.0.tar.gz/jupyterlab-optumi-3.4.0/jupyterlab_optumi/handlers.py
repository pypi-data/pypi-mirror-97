'''
Copyright (C) Optumi Inc - All rights reserved.

You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
'''

## Jupyter imports
from jupyter_core.paths import jupyter_data_dir
from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
from tornado.escape import json_decode
from tornado.ioloop import IOLoop
from tornado.web import authenticated

from ._version import __version__

## Standard library imports

# Generic Operating System Services
import os, io, time

# Python Runtime Services
import traceback

# Concurrent execution
from threading import Lock, Thread

# Internet Protocols and Support
import uuid
from urllib import request
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode
from http.cookiejar import DefaultCookiePolicy, CookieJar

# Internet Data Handling
import json, mimetypes, base64

# Networking and Interprocess Communication
import socket, ssl, select

# Data Compression and Archiving
from zipfile import ZipFile, ZIP_DEFLATED

# Cryptographic Services
import hashlib

## Other imports
from cryptography import x509
from cryptography.hazmat.backends import default_backend

## Flags
# WARNING: This flag will show error tracebacks where normally not shown, but it will cause some < 500 response codes to be 500
DEBUG = False

lock = Lock()
## We need to somehow timeout/remove old progress data from these
compressionProgress = {}
uploadProgress = {}
launchStatus = {}
downloadProgress = {}

sessionSockets = {}

# Initialize the domain from the local file
OPTUMI_FILE = jupyter_data_dir() + "/optumi.txt"

def get_domain():
    if os.path.exists(OPTUMI_FILE):
        with open(OPTUMI_FILE, "r") as f:
            return f.readline().strip()
    return ""

def update_domain(new_domain):
    global domain
    if domain != '':
        domain = new_domain
        # Save the IP to a file so the user doesn't have to keep re-entering it
        with open(OPTUMI_FILE, "w+") as f:
            f.write(domain)

domain = get_domain()
jupyterHome = ""


jupyter_log = None
# Windows doesn't support colors
COLOR_START = '' if os.name == 'nt' else '\033[94m'
COLOR_END = '' if os.name == 'nt' else '\033[0m'
def optumi_start(c=None):
    if c is None:
        return COLOR_START + '[Optumi]' + COLOR_END + ' '
    return COLOR_START + '[Optumi]' + COLOR_END + ' ' + c.__class__.__name__ + ': '

def get_path():
    return "https://" + domain + ":8443"

class VersionHandler(IPythonHandler):
    @authenticated
    async def get(self):
        global domain
        try:
            self.write(__version__)
        except Exception as e:
            # 401 unauthorized
            self.set_status(401)
            self.write(json.dumps({'domain': domain, 'message': 'Encountered error while getting version'}))
            jupyter_log.error(optumi_start(self) + str(e))
            # We don't want to raise an error here, since it will override the domain we send back to the extension 
            # if DEBUG: raise e

class LoginHandler(IPythonHandler):
    @authenticated
    async def get(self):
        global domain
        try:
            response = await IOLoop.current().run_in_executor(None, get_new_agreement)
            if not getattr(response, 'geturl', False) or response.getcode() != 200:
                self.set_status(response.getcode())
                self.write(json.dumps({'domain': domain, 'message': 'Encountered error while getting new user agreement'}))
                jupyter_log.error(optumi_start(self) + str(response))
                return
            newAgreement = True
            buf = io.BytesIO()
            blocksize = 4096 # just made something up
            size = 0
            while True:
                read = response.read(blocksize)
                if not read:
                    break
                buf.write(read)
                size += len(read)
            if size == 0:
                newAgreement = False
            else:
                with open("Agreement.html", "wb") as f:
                    f.write(base64.decodebytes(buf.getvalue()))
            response = await IOLoop.current().run_in_executor(None, get_user_information)
            self.set_status(response.getcode())
            user_information = json.load(response)
            user_information['newAgreement'] = newAgreement
            user_information['message'] = 'Logged in successfully'
            user_information['domain'] = domain
            self.write(user_information)
            if response.getcode() >= 300: jupyter_log.info(optumi_start(self) + str(response))
        except Exception as e:
            # 401 unauthorized
            self.set_status(401)
            self.write(json.dumps({'domain': domain, 'message': 'Encountered error while getting user information'}))
            jupyter_log.error(optumi_start(self) + str(e))
            # We don't want to raise an error here, since it will override the domain we send back to the extension
            # if DEBUG: raise e

    @authenticated
    async def post(self):
        global domain
        try:
            data = json.loads(self.request.body)
            ## Login
            domain = data['domain']
            update_domain(domain)
            loginName = data['loginName']
            password = data['password']
            login_status, message = await IOLoop.current().run_in_executor(None, login_rest_server, loginName, password)
            if login_status == 1:
                ### NOTE: If we succeed logging in but fail after, we want to try to logout
                ## Exchange versions
                extension_version = __version__
                response = await IOLoop.current().run_in_executor(None, exchange_versions, extension_version)
                if not getattr(response, 'geturl', False) or response.getcode() != 200:
                    self.write(json.dumps({'loginFailedMessage': response.read().decode('utf-8'), 'message': 'Version exchange failed', 'loginFailed': True}))
                    jupyter_log.error(optumi_start(self) + str(response))
                    IOLoop.current().run_in_executor(None, logout)
                    return
                controller_version = response.read().decode('utf-8')
                ## Get new agreement
                response = await IOLoop.current().run_in_executor(None, get_new_agreement)
                if not getattr(response, 'geturl', False) or response.getcode() != 200:
                    self.write(json.dumps({'loginFailedMessage': 'Unable to get agreement', 'message': 'Getting agreement failed', 'loginFailed': True}))
                    jupyter_log.error(optumi_start(self) + str(response))
                    IOLoop.current().run_in_executor(None, logout)
                    return
                newAgreement = True
                buf = io.BytesIO()
                blocksize = 4096 # just made something up
                size = 0
                while True:
                    read = response.read(blocksize)
                    if not read:
                        break
                    buf.write(read)
                    size += len(read)
                if size == 0:
                    newAgreement = False
                else:
                    with open("Agreement.html", "wb") as f:
                        f.write(base64.decodebytes(buf.getvalue()))
                # We should check that the versions are valid
                jupyter_log.info(optumi_start(self) + 'Connected to Optumi controller version ' + controller_version)
                ## Get user information
                response = await IOLoop.current().run_in_executor(None, get_user_information)
                if not getattr(response, 'geturl', False) or response.getcode() != 200:
                    self.set_status(response.getcode())
                    self.write(json.dumps({'loginFailedMessage': 'Unable to get user information', 'message': 'Unable to get user information', 'loginFailed': True}))
                    jupyter_log.error(optumi_start(self) + str(response))
                    IOLoop.current().run_in_executor(None, logout)
                    return
                user_information = json.load(response)
                user_information['newAgreement'] = newAgreement
                user_information['message'] = 'Logged in successfully'
                self.write(json.dumps(user_information))
            elif login_status == -1:
                self.write(json.dumps({'loginFailedMessage': message, 'message': 'Login failed with message: ' + message, 'loginFailed': True}))
            elif login_status == -2:
                self.write(json.dumps({'message': 'Login failed due to invalid request', 'domainFailed': True}))
        except Exception as e:
            self.set_status(401)
            self.write(json.dumps({'message': 'Encountered error while handling login'}))
            IOLoop.current().run_in_executor(None, logout)
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

class SignAgreementHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            timeOfSigning = data['timeOfSigning']
            hashOfSignedAgreement = hash_file("Agreement.html")
            response = await IOLoop.current().run_in_executor(None, sign_agreement, timeOfSigning, hashOfSignedAgreement)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() == 200:
                os.remove("Agreement.html")
            if response.getcode() >= 300: jupyter_log.info(optumi_start(self) + str(response))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_start(self) + str(e))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error signing agreement'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

class SetUserInformationHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            param = data['param']
            value = data['value']
            response = await IOLoop.current().run_in_executor(None, set_user_information, param, value)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_start(self) + str(response))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_start(self) + str(e))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error setting user information'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

class LogoutHandler(IPythonHandler):
    @authenticated
    async def get(self):
        try:
            response = await IOLoop.current().run_in_executor(None, logout)
            self.set_status(response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_start(self) + str(response))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_start(self) + str(e))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while logging out'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

class PreviewNotebookHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            notebook = data['notebook']
            response = await IOLoop.current().run_in_executor(None, preview_notebook, notebook)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_start(self) + str(response))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_start(self) + str(e))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while previewing notebook'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

class SetupNotebookHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            name = data['name']
            timestamp = data['timestamp']
            notebook = data['notebook']
            response = await IOLoop.current().run_in_executor(None, setup_notebook, name, timestamp, notebook)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_start(self) + str(response))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_start(self) + str(e))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while setting up notebook'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

class LaunchNotebookHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            requirementsFile = data.get('requirementsFile')     # we use .get() for params that are not required
            dataFiles = data.get('dataFiles')                   # we use .get() for params that are not required
            compress = data['compress']
            uuid = data['uuid']
            timestamp = data['timestamp']
            IOLoop.current().run_in_executor(None, launch_notebook, requirementsFile, dataFiles, compress, uuid, timestamp)
            self.write(json.dumps({'message': 'success'}))
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while launching notebook'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

class GetLaunchStatusHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            uuid = data['uuid']
            json_map = await IOLoop.current().run_in_executor(None, get_launch_status, uuid)
            if json_map == {}:
                self.set_status(204) # 204 No content
            else:
                self.write(json.dumps(json_map))
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while getting launch status'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

def get_launch_status(key):
    data = {}
    try:
        lock.acquire()
        data = launchStatus[key]
    except:
        pass
    finally:
        lock.release()
    return data

class GetLaunchUploadProgressHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            uuid = data['uuid']
            json_map = await IOLoop.current().run_in_executor(None, get_launch_upload_progress, uuid)
            if json_map == {}:
                self.set_status(204) # 204 No content
            else:
                self.write(json.dumps(json_map))
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while getting upload progress'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

def get_launch_upload_progress(key):
    data = {}
    try:
        lock.acquire()
        data = uploadProgress[key]
    except:
        pass
    finally:
        lock.release()
    return data

class GetLaunchCompressionProgressHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            uuid = data['uuid']
            json_map = await IOLoop.current().run_in_executor(None, get_launch_compression_progress, uuid)
            if json_map == {}:
                self.set_status(204) # 204 No content
            else:
                self.write(json.dumps(json_map))
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while getting upload progress'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

def get_launch_compression_progress(key):
    data = {}
    try:
        lock.acquire()
        data = compressionProgress[key]
    except:
        pass
    finally:
        lock.release()
    return data

class StopNotebookHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            uuid = data['uuid']
            response = await IOLoop.current().run_in_executor(None, stop_notebook, uuid)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_start(self) + str(response))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_start(self) + str(e))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while stopping notebook'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

class TeardownNotebookHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            uuid = data['uuid']
            response = await IOLoop.current().run_in_executor(None, teardown_notebook, uuid)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_start(self) + str(response))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_start(self) + str(e))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while tearing down notebook'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

class GetMachinesHandler(IPythonHandler):
    @authenticated
    async def get(self):
        try:
            response = await IOLoop.current().run_in_executor(None, get_machines)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_start(self) + str(response))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_start(self) + str(e))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while getting machines'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

class GetDataConnectorsHandler(IPythonHandler):
    @authenticated
    async def get(self):
        try:
            response = await IOLoop.current().run_in_executor(None, get_data_connectors)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_start(self) + str(response))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_start(self) + str(e))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while getting machines'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

class AddDataConnectorHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            dataService = data['dataService']
            name = data['name']
            info = data['info']
            response = await IOLoop.current().run_in_executor(None, add_data_connector, dataService, name, info)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_start(self) + str(response))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_start(self) + str(e))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while getting machines'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

class RemoveDataConnectorHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            name = data['name']
            response = await IOLoop.current().run_in_executor(None, remove_data_connector, name)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_start(self) + str(response))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_start(self) + str(e))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while getting machines'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

class PushWorkloadStatusUpdateHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            uuid = data['uuid']
            phase = data['phase']
            update = data['update']
            response = await IOLoop.current().run_in_executor(None, push_workload_status_update, uuid, phase, update)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_start(self) + str(response))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_start(self) + str(e))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while pushing workload status update'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

class PullWorkloadStatusUpdateHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            uuid = data['uuid']
            lastInitializingLine = data['lastInitializingLine']
            lastUploadingLine = data['lastUploadingLine']
            lastRequisitioningLine = data['lastRequisitioningLine']
            lastRunningLine = data['lastRunningLine']
            response = await IOLoop.current().run_in_executor(None, pull_workload_status_update, uuid, lastInitializingLine, lastUploadingLine, lastRequisitioningLine, lastRunningLine)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_start(self) + str(response))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_start(self) + str(e))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while pulling workload status update'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

class PullModuleStatusUpdateHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            workloadUUID = data['workloadUUID']
            moduleUUID = data['moduleUUID']
            lastUpdateLine = data['lastUpdateLine']
            lastOutputLine = data['lastOutputLine']
            response = await IOLoop.current().run_in_executor(None, pull_module_status_update, workloadUUID, moduleUUID, lastUpdateLine, lastOutputLine)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_start(self) + str(response))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_start(self) + str(e))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while pulling module status update'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

class PushModuleInputHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            workloadUUID = data['workloadUUID']
            moduleUUID = data['moduleUUID']
            line = data['line']
            response = await IOLoop.current().run_in_executor(None, push_module_input, workloadUUID, moduleUUID, line)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_start(self) + str(response))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_start(self) + str(e))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while pushing module input'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

class SaveNotebookOutputFileHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            workloadUUID = data['workloadUUID']
            moduleUUID = data['moduleUUID']
            name = data['name']
            files = data['files']
            overwrite = data['overwrite']
            response = await IOLoop.current().run_in_executor(None, save_notebook_output_file, workloadUUID, moduleUUID, name, files, overwrite)
            # We only expect a response if something went wrong
            if response != None: raise response
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_start(self) + str(e))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while saving notebook output file'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

class GetFileDownloadProgressHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            name = data['name']
            json_map = await IOLoop.current().run_in_executor(None, get_file_download_progress, name)
            if json_map == {}:
                self.set_status(204) # No content
            else:
                self.write(json.dumps(json_map))
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while getting download progress'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

def get_file_download_progress(key):
    data = {}
    try:
        lock.acquire()
        data = downloadProgress[key]
    except:
        pass
    finally:
        lock.release()
    return data

class GetTotalBillingHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            startTime = data['startTime']
            endTime = data['endTime']
            response = await IOLoop.current().run_in_executor(None, get_total_billing, startTime, endTime)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_start(self) + str(response))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_start(self) + str(e))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while getting total billing'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

class GetDetailedBillingHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            startTime = data['startTime']
            endTime = data['endTime']
            response = await IOLoop.current().run_in_executor(None, get_detailed_billing, startTime, endTime)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_start(self) + str(response))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_start(self) + str(e))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while getting total billing'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

class DeleteMachineHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            uuid = data['uuid']
            response = await IOLoop.current().run_in_executor(None, delete_machine, uuid)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_start(self) + str(response))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_start(self) + str(e))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while deleting machine'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

class ChangePasswordHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            loginName = data['loginName']
            oldPassword = data['oldPassword']
            newPassword = data['newPassword']
            response = await IOLoop.current().run_in_executor(None, change_password, loginName, oldPassword, newPassword)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_start(self) + str(response))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_start(self) + str(e))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while deleting machine'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

class CreateCheckoutHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            items = data['items']
            redirect = data['redirect']
            response = await IOLoop.current().run_in_executor(None, create_checkout, items, redirect)
            self.set_status(401 if response.geturl().endswith('/login') else response.getcode())
            self.write(response.read())
            if response.getcode() >= 300: jupyter_log.info(optumi_start(self) + str(response))
        except (ConnectionError, URLError) as e:
            # If we can't connect to the REST interface, we want the extension to treat it as the user being loggeed out
            self.set_status(401)
            self.write(json.dumps({'message': str(e)}))
            jupyter_log.warning(optumi_start(self) + str(e))
            if DEBUG: raise e
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while creating payment intent'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

class ConnectSessionHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            module = data['module']

            json_map = {}
            if module in sessionSockets.keys() and sessionSockets[module]['thread'].is_alive():
                json_map['port'] = sessionSockets[module]['socket'].getsockname()[1]
            else:
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.setblocking(0)
                bound = False
                port = 49152
                while not bound:
                    # Protect if we somehow try all ports and they are in use
                    if port > 65535:
                        break
                    # Try to bind to new port
                    try:
                        server.bind(('', port))
                        bound = True
                    except Exception as e:
                        port += 1
                        # jupyter_log.info(optumi_start(self) + str(e))
                server.listen(1)

                json_map['port'] = port

                # Keep track of the socket object, the send/receive threads, and the lock object to make it easy to close things property
                socket_info = {}
                socket_info['socket'] = server
                socket_info['thread'] = Thread(target=handle_session, args=(module, server), daemon=True)

                sessionSockets[module] = socket_info

                # Start the threads
                socket_info['thread'].start()

            self.write(json.dumps(json_map))
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while connecting session'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

class DisconnectSessionHandler(IPythonHandler):
    @authenticated
    async def post(self):
        try:
            data = json.loads(self.request.body)
            module = data['module']
            if module in sessionSockets.keys():
                sessionSockets[module]['socket'].close()
                sessionSockets.pop(module, None)
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'message': 'Encountered error while disconnection session'}))
            jupyter_log.error(optumi_start(self) + str(e))
            if DEBUG: raise e

# Get a windows path in a format we can use on linux
def fix_path_for_linux(path):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    fixed = path

    # Remove letter and : at the beginning
    for letter in letters:
        if fixed.startswith(letter + ':'):
            fixed = fixed.replace(letter + ':', '', 1)
            break
        if fixed.startswith(letter.upper() + ':'):
            fixed = fixed.replace(letter.upper() + ':', '', 1)
            break

    # Switch slashes to correct direction
    fixed = fixed.replace('\\', '/')

    return fixed

def setup_handlers(server_app):
    global jupyterHome
    global jupyter_log

    jupyter_log = server_app.log

    web_app = server_app.web_app
    base_url = web_app.settings['base_url']
    jupyterHome = fix_path_for_linux(os.path.expanduser(web_app.settings['server_root_dir']))
    host_pattern = '.*$'
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/version'), VersionHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/login'), LoginHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/sign-agreement'), SignAgreementHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/set-user-information'), SetUserInformationHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/logout'), LogoutHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/preview-notebook'), PreviewNotebookHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/setup-notebook'), SetupNotebookHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/launch-notebook'), LaunchNotebookHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/get-launch-status'), GetLaunchStatusHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/get-launch-compression-progress'), GetLaunchCompressionProgressHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/get-launch-upload-progress'), GetLaunchUploadProgressHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/stop-notebook'), StopNotebookHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/teardown-notebook'), TeardownNotebookHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/get-machines'), GetMachinesHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/get-data-connectors'), GetDataConnectorsHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/add-data-connector'), AddDataConnectorHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/remove-data-connector'), RemoveDataConnectorHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/push-workload-status-update'), PushWorkloadStatusUpdateHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/pull-workload-status-update'), PullWorkloadStatusUpdateHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/pull-module-status-update'), PullModuleStatusUpdateHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/push-module-input'), PushModuleInputHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/save-notebook-output-file'), SaveNotebookOutputFileHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/get-file-download-progress'), GetFileDownloadProgressHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/get-total-billing'), GetTotalBillingHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/get-detailed-billing'), GetDetailedBillingHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/delete-machine'), DeleteMachineHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/change-password'), ChangePasswordHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/create-checkout'), CreateCheckoutHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/connect-session'), ConnectSessionHandler)])
    web_app.add_handlers(host_pattern, [(url_path_join(base_url, '/optumi/disconnect-session'), DisconnectSessionHandler)])

###############################################################################################
####    Login
####

def install_auth_opener(loginName, password):
    policy = DefaultCookiePolicy(allowed_domains=[domain])
    cj = CookieJar(policy)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    opener = request.build_opener(request.HTTPCookieProcessor(cj), request.HTTPSHandler(context=ctx))
    request.install_opener(opener)
    info = urlencode({"username": loginName, "password": password}).encode('utf8')
    return info

def login_rest_server(loginName, password):
    try:
        # Since we are bypassing the hostname check for the SSL context, we manually check it here
        cert = ssl.get_server_certificate((domain, 8443))
        cert = x509.load_pem_x509_certificate(cert.encode(), default_backend())
        name = cert.subject.get_attributes_for_oid(x509.oid.NameOID.COMMON_NAME)[0].value
        if name != 'devserver.optumi.com':
            raise ssl.SSLCertVerificationError("SSL domain check failed (" + name + " is not devserver.optumi.com)")

        URL = get_path() + '/login'
        errorURL = URL + '?error'

        req = request.Request(URL, data=install_auth_opener(loginName, password))
        response = request.urlopen(req, timeout=30)
        if response.geturl() == errorURL:
            # Parse the error message to pass on to the user
            html = response.read().decode()
            try:
                message = html.split('<div class="alert alert-danger" role="alert">')[1].split('</div>')[0]
            except:
                message = "Invalid username/password"
            return -1, message
        return 1, ""
    except Exception as err:
        jupyter_log.error(optumi_start() + str(err))
        return -2, ""

def logout():
    URL = get_path() + '/logout'
    try:
        req = request.Request(URL)
        return request.urlopen(req)
    except HTTPError as e:
        return e

###############################################################################################
####    Optumi REST Interface
####

def sign_agreement(timeOfSigning, hashOfSignedAgreement):
    URL = get_path() + '/exp/jupyterlab/sign-agreement'
    try:
        form = MultiPartForm()
        form.add_field('timeOfSigning', timeOfSigning)
        form.add_field('hashOfSignedAgreement', hashOfSignedAgreement)
        data = bytes(form)
        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req)
    except HTTPError as e:
        return e

def get_new_agreement():
    URL = get_path() + '/exp/jupyterlab/get-new-agreement'
    try:
        req = request.Request(URL)
        return request.urlopen(req)
    except HTTPError as e:
        return e

def exchange_versions(version):
    URL = get_path() + '/exp/jupyterlab/exchange-versions'
    try:
        form = MultiPartForm()
        form.add_field('version', version)
        data = bytes(form)
        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req)
    except HTTPError as e:
        return e

def get_user_information():
    URL = get_path() + '/exp/jupyterlab/get-user-information'
    try:
        req = request.Request(URL)
        return request.urlopen(req)
    except HTTPError as e:
        return e

def set_user_information(param, value):
    URL = get_path() + '/exp/jupyterlab/set-user-information'
    try:
        form = MultiPartForm()
        form.add_field('param', param)
        form.add_field('value', value)
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req)
    except HTTPError as e:
        return e

def preview_notebook(notebook):
    URL = get_path() + '/exp/jupyterlab/preview-notebook'
    try:
        form = MultiPartForm()
        form.add_file('notebook', notebook['path'], fileHandle=io.BytesIO(notebook['content'].encode('utf-8')))

        # Build the request, including the byte-string
        # for the data to be posted.
        data = bytes(form)
        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))

        # jupyter_log.info(optumi_start() + )
        # jupyter_log.info(optumi_start() + 'OUTGOING DATA:')
        # for name, value in req.header_items():
        #     jupyter_log.info(optumi_start() + '{}: {}'.format(name, value))
        # jupyter_log.info(optumi_start() + )
        # jupyter_log.info(optumi_start() + req.data.decode('utf-8'))

        # jupyter_log.info(optumi_start() + )
        # jupyter_log.info(optumi_start() + 'SERVER RESPONSE:')
        # jupyter_log.info(optumi_start() + request.urlopen(req).read().decode('utf-8'))

        return request.urlopen(req)
    except HTTPError as e:
        return e

def setup_notebook(name, timestamp, notebook):
    URL = get_path() + '/exp/jupyterlab/setup-notebook'
    try:
        form = MultiPartForm()
        form.add_field('name', name)
        form.add_field('timestamp', timestamp)
        form.add_file('notebook', notebook['path'], fileHandle=io.BytesIO(notebook['content'].encode('utf-8')))
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req)
    except HTTPError as e:
        return e

def launch_notebook(requirementsFile, dataFiles, compress, uuid, timestamp):
    URL = get_path() + '/exp/jupyterlab/launch-notebook'
    try:
        form = MultiPartForm()
        form.add_field('compressed', str(compress))
        form.add_field('uuid', uuid)
        ## Send this list as a file since it can have arbitrary length and cause issues for the REST Interface if sent as an array
        form.add_file('dataFileNames', 'dataFileNames', fileHandle=io.BytesIO(','.join(dataFiles).encode('utf-8')))
        form.add_field('timestamp', timestamp)
        form.add_field('jupyterHome', jupyterHome)
        form.add_field('userHome', fix_path_for_linux(os.path.expanduser('~')))

        try:
            lock.acquire()
            if uuid in launchStatus and 'status' in launchStatus[uuid] and launchStatus[uuid]['status'] == "Failed":
                raise CancelledError("Job canceled")
            launchStatus[uuid] = {'status': 'Started'}
        except CancelledError:
            raise
        except:
            pass
        finally:
            lock.release()
        if requirementsFile != None:
            form.add_file('requirementsFile', 'requirements.txt', fileHandle=io.BytesIO(requirementsFile.encode('utf-8')))
            # form.add_file('requirementsFile', requirementsFile, fileHandle=open(requirementsFile, 'rb'))
        filesToZip = [] # We use this only if we are compressing files
        zipFile = "" # We use this only if we are compressing files
        if dataFiles != None and len(dataFiles) > 0:
            ## Check for files in chunks of 100
            while len(dataFiles) > 100:
                chunk = dataFiles[:100]
                for exists, file in zip(json.load(check_if_files_exist(chunk))['exists'], chunk):
                    try:
                        if not exists:
                            if compress:
                                filesToZip.append(file)
                            else:
                                form.add_file('dataFiles', file, fileHandle=open(file, 'rb'))
                    except Exception as e:
                        raise e
                dataFiles = dataFiles[100:]
            ## Check last chunk
            for exists, file in zip(json.load(check_if_files_exist(dataFiles))['exists'], dataFiles):
                try:
                    if not exists:
                        if compress:
                            filesToZip.append(file)
                        else:
                            form.add_file('dataFiles', file, fileHandle=open(file, 'rb'))
                except Exception as e:
                    raise e
        if len(filesToZip) > 0:
            zipFile = zip_files(uuid, filesToZip)
            form.add_file('dataFiles', 'dataFiles.zip', fileHandle=open(zipFile, 'rb'))
        else:
            try:
                lock.acquire()
                compressionProgress[uuid] = {'read': 1, 'total': 1}
            except CancelledError:
                raise
            except:
                pass
            finally:
                lock.release()

        b = bytes(form)
        data = UploadProgressOpener(b, uuid)

        ## This check should be kept in sync with max-file-size and max-request-size in Swagger2SpringBoot.java
        maxRequestSize = 5 * 1024 * 1024 * 1024
        if len(b) > maxRequestSize:
            raise CancelledError("Upload limit (5GiB) exceeded")

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        response = request.urlopen(req)
        if zipFile != "":
            response.getcode() # wait for the response to come back
            os.remove(zipFile)
        try:
            lock.acquire()
            if response.getcode() == 200:
                launchStatus[uuid] = json.loads(response.read())
                launchStatus[uuid]['status'] = "Finished"
        except:
            pass
        finally:
            lock.release()
    except CancelledError as err:
        try:
            lock.acquire()
            launchStatus[uuid]['status'] = "Failed"
            launchStatus[uuid]['message'] = err.message
        except:
            pass
        finally:
            lock.release()
        raise
    except FileNotFoundError as err:
        try:
            lock.acquire()
            launchStatus[uuid]['status'] = "Failed"
            launchStatus[uuid]['message'] = "Unable to find upload file(s)"
            launchStatus[uuid]['snackbar'] = 'Unable to find: ' + str(err).split(' ')[-1] + '. Please check the path in "Upload Files".'
        except:
            pass
        finally:
            lock.release()
        raise
    except:
        try:
            lock.acquire()
            launchStatus[uuid]['status'] = "Failed"
        except:
            pass
        finally:
            lock.release()
        raise

def stop_notebook(uuid):
    URL = get_path() + '/exp/jupyterlab/stop-notebook'
    try:
        form = MultiPartForm()
        form.add_field('uuid', uuid)
        data = bytes(form)

        try:
            lock.acquire()
            launchStatus[uuid]['status'] = "Failed"
            compressionProgress[uuid] = None
            uploadProgress[uuid] = None
        except:
            pass
        finally:
            lock.release()

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req)
    except HTTPError as e:
        return e

def teardown_notebook(uuid):
    URL = get_path() + '/exp/jupyterlab/teardown-notebook'
    try:
        form = MultiPartForm()
        form.add_field('uuid', uuid)
        data = bytes(form)

        try:
            lock.acquire()
            launchStatus[uuid]['status'] = "Failed"
            compressionProgress[uuid] = None
            uploadProgress[uuid] = None
        except:
            pass
        finally:
            lock.release()

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req)
    except HTTPError as e:
        return e

def check_if_files_exist(fileNames):
    URL = get_path() + '/exp/jupyterlab/check-if-files-exist'
    try:
        form = MultiPartForm()
        for file in fileNames:
            form.add_field('fileNames', file)
            form.add_field('hashes', hash_file(file))
        form.add_field('jupyterHome', jupyterHome)
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req)
    except HTTPError as e:
        return e

def get_machines():
    URL = get_path() + '/exp/jupyterlab/get-machines'
    try:
        req = request.Request(URL)
        return request.urlopen(req)
    except HTTPError as e:
        return e

def get_data_connectors():
    URL = get_path() + '/exp/jupyterlab/get-data-connectors'
    try:
        req = request.Request(URL)
        return request.urlopen(req)
    except HTTPError as e:
        return e

def add_data_connector(dataService, name, info):
    URL = get_path() + '/exp/jupyterlab/add-data-connector'
    try:
        form = MultiPartForm()
        form.add_field('dataService', dataService)
        form.add_field('name', name)
        form.add_field('info', info)
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req)
    except HTTPError as e:
        return e

def remove_data_connector(name):
    URL = get_path() + '/exp/jupyterlab/remove-data-connector'
    try:
        form = MultiPartForm()
        form.add_field('name', name)
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req)
    except HTTPError as e:
        return e

def push_workload_status_update(uuid, phase, update):
    URL = get_path() + '/exp/jupyterlab/push-workload-status-update'
    try:
        form = MultiPartForm()
        form.add_field('uuid', uuid)
        form.add_field('phase', phase)
        form.add_field('update', update)
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req)
    except HTTPError as e:
        return e

def pull_workload_status_update(uuid, lastInitializingLine, lastUploadingLine, lastRequisitioningLine, lastRunningLine):
    URL = get_path() + '/exp/jupyterlab/pull-workload-status-update'
    try:
        form = MultiPartForm()
        form.add_field('uuid', uuid)
        form.add_field('lastInitializingLine', lastInitializingLine)
        form.add_field('lastUploadingLine', lastUploadingLine)
        form.add_field('lastRequisitioningLine', lastRequisitioningLine)
        form.add_field('lastRunningLine', lastRunningLine)
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req)
    except HTTPError as e:
        return e

def pull_module_status_update(workloadUUID, moduleUUID, lastUpdateLine, lastOutputLine):
    URL = get_path() + '/exp/jupyterlab/pull-module-status-update'
    try:
        form = MultiPartForm()
        form.add_field('workloadUUID', workloadUUID)
        form.add_field('moduleUUID', moduleUUID)
        form.add_field('lastUpdateLine', lastUpdateLine)
        form.add_field('lastOutputLine', lastOutputLine)
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req)
    except HTTPError as e:
        return e

def push_module_input(workloadUUID, moduleUUID, line):
    URL = get_path() + '/exp/jupyterlab/push-module-input'
    try:
        form = MultiPartForm()
        form.add_field('workloadUUID', workloadUUID)
        form.add_field('moduleUUID', moduleUUID)
        form.add_field('line', line)
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req)
    except HTTPError as e:
        return e

def save_notebook_output_file(workloadUUID, moduleUUID, name, files, overwrite):
    URL = get_path() + '/exp/jupyterlab/get-notebook-output-file'
    try:
        for file in files:
            form = MultiPartForm()
            form.add_field('workloadUUID', workloadUUID)
            form.add_field('moduleUUID', moduleUUID)
            form.add_field('fileName', file)
            data = bytes(form)

            req = request.Request(URL, data=data)
            req.add_header('Content-type', form.get_content_type())
            req.add_header('Content-length', len(data))

            response = request.urlopen(req)
            total = response.getheader('content-length')

            buf = io.BytesIO()
            if total:
                total = int(total)
                blocksize = max(4096, total//100)
                downloadProgress[name] = { 'read': 0, 'total': total }
            else:
                blocksize = 4096 # just made something up
            size = 0
            while True:
                read = response.read(blocksize)
                if not read:
                    break
                buf.write(read)
                size += len(read)
                if total:
                    try:
                        lock.acquire()
                        downloadProgress[name]['read'] = size
                    except:
                        pass
                    finally:
                        lock.release()
            if not overwrite:
                newName = file
                num = 1
                while os.path.exists(newName) and os.path.isfile(newName):
                    f, ext = os.path.splitext(file)
                    newName = f + '(' + str(num) + ')' + ext
                    num += 1
                file = newName
            dirs = os.path.dirname(file)
            if dirs != "":
                os.makedirs(dirs, exist_ok=True)
            with open(file, "wb") as f:
                f.write(base64.decodebytes(buf.getvalue()))
        return
    except HTTPError as e:
        return e

def get_total_billing(startTime, endTime):
    URL = get_path() + '/exp/jupyterlab/get-total-billing'
    try:
        form = MultiPartForm()
        form.add_field('startTime', startTime)
        form.add_field('endTime', endTime)
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req)
    except HTTPError as e:
        return e

def get_detailed_billing(startTime, endTime):
    URL = get_path() + '/exp/jupyterlab/get-detailed-billing'
    try:
        form = MultiPartForm()
        form.add_field('startTime', startTime)
        form.add_field('endTime', endTime)
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req)
    except HTTPError as e:
        return e

def delete_machine(uuid):
    URL = get_path() + '/exp/jupyterlab/release-machine'
    try:
        form = MultiPartForm()
        form.add_field('uuid', uuid)
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req)
    except HTTPError as e:
        return e

def change_password(loginName, oldPassword, newPassword):
    URL = get_path() + '/exp/jupyterlab/change-password'
    try:
        form = MultiPartForm()
        form.add_field('loginName', loginName)
        form.add_field('oldPassword', oldPassword)
        form.add_field('newPassword', newPassword)
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req)
    except HTTPError as e:
        return e

def create_checkout(items, redirect):
    URL = get_path() + '/exp/jupyterlab/create-checkout'
    try:
        form = MultiPartForm()
        for item in items:
            form.add_field('items', item)
        form.add_field('redirect', redirect)
        data = bytes(form)

        req = request.Request(URL, data=data)
        req.add_header('Content-type', form.get_content_type())
        req.add_header('Content-length', len(data))
        return request.urlopen(req)
    except HTTPError as e:
        return e

###############################################################################################
####    Hash files
####

def hash_file(fileName):
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(fileName, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()

###############################################################################################
####    Zip files
####

def zip_files(uuid, files):
    path = uuid + '.zip'
    files.sort(key=lambda x: os.path.getsize(x))
    # add up total files
    try:
        lock.acquire()
        compressionProgress[uuid] = {'read': 0, 'total': len(files)}
    except CancelledError:
        raise
    except:
        pass
    finally:
        lock.release()
    # writing files to a zipfile 
    with ZipFile(path, 'w', ZIP_DEFLATED) as zip:
        # writing each file one by one 
        for file in files:
            zip.write(file)
            try:
                lock.acquire()
                if compressionProgress[uuid] == None:
                    raise CancelledError("Compression canceled")
                compressionProgress[uuid]['read'] = compressionProgress[uuid]['read'] + 1
            except CancelledError:
                raise
            except:
                pass
            finally:
                lock.release()
    return path

###############################################################################################
####    Upload progress
####

class CancelledError(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        self.message = message

class UploadProgressOpener:
    def __init__ (self, _bytes, key):
        self._f = io.BytesIO(_bytes)
        self._key = key
        self._total = len(_bytes)
        self._uploadProgress = uploadProgress
        self._uploadProgress[self._key] = {'read': 0, 'total': self._total}

    def __len__(self):
        return self._total

    def __enter__ (self):
        return self._f

    def __exit__ (self, exc_type, exc_value, traceback):
        self.f.close()

    def read(self, n_bytes=-1):
        data = self._f.read(n_bytes)
        try:
            lock.acquire()
            if self._uploadProgress[self._key] == None:
                raise CancelledError("Upload canceled")
            self._uploadProgress[self._key]['read'] = self._uploadProgress[self._key]['read'] + len(data)
        except CancelledError:
            raise
        except:
            pass
        finally:
            lock.release()
        return data

###############################################################################################
####    FormData
####

class MultiPartForm:
    """Accumulate the data to be used when posting a form."""

    def __init__(self):
        self.form_fields = []
        self.files = []
        # Use a large random byte string to separate
        # parts of the MIME data.
        self.boundary = uuid.uuid4().hex.encode('utf-8')
        return

    def get_content_type(self):
        return 'multipart/form-data; boundary={}'.format(
            self.boundary.decode('utf-8'))

    def add_field(self, name, value):
        """Add a simple field to the form data."""
        self.form_fields.append((name, value))

    def add_file(self, fieldname, filename, fileHandle,
                 mimetype=None):
        """Add a file to be uploaded."""
        body = fileHandle.read()
        if mimetype is None:
            mimetype = (
                mimetypes.guess_type(filename)[0] or
                'application/octet-stream'
            )
        self.files.append((fieldname, filename, mimetype, body))
        return

    @staticmethod
    def _form_data(name):
        return ('Content-Disposition: form-data; '
                'name="{}"\r\n').format(name).encode('utf-8')

    @staticmethod
    def _attached_file(name, filename):
        return ('Content-Disposition: form-data; '
                'name="{}"; filename="{}"\r\n').format(
                    name, filename).encode('utf-8')

    @staticmethod
    def _content_type(ct):
        return 'Content-Type: {}\r\n'.format(ct).encode('utf-8')

    def __bytes__(self):
        """Return a byte-string representing the form data,
        including attached files.
        """
        buffer = io.BytesIO()
        boundary = b'--' + self.boundary + b'\r\n'

        # Add the form fields
        for name, value in self.form_fields:
            buffer.write(boundary)
            buffer.write(self._form_data(name))
            buffer.write(b'\r\n')
            buffer.write(value.encode('utf-8'))
            buffer.write(b'\r\n')

        # Add the files to upload
        for f_name, filename, f_content_type, body in self.files:
            buffer.write(boundary)
            buffer.write(self._attached_file(f_name, filename))
            buffer.write(self._content_type(f_content_type))
            buffer.write(b'\r\n')
            buffer.write(body)
            buffer.write(b'\r\n')

        buffer.write(b'--' + self.boundary + b'--\r\n')
        return buffer.getvalue()

###############################################################################################
####    SessionHandler
####

DEBUG_SESSIONS = False

def handle_session(module, server):
    #jupyter_log.info(optumi_start() + 'Session connected for ' + module, flush=True)

    try:
        inputs = [server]
        connections = {}

        while True:
            readable, _, _ = select.select(inputs, [], [], 0.01)

            for s in readable:
                if s is server:
                    connection, addr = s.accept()
                    connection.setblocking(0)
                    inputs.append(connection)
                    connections[connection] = addr
                else:
                    session_data = b''
                    try :
                        session_data = s.recv(1024 * 1024)
                    except Exception as e:
                        if DEBUG_SESSIONS: jupyter_log.info(optumi_start() + str(e))

                    addr = connections[s]

                    closed = False
                    if not session_data:
                        closed = True
                        inputs.remove(s)
                        s.close()
                        connections.pop(s, None)

                    ## Send data to the rest interface
                    ## We will try send an empty session_data to the controller to signal that a socket was closed
                    URL = get_path() + '/exp/jupyterlab/send-session-data'
                    try:
                        form = MultiPartForm()
                        form.add_field('module', module)
                        form.add_field('addr', addr[0])
                        form.add_field('port', str(addr[1]))
                        form.add_file('data', 'data', fileHandle=io.BytesIO(session_data))
                        form.add_field('closed', str(closed))
                        # form.add_raw_field('data', session_data)
                        data = bytes(form)

                        req = request.Request(URL, data=data)
                        req.add_header('Content-type', form.get_content_type())
                        req.add_header('Content-length', len(data))
                        response = request.urlopen(req, timeout=10)
                        if DEBUG_SESSIONS: jupyter_log.info(optumi_start() + "Received (from browser) and sent (to controller) data for module " + str((module, addr)) + " (" + str(len(session_data)) + ")")
                    
                    except HTTPError as e:
                        # if e.getcode() == 501:
                        #     inputs.remove(s)
                        #     s.close()
                        #     connections.pop(s, None)
                        jupyter_log.warning(optumi_start() + 'HTTP error when sending session data: ' + str(e))
                    except (ConnectionError, URLError) as e:
                        jupyter_log.warning(optumi_start() + 'Connection error when sending session data: ' + str(e))
                    except Exception as e:
                        jupyter_log.error(optumi_start() + 'Error when sending session data: ' + str(e))

            closed = []

            # fire off polling requests
            for s, addr in connections.items():
                URL = get_path() + '/exp/jupyterlab/receive-session-data'
                try:
                    form = MultiPartForm()
                    form.add_field('module', module)
                    form.add_field('addr', addr[0])
                    form.add_field('port', str(addr[1]))
                    data = bytes(form)

                    req = request.Request(URL, data=data)
                    req.add_header('Content-type', form.get_content_type())
                    req.add_header('Content-length', len(data))
                    # Write the response data back to the socket
                    response = request.urlopen(req, timeout=10)

                    if not response.geturl().endswith('/login'):
                        session_data = response.read()
                        if session_data:
                            s.sendall(session_data)
                            if DEBUG_SESSIONS: jupyter_log.info(optumi_start() + "Received (from controller) and sent (to browser) data for module " + str((module, addr)) + " (" + str(len(session_data)) + ")")
                
                except HTTPError as e:
                    # if e.getcode() == 501:
                    #     inputs.remove(s)
                    #     s.close()
                    #     closed.append(s)
                    jupyter_log.warning(optumi_start() + 'HTTP error when getting session data: ' + str(e))
                except (ConnectionError, URLError) as e:
                    jupyter_log.warning(optumi_start() + 'Connection error when getting session data: ' + str(e))
                except Exception as e:
                    jupyter_log.info(optumi_start() + 'Connection error when getting session data: ' + str(e))

            # Remove any closed connections
            for s in closed:
                connections.pop(s, None)

    except Exception as e:
        jupyter_log.warn(optumi_start() + 'Session closed: ' + str(e))

    #jupyter_log.info(optumi_start() + 'Session disconnected for ' + module, flush=True)
