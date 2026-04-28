# Created by vsuman
import os
from abc import ABC
from typing import Optional

from ..exceptions.environment_exceptions import MissingEnvironmentVariable


class BaseConfigurations(ABC):
    """Abstract class for defining base configuration."""

    def get_env(self, env_name: str, default: Optional[str] = None) -> str:
        """Gives Environment value for `env_name`.

        Args:
            env_name (str): get environment variable name

        Returns:
            (str): return environment variable value
        """
        env_value = os.getenv(env_name, default=default)
        if not env_value:
            raise MissingEnvironmentVariable(f"Environment Variable: {env_name} does not exist")
        return env_value
