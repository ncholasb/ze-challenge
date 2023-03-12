from pydantic import BaseModel
from typing import List, Tuple


class Point(BaseModel):
    type: str = "Point"
    coordinates: Tuple[float, float]


class PartnerCoverage(BaseModel):
    coordinates: List[List[List[float]]]
    type: str


class Partner(BaseModel):
    id: str
    tradingName: str
    ownerName: str
    document: str
    coverageArea: PartnerCoverage
    address: dict

    # validator document
