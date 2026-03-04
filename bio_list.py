from typing import List
import csv

from models import Bio


def _clean(value: str | None) -> str | None:
    if value is None:
        return None
    v = value.strip()
    if not v:
        return None
    # remove surrounding quotes and trailing commas
    if v.startswith('"') and v.endswith('"'):
        v = v[1:-1]
    v = v.strip().strip('"')
    v = v.rstrip(',').strip()
    return v or None


def _to_int(value: str | None) -> int | None:
    v = _clean(value)
    if v is None:
        return None
    try:
        return int(v)
    except ValueError:
        return None


def load_bios(csv_path: str = "roster.csv") -> List[Bio]:
    """Parse `csv_path` and return a list of `Bio` instances.

    The CSV is expected to have headers: number,first_name,last_name,position,weight,height,hometown,class,high_school
    """
    bios: List[Bio] = []
    with open(csv_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            first_name = _clean(row.get("first_name"))
            last_name = _clean(row.get("last_name"))
            if not first_name or not last_name:
                continue

            bio = Bio(
                first_name=first_name,
                last_name=last_name,
                number=_to_int(row.get("number")),
                position=_clean(row.get("position")),
                height=_clean(row.get("height")),
                weight=_to_int(row.get("weight")),
                academic_class=_clean(row.get("class")),
                hometown=_clean(row.get("hometown")),
                high_school=_clean(row.get("high_school")),
            )
            bios.append(bio)
    return bios


__all__ = ["load_bios"]
