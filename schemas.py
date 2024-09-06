from pydantic import BaseModel, model_validator, HttpUrl, EmailStr
from typing import Any, ClassVar, Optional, List


class ResumeInput(BaseModel):
    """
    A pydantic model for the data ingestion for the resume builder. Includes a required fields list for validation as non-empty strings.
    """
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


class ContactInfo(BaseModel):
    location: str
    phone_number: str
    email: EmailStr
    linkedin_profile: HttpUrl
    github_profile: HttpUrl
class Experience(BaseModel):
    job_title: str
    company: str
    location: str
    start_date: str
    end_date: Optional[str]
    description: List[str]
class Project(BaseModel):
    title: str
    description: str
    github_link: Optional[HttpUrl]
    technologies: Optional[List[str]]
class Education(BaseModel):
    degree: str
    school: str
    location: str
    graduation_date: str
class Certificate(BaseModel):
    name: str
    date: str
class Involvement(BaseModel):
    role: str
    organization: str
    description: str
class Skills(BaseModel):
    all_skills: List[str]


class ResumeSchema(BaseModel):
    name: str
    contact_info: ContactInfo
    experience: List[Experience]
    projects: List[Project]
    education: List[Education]
    certificates: List[Certificate]
    involvement: List[Involvement]
    skills: Skills
    summary: Optional[str]