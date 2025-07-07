from typing import Optional, List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.db.session import get_db
from app.schemas.emergency_contact import CreateEmergencyContact, ReadEmergencyContact
from app.services.emergency_contact import EmergencyContactService



router = APIRouter(prefix="/emergency_contact", tags=["emergency_contact"])



@router.post("/create", response_model=CreateEmergencyContact, status_code=status.HTTP_201_CREATED)
async def create_emergency_contact(emergency_contact_data: CreateEmergencyContact, db: AsyncSession = Depends(get_db)):
    new_emergency_contact = await EmergencyContactService.create_emergency_contact(db, emergency_contact_data)
    return ReadEmergencyContact.model_validate(new_emergency_contact)


@router.get("/", response_model=List[ReadEmergencyContact])
async def get_emergency_contacts(
        user_location: Optional[str] = None,
        user_lat: Optional[float] = None,
        user_lon: Optional[float] = None,
        db: AsyncSession = Depends(get_db)
):
    all_contacts = await EmergencyContactService.get_emergency_contact(
        db, user_location, user_lat, user_lon
    )

    # Fixed: Validate each contact individually, not the whole list
    return [ReadEmergencyContact.model_validate(contact) for contact in all_contacts]







