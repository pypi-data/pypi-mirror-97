"""DNS Authenticator for subdomain provider"""
import logging

import zope.interface

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common

import requests

logger = logging.getLogger(__name__)


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for subdomain provider

    This Authenticator uses the subdomain provider API to fulfill a dns-01 challenge.
    """
    description = 'Obtain certificates using a DNS TXT record (if you are ' + \
                  'using subdomain provider for DNS).'

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add):  # pylint: disable=arguments-differ
        super(Authenticator, cls).add_parser_arguments(add)
        add('credentials', help='subdomain provider credentials INI file.')

    def more_info(self):  # pylint: disable=missing-function-docstring
        return 'This plugin configures a DNS TXT record to respond to a dns-01 challenge using ' + \
               'the subdomain provider API.'

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            'credentials',
            'subdomain provider credentials INI file',
            {
                'endpoint_url': 'API endpoint url for subdomain provider',
                'token': 'API token for subdomain provider account'
            }
        )

    def _perform(self, domain, validation_name, validation):
        self._get_subdomain_provider_client().add_txt_record(domain, validation_name, validation)

    def _cleanup(self, domain, validation_name, validation):
        self._get_subdomain_provider_client().del_txt_record(domain, validation_name, validation)

    def _get_subdomain_provider_client(self):
        return _SubdomainProviderClient(self.credentials.conf('endpoint_url'), self.credentials.conf('token'))


class _SubdomainProviderClient:
    """
    Encapsulates all communication with the endpoint provider API.
    """

    def __init__(self, endpoint_url, token):
        response = requests.get('{0}/manifest'.format(endpoint_url))

        if response.status_code != 200:
            raise errors.PluginError('API manifest content not exists')

        json = response.json()
        self.root_domain = json['root_domain']
        self.endpoint_url = endpoint_url
        self.token = token

    def add_txt_record(self, domain_name, record_name, record_content):
        """
        Add a TXT record using the supplied information.

        :param str domain_name: The domain to use to associate the record with.
        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :param str record_content: The record content (typically the challenge validation).
        :raises certbot.errors.PluginError: if an error occurs communicating with the api
        """
        position = domain_name.find(self.root_domain)
        if position == -1:
            raise errors.PluginError('root domain ({0}) is not compatible with subdomain ({1})'
                                     .format(domain_name, self.root_domain))

        response = requests.post('{0}/assign-validation-data'.format(self.endpoint_url),
                                 json={'subdomain': domain_name[:position - 1], 'data': record_content,
                                       'record_name': record_name},
                                 headers={'Authorization': 'Bearer {0}'.format(self.token)})

        if response.status_code != 200:
            raise errors.PluginError('validation data is not accepted by API')

        json = response.json()

        if not json['success']:
            raise errors.PluginError(json['message'])

    def del_txt_record(self, domain_name, record_name, record_content):
        """
        Delete a TXT record using the supplied information.

        Note that both the record's name and content are used to ensure that similar records
        created concurrently (e.g., due to concurrent invocations of this plugin) are not deleted.

        Failures are logged, but not raised.

        :param str domain_name: The domain to use to associate the record with.
        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :param str record_content: The record content (typically the challenge validation).
        """
        position = domain_name.find(self.root_domain)
        if position == -1:
            raise errors.PluginError('root domain ({0}) is not compatible with subdomain ({1})'
                                     .format(domain_name, self.root_domain))
        response = requests.delete('{0}/clean-validation-data'.format(self.endpoint_url),
                                   json={'subdomain': domain_name[:position - 1], 'data': record_content,
                                         'record_name': record_name},
                                   headers={'Authorization': 'Bearer {0}'.format(self.token)})
        if response.status_code != 200:
            raise errors.PluginError('validation data is not accepted by API')

        json = response.json()

        if not json['success']:
            raise errors.PluginError(json['message'])
