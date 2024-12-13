from typing import Tuple


def get_none_fields(**kwargs) -> list:
    return [k for k, v in kwargs.items() if v is None]

def if_all_or_none(*args) -> bool:
    """
    Check if all or none of the arguments are None
    :param args:
    :return:
    """
    return all(x is None for x in args) or all(x is not None for x in args)

def none_check(**kwargs) -> Tuple[bool, list[str]]:
    """
    Check if all or none of the arguments are None
    :param args: the arguments to check
    :return: if all or none of the arguments are None, list of fields that are None
    """
    none_fields = get_none_fields(**kwargs)
    return if_all_or_none(*kwargs.values()), none_fields