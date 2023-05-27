import collections
import os

import yaml


class Config(collections.UserDict):
    def __init__(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        data = yaml.load(
            open(os.path.join(current_dir, "config.yaml")), Loader=yaml.FullLoader
        )
        for key in data.keys():
            self._replace_env_vars(data[key])
            self.__setattr__(key, data[key])

    def _replace_env_vars(self, data: dict) -> None:
        """
        Replaces $ prefixes with env variable. Returns value by pointer.
        """

        for key, value in data.items():
            if isinstance(value, str) and len(value) > 0 and value[0] == "$":
                value_parts = value.split(",")

                env_key = value_parts[0].strip()[1:]
                if len(value_parts) > 1:
                    default_value = value_parts[1].strip()
                    data[key] = os.environ.get(env_key, default_value)
                else:
                    data[key] = os.environ[env_key]

    def __getattr__(self, attr):
        """
        Fallback function for missing attributes
        """

        return ""
