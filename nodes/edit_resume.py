'''
This file contains all tools for edit_resume node
Tools can include python methods, LLMChains, independent sub-Agents
'''

from langchain.prompts import ChatPromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_cohere import ChatCohere
from langchain.schema.runnable import RunnableLambda, RunnableSequence
from rag.query import query_vectorstore  # this should return a list of relevant text chunks

def get_resume_edit_chain(llm: BaseChatModel | None = None) -> RunnableSequence:
    """
    Returns an LLMChain that edits a LaTeX resume using structured suggestions, job description, and similar examples.
    """
    if llm is None:
        llm = ChatCohere(model="command-r-plus", temperature=0)

    system_prompt = """
You are a LaTeX resume editing assistant.

Given:
1. A LaTeX resume document (as a string),
2. A plain English job description,
3. A list of structured improvement suggestions,
4. Example resume snippets from high-quality resumes (these can guide tone, phrasing, structure),

Apply edits to the LaTeX string:
- Reword or replace bullets as specified
- Insert new bullet points under correct roles/sections
- Add missing keywords subtly if possible
- Use the retrieved examples to guide improvements
- Preserve LaTeX formatting and syntax
    - Each section should have a resumeSubheadingListStart, with jobs as resumeSubheadings.
    - Each job should have resumeItemListStart and all the bullet points go under this, as resumeItem tags.
    - All vspace, href, and textcolor tags from the old resume should be copied to the new resume
    - If two bullet points for the same job can be merged, such that the new bullet point is smaller than 250 characters, then do it.

Do NOT hallucinate new companies, degrees, or experiences.

Return only the **edited LaTeX document** (no markdown, no explanation).
    """

    resume_edit_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", """
RESUME (LaTeX):
{resume_latex}

JOB DESCRIPTION:
{jd_text}

EDIT SUGGESTIONS:
{suggestions_json}

SIMILAR RESUME EXAMPLES TO INSPIRE EDITS:
{examples}
""")
    ])

    def augment_with_examples(inputs: dict) -> dict:
        retrieved = query_vectorstore(inputs["jd_text"], k=5)
        inputs["examples"] = "\n---\n".join(retrieved)
        return inputs

    return resume_edit_prompt | RunnableLambda(augment_with_examples) | llm
