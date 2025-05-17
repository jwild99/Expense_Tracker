import json
import os
from . import terminal as tUtils

def exists(file_path: str) -> bool:
    return os.path.exists(file_path)

def open_json(file_path: str, mode: str) -> json:
    with open(file_path, mode) as file:
        return file
