import os
from PyQt5.QtCore import QSettings, QStandardPaths

from chatgpdp.modules.utils.config import DEFAULT_SETTINGS


class Settings:
    """
    This class handles the settings of the application
    """

    app_name = "chatGPDP"

    def __init__(self):
        self._settings = self._setup()
        self._load()

    def _setup(self):
        """
        Creates the config file if it doesn't exist and returns the QSettings object
        """
        documents_path = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
        settings_dir = os.path.join(documents_path, self.app_name)
        os.makedirs(settings_dir, exist_ok=True)

        settings = QSettings(QSettings.IniFormat, QSettings.UserScope, self.app_name, "config")
        settings.setFallbacksEnabled(False)
        settings.setIniCodec("UTF-8")
        return settings

    def _load(self):
        """
        Loads the saved settings from the config file, if present, otherwise sets default options
        """
        for key, value in DEFAULT_SETTINGS.items():
            if isinstance(value, dict):
                self._settings.beginGroup(key)
                for subkey, subvalue in value.items():
                    if isinstance(subvalue, dict):
                        for subsubkey, subsubvalue in subvalue.items():
                            actual_setting = self._settings.value(f"{subkey}/{subsubkey}", subsubvalue)
                            self._settings.setValue(f"{subkey}/{subsubkey}", actual_setting)
                    else:
                        actual_setting = self._settings.value(subkey, subvalue)
                        self._settings.setValue(subkey, actual_setting)

                self._settings.endGroup()
            else:
                actual_setting = self._settings.value(key, value)
                self._settings.setValue(key, actual_setting)

    def set_environ(self, key, value):
        """
        Sets the environment variable with the given key to the given value
        """
        os.environ.setdefault(key, value)

    def get(self):
        """
        Returns the QSettings
        """
        return self._settings

    def get_by_key(self, key):
        """
        Returns the value of the setting with the given key
        """
        return self._settings.value(key, "")
