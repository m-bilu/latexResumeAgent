'''
This file contains all tools needed for the parse_jd node
Tools can include python methods, LLMChains, independent sub-Agents
'''

import re
from typing import Dict, List, Tuple
from collections import defaultdict

from pydantic import BaseModel
from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

import nodes.config as config

##
## --- LLMChains ---
##

class JDInsights(BaseModel):
    role_summary: str
    must_have_skills: List[str]
    nice_to_have_skills: List[str]
    responsibilities: List[str]
    keywords: List[str]
    seniority_level: str
    
def get_details_llmchain():
    '''
    Method returns an LLMChain for extracting different information about JD
    '''

    llm = ChatCohere(model="command-r-plus", temperature=0)
    output_parser = JsonOutputParser(pydantic_object=JDInsights)

    prompt_text = '''
    You are an AI assistant that extracts structured, factual insights from job descriptions to help tailor resumes for specific roles.

    Your task is to read the job description below and extract the following as structured JSON:

    - `role_summary` (string): A short summary of what the role is about (1–2 sentences).
    - `must_have_skills` (list of strings): Technologies, tools, or skills explicitly marked as required or essential. If some resume did not have them, it would be at a disadvantage.
    - `nice_to_have_skills` (list of strings): Skills that are mentioned as optional, preferred, or bonuses. This skills push a good candidate past other good candidates, and takes probability of interview from high to 100%.
    - `responsibilities` (list of strings): Key tasks the candidate will be responsible for. Imagine that a given resume is good for this role, then it SHOULD be able to fulfil these responsibilities.
    - `keywords` (list of strings): Domain-specific phrases, concepts, tools, or responsibilities relevant for tailoring a resume (e.g. "fraud detection", "AWS", "real-time systems").
    - `specific_technologies` (list of strings): All the technologies, tools and technical workflows, platforms mentioned in the job description.
    - `general_technologies` (list of strings): More general technicals things someone should demonstrate, according to this job description. Being able to build a certain type of technical product (data pipeline, web app), solve a certain type of technical problem.
    - `years_of_experience` (string): How many years of experience needed to be reasonably considered for this job. Give a range, with a lower limit and upper limit.

    Rules:
    - ONLY extract what's mentioned or clearly implied in the job description.
    - DO NOT invent or hallucinate skills or responsibilities not present.
    - Be strict in separating required vs optional skills.
    - Follow the output schema exactly.

    '''

    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_text),
        ("human", "Job Description:\n{job_description}\nRespond in **valid JSON** that matches this format:{schema}")
    ])

    chain = prompt | llm | output_parser ## same as input -> invoke -> output -> input of next ...

    return chain, output_parser
