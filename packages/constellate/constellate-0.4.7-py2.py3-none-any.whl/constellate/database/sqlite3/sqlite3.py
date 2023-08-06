from typing import Dict, Tuple, Callable


def register_functions(connection, functions: Dict[str, Tuple[int, Callable]] = {}):
    """
    Register custom functions
    """

    def _register(
        connection, function_name: str = "my_func", num_params: int = 0, function: Callable = None
    ):
        connection.create_function(function_name, num_params, function)

    for function_name, value in functions.items():
        _register(
            connection=connection,
            function_name=function_name,
            num_params=value[0],
            function=value[1],
        )


# str: function name
# int: number of parameters in the function
# Callable: Function implementation
Functions = Dict[str, Tuple[int, Callable]]


def patch_sqlite3_connect(original_connect, enable: bool = True, functions: Functions = {}):
    """Monkey patch sqlite.connect before any other library uses it with goal to register custom sql function.
    This monkey matching provides that
    :functions:
    - Key: Function name (like it would be called in a sql script)
    - Value: Tuple(Function Parameters Count, Method implementation)

    :enable: True to enable monkey patching

    :original_connect: See example below

    import _sqlite3
    import sqlite3

    sqlite3.connect = ...monkeypatch_sqlite3_connect_enable(_sqlite3.connect)
    """

    def connect_decorator(*args, **kwargs):
        connection = original_connect(*args, **kwargs)
        register_functions(connection=connection, functions=functions)
        return connection

    return connect_decorator
