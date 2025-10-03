'''
This file contains all tools for gap_analysis node
Tools can include python methods, LLMChains, independent sub-Agents
'''

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableSequence
import json

from nodes.config import llm


##
## --- LLMChains ---
##

def get_suggestions_llmchains() -> RunnableSequence:
    '''
    Method to return an LLMChain for getting suggestions
    '''

    prompt = f"""
        You are a resume-job description alignment expert.

        Compare the following parsed resume and parsed job description, and return a JSON object containing:
        1. missing_keywords: A list of relevant keywords in the JD but missing from the resume.
        2. weak_bullets: A list of resume bullet points that should be rewritten for better alignment. Include the section, role, company, index, and a suggested replacement.
        3. additional_bullets: New bullet points (max 2) that could be added under existing roles to better match the JD.

        Note: For each missing_keyword, weak_bullets or additional_bullets entry, include the resume section, role and company where the bullet is relevant.

        WARNING: DO NOT INCLUDE ANY EXPLANATION, COMMENTS. ONLY THE JSON

        """

    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt),
        ("human","\n\nResume JSON: {resume_sections}\n\nJob Description Profile:{jd_sections}\n\nFormat your output as a JSON object exactly as described.")
    ])

    chain = prompt | llm

    return chain

