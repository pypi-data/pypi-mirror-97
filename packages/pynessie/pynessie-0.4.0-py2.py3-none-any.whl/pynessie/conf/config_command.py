# -*- coding: utf-8 -*-
"""Execute config command from cli."""
from typing import cast
from typing import Optional
from typing import Union

import click
import confuse

from .config_parser import build_config
from .io import write_to_file


def process(
    get_op: Optional[str],
    add_op: Optional[str],
    list_op: bool,
    unset_op: Optional[str],
    key: Optional[str],
    type_str: Optional[str] = "str",
) -> str:
    """Perform nessie config operations."""
    if (get_op or list_op or unset_op) and key:
        raise click.UsageError("can't set argument and specify option flags")
    if get_op or (key and not add_op):
        if not key and not get_op:
            raise click.UsageError("to show a key either the --get option or an argument must be supplied")
        config = _get_key(cast(str, get_op or key))
        return str(config.get(_get_type(type_str)))
    if add_op:
        config = build_config()
        config.set_args({add_op: _set_type(cast(str, key), type_str)}, dots=True)
        write_to_file(config)
        return ""
    if unset_op:
        config = build_config()
        for k in unset_op.split("."):
            config = config[k]
        config.set(None)
        write_to_file(config.root())
        return ""
    if list_op:
        config = build_config()
        return config.dump(redact=True)
    raise click.UsageError("no options set for config")


def _get_type(type_str: Optional[str]) -> type:
    if type_str == "bool":
        return bool
    elif type_str == "int":
        return int
    else:
        return str


def _set_type(key: str, type_str: Optional[str]) -> Union[bool, int, str]:
    if type_str == "bool":
        return key.lower() in {"true", "1", "t", "y", "yes", "yeah", "yup", "certainly", "uh-huh"}
    elif type_str == "int":
        return int(key)
    else:
        return key


def _get_key(key: str) -> confuse.Configuration:
    config = build_config()
    for i in key.split("."):
        if not i:
            continue
        config = config[i]
    return config
