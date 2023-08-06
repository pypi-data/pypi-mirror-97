import sys

from bdrk import model  # noqa: F401 F403

# Creating alias for backward compatible calls
sys.modules["bedrock_client.bedrock.model"] = model
