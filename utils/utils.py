from typing import Tuple
import base64
import struct

from simulation.heatmaps.heatmap import Heatmap


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


def heatmap_to_bytes(heatmap: Heatmap) -> bytes:
    """
    Converts a heatmap to a byte array
    :param heatmap: heatmap to convert
    :return: byte array
    """
    cell_count = heatmap.get_width() * heatmap.get_height()
    struct_fmt = 'II' + 'd' * cell_count
    return struct.pack(struct_fmt, heatmap.get_width(), heatmap.get_height(), *heatmap.cells)

def heatmap_to_base64(heatmap: Heatmap) -> str|None:
    """
    Converts a heatmap to a base64 string
    :param heatmap: heatmap to convert
    :return: base64 string
    """
    if heatmap is None:
        return None

    data = heatmap_to_bytes(heatmap)
    return base64.b64encode(data).decode()

def heatmap_from_bytes(data: bytes) -> Heatmap:
    """
    Converts a byte array to a heatmap
    :param data: byte array
    :return: heatmap
    """
    struct_fmt = '<I<I'
    header_size = struct.calcsize(struct_fmt)
    width, height = struct.unpack(struct_fmt, data[:header_size])
    cell_count = width * height
    struct_fmt += '<d' * cell_count
    cells = struct.unpack(struct_fmt, data[header_size:])
    heatmap = Heatmap(width, height)
    heatmap.cells = list(cells)
    return heatmap

def heatmap_from_base64(data: str) -> Heatmap:
    """
    Converts a base64 string to a heatmap
    :param data: base64 string
    :return: heatmap
    """
    decoded = base64.b64decode(data)
    return heatmap_from_bytes(decoded)