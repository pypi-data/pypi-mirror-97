import sys
from typing import List


def debugger_setup(enabled: bool = False, host: str = "host.docker.internal", port: int = 4444):
    if enabled is True:
        try:
            sys.path.append("pydevd-pycharm.egg")
            import pydevd_pycharm
        except BaseException:
            print(
                "ERROR: PyCharm's remote debugging library not installed: "
                " - pydevd-pycharm~=202.7660.27; sys.platform=='linux'"
            )
            raise

        pydevd_pycharm.settrace(
            host, port=port, stdoutToServer=True, stderrToServer=True, suspend=False
        )


def debugger_setup_stage(stage: str = None, enabled_stages: List[str] = []):
    """
    Enable remote debugger if the current stage is one of the enabled stages
    """
    debugger_setup(enabled=stage in enabled_stages)
