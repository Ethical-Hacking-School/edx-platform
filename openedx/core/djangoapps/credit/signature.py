"""
Calculate digital signatures for messages sent to/from credit providers,
using a shared secret key.

The signature is calculated as follows:

    1) Encode all parameters of the request (except the signature) in a string.
    2) Encode each key/value pair as a string of the form "{key}:{value}".
    3) Concatenate key/value pairs in ascending alphabetical order by key.
    4) Calculate the HMAC-SHA256 digest of the encoded request parameters, using a 32-character shared secret key.
    5) Encode the digest in hexadecimal.

It is the responsibility of the credit provider to check the signature of messages
we send them, and it is our responsibility to check the signature of messages
we receive from the credit provider.

"""

from __future__ import absolute_import

import hashlib
import hmac
import logging

import six
from django.conf import settings

log = logging.getLogger(__name__)


def get_shared_secret_key(provider_id):
    """
    Retrieve the shared secret key for a particular credit provider.
    """
    secret = getattr(settings, "CREDIT_PROVIDER_SECRET_KEYS", {}).get(provider_id)

    if isinstance(secret, six.text_type):
        try:
            secret.encode('ascii')
        except UnicodeEncodeError:
            secret = None
            log.error(u'Shared secret key for credit provider "%s" contains non-ASCII unicode.', provider_id)

    return secret


def signature(params, shared_secret):
    """
    Calculate the digital signature for parameters using a shared secret.

    Arguments:
        params (dict): Parameters to sign.  Ignores the "signature" key if present.
        shared_secret (str): The shared secret string.

    Returns:
        str: The 32-character signature.

    """
    encoded_params = u"".join([
        u"{key}:{value}".format(key=key, value=params[key])
        for key in sorted(params.keys())
        if key != u"signature"
    ])
    hasher = hmac.new(shared_secret.encode('utf-8'), encoded_params.encode('utf-8'), hashlib.sha256)
    return hasher.hexdigest()
