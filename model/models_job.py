import uuid
from typing import Optional
from pydantic import BaseModel, Field


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

