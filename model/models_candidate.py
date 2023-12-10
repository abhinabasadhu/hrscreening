import uuid
from typing import Optional
from pydantic import BaseModel, Field


class Candidate(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    full_name: str = Field(...)
    dob: str = Field(...)
    contact_number: str = Field(...)
    address: str = Field(...)
    postcode: str = Field()
    skills: list = Field(...)
    education: list = Field(...)
    experience: list = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {}


class CandidateUpdate(BaseModel):
    full_name: Optional[str]
    dob: Optional[str]
    contact_number: Optional[str]
    address: Optional[str]
    postcode: Optional[str]
    skills: Optional[list]
    education: Optional[list]
    experience: Optional[list]

    class Config:
        schema_extra = {}