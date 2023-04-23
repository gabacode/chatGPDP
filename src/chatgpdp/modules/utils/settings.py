import os
from PyQt5.QtCore import QSettings, QStandardPaths


class Settings:
    def __init__(self):
        self._create_settings_dir()
        self._settings = self._create_settings()

    def _create_settings_dir(self):
        documents_path = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
        settings_dir = os.path.join(documents_path, "chatGPDP")
        os.makedirs(settings_dir, exist_ok=True)

    def _create_settings(self):
        settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "chatGPDP", "config")
        settings.setFallbacksEnabled(False)
        settings.setIniCodec("UTF-8")
        return settings

    def set_environ(self, key, value):
        os.environ.setdefault(key, value)

    def get_settings(self):
        return self._settings

    def get_setting_by_key(self, key):
        return self._settings.value(key) if self._settings.value(key) else ""
