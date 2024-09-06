import streamlit as st
import base64
from streamlit import session_state as ss
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from datetime import datetime
from schemas import ResumeSchema
from utils.ai import invoke_resume_chain


def save_resume_to_pdf(resume_data: ResumeSchema):
    today_date = datetime.today().strftime('%Y-%m-%d')
    file_name = f"{resume_data.name}_Resume_{today_date}.pdf"
    
    pdf_bytes = BytesIO()
    doc = SimpleDocTemplate(pdf_bytes, pagesize=letter,
                            rightMargin=1*cm, leftMargin=1*cm,
                            topMargin=0.5*cm, bottomMargin=0.5*cm)

    # Styles
    text_color = colors.HexColor("#303E48")
    custom_heading_style = ParagraphStyle(name='CustomHeading', fontSize=14, textColor=text_color, leading=18)
    custom_normal_style = ParagraphStyle(name='CustomNormal', fontSize=10, textColor=text_color, leading=14)

    story = []

    # Add Name and Contact Info
    story.append(Paragraph(f"<b>{resume_data.name}</b>", custom_heading_style))
    contact_info = resume_data.contact_info
    contact_text = f"{contact_info.location} | {contact_info.phone_number} | {contact_info.email} | <a href='{contact_info.linkedin_profile}'>LinkedIn</a> | <a href='{contact_info.github_profile}'>GitHub</a>"
    story.append(Paragraph(contact_text, custom_normal_style))
    story.append(Spacer(1, 12))

    # Add Summary
    story.append(Paragraph("<b>Summary</b>", custom_heading_style))
    story.append(Paragraph(resume_data.summary, custom_normal_style))
    story.append(Spacer(1, 12))

    # Add Experience Section
    story.append(Paragraph("<b>Experience</b>", custom_heading_style))
    for job in resume_data.experience:
        story.append(Paragraph(f"{job.job_title} - {job.company} ({job.location})", custom_normal_style))
        story.append(Paragraph(f"{job.start_date} - {job.end_date or 'Present'}", custom_normal_style))
        for bullet in job.description:
            story.append(Paragraph(f"• {bullet}", custom_normal_style))
        story.append(Spacer(1, 12))

    # Add Projects Section
    story.append(Paragraph("<b>Projects</b>", custom_heading_style))
    for project in resume_data.projects:
        story.append(Paragraph(f"{project.title}", custom_normal_style))
        story.append(Paragraph(f"{project.description}", custom_normal_style))
        story.append(Paragraph(f"Technologies: {', '.join(project.technologies)}", custom_normal_style))
        story.append(Paragraph(f"<a href='{project.github_link}'>GitHub Link</a>", custom_normal_style))
        story.append(Spacer(1, 12))

    # Add Education Section
    story.append(Paragraph("<b>Education</b>", custom_heading_style))
    for edu in resume_data.education:
        story.append(Paragraph(f"{edu.degree} - {edu.school} ({edu.location})", custom_normal_style))
        story.append(Paragraph(f"Graduation: {edu.graduation_date}", custom_normal_style))
        story.append(Spacer(1, 12))

    # Add Certificates Section
    story.append(Paragraph("<b>Certificates</b>", custom_heading_style))
    for cert in resume_data.certificates:
        story.append(Paragraph(f"{cert.name} - {cert.date}", custom_normal_style))
        story.append(Spacer(1, 12))

    # Add Involvement Section
    story.append(Paragraph("<b>Involvement</b>", custom_heading_style))
    for inv in resume_data.involvement:
        story.append(Paragraph(f"{inv.role} - {inv.organization}", custom_normal_style))
        story.append(Paragraph(f"{inv.description}", custom_normal_style))
        story.append(Spacer(1, 12))

    # Add Skills Section
    story.append(Paragraph("<b>Skills</b>", custom_heading_style))
    story.append(Paragraph(", ".join(resume_data.skills.all_skills), custom_normal_style))
    story.append(Spacer(1, 12))

    doc.build(story)
    pdf_bytes.seek(0)

    return pdf_bytes, file_name


def display_pdf(pdf_bytes):
    # Get PDF bytes from BytesIO and encode in B64
    base64_pdf = base64.b64encode(pdf_bytes.read()).decode("utf-8")

    # Embedding PDF in HTML
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)


def preview_screen(app_env: str = None):
    """
    Renders the preview screen for the resume builder.
    """
    st.title("Preview")
    
    with st.spinner("Generating Resume..."):
        # Check if cache exists
        if "resume_data" not in ss:
            resume_data = invoke_resume_chain(ss["resume_input"])
        
            # Cache resume data in ss for future use
            ss["resume_data"] = resume_data
        else:
            print(f"Found resume data in session state as cache.")
            resume_data = ss["resume_data"]
        
        pdf_bytes, file_name = save_resume_to_pdf(resume_data)
        
        display_pdf(pdf_bytes)
