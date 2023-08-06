"""
    LABUNIX AWS KEYSPACES AUTH PROVIDER
"""
import os
from ssl import SSLContext, PROTOCOL_TLSv1_2, CERT_REQUIRED

from .config import AMAZON_CA, _CLUSTER_USER, _CLUSTER_PASS 

try:
    from cassandra_sigv4.auth import SigV4AuthProvider   
    _auth_provider = SigV4AuthProvider()
except:
    from cassandra.auth import PlainTextAuthProvider
    _auth_provider = PlainTextAuthProvider(
        username=_CLUSTER_USER,
        password=_CLUSTER_PASS,
    )

_CLUSTER_USER = None
_CLUSTER_PASS = None

_ssl_context = SSLContext(PROTOCOL_TLSv1_2)
_ssl_context.load_verify_locations(AMAZON_CA)
_ssl_context.verify_mode = CERT_REQUIRED

__all__ = ["_auth_provider", "_ssl_context"]
