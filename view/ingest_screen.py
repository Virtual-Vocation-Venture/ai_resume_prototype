import streamlit as st
import tempfile
from streamlit import session_state as ss
from pydantic import ValidationError
from schemas import ResumeInput
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils.resume_reader import analyze_resume_content


def create_sample_resume_input():
    """
    Creates a sample resume input for testing.
    """
    sample_data = {
        "name": "Mikhail Ocampo",
        "email": "mikhail.ocampo@sjsu.edu",
        "phone_number": "6613401355",
        "linkedin_profile": "https://www.linkedin.com/in/mikhail-ocampo/",
        "github_profile": "https://github.com/mikhailocampo",
        "experience": "Software Engineer Intern at Tech Solutions Inc. - Developed web applications using React and Node.js.",
        "projects": "Personal Portfolio Website - Created a portfolio using HTML, CSS, and JavaScript.",
        "education": "Bachelor of Science in Computer Science, San Jose State University, Expected Graduation: May 2024.",
        "skills": "JavaScript, Python, React, Node.js.",
        "coursework": "Data Structures, Operating Systems, Software Engineering.",
        "certifications": "AWS Certified Solutions Architect.",
        "involvement": "Member of SJSU Computer Science Club.",
        "summary": "Aspiring software engineer with skills in full-stack development and problem-solving.",
        "target_job_title": "Software Engineer",
        "target_job_description": "Seeking a software engineering role to leverage full-stack development skills."
    }
    resume_input = ResumeInput(**sample_data)
    return resume_input


def parse_resume_content(file_upload):
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp_file:
        # Save the uploaded file to the temporary file
        tmp_file.write(file_upload.getvalue())
        tmp_file.flush()
        
        # Pass the temporary file path to the PyPDFLoader
        loader = PyPDFLoader(tmp_file.name)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)
        pages = loader.load_and_split(text_splitter)
        
        # Call LLM to Analyze
        result = analyze_resume_content(pages)
        print("Successfully analyzed resume content.")
        
        return result


def get_prefill_value(key, default=""):
    if "prefill_data" in ss:
        return getattr(ss["prefill_data"], key, default)
    return default


def ingest_screen(app_env: str = None):
    """
    Renders the data ingestion for the resume builder. Input fields with streamlit components should coordiante with a ResumeInput schema.
    """
    
    file_upload = st.file_uploader("Upload your resume", type=["pdf"])
    
    if file_upload:
        ss['prefill_data'] = parse_resume_content(file_upload)
        
        
    with st.form("resume_form"):
        
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander("**Contact Info**"):
                name = st.text_input("Name", value=get_prefill_value("name"))
                email = st.text_input("Email", value = get_prefill_value("email"))
                phone_number = st.text_input("Phone Number", value = get_prefill_value("phone_number"))
                linkedin_profile = st.text_input("LinkedIn Profile", value = get_prefill_value("linkedin_profile"))
                github_profile = st.text_input("GitHub Profile", value = get_prefill_value("github_profile"))
            
            with st.expander("**Experience**"):
                experience = st.text_area("Experience (e.g. work experience, internships)", value=get_prefill_value("experience"))
            
            with st.expander("**Projects**"):
                projects = st.text_area("Projects (e.g. personal projects, group projects)", value=get_prefill_value("projects"))
            
            with st.expander("**Education**"):
                education = st.text_area("Education (e.g. degrees, certifications)", value=get_prefill_value("education"))
            
            with st.expander("**Skills**"):
                skills = st.text_area("Skills (e.g. programming languages, software proficiency)", value=get_prefill_value("skills"))
            
            with st.expander("**Coursework**"):
                coursework = st.text_area("Coursework (e.g. relevant courses, academic achievements)", value=get_prefill_value("coursework"))
            
            with st.expander("**Certifications**"):
                certifications = st.text_area("Certifications (e.g. professional certifications, licenses)", value=get_prefill_value("certifications"))
            
            with st.expander("**Involvement**"):
                involvement = st.text_area("Involvement (e.g. extracurricular activities, volunteer work)", value=get_prefill_value("involvement"))
            
            with st.expander("**Summary**"):
                summary = st.text_area("Summary (e.g. professional summary, career goals)", value=get_prefill_value("summary"))
        
        with col2:
            with st.expander("**Target Job**", expanded=True):
                st.caption(f"Please enter the job title and job description for which you would like to build a resume. You can paste the job description from a job posting.")
                job_title = st.text_input("Job Title")
                job_description = st.text_area("Job Description", max_chars=5000)
        
        submit = st.form_submit_button("Generate Resume")
    
    if submit:
        with st.spinner("Generating Resume..."):
            try:
                if app_env == "dev":
                    resume_input = create_sample_resume_input()
                else:
                    resume_input = ResumeInput(
                        name = name,
                        email = email,
                        phone_number = phone_number,
                        linkedin_profile = linkedin_profile,
                        github_profile = github_profile,
                        experience = experience,
                        projects = projects,
                        education = education,
                        skills = skills,
                        coursework = coursework,
                        certifications = certifications,
                        involvement = involvement,
                        summary = summary,
                        target_job_title = job_title,
                        target_job_description = job_description
                )
                # Package and store resume input in session state
                ss["resume_input"] = resume_input
                st.success("Resume generated!")
                # Call rerun to update the app view
                st.rerun()
            except ValidationError as e:
                error = e.errors()
                st.error(f"{error[0]['msg']}")
                st.error(f"Please enter a value for all required fields.")

