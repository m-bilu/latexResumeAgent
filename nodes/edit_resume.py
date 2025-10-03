'''
This file contains all tools for edit_resume node
Tools can include python methods, LLMChains, independent sub-Agents
'''

from langchain.prompts import ChatPromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.schema.runnable import RunnableLambda, RunnableSequence
from rag.query import query_vectorstore  # this should return a list of relevant text chunks

from nodes.config import llm

def get_resume_edit_chain() -> RunnableSequence:
    """
    Returns an LLMChain that edits a resume using structured suggestions, job description, and similar examples.
    """


    system_prompt = """
You are a resume editing assistant.

Given:
1. A resume document (as a string),
2. A plain English job description,
3. A list of structured improvement suggestions,
4. Example resume snippets from high-quality resumes (these can guide tone, phrasing, structure),

Apply edits to the resume string:
- Reword or replace bullets as specified
- Insert new bullet points under correct roles/sections
- Add missing keywords subtly if possible

Do NOT hallucinate new companies, degrees, or experiences.

Return only the **edited resume string** (no explanation).
    """

    resume_edit_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", """
            RESUME TEXT:
            {resume}

            JOB DESCRIPTION:
            {jd_text}

            EDIT SUGGESTIONS:
            {suggestions_json}

            """

            ### SIMILAR RESUME EXAMPLES TO INSPIRE EDITS:
            ## {examples}
        )
    ])

    # def augment_with_examples(inputs: dict) -> dict:
    #     retrieved = query_vectorstore(inputs["jd_text"], k=5)
    #     inputs["examples"] = "\n---\n".join(retrieved)
    #     return inputs

    return resume_edit_prompt    | llm
    ##                        ^^ | RunnableLambda(augment_with_examples)
