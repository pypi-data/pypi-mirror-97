from zeep import Client
from zeep.plugins import HistoryPlugin
from lxml.etree import Element
from lxml import etree
import requests
import re
from urllib.parse import urljoin
from .project import Project

_baseServiceUrl = 'ws/services'


class Polarion(object):
    """
    Create a Polarion client which communicates to the Polarion server.

    :param polarion_url: The base URL for the polarion instance. For example http://example/com/polarion
    :param user: The user name to login
    :param password: The password for that user

    """

    def __init__(self, polarion_url, user, password):
        self.user = user
        self.password = password
        self.url = polarion_url

        self.services = {}

        if not self.url.endswith('/'):
            self.url += '/'
        self.url = urljoin(self.url, _baseServiceUrl)

        self._getServices()
        self._createSession()

    def _getServices(self):
        """
        Parse the list of services available in the overview
        """
        service_overview = requests.get(self.url)
        service_base_url = self.url + '/'
        if service_overview.ok:
            services = re.findall("(\w+)WebService", service_overview.text)
            for service in services:
                if service not in self.services:
                    self.services[service] = {'url': urljoin(
                        service_base_url, service + 'WebService')}

    def _createSession(self):
        """
        Starts a session with the specified user/password
        """
        if 'Session' in self.services:
            self.history = HistoryPlugin()
            self.services['Session']['client'] = Client(
                self.services['Session']['url'] + '?wsdl', plugins=[self.history])
            try:
                self.sessionHeaderElement = None
                self.services['Session']['client'].service.logIn(
                    self.user, self.password)
                tree = self.history.last_received['envelope'].getroottree()
                self.sessionHeaderElement = tree.find(
                    './/{http://ws.polarion.com/session}sessionID')
            except:
                raise Exception(
                    f'Could not log in to Polarion for user {self.user}')
            if self.sessionHeaderElement is not None:
                self._updateServices()
        else:
            raise Exception(
                'Cannot login because WSDL has no SessionWebService')

    def _updateServices(self):
        """
        Updates all services with the correct session ID
        """
        if self.sessionHeaderElement == None:
            raise Exception('Cannot update services when not logged in')
        for service in self.services:
            if service != 'Session':
                if 'client' not in service:
                    self.services[service]['client'] = Client(
                        self.services[service]['url'] + '?wsdl')
                self.services[service]['client'].set_default_soapheaders(
                    [self.sessionHeaderElement])
            if service == 'Tracker':
                # allow addComment to be send without title, needed for reply comments
                self.services[service]['client'].service.addComment._proxy._binding.get(
                    'addComment').input.body.type._element[1].nillable = True

    def hasService(self, name: str):
        """
        Checks if a WSDL service is available
        """
        if name in self.services:
            return True
        return False

    def getService(self, name: str):
        """
        Get a WSDL service client. The name can be 'Trakcer' or 'Session'
        TODO: When a service is requested, check if the user's sessions is still valid.
        """
        if name in self.services:
            return self.services[name]['client'].service
        else:
            raise Exception('Service does not exsist')

    def getProject(self, project_id):
        """Get a Polarion project

        :param project_id: The ID of the project.
        :return: The request project
        :rtype: Project
        """
        return Project(self, project_id)

    def __repr__(self):
        return f'Polarion client for {self.url} with user {self.user}'

    def __str__(self):
        return f'Polarion client for {self.url} with user {self.user}'
