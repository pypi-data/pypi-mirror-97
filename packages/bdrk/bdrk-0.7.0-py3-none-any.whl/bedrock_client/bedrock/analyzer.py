import sys

from bdrk import model_analyzer  # noqa: F401 F403

# Creating alias for backward compatible calls
sys.modules["bedrock_client.bedrock.analyzer"] = model_analyzer
