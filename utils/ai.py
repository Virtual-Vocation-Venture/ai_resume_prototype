from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableSerializable
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from utils.constants import BASE_PROMPT
from schemas import ResumeInput, ResumeSchema


def initialize_resume_chain() -> RunnableSerializable:
    response_schema = PydanticOutputParser(pydantic_object = ResumeSchema)
    prompt = PromptTemplate(
        template = BASE_PROMPT,
        input_variables = [ResumeInput.required_fields],
        partial_variables={"format_instrutions": response_schema.get_format_instructions()}
    )
    llm = ChatOpenAI(
        model_name = "gpt-4o-mini",
        temperature = 0,
        model_kwargs={
            "response_format": {"type": "json_object"}
        }
    )
    
    chain = prompt | llm | response_schema
    return chain


def invoke_resume_chain(
    resume_input: ResumeInput
) -> ResumeSchema:
    chain = initialize_resume_chain()
    return chain.invoke(resume_input.model_dump())
