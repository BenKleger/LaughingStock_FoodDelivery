from pathlib import Path
import json, os
from typing import List, Dict, Any

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "menus.json"

def load_all() -> List[Dict[str, Any]]:
    """
    Loads all menus from the JSON data file containing all menus.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing stored items.
        [] Empty list if the data file doesnt exist.
    """
    if not DATA_PATH.exists():
        return []
    with DATA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_all(items: List[Dict[str, Any]]) -> None:
    """
    Saves all items to JSON data file.

    JSON file contents gets override with updated data upon save to prevent data corruption
    """
    tmp = DATA_PATH.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    os.replace(tmp, DATA_PATH)