import logging
import math
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status, HTTPException, Depends
from sqlalchemy.future import select
from app.models import EmergencyContact
from app.schemas.emergency_contact import CreateEmergencyContact



logger = logging.getLogger(__name__)


class EmergencyContactService:

    @staticmethod
    async def create_emergency_contact(db:AsyncSession, emergency_contact_data:CreateEmergencyContact):
        try:
            existing_emergency_contact = await db.execute(
                select(EmergencyContact).where(EmergencyContact.phone == emergency_contact_data.phone)
            )

            existing_emergency_contact = existing_emergency_contact.scalars().first()

            if existing_emergency_contact:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Emergency Contact already exists",
                )

            new_emergency_contact = EmergencyContact(
                name=emergency_contact_data.name,
                address=emergency_contact_data.address,
                phone=emergency_contact_data.phone
            )

            db.add(new_emergency_contact)
            await db.commit()
            await db.refresh(new_emergency_contact)
            return new_emergency_contact

        except Exception as e:
            await db.rollback()
            logger.error(f"Emergency contact creation failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="This contact already exists !",
            )


    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:

        # Haversine formula

        R = 6371

        dlat = math.radians(lat2 - lat1) # Difference in latitude
        dlon = math.radians(lon2 - lon1) # Difference in longitude

        a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) * math.sin(dlon / 2))

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c

        return distance

    @staticmethod
    async def get_emergency_contact(
            db: AsyncSession,
            user_location: Optional[str] = None,
            user_lat: Optional[float] = None,
            user_lon: Optional[float] = None,
    ) -> List[EmergencyContact]:

        try:
            result = await db.execute(
                select(EmergencyContact)
            )
            emergency_contacts = result.scalars().all()

            if not emergency_contacts:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Emergency Contact not found",
                )

            # If no location provided, return all contacts
            if not user_location and (not user_lat or not user_lon):
                return list(emergency_contacts)

            if user_location:
                exact_matches = []
                partial_matches = []
                other_contacts = []

                user_location_lower = user_location.lower()

                for emergency_contact in emergency_contacts:
                    emergency_address_lower = emergency_contact.address.lower()

                    if emergency_address_lower == user_location_lower:
                        exact_matches.append(emergency_contact)
                    elif any(word in emergency_address_lower for word in user_location_lower.split()):
                        partial_matches.append(emergency_contact)
                    else:
                        other_contacts.append(emergency_contact)

                sorted_contacts = exact_matches + partial_matches + other_contacts
                return sorted_contacts

            elif user_lat and user_lon:
                contact_with_distance = []

                for emergency_contact in emergency_contacts:
                    if hasattr(emergency_contact, 'latitude') and hasattr(emergency_contact, 'longitude'):
                        if emergency_contact.latitude is not None and emergency_contact.longitude is not None:
                            distance = EmergencyContactService.calculate_distance(
                                user_lat, user_lon, emergency_contact.latitude, emergency_contact.longitude
                            )
                            contact_with_distance.append((emergency_contact, distance))
                        else:
                            contact_with_distance.append((emergency_contact, float("inf")))
                    else:
                        contact_with_distance.append((emergency_contact, float("inf")))

                contact_with_distance.sort(key=lambda x: x[1])
                return [contact for contact, distance in contact_with_distance]

            return list(emergency_contacts)

        except Exception as e:
            logger.error(f"Failed to get emergency contacts: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Cannot find the emergency contact",
            )