from pydantic import BaseModel, model_validator
from typing import Any, ClassVar, Optional, List, Dict


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
    email: str
    linkedin_profile: str
    github_profile: str
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
    github_link: Optional[str]
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
    target_job_title: str
    target_job_description: str

    def flatten(self) -> Dict[str, Any]:
        flattened = {}

        for field in self.model_fields.keys():
            if field == "name":
                flattened[field] = self.name
            if field == "contact_info":
                flattened["email"] = self.contact_info.email
                flattened["phone number"] = self.contact_info.phone_number
                flattened["linkedin profile"] = self.contact_info.linkedin_profile
                flattened["github profile"] = self.contact_info.github_profile
            elif field == "experience":
                flattened[field] = "\n".join([f"{exp.job_title} - {exp.company}" for exp in self.experience])
            elif field == "projects":
                flattened[field] = "\n".join([f"{proj.title} - {proj.description}" for proj in self.projects])
            elif field == "education":
                flattened[field] = "\n".join([f"{edu.degree} - {edu.school}" for edu in self.education])
            elif field == "certificates":
                flattened[field] = "\n".join([f"{cert.name} - {cert.date}" for cert in self.certificates])
            elif field == "involvement":
                flattened[field] = "\n".join([f"{inv.role} - {inv.organization}" for inv in self.involvement])
            elif field == "skills":
                flattened[field] = ", ".join(self.skills.all_skills)
            elif field == "summary" and self.summary:
                flattened[field] = self.summary
            elif field == "target_job_title":
                flattened["target job title"] = self.target_job_title
            elif field == "target_job_description":
                flattened["target job description"] = self.target_job_description


        return flattened