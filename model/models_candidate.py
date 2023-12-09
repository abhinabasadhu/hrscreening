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


class Job(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    company_name: str = Field(...)
    description: str = Field(...)
    company_address: str = Field(...)
    skill_requirement: list = Field(...)
    custom_requirements: list = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {}


class JobUpdate(BaseModel):
    company_name: Optional[str]
    description: Optional[str]
    company_address: Optional[str]
    skill_requirement: Optional[list]
    custom_requirements: Optional[list]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {}
