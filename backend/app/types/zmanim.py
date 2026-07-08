from enum import StrEnum
from typing import Literal

TimeMode = Literal["fixed", "zmanim"]


class ZmanRef(StrEnum):
    ALOT_HASHACHAR = "alot_hashachar"
    SUNRISE = "sunrise"
    SUNSET = "sunset"
    TZEIT = "tzeit"
    CHATZOT = "chatzot"


HEBCAL_FIELD_MAP: dict[ZmanRef, str] = {
    ZmanRef.ALOT_HASHACHAR: "alotHaShachar",
    ZmanRef.SUNRISE: "sunrise",
    ZmanRef.SUNSET: "sunset",
    ZmanRef.TZEIT: "tzeit",
    ZmanRef.CHATZOT: "chatzos",
}

ZMAN_REF_LABELS_HE: dict[ZmanRef, str] = {
    ZmanRef.ALOT_HASHACHAR: "עלות השחר",
    ZmanRef.SUNRISE: "זריחה",
    ZmanRef.SUNSET: "שקיעה",
    ZmanRef.TZEIT: "צאת הכוכבים",
    ZmanRef.CHATZOT: "חצות היום",
}
