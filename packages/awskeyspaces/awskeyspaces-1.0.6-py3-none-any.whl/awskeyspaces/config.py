import os

AMAZON_CA = f"{os.path.dirname(__file__)}/AmazonRootCA1.pem"
CLUSTER_HOST = os.getenv("CLUSTER_HOST", "127.0.0.1").split(",")
CLUSTER_PORT = int(os.getenv("CLUSTER_PORT", 9142))
CLUSTER_KSP  = os.getenv("CLUSTER_KSP")
_CLUSTER_USER = os.getenv("CLUSTER_USER")
_CLUSTER_PASS = os.getenv("CLUSTER_PASS")
