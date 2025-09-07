from fastapi import APIRouter, HTTPException, status
from typing import List
from models.contact import Contact
from services.contact_service import contact_service

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.get("/", response_model=List[Contact])
async def get_all_contacts():
    """Get all contacts"""
    contacts = await contact_service.get_all_contacts()
    return contacts

@router.get("/{contact_id}", response_model=Contact)
async def get_contact_by_id(contact_id: str):
    """Get a contact by ID"""
    contact = await contact_service.get_contact_by_id(contact_id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    return contact

@router.post("/", response_model=Contact, status_code=status.HTTP_201_CREATED)
async def create_contact(contact: Contact):
    """Create a new contact"""
    try:
        created_contact = await contact_service.create_contact(contact)
        return created_contact
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating contact: {str(e)}"
        )

@router.put("/{contact_id}", response_model=Contact)
async def update_contact(contact_id: str, contact: Contact):
    """Update a contact by ID"""
    updated_contact = await contact_service.update_contact(contact_id, contact)
    if not updated_contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    return updated_contact

@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: str):
    """Delete a contact by ID"""
    success = await contact_service.delete_contact(contact_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
