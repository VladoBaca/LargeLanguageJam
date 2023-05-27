import logging

logger = logging.getLogger(__name__)


class OpenAIAPI:

    def __init__(self, config):
        pass

    def _get_headers(self):
        return {
            "Authorization": self.token,
            "X-Requested-With": "XMLHttpRequest",
        }
