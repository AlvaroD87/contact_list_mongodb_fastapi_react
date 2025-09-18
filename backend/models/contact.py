from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId  # pyright: ignore[reportMissingImports]
from pydantic import ConfigDict

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")
        return field_schema

class Contact(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str
    primary_surname: str
    secondary_surname: str
    phone: str
    email: str
    notes: str


    model_config = ConfigDict(
        populate_by_name = True,
        arbitrary_types_allowed = True,
        json_encoders = {ObjectId: str}
    )

    def to_dict(self):
        return {
            "_id": str(self.id) if self.id else None,
            "name": self.name,
            "primary_surname": self.primary_surname,
            "secondary_surname": self.secondary_surname,
            "phone": self.phone,
            "email": self.email,
            "notes": self.notes
        }