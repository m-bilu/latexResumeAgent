'''
This file contains all tools needed for the parse_jd node
Tools can include python methods, LLMChains, independent sub-Agents
'''

from typing import Dict

from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableSequence

from nodes.config import targets, llm

##
## --- LLMChains ---
##


def get_details_llmchain() -> Dict[str, RunnableSequence]:
    '''
    Method returns an LLMChain for extracting different information about JD
    '''
    prompt_texts = {target_type: f'''
    You are an AI assistant that extracts structured, factual insights from job descriptions to help tailor resumes for specific roles.

    Your task is to read the job description below and extract the following information:

    {target_desc}

    Rules:
    - ONLY extract what's mentioned or clearly implied in the job description.
    - DO NOT invent or hallucinate skills or responsibilities not present.
    - Follow the output schema exactly.
    - Be strict in separating required vs optional skills.

    ''' for target_type, target_desc in targets.items()}

    prompts = {

        target : ChatPromptTemplate.from_messages([
        ("system", prompt_text),
        ("human", "Job Description:\n{job_description}\nYour output schema is: text, where text is your answer.")
        ]) for target, prompt_text in prompt_texts.items()

    }

    chains = {target : prompt | llm
              for target, prompt in prompts.items()}

    return chains
