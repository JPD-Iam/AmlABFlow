# plugin_manager.py
import os
import importlib
from plugins.base_plugin import BasePlugin

class PluginManager:
    def __init__(self, plugin_folder='plugins'):
        self.plugin_folder = plugin_folder
        self.plugins = {}

    def load_plugins(self):
        for filename in os.listdir(self.plugin_folder):
            if filename.endswith('_plugin.py'):
                module_name = filename[:-3]
                module = importlib.import_module(f"{self.plugin_folder}.{module_name}")
                for attribute_name in dir(module):
                    attribute = getattr(module, attribute_name)
                    if isinstance(attribute, type) and issubclass(attribute, BasePlugin) and attribute is not BasePlugin:
                        self.plugins[module_name] = attribute()

    def get_plugin(self, name):
        return self.plugins.get(name)
