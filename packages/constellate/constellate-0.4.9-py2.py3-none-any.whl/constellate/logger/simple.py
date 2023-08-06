import multiprocessing
from typing import Dict

from narration.narration import teardown_handlers

from constellate.logger.log import Log
from constellate.logger.logmode import LogMode
from constellate.logger.loggers import Loggers


def setup_any_process_loggers(
    root_logger_name="unnamped",
    log_dir_path: str = None,
    mode: LogMode = None,
    config_dict: Dict = None,
    template_dict: Dict = None,
):
    """
    Setup constant applying to all loggers
    """
    kwargs = {}
    if root_logger_name is not None:
        kwargs.update(root_logger_name=root_logger_name)
    if log_dir_path is not None:
        kwargs.update(log_dir_path=log_dir_path)
    if mode is not None:
        kwargs.update(mode=mode)

    if config_dict is not None and template_dict is not None:
        raise ValueError(
            "config_dict and template_dict cannot be set together. It is one of them only, or none"
        )
    elif config_dict is not None:
        kwargs.update(config_dict=config_dict)
    elif template_dict is not None:
        kwargs.update(template_config_dict=template_dict)

    Log.setup(**kwargs)


def setup_standalone_process_loggers() -> Loggers:
    """
    Setup loggers for an project (no logging to be shared with child processes , if any)
    """
    mode_settings = {}
    return Log.loggers(mode=LogMode.OPERATE_STANDALONE, mode_settings=mode_settings)


def setup_main_process_loggers(ctx=multiprocessing.get_context()) -> Loggers:
    """
    Setup loggers in "server mode" for an project's main process
    """
    mode_settings = {"ctx": ctx, "ctx_manager": ctx.Manager()}
    return Log.loggers(
        mode=LogMode.OPERATE_SERVER
        | LogMode.OPERATE_SERVER_OPTION_DEFAULT
        | LogMode.DISPATCH_ASYNC,
        mode_settings=mode_settings,
    )


def setup_child_process_loggers(mode_settings: Loggers = Loggers()) -> Loggers:
    """
    Setup loggers in "client" mode for an project's child process (ie forked, spawn, etc)
    """

    kwargs = {}
    if mode_settings is not None:
        kwargs.update(mode_settings=mode_settings)
    return Log.loggers(mode=LogMode.OPERATE_CLIENT, **kwargs)


def teardown_loggers(loggers: Loggers = None, timeout=None):
    native_loggers = loggers.native_loggers() if loggers is not None else []
    teardown_handlers(loggers=native_loggers, timeout=timeout)
    "Free/Remove all loggers setup previously"
    Log.teardown_loggers(loggers=native_loggers)
