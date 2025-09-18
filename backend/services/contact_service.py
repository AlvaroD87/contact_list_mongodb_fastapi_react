from typing import List, Optional
from bson import ObjectId  # pyright: ignore[reportMissingImports]
from backend.database import get_database
from backend.models.contact import Contact

class ContactService:
    def __init__(self):
        self.collection_name = "contacts"
    
    def get_collection(self):
        """Get the contacts collection"""
        db = get_database()
        return db[self.collection_name]
    
    async def create_contact(self, contact: Contact) -> Contact:
        """Create a new contact"""
        collection = self.get_collection()
        contact_dict = contact.to_dict()
        # Remove the _id if it exists to let MongoDB generate a new one
        if "_id" in contact_dict:
            del contact_dict["_id"]
        
        result = await collection.insert_one(contact_dict)
        contact.id = result.inserted_id
        return contact
    
    async def get_contact_by_id(self, contact_id: str) -> Optional[Contact]:
        """Get a contact by ID"""
        collection = self.get_collection()
        try:
            contact_doc = await collection.find_one({"_id": ObjectId(contact_id)})
            if contact_doc:
                return Contact(**contact_doc)
            return None
        except Exception:
            return None
    
    async def get_all_contacts(self) -> List[Contact]:
        """Get all contacts"""
        collection = self.get_collection()
        contacts = []
        async for contact_doc in collection.find():
            contacts.append(Contact(**contact_doc))
        return contacts
    
    async def update_contact(self, contact_id: str, contact: Contact) -> Optional[Contact]:
        """Update a contact by ID"""
        collection = self.get_collection()
        try:
            contact_dict = contact.to_dict()
            # Remove the _id to avoid conflicts
            if "_id" in contact_dict:
                del contact_dict["_id"]
            
            result = await collection.update_one(
                {"_id": ObjectId(contact_id)},
                {"$set": contact_dict}
            )
            
            if result.modified_count > 0:
                return await self.get_contact_by_id(contact_id)
            return None
        except Exception:
            return None
    
    async def delete_contact(self, contact_id: str) -> bool:
        """Delete a contact by ID"""
        collection = self.get_collection()
        try:
            result = await collection.delete_one({"_id": ObjectId(contact_id)})
            return result.deleted_count > 0
        except Exception:
            return False

    async def get_contact_by_name_like(self, c_name: str) -> List[Contact]:
        collection = self.get_collection()

        try:
            list_contact_doc = await collection.find({"name": {"$regex": c_name, "$options": "i"}})
            list_return = [Contact(**c) for c in list_contact_doc]
            return list_return
        except Exception:
            None
    
# Create a singleton instance
contact_service = ContactService()
