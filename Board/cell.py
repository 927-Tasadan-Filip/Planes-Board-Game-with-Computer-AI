"""
@author: Tasadan Filip
"""

from dataclasses import dataclass


@dataclass
class Cell:
    line: int
    column: int
    status: any
    plane_id: int
