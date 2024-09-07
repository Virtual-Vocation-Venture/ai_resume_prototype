import os
from openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from config import OPENAI_API_KEY

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

def analyze_resume_content(resume_text):
    """Uses OpenAI to extract structured information from the resume text."""
    prompt_template = """
    You are a professional resume reader. Analyze the following resume content and extract the following information:
    1. Email Address
    2. User's State
    3. User's Country
    4. LinkedIn Link
    5. Education (school name, start and end dates, location, description)
    6. Experience (company name, start and end dates, location, description)
    7. Skills (comma-separated list)
    8. Certifications (comma-separated list)

    Here's the resume content:
    
    {resume_text}

    Return the extracted information in a structured format.
    """

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["resume_text"]
    )

    llm = OpenAI(
        model="text-davinci-003",
        temperature=0.7,
        max_tokens=1500
    )

    chain = LLMChain(llm=llm, prompt=prompt)
    
    resume_info = chain.run({"resume_text": resume_text})

    return resume_info
