from cassandra import ConsistencyLevel
from cassandra.cluster import ExecutionProfile
from cassandra.cluster import EXEC_PROFILE_DEFAULT
from cassandra.policies import RoundRobinPolicy

read = ExecutionProfile(
             consistency_level=ConsistencyLevel.ONE,
             load_balancing_policy=RoundRobinPolicy(),
             request_timeout=10,
     )

write = ExecutionProfile(
             consistency_level=ConsistencyLevel.LOCAL_QUORUM,
             load_balancing_policy=RoundRobinPolicy(),
             request_timeout=15,
     )

profile = write

default = {EXEC_PROFILE_DEFAULT: profile}

__all__ = ['default', 'read', 'write', 'profile']
