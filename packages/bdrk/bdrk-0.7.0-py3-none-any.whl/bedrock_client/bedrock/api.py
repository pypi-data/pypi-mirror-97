import sys

from bdrk.tracking import client_old  # noqa: F401 F403

# Creating alias for backward compatible calls
sys.modules["bedrock_client.bedrock.api"] = client_old
