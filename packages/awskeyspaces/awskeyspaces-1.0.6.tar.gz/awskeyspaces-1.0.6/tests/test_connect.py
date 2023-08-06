from datetime import datetime
import uuid

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from awskeyspaces.util import *


class TestModelA(Model):
    uid = columns.UUID(primary_key=True, default=uuid.uuid4)
    name = columns.Text()
    age = columns.TinyInt()
    enabled = columns.Boolean()
    created_at = columns.DateTime(default=datetime.utcnow)


def test_migrate():
    assert migrate(TestModelA) == None

# def test_proxydb():
#    assert proxydb() == True

# def test_run_migrate():
#    asser run_migrate() == True 
