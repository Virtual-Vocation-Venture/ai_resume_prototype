from pdf_extract import extract_text_from_pdf
from resume_reader import analyze_resume_content
from resume_data_upload import write_to_airtable

def main():
    # Path to the resume PDF
    pdf_file = "resume.pdf"
    
    # Step 1: Extract raw text from the PDF
    resume_text = extract_text_from_pdf(pdf_file)
    
    # Step 2: Analyze the extracted resume text using OpenAI
    resume_info = analyze_resume_content(resume_text)
    
    # Step 3: Upload the structured data to Airtable
    write_to_airtable(resume_info)

if __name__ == "__main__":
    main()
