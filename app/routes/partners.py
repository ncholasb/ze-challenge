import base64
import io
from typing import List
import folium
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from app.database import partners_collection
from app.models import Partner

router = APIRouter()


def convert_objectid_to_str(obj):
    if isinstance(obj, list):
        return [convert_objectid_to_str(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_objectid_to_str(value) for key, value in obj.items()}
    elif isinstance(obj, ObjectId):
        return str(obj)
    else:
        return obj


@router.get("/", response_model=List[Partner])
async def read_partners(skip: int = 0, limit: int = 100):
    partners = []
    async for partner in partners_collection.find().skip(skip).limit(limit):
        partner_obj = Partner(**partner)
        partner_obj.id = int(partner['id'])
        partners.append(partner_obj)
    return partners


async def get_partner_by_id(partner_id: int, partners_collection):
    partner = await partners_collection.find_one({"id": int(partner_id)})
    if partner:
        partner = convert_objectid_to_str(partner)
        partner['id'] = str(partner['id'])
        return partner
    else:
        raise HTTPException(status_code=404, detail="Partner not found")


@router.get("/{partner_id}")
async def get_partner(partner_id: int):
    partner = await get_partner_by_id(int(partner_id), partners_collection)
    if partner:
        return partner
    else:
        raise HTTPException(status_code=404, detail="Partner not found")


@router.post("/", response_model=Partner)
async def create_partner(partner: Partner):
    partner_dict = partner.dict()
    result = await partners_collection.insert_one(partner_dict)
    partner_dict["_id"] = str(result.inserted_id)
    partner = Partner.parse_obj(partner_dict)
    return partner


@router.put("/{partner_id}", response_model=Partner)
async def update_partner(partner_id: int, partner: Partner):
    partner_id = int(partner_id)
    partner_dict = partner.dict(exclude_unset=True)
    result = await partners_collection.update_one(
        {"id": int(partner_id)},
        {"$set": partner_dict}
    )
    if result.modified_count == 1:
        if updated_partner := await partners_collection.find_one({"id": int(partner_id)}):
            return Partner(**updated_partner)
    if existing_partner := await partners_collection.find_one({"id": int(partner_id)}):
        existing_partner["id"] = int(existing_partner["id"])
        return Partner(**existing_partner)
    raise HTTPException(status_code=404, detail="Partner not found")


@router.delete("/{partner_id}")
async def delete_partner(partner_id: int):
    result = await partners_collection.delete_one(
        {"id": int(partner_id)}
    )
    if result.deleted_count == 1:
        return {"success": True}
    raise HTTPException(status_code=404, detail="Partner not found")


@router.get("/partner_coverage/")
async def get_partner_coverage(latitude: float = Query(...), longitude: float = Query(...)):
    m = folium.Map(location=[latitude, longitude], zoom_start=16)

    folium.Marker([latitude, longitude]).add_to(m)
    img_data = io.BytesIO()
    m.save(img_data, close_file=False)
    img_data.seek(0)

    # Converta a imagem em bytes para uma string base64
    img_base64 = base64.b64encode(img_data.getvalue()).decode()

    # Retorne a imagem como uma resposta de streaming
    return StreamingResponse(io.BytesIO(base64.b64decode(img_base64)), media_type="image/png")
