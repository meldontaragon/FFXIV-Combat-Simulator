"""
This code was taken from a comment in : https://github.com/IAmPythagoras/FFXIV-Combat-Simulator/issues/17
and was written by https://github.com/Alex-Ueki @apollo#3810
and modified to fit the use I have of it.
"""
# Installed versions I use
# coreapi==2.3.3
# coreapi-cli==1.0.9
import coreapi

from ffxivcalc.Constants import LevelConstants
from ffxivcalc.Jobs.PlayerEnum import JobEnum

# from ffxivcalc.Jobs.Stats import Stats


def get_gearset_data(set_id: str) -> dict:
    """
    Gets the gearset data (stats) via an id. Allows url too (handles it for free)
    set_id : str -> URL of the set from etro
    """
    # Handles urls by checking for webpage name and splitting
    cleaned_set_id = set_id.split("/")[-1] if "etro.gg/gearset" in set_id else set_id  # Cleans the URL
    client = coreapi.Client()
    data = client.action(
        client.get("https://etro.gg/api/docs/"),
        ["gearsets", "read"],
        params={
            "id": cleaned_set_id,
        },
    )

    # Since the first 8 data points are the stats. That's all we are interested in.
    # We will not use all of them since we will filter through. But this contains all we need

    stats = {data["totalParams"][i]["name"]: data["totalParams"][i]["value"] for i in range(len(data["totalParams"]))}

    constants = LevelConstants(int(data['level']))

    stats = {
        "Job": JobEnum(data["job"]),
        "Level": data['level'],
        "iLvlSync": data['itemLevelSync'],
        "partyBonus": data['partyBonus'],
        "MainStat": data["totalParams"][0]["value"],  # Always first value
        "WD": stats["Weapon Damage"] if "Weapon Damage" in stats.keys() else 0,
        "Vit": stats["VIT"] if "VIT" in stats.keys() else 0,
        "Det": stats["DET"] if "DET" in stats.keys() else constants.BaseMain,
        "Ten": stats["TEN"] if "TEN" in stats.keys() else constants.BaseSub,
        "Sps": stats["SPS"] if "SPS" in stats.keys() else constants.BaseSub,
        "Sks": stats["SKS"] if "SKS" in stats.keys() else constants.BaseSub,
        "Crit": stats["CRT"] if "CRT" in stats.keys() else constants.BaseSub,
        "DH": stats["DH"] if "DH" in stats.keys() else constants.BaseSub,
        "Pie": stats["PIE"] if "PIE" in stats.keys() else constants.BaseMain,
    }
    return stats
