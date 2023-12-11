import uuid
from typing import Optional, List
from pydantic import BaseModel, Field

class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    company_name: str = Field(...)
    operator_full_name: str = Field(...)
    company_address: str = Field(...)
    company_postcode: str = Field(...)
    email: str = Field(...)
    job_ids: Optional[list] = Field(default=[])

    class Config:
        allow_population_by_field_name = True
        schema_extra = {}


class UserUpdate(BaseModel):
    company_name: Optional[str]
    operator_full_name: Optional[str]
    company_address: Optional[str]
    company_postcode: Optional[str]
    job_ids: Optional[list]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {}


class Job(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    job_title: str = Field(...)
    description: str = Field(...)
    skill_requirements: list = Field(...)
    custom_requirements: list = Field(...)
    candidates: Optional[list] = Field(default=[])

    class Config:
        allow_population_by_field_name = True
        schema_extra = {}


class JobUpdate(BaseModel):
    job_title: Optional[str]
    description: Optional[str]
    skill_requirements: Optional[list]
    custom_requirements: Optional[list]
    candidates: Optional[list]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {}
