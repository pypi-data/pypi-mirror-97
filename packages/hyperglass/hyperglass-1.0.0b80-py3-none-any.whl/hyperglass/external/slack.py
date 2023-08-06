"""Session handler for Slack API."""

# Project
from hyperglass.log import log
from hyperglass.external._base import BaseExternal
from hyperglass.models.webhook import Webhook


class SlackHook(BaseExternal, name="Slack"):
    """Slack session handler."""

    def __init__(self, config):
        """Initialize external base class with Slack connection details."""

        super().__init__(base_url="https://hooks.slack.com", config=config, parse=False)

    async def send(self, query):
        """Send an incoming webhook to Slack."""

        payload = Webhook(**query)

        log.debug("Sending query data to Slack:\n{}", payload)

        return await self._apost(endpoint=self.config.host.path, data=payload.slack())
