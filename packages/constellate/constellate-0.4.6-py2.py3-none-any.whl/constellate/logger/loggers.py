from typing import Dict, List


class Loggers:
    def __init__(self):
        self._logger_settings_property_names = set()
        self._logger_property_names = {}

    def setup_logger(self, parts: List[str] = None, logger=None, settings: Dict = None):
        """
        Once populated with name 'foobar':
         - Loggers().foobar and Loggers().foobar_settings will exists
        Once populated with name 'foobar.test':
         - Loggers().foobar.test and Loggers().foobar_test_settings will exists
        """
        if parts is None or len(parts) <= 1:
            return

        count = len(parts) + 1
        parent = self
        for part_index in range(1, count):
            is_first = part_index == 1
            is_last = part_index == count - 1

            selected_parts = parts[1:part_index]

            if len(selected_parts) == 0:
                continue

            short_name = selected_parts[-1]
            long_name = "_".join(selected_parts)

            if is_last:
                if logger is not None:
                    self._set_property_logger(parent, short_name, long_name, logger)
                if settings is not None:
                    key = self._get_logger_setting_property_name(long_name)
                    self._set_property_settings(key, settings)
            elif is_first:
                parent = self
            else:
                parent = self._get_property(parent, short_name, None)

    def _set_property_logger(self, obj, short_name, long_name, value):
        self._set_property(obj, short_name, value)
        self._logger_property_names.update({long_name: value})

    def _set_property_settings(self, name, value):
        self._set_property(self, name, value)
        self._logger_settings_property_names.add(name)

    def _get_logger_setting_property_name(self, name):
        return f"{name}_settings"

    def _get_settings(self, parts: List[str]):
        long_name = "_".join(parts)
        key = self._get_logger_setting_property_name(long_name)
        return self._get_property(self, key, None)

    def _get_property(self, obj, key, default_value):
        return obj.__dict__.get(key, default_value)

    def _set_property(self, obj, key, value):
        obj.__dict__[key] = value

    def settings(self):
        loggers = Loggers()
        for name in self._logger_settings_property_names:
            value_settings = self._get_property(self, name, None)
            loggers._set_property_settings(name, value_settings)
        for long_name in list(self._logger_property_names.keys()):
            short_name = long_name.split("_")[-1]
            loggers._set_property_logger(loggers, short_name, long_name, None)
        return loggers

    def native_loggers(self):
        return list(
            filter(
                None,
                [logger for logger in list(self._logger_property_names.values())],
            )
        )
