#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import warnings
import os


warnings.filterwarnings(
    'always', module="dli"
)

warnings.filterwarnings(
    'ignore', module="dli", category=ResourceWarning
)

warnings.filterwarnings(
    action='ignore',
    category=FutureWarning,
    message='^pandas.util.testing is deprecated'
)

__version__ = '1.13.0'
__product__ = "ihsm-datalake"


try:
    import simplejson as _  # noqa
    warnings.warn(
        'Incompatible Package `simplejson`.\n\n'
        '\t`simplejson` is a backport of the built in json library in Python. '
        'It contains subtle differences, and is not intended for use beyond '
        'Python 2.6. Please uninstall `simplejson` by running:\n\n'
        '\t\tpip uninstall simplejson\n\n'
        '\tOr run the DLI from a virtual environment as it is known to cause '
        'issues within the DLI.\n',
        ImportWarning
    )
except ImportError:
    pass


def connect(
    api_key=None,
    root_url="https://catalogue.datalake.ihsmarkit.com/__api",
    host=None,
    debug=None,
    strict=True,
    use_keyring=True,
    log_level=None,
):
    """
    Entry point for the Data Lake SDK, returns a client instance that
    can be used to consume or register datasets.

    Example for starting a session:


    .. code:: python

        import dli
        client = client.connect()

    :param str api_key: Your API key, can be retrieved from your dashboard in
                        the Catalogue UI.
    :param str root_url: Optional. The environment you want to point to. By default it
                        points to Production.
    :param str host: Optional. Advanced usage, meant to force a hostname when DNS resolution
                     is not reacheable from the user's network.
                     This is meant to be used in conjunction with an
                     IP address as the root url.
                     Example: catalogue.datalake.ihsmarkit.com

    :param bool debug: Optional. Log SDK operations to a file in the current working
                       directory with the format "sdk-{end of api key}-{timestamp}.log"

    :param bool strict: Optional. When True, all exception messages and stack
                        trace are printed. When False, a shorter message is
                        printed and `None` should be returned.
    :param bool use_keyring: Optional. When True, cache the JWT in the system keyring
                             and retrieve that JWT from the system keyring if set.
                             Otherwise disable the keyring completely.

    :returns: Data Lake interface client
    :rtype: dli.client.dli_client.DliClient

    .. deprecated:: 1.8.3

        `api_key`: please use the basic flow or client credentials.

    """
    from dli.client.session import _start_session

    return _start_session(
        api_key,
        root_url=root_url,
        host=host,
        debug=debug,
        strict=strict,
        use_keyring=use_keyring,
        log_level=log_level,
    )

