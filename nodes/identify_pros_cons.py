'''
This file contains all tools for identify_pros_cons node
Tools can include python methods, LLMChains, independent sub-Agents
'''

from langchain_cohere import ChatCohere
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableSequence


##
## --- LLMChains ---
##

def get_suggestions_llmchains(
    llm: BaseChatModel = ChatCohere(model="command-r-plus", temperature=0)
    ) -> RunnableSequence:
    '''
    Method to return an LLMChain for getting suggestions
    '''

    prompt_text = '''

    You are an expert in resume design, specifically for jobs in computer science and tech.

    Your task is to interpret the sections of a resume, and the details of a job description, and suggest edits to the resume, to better match the job description.
    The suggestions should maximize the chance the resume leads to an interview.

    The resume information will be given to you as a structured JSON.

    The job details will be given to you as a structured JSON.

    Rules:
    - Only use the details in the resume and the job description JSONs. If a suggestion requires information not present, ask for it.
    - DO NOT invent or hallucinate skills or responsibilities not present.
    - When suggesting a new sentence to replace a sentence of the resume, follow the language style of the resume as much as possible.
        - This includes how condensed/compressed the sentences are, etc.

    '''

    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_text),
        ("human", "Job Description:\n{jd_details}\n\nResume Details:\n{resume_details}\nYour output schema is: text, where text is your answer.")
    ])

    chain = prompt | llm

    return chain

    