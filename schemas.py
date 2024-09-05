from pydantic import BaseModel, model_validator
from typing import Any, ClassVar


class ResumeInput(BaseModel):
    name: str = None
    email: str = None
    phone_number: str = None
    linkedin_profile: str = None
    github_profile: str = None
    experience: str = None
    projects: str = None
    education: str = None
    skills: str = None
    coursework: str = None
    certifications: str = None
    involvement: str = None
    summary: str = None
    target_job_title: str = None
    target_job_description: str = None
    required_fields: ClassVar[list[str]] = [
        "name",
        "email",
    ]
    
    @model_validator(mode = "before")
    @classmethod
    def validate_required(cls, data: Any) -> Any:
        # Check if data is a dict with required fields
        if isinstance(data, dict):
            for field in cls.required_fields:
                assert field in data, f"{field} is required"
        
        # Check if fields are empty strings
        for field in cls.required_fields:
            assert data[field] != "", f"{field} cannot be empty. Please enter a value for {field}"
        
        # Check if fields are strings
        for field in cls.required_fields:
            assert isinstance(data[field], str), f"{field} must be a string"
        
        return data