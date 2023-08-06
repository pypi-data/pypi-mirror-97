from spell.api import base_client
from spell.api.utils import url_path_join

CONFIG_RESOURCE_URL = "config"


class ConfigClient(base_client.BaseClient):
    def get_trusted_cidrs(self):
        """Get cidrs for Spell services"""
        r = self.request("get", url_path_join(CONFIG_RESOURCE_URL, "cidrs"))
        self.check_and_raise(r)
        return self.get_json(r)["trusted_cidrs"]
