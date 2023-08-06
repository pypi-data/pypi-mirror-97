import numpy as np
import subprocess
import logging

def listify(obj):
    # Make a list if not a list
    if isinstance(obj, list):
        return obj
    elif isinstance(obj, tuple):
        return list(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return [obj]


def list2str(li, elem_format):
    # Make a string that looks like the list ``li`` using %-specifying string 
    # ``elem_format`` for each element
    return "[" + ", ".join([elem_format % elem for elem in li]) + "]"


def subprocess_cmd(command):
    """Execute a (multi-line) shell command.

    Parameters
    ----------
    command : str
        Semicolon separated lines.
    """
    comm_lines = command.split(";")
    for line in comm_lines:
        comm_list = list(line.split())
        process = subprocess.run(
            comm_list, stdout=None, check=True, stdin=subprocess.DEVNULL
        )


def object_name(obj_list, obj, prefix=""):
    """Return a name for the object that is unique within the names in a
    given list. The optional prefix is to be used if object.name is None.
    """
    if obj.name is not None:
        prefix = obj.name

    name_list = [obj.name for obj in obj_list]
    count = 1
    name = prefix
    if obj.name is None:
        name += "_0"

    while name in name_list:
        name = prefix + "_" + str(count)
        count += 1

    return name