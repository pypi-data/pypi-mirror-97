#!/usr/bin/env/ python
"""
    LABUNIX AWS KEYSPACES CONNECTOR
"""
from functools import wraps
import os

from cassandra import ConsistencyLevel
from cassandra.cqlengine import connection
from cassandra.io.libevreactor import LibevConnection
from cassandra.policies import ExponentialReconnectionPolicy

from .auth import _auth_provider, _ssl_context
from .config import CLUSTER_HOST, CLUSTER_PORT, CLUSTER_KSP
from .profile import default


__all__ = ["connection", "get_session"]


def connect(orig_function):
    """
    Decorator  connect to aws keypaces

    @connect
    def ....():
    """

    @wraps(orig_function)
    def wrapper(*args, **kwargs):
        connection.setup(
            hosts=CLUSTER_HOST,
            ssl_context=_ssl_context,
            auth_provider=_auth_provider,
            port=CLUSTER_PORT,
            idle_heartbeat_interval=5,
            idle_heartbeat_timeout=10,
            reconnection_policy=ExponentialReconnectionPolicy(
                1.0, 
                900.0, 
                max_attempts=None
            ),
            default_keyspace=CLUSTER_KSP,
            protocol_version=4,
            lazy_connect=False,
            retry_connect=True,
            control_connection_timeout=30,
            connect_timeout=30,
            execution_profiles=default,
            consistency=ConsistencyLevel.LOCAL_QUORUM,
            connection_class=LibevConnection,
        )
        return orig_function(*args, **kwargs)

    return wrapper


@connect
def get_session(name="default", keyspace=None):
    _session = connection.get_session(name)
    if keyspace:
        _session.set_keyspace(keyspace)
    return _session
