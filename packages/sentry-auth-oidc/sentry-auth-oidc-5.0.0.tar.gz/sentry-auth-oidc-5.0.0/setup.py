# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oidc']

package_data = \
{'': ['*'], 'oidc': ['templates/oidc/*']}

entry_points = \
{'sentry.apps': ['oidc = oidc.apps.Config']}

setup_kwargs = {
    'name': 'sentry-auth-oidc',
    'version': '5.0.0',
    'description': 'OpenID Connect authentication provider for Sentry',
    'long_description': 'OpenIDConnect Auth for Sentry\n=============================\n\nAn SSO provider for Sentry which enables `OpenID Connect <http://openid.net/connect/>`_ Apps authentication.\n\nThis is a fork of `sentry-auth-google <https://github.com/getsentry/sentry-auth-google/>`_.\n\nWhy fork, instead of adapting sentry-auth-google to work with every OpenID Connect provider?\n--------------------------------------------------------------------------------------------\nThe maintainer has different ideas with sentry-auth-google. See:\n\n* https://github.com/getsentry/sentry-auth-google/pull/29\n* https://github.com/getsentry/sentry/issues/5650\n\nInstall\n-------\n\n::\n\n    $ pip install sentry-auth-oidc\n\nExample Setup for Google\n------------------------\n\nStart by `creating a project in the Google Developers Console <https://console.developers.google.com>`_.\n\nIn the **Authorized redirect URIs** add the SSO endpoint for your installation::\n\n    https://sentry.example.com/auth/sso/\n\nNaturally other providers, that are supporting OpenID-Connect can also be used (like GitLab).\n\nFinally, obtain the API keys and the well-known account URL and plug them into your ``sentry.conf.py``:\n\n.. code-block:: python\n\n    OIDC_CLIENT_ID = ""\n\n    OIDC_CLIENT_SECRET = ""\n\n    OIDC_SCOPE = "openid email"\n\n    OIDC_DOMAIN = "https://accounts.google.com"  # e.g. for Google\n\nThe ``OIDC_DOMAIN`` defines where the OIDC configuration is going to be pulled from.\nBasically it specifies the OIDC server and adds the path ``.well-known/openid-configuration`` to it.\nThat\'s where different endpoint paths can be found.\n\nDetailed information can be found in the `ProviderConfig <https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderConfig>`_ specification.\n\nYou can also define ``OIDC_ISSUER`` to change the default provider name in the UI, even when the ``OIDC_DOMAIN`` is set.\n\nIf your provider doesn\'t support the ``OIDC_DOMAIN``, then you have to set these\nrequired endpoints by yourself (autorization_endpoint, token_endpoint, userinfo_endpoint, issuer).\n\n.. code-block:: python\n\n    OIDC_AUTHORIZATION_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"  # e.g. for Google\n\n    OIDC_TOKEN_ENDPOINT = "https://www.googleapis.com/oauth2/v4/token"  # e.g. for Google\n\n    OIDC_USERINFO_ENDPOINT = "https://www.googleapis.com/oauth2/v3/userinfo" # e.g. for Google\n\n    OIDC_ISSUER = "Google"\n',
    'author': 'Max Wittig',
    'author_email': 'max.wittig@siemens.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
