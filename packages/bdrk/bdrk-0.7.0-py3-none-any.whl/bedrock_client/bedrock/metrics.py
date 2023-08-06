import sys

from bdrk import monitoring  # noqa: F401 F403

# Creating alias for backward compatible calls
sys.modules["bedrock_client.bedrock.metrics"] = monitoring
