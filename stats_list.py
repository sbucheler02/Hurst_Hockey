from typing import List
import csv

from models import Stats


def _clean(value: str | None) -> str | None:
    if value is None:
        return None
    v = value.strip()
    if not v:
        return None
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


def _to_float(value: str | None) -> float | None:
    v = _clean(value)
    if v is None:
        return None
    try:
        return float(v)
    except ValueError:
        return None


def load_stats(csv_path: str = "stats.csv") -> List[Stats]:
    """Parse `csv_path` and return a list of `Stats` instances.

    Expected headers: Number,First_Name,Last_Name,GP,G,A,PTS,SH,SH_PCT,Plus_Minus,PPG,SHG,FG,GWG,GTG,OTG,HTG,UAG,PN-PIM,MIN,MAJ,OTH,BLK
    """
    stats_list: List[Stats] = []
    with open(csv_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            first_name = _clean(row.get("First_Name") or row.get("First_Name"))
            last_name = _clean(row.get("Last_Name") or row.get("Last_Name"))
            if not first_name or not last_name:
                continue

            stat = Stats(
                number=_to_int(row.get("Number") or row.get("number")),
                first_name=first_name,
                last_name=last_name,
                GP=_to_int(row.get("GP")),
                G=_to_int(row.get("G")),
                A=_to_int(row.get("A")),
                PTS=_to_int(row.get("PTS")),
                SH=_to_int(row.get("SH")),
                SH_PCT=_to_float(row.get("SH_PCT")),
                PLUS_MINUS=_to_int(row.get("Plus_Minus") or row.get("PLUS_MINUS") or row.get("Plus-Minus")),
                PPG=_to_int(row.get("PPG")),
                SHG=_to_int(row.get("SHG")),
                FG=_to_int(row.get("FG")),
                GWG=_to_int(row.get("GWG")) or _to_int(row.get("GWG")),
                GTG=_to_int(row.get("GTG")),
                OTG=_to_int(row.get("OTG")),
                HTG=_to_int(row.get("HTG")),
                UAG=_to_int(row.get("UAG")),
                PN_PIM=_clean(row.get("PN-PIM") or row.get("PN_PIM")),
                MIN=_to_int(row.get("MIN")),
                MAJ=_to_int(row.get("MAJ")),
                OTH=_to_int(row.get("OTH")),
                BLK=_to_int(row.get("BLK")),
            )
            stats_list.append(stat)

    return stats_list


__all__ = ["load_stats"]
