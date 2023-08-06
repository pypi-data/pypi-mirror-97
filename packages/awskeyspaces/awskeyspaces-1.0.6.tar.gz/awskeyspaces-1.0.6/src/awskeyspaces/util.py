#!/usr/bin/env/ python
"""
    AWS KEYSPACE CONNECTOR UTIL
"""
from datetime import date, datetime, time
import json
import logging
import os
import uuid

import cassandra
from cassandra.cqlengine import management
from cassandra.cqlengine.models import Model
from cassandra.util import Date

from .connection import connect


__all__ = ["migrate", "run_migrate", "create_ksp", "proxydb", "cassandra2json"]
_models_to_migrate = set()


def migrate(cls):
    """
    # add tables for sync
    migrate(ModelA)
    """
    _models_to_migrate.add(cls)


@connect
def run_migrate():
    """
    migrate(ModelA)
    migrate(ModelB)

    run_migrate()
    # connect once
    """
    os.environ["CQLENG_ALLOW_SCHEMA_MANAGEMENT"] = "1"
    for model in _models_to_migrate:
        try:
            management.sync_table(model, keyspaces=[os.getenv("CLUSTER_KSP")])
            logging.info(f"{model.__table_name__} table successfully synchronized.")
        except KeyError as e:
            logging.warning(f"table creation {e} has started, please wait a minute.")
        except cassandra.InvalidRequest as e:
            logging.warning(e)
            logging.warning(f"the {model.__table_name__} is not ready yet, please wait a minute.")


@connect
def create_ksp(keyspace=None):
    if (ksp := keyspace) is None:
        ksp = os.getenv("CLUSTER_KSP")

    os.environ["CQLENG_ALLOW_SCHEMA_MANAGEMENT"] = "1"
    management.create_keyspace_simple(ksp, 1)
    logging.info(f"the keyspace {ksp} was created.")


@connect
def proxydb():
    """
    initialize connection with cassandra
    """
    return True


class CassandraJsonEncoder(json.JSONEncoder):
    """ Parser Cassandra Object to Json """
    def default(self, obj):
        if issubclass(obj.__class__, Model):
            return dict(obj)
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, (set, tuple)):
            return list(obj)
        if isinstance(obj, (date, Date, datetime, time)):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def cassandra2json(obj):
    """ Convert a cassandra parsed model to json """
    return json.dumps(obj, cls=CassandraJsonEncoder)

