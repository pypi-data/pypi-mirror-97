r"""A module for data visualization."""

from typing import Optional

def print_tr(data: dict, offset: Optional[int]=1) -> None:
    r"""Triverse entire dictionary.

    Parameters
    ==========
    data: dict
        The data wanted to be triversed.
    offset: Optional[int], default: 1
        The offset for the indentation when displaying.
    """
    if data is None: return None

    if type(data) is dict:
        for key, val in data.items():
            if val is None:
                print(f"{' '*offset*4}{key}: None")
            elif type(val) is list:
                print(f"{' '*offset*4}{key}: (List)")
                print_tr(val, offset+1)
            elif type(val) is dict:
                print(f"{' '*offset*4}{key}: (Dict)")
                print_tr(val, offset+1)
            else:
                print(f"{' '*offset*4}{key}: {val}")

    elif type(data) is list:
        for ele in data:
            print_tr(ele, offset)

    else:
        print(f"{'    '*offset}- {data}")
