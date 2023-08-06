from typing import Optional, List

from openmodule.models.base import OpenModuleModel


def _truncate(x):
    if len(x) > 10:
        return x[:10] + "..."
    else:
        return x


class Medium(OpenModuleModel):
    id: str
    type: str

    def __str__(self):
        return f"{self.type}:{_truncate(self.id)}"


class LPRCountry(OpenModuleModel):
    code: str
    state: str = ""
    confidence: float = 1


class LPRAlternative(OpenModuleModel):
    confidence: float
    plate: str


class LPRMedium(Medium):
    type: str = "lpr"
    country: LPRCountry = LPRCountry(code="OTHER")
    confidence: float = 1
    alternatives: List[LPRAlternative] = []

    def __str__(self):
        return f"{self.type}:[{self.country.code}]{_truncate(self.id)}"


class Vehicle(OpenModuleModel):
    id: int
    lpr: Optional[LPRMedium]
    qr: Optional[Medium]
    nfc: Optional[Medium]
    pin: Optional[Medium]

    def __str__(self):
        media = ", ".join(str(x) for x in [self.lpr, self.qr, self.nfc] if x)
        return f"Vehicle<id:{str(self.id)[-7:]}, {media}>"
