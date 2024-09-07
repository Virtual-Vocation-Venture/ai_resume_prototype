import os
from typing import List
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain.output_parsers import PydanticOutputParser
from langchain_core.runnables import Runnable
from schemas import ResumeInput


def analyze_resume_content(pdf_docs: List[Document]):
    """Uses OpenAI to extract structured information from the resume text."""
    prompt_template = """
    You are a professional resume reader. Analyze the following resume content and extract the following information:
    
    Special Instructions:
    - When presented with a link, return the URL, not markdown format.
    - When given a list of items, return each item on a separate line.
    - When given experience, respond as a string where each experience is separated by a new line and each experience includes accomplishments.
        - Example: Data Analyst at Azure Capital (2023-2024): Analyzed financial data to identify trends and make recommendations. 
        - Example: Software Engineer Intern at Tech Solutions Inc. (2022-2023): Developed web applications using React and Node.js.
    - When given education, list out the degree and the school. Do not make up dates.
    - When given skills, list out the skills and the proficiency. Do not make up numbers.
    
    Any fields without relevant information should be an empty string
    
    Format Instructions:
    {format_instructions}

    Here's the resume content:
    {content}


    Return the extracted information in a structured format.
    """

    response_schema = PydanticOutputParser(pydantic_object=ResumeInput)
    
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["content"],
        partial_variables={"format_instructions": response_schema.get_format_instructions()}
    )

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        model_kwargs={
            "response_format": {"type": "json_object"}
        }
    )

    chain = (
        prompt 
        | llm 
        | response_schema
    ).with_config({"run_name": "Resume Parser"})

    content = "\n".join([doc.page_content for doc in pdf_docs])
    
    resume_info = chain.invoke({"content": content})

    return resume_info
