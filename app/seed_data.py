import os
import json
from app.database import db
from app.models import Partner, MultiPolygon
from app.database import partners_collection

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


async def seed_partners():
    with open(os.path.join(BASE_DIR, "app/pdvs.json")) as f:
        data = json.load(f)

    for partner_data in data:
        address = partner_data["address"]
        partner_data["address"] = address["coordinates"]
        partner_data["address_type"] = address["type"]
        partner = Partner(**partner_data)
        await partners_collection.insert_one(partner.dict(by_alias=True))
