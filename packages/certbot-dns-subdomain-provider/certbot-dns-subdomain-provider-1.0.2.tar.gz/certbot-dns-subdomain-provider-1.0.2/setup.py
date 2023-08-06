import os
import sys

from setuptools import find_packages
from setuptools import setup

version = '1.0.2'

# Remember to update local-oldest-requirements.txt when changing the minimum
# acme/certbot version.
install_requires = [
    'setuptools>=39.0.1',
    'zope.interface',
    'requests'
]

if not os.environ.get('SNAP_BUILD'):
    install_requires.extend([
        'acme>=0.29.0',
        'certbot>=1.1.0',
    ])
elif 'bdist_wheel' in sys.argv[1:]:
    raise RuntimeError('Unset SNAP_BUILD when building wheels '
                       'to include certbot dependencies.')
if os.environ.get('SNAP_BUILD'):
    install_requires.append('packaging')

setup(
    name='certbot-dns-subdomain-provider',
    version=version,
    description="Subdomain Provider DNS Authenticator plugin for Certbot",
    url='https://github.com/tugrul/certbot-dns-subdomain-provider',
    author="Certbot Project",
    author_email='tugrultopuz@gmail.com',
    license='Apache License 2.0',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],

    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'certbot.plugins': [
            'dns-subdomain-provider = certbot_dns_subdomain_provider._internal.dns_subdomain_provider:Authenticator',
        ],
    },
)
